import random

battery_percent = random.randint(0, 100)

sun_svg = '<path d="M4.464 4.465a.5.5 0 000-.708L3.05 2.343a.5.5 0 10-.707.707L3.757 4.465a.5.5 0 00.707 0m9.193 9.192a.5.5 0 000-.707l-1.414-1.414a.5.5 0 00-.707.707l1.414 1.414a.5.5 0 00.707 0M4.464 11.536a.5.5 0 00-.707 0L2.343 12.95a.5.5 0 00.707.707l1.414-1.414a.5.5 0 000-.707m9.193-9.193a.5.5 0 00-.707 0L11.536 3.757a.5.5 0 10.707.708L13.657 3.05a.5.5 0 000-.707M3 8a.5.5 0 00-.5-.5H.5a.5.5 0 000 1h2A.5.5 0 003 8M16 8a.5.5 0 00-.5-.5h-2a.5.5 0 000 1h2A.5.5 0 0016 8M8 13a.5.5 0 00-.5.5v2a.5.5 0 001 0v-2A.5.5 0 008 13M8 0A.5.5 0 007.5.5v2a.5.5 0 001 0V.5A.5.5 0 008 0M8 12A4 4 0 018 4a4 4 0 110 8m0-1A3 3 0 008 5a3 3 0 100 6"/>'

# Define the SVG path for the battery outline
battery_outline_svg = f'<path d="m 0 2 h 3 v -2 h 3 v 2 h 4 v -2 h 3 v 2 h 3 v 14 h -16 v -14 z m 1 1 v 12 h 14 v -12 h -14 z M 2 14 h 12 v -{battery_percent / 10} h -12 z"/>'

def create_battery_svg(percent):
    BATTERY_WIDTH = 70
    BATTERY_HEIGHT = 30
    TERMINAL_HEIGHT = 20
    MARGIN = 1

    # Calculate the fill height based on the percentage
    fill_height = BATTERY_HEIGHT * (percent / 100.0)

    # Coordinates for the fill rectangle
    x = MARGIN
    y = TERMINAL_HEIGHT + BATTERY_HEIGHT - MARGIN - fill_height
    width = BATTERY_WIDTH - 2 * MARGIN
    height = fill_height

    # Create the SVG path for the fill rectangle
    path_data = 'm {x} {y} h {x_plus_width} v {y_plus_height} h {x} v {y} z'.format(
        x=x,
        y=y,
        x_plus_width=BATTERY_WIDTH - MARGIN,
        y_plus_height=y + height
    )

    return '<path d="{0}"/>'.format(path_data)

fill_svg = create_battery_svg(battery_percent)
battery_svg = f'{battery_outline_svg}'



home_svg = '<path d="m 0 6 v 0 l 8 -6 l 8 6 v 9 h -16 z m 1 8 h 14 v -7.383 l -7 -5 l -7 5 z"/></svg>'
solar_blog = '\
{p}{\#2 + 3\#}\
'


banner_html = f'\
            <div id="header">\
                <div id="banner">\
                \
                    <div class="off-left banner-pos">\
                        <a href="index.html">\
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-home" viewBox="0 0 16 16">\
                                {home_svg}\
                            </svg>\
                        </a>\
                    </div>\
                    \
                    <div class="left banner-pos" style="opacity: 0">\
                    </div>\
                    \
                    <div class="middle banner-pos">\
                        <h3 id="solar_text">This is a solar-powered website, so it occasionally goes offline. <a href="{solar_blog}">Read why</a>.</h3>\
                    </div>\
                    \
                    <div class="right banner-pos" style="opacity: 0">\
                    </div>\
                    \
                    <div class="off-right banner-pos">\
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-sun" viewBox="0 0 16 16">\
                            {sun_svg if battery_percent > 95 else battery_svg}\
                        </svg>\
                        <span id="battery_percent" style="white-space: pre"> {battery_percent}%</span>\
                    </div>\
                    \
                </div>\
            </div>'

sonne_var("banner", banner_html)