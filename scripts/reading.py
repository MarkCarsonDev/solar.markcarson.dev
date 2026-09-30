"""Reading shelves for the home page, from the books app at books.markcarson.dev.

Sets ``reading_shelves``: a list of shelves (in progress, recently finished,
up next), each with the first few books to show and the rest to tuck behind
a "more" toggle. Book covers are downloaded once, dithered with the site's
image settings, and written straight into the output directory.
"""

import io
import json
import logging
import urllib.request
from pathlib import Path

from sonne.script_api import sonne_config, sonne_var

logger = logging.getLogger("sonne")

BOOKS_BASE_URL = "https://books.markcarson.dev"
REQUEST_TIMEOUT_SECONDS = 10
USER_AGENT = "Sonne/1.0"
COVER_MAX_WIDTH = 200
BOOKS_SHOWN_PER_SHELF = 3

SITE_ROOT = Path(__file__).resolve().parent.parent
# Covers bypass Sonne's static pipeline: copy_static_files only copies what
# exists in static/, so it leaves this directory alone.
COVERS_DIR = SITE_ROOT / sonne_config("paths", "output", default="build") / "images" / "books"


def main():
    shelves = fetch_shelves()
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    sonne_var(
        "reading_shelves",
        [
            shelf(
                "In Progress", "in progress", newest_first(shelves.get("currently_reading"), "last_read_at")
            ),
            shelf("Recently Finished", "finished", newest_first(shelves.get("finished"), "finished_at")),
            shelf("Up Next", "queued", shelves.get("up_next") or []),
        ],
    )


def fetch_shelves():
    """The books app's shelves, or no shelves when it can't be reached."""
    try:
        return get_json(f"{BOOKS_BASE_URL}/api/reading")
    except (OSError, ValueError) as error:
        logger.warning(f"reading: failed to fetch API: {error}")
        return {}


def newest_first(books, date_field):
    return sorted(books or [], key=lambda book: book.get(date_field) or "", reverse=True)


def shelf(label, more_label, books):
    books = [with_link_and_cover(book) for book in books]
    return {
        "label": label,
        "more_label": more_label,
        "top": books[:BOOKS_SHOWN_PER_SHELF],
        "rest": books[BOOKS_SHOWN_PER_SHELF:],
    }


def with_link_and_cover(book):
    return {**book, "link": book_link(book), "has_cover": ensure_cover(book)}


def book_link(book):
    if book.get("isbn"):
        return f"https://openlibrary.org/isbn/{book['isbn']}"
    if book.get("goodreads_id"):
        return book.get("goodreads_url") or f"https://www.goodreads.com/book/show/{book['goodreads_id']}"
    return None


def ensure_cover(book):
    """Make sure a dithered cover exists for the book; returns whether one does."""
    cover_path = COVERS_DIR / f"{book.get('id')}.png"
    if cover_path.exists():
        return True
    if not book.get("cover_url"):
        return False
    try:
        save_dithered_cover(download(absolute_url(book["cover_url"])), cover_path)
        return True
    except Exception as error:  # a bad cover must never break the build
        logger.warning(f"reading: cover fetch failed for id={book.get('id')}: {error}")
        return False


def save_dithered_cover(image_bytes, cover_path):
    from PIL import Image, ImageOps

    from sonne.core.config import Config
    from sonne.processors.image_processor import ImageProcessor

    image = ImageOps.exif_transpose(Image.open(io.BytesIO(image_bytes)))
    if image.width > COVER_MAX_WIDTH:
        height = int(image.height * COVER_MAX_WIDTH / image.width)
        image = image.resize((COVER_MAX_WIDTH, height), Image.LANCZOS)
    # ImageProcessor needs a Config object (sonne_config only returns values),
    # so the site config is loaded once more here; see docs/REVIEW_NOTES.md.
    site_config = Config(base_dir=str(SITE_ROOT))
    dithered = ImageProcessor(site_config, {}).dither(image)
    dithered.save(cover_path, format="PNG", optimize=True)


def absolute_url(url):
    return BOOKS_BASE_URL + url if url.startswith("/") else url


def get_json(url):
    return json.loads(download(url).decode("utf-8"))


def download(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        return response.read()


main()
