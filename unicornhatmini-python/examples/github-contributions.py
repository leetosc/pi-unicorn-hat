#!/usr/bin/env python3
"""Show a GitHub user's contribution graph on the Unicorn HAT Mini.

The display is 17x7 pixels which is a perfect fit for the last 17 weeks
of a GitHub contribution graph: one column per week, one row per weekday
(Sunday at the top, Saturday at the bottom) just like github.com.

Usage:
    ./github-contributions.py <username>

Contribution data is fetched from the public, no-auth API at
https://github-contributions-api.jogruber.de which mirrors the data shown
on a user's GitHub profile.
"""
import json
import sys
import time
from datetime import datetime, timedelta
from urllib.request import urlopen, Request

from unicornhatmini import UnicornHATMini


# GitHub-style green levels 0-4. Level 0 is "no contributions" and is shown
# as a very dim slate so the empty cells are still visible on the board.
LEVEL_COLOURS = [
    (4, 8, 10),       # 0 - none
    (14, 68, 41),     # 1 - low
    (38, 166, 65),    # 2 - medium
    (57, 211, 102),   # 3 - high
    (86, 255, 130),   # 4 - max
]

WIDTH = 17   # weeks
HEIGHT = 7   # days per week


def fetch_contributions(username):
    """Return a flat, date-sorted list of {date, count, level} dicts."""
    url = "https://github-contributions-api.jogruber.de/v4/{}".format(username)
    request = Request(url, headers={"User-Agent": "unicornhatmini"})
    with urlopen(request, timeout=15) as response:
        data = json.loads(response.read().decode("utf-8"))

    if "contributions" not in data:
        raise ValueError("No contribution data for user '{}'".format(username))

    contributions = data["contributions"]
    contributions.sort(key=lambda c: c["date"])
    return contributions


def build_grid(contributions):
    """Map the last 17 weeks of contributions onto a 17x7 grid of levels.

    Columns are weeks (oldest on the left), rows are weekdays with Sunday at
    the top to match the github.com layout.
    """
    # Group contributions by the Sunday that starts their week.
    weeks = {}
    for entry in contributions:
        date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
        # Python: Monday=0..Sunday=6. GitHub rows: Sunday=0..Saturday=6.
        row = (date.weekday() + 1) % 7
        week_start = date - timedelta(days=row)
        weeks.setdefault(week_start, [0] * HEIGHT)[row] = entry["level"]

    # Keep only the most recent 17 weeks.
    recent = sorted(weeks)[-WIDTH:]

    grid = [[0] * HEIGHT for _ in range(WIDTH)]
    for x, week_start in enumerate(recent):
        grid[x] = weeks[week_start]
    return grid


def main():
    if len(sys.argv) != 2:
        print("Usage: {} <github-username>".format(sys.argv[0]))
        sys.exit(1)

    username = sys.argv[1]

    print("Fetching contributions for '{}'...".format(username))
    contributions = fetch_contributions(username)
    grid = build_grid(contributions)

    unicornhatmini = UnicornHATMini()
    unicornhatmini.set_rotation(0)
    unicornhatmini.set_brightness(0.5)

    for x in range(WIDTH):
        for y in range(HEIGHT):
            level = grid[x][y]
            unicornhatmini.set_pixel(x, y, *LEVEL_COLOURS[level])

    unicornhatmini.show()
    print("Showing last {} weeks. Press Ctrl+C to exit.".format(WIDTH))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        unicornhatmini.clear()
        unicornhatmini.show()


if __name__ == "__main__":
    main()
