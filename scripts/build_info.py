# Build timestamp for the footer (templates/partials/footer.html).
from datetime import datetime
import zoneinfo

build_time = datetime.now(zoneinfo.ZoneInfo("America/Los_Angeles"))
sonne_var("compiled_at", build_time.strftime("%Y-%m-%d %H:%M %Z"))
