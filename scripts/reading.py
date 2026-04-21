import io
import json
import logging
import os
import urllib.error
import urllib.request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("reading")

BOOKS_BASE = "https://books.markcarson.dev"

try:
    req = urllib.request.Request(
        f"{BOOKS_BASE}/api/reading",
        headers={"User-Agent": "Sonne/1.0"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        _data = json.loads(resp.read().decode("utf-8"))
except Exception as e:
    logger.warning(f"reading: failed to fetch API: {e}")
    _data = {}

try:
    from PIL import Image, ImageOps
    from sonne.processors.image_processor import ImageProcessor as _IP

    class _MinCfg:
        def get(self, *a, **kw): return kw.get("default")

    _ip = _IP(_MinCfg(), {})
    _PIL = True
except Exception:
    _PIL = False

COVER_MAX_WIDTH = 200


def _build_link(book):
    isbn = book.get("isbn")
    gid = book.get("goodreads_id")
    gurl = book.get("goodreads_url")
    if isbn:
        return f"https://openlibrary.org/isbn/{isbn}"
    if gid:
        return gurl or f"https://www.goodreads.com/book/show/{gid}"
    return None


# Save dithered covers directly to build/ so sonne's static pipeline is bypassed.
# copy_static_files only copies files that exist in static/, so build/images/books/
# won't be touched by step 3 of the pipeline.
_covers_dir = os.path.join(os.path.dirname(__file__), "..", "build", "images", "books")
os.makedirs(_covers_dir, exist_ok=True)


def _fetch_cover(book):
    book_id = book.get("id")
    cover_url = book.get("cover_url")
    out_path = os.path.join(_covers_dir, f"{book_id}.png")
    if os.path.exists(out_path):
        book["has_cover"] = True
        return
    if not cover_url:
        book["has_cover"] = False
        return
    full_url = (BOOKS_BASE + cover_url) if cover_url.startswith("/") else cover_url
    try:
        req = urllib.request.Request(full_url, headers={"User-Agent": "Sonne/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read()
        if _PIL:
            img = Image.open(io.BytesIO(raw))
            img = ImageOps.exif_transpose(img)
            if img.width > COVER_MAX_WIDTH:
                h = int(img.height * COVER_MAX_WIDTH / img.width)
                img = img.resize((COVER_MAX_WIDTH, h), Image.LANCZOS)
            dithered = _ip._apply_dither(img)
            dithered.save(out_path, format="PNG", optimize=True)
        else:
            # No PIL: save raw bytes as jpg fallback (won't be dithered)
            jpg_path = os.path.join(_covers_dir, f"{book_id}.jpg")
            with open(jpg_path, "wb") as f:
                f.write(raw)
        book["has_cover"] = True
    except Exception as e:
        logger.warning(f"reading: cover fetch failed for id={book_id}: {e}")
        book["has_cover"] = False


def _process(books):
    out = []
    for b in books:
        b = dict(b)
        b["link"] = _build_link(b)
        _fetch_cover(b)
        out.append(b)
    return out


finished = _process(
    sorted(
        _data.get("finished", []),
        key=lambda b: b.get("finished_at") or "",
        reverse=True,
    )
)

inprogress = _process(
    sorted(
        _data.get("currently_reading", []),
        key=lambda b: b.get("percent_complete") or 0,
        reverse=True,
    )
)

up_next = _process(_data.get("up_next", []))

sonne_var("reading_inprogress_top",  inprogress[:3])
sonne_var("reading_inprogress_rest", inprogress[3:])
sonne_var("reading_finished_top",    finished[:3])
sonne_var("reading_finished_rest",   finished[3:])
sonne_var("reading_up_next_top",     up_next[:3])
sonne_var("reading_up_next_rest",    up_next[3:])
