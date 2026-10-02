# Data Scripts

This directory contains Python scripts that run at build time to generate dynamic content for your site.

## How It Works

1. **Scripts are executed during build** - Every `.py` file in this directory runs when you build your site
2. **Set variables with `sonne_var()`** - `from sonne.script_api import sonne_var, sonne_config`, then `sonne_var('name', value)` makes data available to templates and `sonne_config('section', 'key')` reads the site config
3. **Variables available everywhere** - Use `{{ data.variable_name }}` in Jinja templates

## Example

```python
# scripts/example.py
from datetime import datetime

from sonne.script_api import sonne_var

# Get current date
build_date = datetime.now().strftime("%Y-%m-%d %H:%M")

# Make it available to templates
sonne_var('build_date', build_date)
sonne_var('build_year', datetime.now().year)
```

Then use in templates:
```html
<footer>Built on {{ data.build_date }} © {{ data.build_year }}</footer>
```

## Included Scripts

Scripts supply data only; the HTML that shows it lives in `templates/`.

- **solar_status.py** - battery level / charging flag shown in the banner (`partials/banner.html`)
- **build_info.py** - `compiled_at` timestamp (LA time) shown in the footer (`partials/footer.html`)
- **random_intro.py** - randomly selects a fun intro line for the homepage
- **reading.py** - reading shelves and dithered book covers from books.markcarson.dev (`home.html`)
