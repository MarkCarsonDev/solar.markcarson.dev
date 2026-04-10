---
title: Personal Timeclock
date_posted: 2025-2-4
date_edited: 2025-2-4
description: About the tool I made to keep track of my time spent on personal projects, cLockIn
author: Mark
page_url: about-clockin
cover_img: none
tags: project
---
# Inspiration

With one of my employers, we used the tool Wrike as a digital timesheet. Wrike has a satisfying feature to quickly name a task, start a timer on that task, and when you stop it, it's automatically added to a timesheet. At a period where I was spending more than just work-hours on my computer and online, I wanted a tool to track my time, help me build accountability, and have easy to reference entries for when looking back on some period in my life.

Thus **cLockIn** was born.

# What it is

**cLockIn** is a simple, OS toolbar based application (built for MacOS) that asks a user what they're working on, starts a timer when they respond, and saves that entry to their Google Calendar when they stop the timer. The application is built in Python and leverages Google's Workspace API and OAuth2 tooling to authenticate the user and application.
