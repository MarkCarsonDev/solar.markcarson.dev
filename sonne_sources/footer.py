from datetime import datetime

footer_html = f'<div id="footer">\
            <p>Designed intentionally to be lightweight.</p>\
            <p>Efficiently compiled using <a href="https://github.com/MarkCarsonDev/Sonne">Sonne</a>, my static site generator.</a></p>\
            <p>Kept dynamically static with an elegant but simple homemade CI/CD solution.</p>\
            <p>Built from scratch in 2025 using simple HTML, JS, and CSS.</p>\
            <p>Compiled at {datetime.now()}<p>\
        </div>'

sonne_var("footer", footer_html)