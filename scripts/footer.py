from datetime import datetime

footer_html = f'''<div id="footer">
    <span id="footer-solar">This site runs on an RPi 3b &amp; a couple balcony solar panels.</span>
    <span id="footer-build">Compiled {datetime.now().strftime("%Y-%m-%d %H:%M")}</span>
</div>'''

sonne_var("footer", footer_html)
