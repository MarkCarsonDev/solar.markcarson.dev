# Build timestamp for the footer (templates/partials/footer.html).
import zoneinfo
from datetime import datetime

from sonne.script_api import sonne_var

build_time = datetime.now(zoneinfo.ZoneInfo("America/Los_Angeles"))
sonne_var("compiled_at", build_time.strftime("%Y-%m-%d %H:%M %Z"))
