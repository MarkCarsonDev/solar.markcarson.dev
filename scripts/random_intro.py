"""
Data script to generate a random intro line for the homepage.
This replaces the embedded Python in the original index.html
"""

import random

# List of possible intro lines
intro_options = [
    "a fan of slow computers, sometimes.",
    "enjoyer of plants and the tiny.",
    "solarpunk-ish kinda guy.",
    "amateur (and mid) photographer."
]

# Pick a random one and set it as a Sonne variable
random_intro = random.choice(intro_options)

# Make it available to templates as {+}{random_intro} or {{ random_intro }}
sonne_var('random_intro', random_intro)
