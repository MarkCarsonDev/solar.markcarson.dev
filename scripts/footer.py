from datetime import datetime
import zoneinfo

la_time = datetime.now(zoneinfo.ZoneInfo("America/Los_Angeles"))

footer_html = f'''<div id="footer">
    <span id="footer-solar">This site runs on an RPi Zero 2W &amp; a couple balcony solar panels.</span>
    <span id="footer-build">Compiled {la_time.strftime("%Y-%m-%d %H:%M %Z")}</span>
</div>'''

sonne_var("footer", footer_html)
