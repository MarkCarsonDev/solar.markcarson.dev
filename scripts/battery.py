# Solar / battery status
# Update these two values to reflect real sensor data in the future.
# e.g. read from a file: battery_level = int(open('/sys/class/power_supply/BAT0/capacity').read())
#      battery_charging = open('/sys/class/power_supply/BAT0/status').read().strip() == 'Charging'

battery_level   = 100
battery_charging = True   # True = solar is charging, False = running on stored battery

# --- Build SVG icons ---

fill_px = round(battery_level / 100 * 28)  # inner fill bar, max 28px wide

battery_svg = f'''<svg class="batt-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 44 20" aria-hidden="true">
  <rect x="1" y="3" width="36" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <rect x="37" y="7" width="5" height="6" rx="1.5" fill="currentColor"/>
  <rect x="3" y="5" width="{fill_px}" height="10" rx="1" fill="currentColor"/>
</svg>'''

sun_svg = '''<svg class="sun-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" aria-hidden="true">
  <circle cx="10" cy="10" r="3.5" fill="currentColor"/>
  <line x1="10" y1="1"    x2="10" y2="4"    stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="10" y1="16"   x2="10" y2="19"   stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="1"  y1="10"   x2="4"  y2="10"   stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="16" y1="10"   x2="19" y2="10"   stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="3.2" y1="3.2"   x2="5.3" y2="5.3"   stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="14.7" y1="14.7" x2="16.8" y2="16.8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="16.8" y1="3.2"  x2="14.7" y2="5.3"  stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="3.2"  y1="16.8" x2="5.3"  y2="14.7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
</svg>'''

icon   = sun_svg if battery_charging else battery_svg
label  = 'charging' if battery_charging else f'{battery_level}%'
status = 'charging' if battery_charging else 'on battery'

battery_html = f'''<div id="battery-widget" data-charging="{'yes' if battery_charging else 'no'}" aria-label="Solar status: {status}">
  {icon}
  <span id="battery-label">{label}</span>
</div>'''

sonne_var("battery_level",   battery_level)
sonne_var("battery_charging", battery_charging)
sonne_var("battery_html",    battery_html)
