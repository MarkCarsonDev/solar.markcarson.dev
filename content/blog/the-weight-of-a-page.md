---
draft: true
title: The Weight of a Page
date: 2026-04-06
date_edited: auto
description: On page weight, dithered images, and what it actually means to run a website on a solar panel.
author: Mark
tags:
  - solar
  - web
  - performance
cover_img: ./img/seattle_flowers.jpg
---

[TOC]

This site runs on a few panels laying haphazardly on my apartment balcony. When the battery runs low, the site goes offline -  and stays offline -  until the sun comes back up. So, why run a site like this when all of my friends are shipping 200 MB game engines to their visitors browsers?

## Why Page Weight Matters {#weight}

The average webpage in 2024 transferred around 2.6 MB to load.[^httparchive] For a solar-powered server drawing around 3W idle and peaking at 7W under load, serving that page to a thousand visitors costs meaningful watt-hours. 

But the server-side cost is only half the story. Every visitor's device also has to download, decode, and render that payload. On a phone on a slow connection, 2.6 MB takes seconds and drains some of someone else's battery too. The weight of a page doesn't disappear when it leaves the server.

This site targets under 100 KB per page transfer, uncompressed.

## Key Techniques {#techniques}

A few things actually move the needle on page weight:

Downscaling and dithering
:   Generally, images are the biggest ticket item for a page. Converting full-color photographs to a small indexed palette before serving them. A 400px wide dithered PNG is typically 8--25 KB versus 80--200 KB for an equivalent JPEG. 

Static generation
:   No database queries, no server-side rendering per request. The HTML is pre-built at deploy time and served directly from SD card. The server does almost no computation per visit.

System fonts
:   Using `monospace` and `serif` font stacks means zero font files are ever downloaded. The browser uses whatever the OS ships, which is good enough to read with..

No JS frameworks
:   The only JS on this site handles the dither/original image toggle and keyboard navigation. It's under 2 KB, inline, and adds no network round-trips.

## Page Weight in Practice {#comparison}

Rough numbers, measured from the built output:

| Page | Images served | Approx. transfer |
|---|---|---|
| Home | None | ~18 KB |
| Blog list | Dithered covers | ~35--60 KB |
| Blog post (text only) | None | ~14 KB |
| Blog post (with images) | Dithered inline + cover | ~40--90 KB |
| After "view original" | Original loaded on demand | ~150--400 KB |

The "view original" cost is real but opt-in. You clicked a button to get there --- it wasn't pushed to you.

## The Dithering Pipeline {#dithering}

When you add an image to a post, Sonne processes it at build time rather than runtime. Simplified version of what happens:

```python
def _process_blog_image(self, source_path, output_path, max_width):
    img = Image.open(source_path).convert("RGB")
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
    img = img.convert("P", palette=Image.ADAPTIVE, colors=self.dither_colors)
    img.save(output_path, format="PNG", optimize=True)
```

The result is saved alongside the original. The dithered version loads by default; the original is fetched only if you request it via the "view original" button.[^blendmode]

This approach means a visitor who never clicks anything never pays the cost of the original. A visitor who wants the full image gets it --- but they asked for it.

## What "Solar-Powered" Actually Means {#solar}

It's not a metaphor or a branding exercise. The stack is:

1. A SBC running Linux on a draw of around 2--4W idle
2. A small LiPo battery pack with a charge controller
3. A 10W solar panel on a south-facing windowsill

When battery state drops below a threshold, the server shuts down gracefully. When it recovers, it comes back up. There's no cloud fallback, no secondary host, no CDN keeping a cached copy alive.

The tradeoff is uptime. This site is offline on cloudy days. In winter, it might be down most evenings. That's intentional --- the availability of the site is a live signal of the weather outside. I find that more honest than pretending the energy comes from nowhere.[^uptime]

## Does It Actually Matter? {#conclusion}

Probably not at my scale. The difference between this site and a 2.6 MB page, summed across all my visitors, rounds to zero against global data center consumption.

But that's not really the point. The constraint is useful because it forces decisions that are otherwise easy to defer. When every KB costs something, you think about what's actually necessary. That habit --- asking what's necessary --- is worth more than the watt-hours saved.

---

*[SSG]: Static Site Generator
*[SBC]: Single-Board Computer
*[KB]: Kilobyte
*[MB]: Megabyte
*[JS]: JavaScript
*[CSS]: Cascading Style Sheets
*[PNG]: Portable Network Graphics
*[JPEG]: Joint Photographic Experts Group
*[CDN]: Content Delivery Network
*[LiPo]: Lithium Polymer

[^httparchive]: HTTP Archive tracks median page weight across millions of crawled URLs. As of late 2024 the median desktop page was approximately 2.6 MB transferred. See [httparchive.org/reports/page-weight](https://httparchive.org/reports/page-weight).

[^blendmode]: In light mode, the figure element gets `mix-blend-mode: multiply`. This works because the dithered image has a white background --- multiplying white (1.0) against any color returns that color unchanged, making the background invisible. Dark pixels are near-zero and naturally darken whatever sits behind them. No masking required.

[^uptime]: Low-tech Magazine's solar-powered site has tracked its uptime publicly since 2018 and publishes monthly battery and generation stats. It's the clearest precedent for this approach. See [solar.lowtechmagazine.com/about](https://solar.lowtechmagazine.com/about).
