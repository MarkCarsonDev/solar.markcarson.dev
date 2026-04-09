# Data Scripts

This directory contains Python scripts that run at build time to generate dynamic content for your site.

## How It Works

1. **Scripts are executed during build** - Every `.py` file in this directory runs when you build your site
2. **Set variables with `sonne_var()`** - Use `sonne_var('name', value)` to make data available to templates
3. **Variables available everywhere** - Use `{{ variable_name }}` in Jinja templates or `{+}{variable_name}` in content

## Example

```python
# scripts/build_info.py
from datetime import datetime

# Get current date
build_date = datetime.now().strftime("%Y-%m-%d %H:%M")

# Make it available to templates
sonne_var('build_date', build_date)
sonne_var('build_year', datetime.now().year)
```

Then use in templates:
```html
<footer>Built on {{ build_date }} © {{ build_year }}</footer>
```

Or in content files:
```markdown
Last updated: {+}{build_date}
```

## Included Scripts

- **random_intro.py** - Randomly selects a fun intro line for the homepage
