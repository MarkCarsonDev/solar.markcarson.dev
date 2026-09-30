# Solar / battery status shown in the banner (templates/partials/banner.html).
# Update these two values, or replace them with a sensor read, e.g.
#   BATTERY_LEVEL    = int(open('/sys/class/power_supply/BAT0/capacity').read())
#   BATTERY_CHARGING = open('/sys/class/power_supply/BAT0/status').read().strip() == 'Charging'

BATTERY_LEVEL = 100
BATTERY_CHARGING = True  # True = solar charging, False = running on stored battery

sonne_var("battery_level", BATTERY_LEVEL)
sonne_var("battery_charging", BATTERY_CHARGING)
