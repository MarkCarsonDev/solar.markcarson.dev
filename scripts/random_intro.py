# A random intro line for the home page ({{ random_intro }} in home.html).
import random

from sonne.script_api import sonne_var

INTRO_LINES = [
    "a fan of slow computers... sometimes...",
    "enjoyer of plants and the tiny.",
    "imbibed with a polyannish, solarpunk whimsy.",
]

sonne_var("random_intro", random.choice(INTRO_LINES))
