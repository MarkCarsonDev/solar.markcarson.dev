# ── Solar / battery status ──────────────────────────────────────────────────
# Update these two values, or replace with a sensor/API read:
#   e.g. battery_level   = int(open('/sys/class/power_supply/BAT0/capacity').read())
#        battery_charging = open('/sys/class/power_supply/BAT0/status').read().strip() == 'Charging'

BATTERY_LEVEL    = 100
BATTERY_CHARGING = True   # True = solar charging, False = running on stored battery
# ────────────────────────────────────────────────────────────────────────────

# Make values available in templates too
sonne_var("battery_level",    BATTERY_LEVEL)
sonne_var("battery_charging", BATTERY_CHARGING)

battery_status = 'charging' if BATTERY_CHARGING else f'{BATTERY_LEVEL}%'

# Dynamic link to the "why solar" post
why_solar_post = get_post(slug='why-solar')
read_why_link  = why_solar_post.get('full_url', '/blog/') if why_solar_post else '/blog/'

banner_html = f'''<div id="banner">
    <div id="stamp">
        <a href="/">markcarson.dev</a>
        <span id="battery-status">{'☀' if BATTERY_CHARGING else '⬡'} {battery_status}</span>
    </div>
    <div id="message">
        <p>This site will soon be solar-powered. <a href="{read_why_link}">Read why.</a></p>
    </div>
    <div id="items">
        <div class="theme-switch-wrapper">
            <div class="theme-switch keypress keypress-reverse" id="kpD">
                <span class="keycap">D</span>
                <span id="theme-icon" class="theme-icon">
                    <svg></svg>
                </span>
            </div>
        </div>
        <a href="/feed.xml" class="rss-link keypress keypress-reverse" title="RSS Feed" aria-label="RSS Feed">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true">
                <circle cx="6.18" cy="17.82" r="2.18"/>
                <path d="M4 4.44v2.83c7.03 0 12.73 5.7 12.73 12.73h2.83c0-8.59-6.97-15.56-15.56-15.56zm0 5.66v2.83c3.9 0 7.07 3.17 7.07 7.07h2.83c0-5.47-4.43-9.9-9.9-9.9z"/>
            </svg>
        </a>
    </div>
</div>'''

sonne_var("banner", banner_html)
