"""The views capture.py records, the names of their images, and its time budget.

capture.py writes the images, pairs.py chooses those judges see, and score.py
judges each capture's elapsed time against the budget.
"""

CAPTURE_BUDGET_SECONDS = 90.0
MOTION_FRAME_SECONDS = (0.25, 0.75, 1.5, 3.0)
SCROLL_DEPTHS_PERCENT = (25, 50, 75)


def motion_image(viewport: str, seconds: float) -> str:
    """The first screen of viewport, seconds after navigation."""
    return f"{viewport}-motion-{seconds}s.png"


def scroll_image(viewport: str, percent: int) -> str:
    """The screen of viewport scrolled to percent of the page's depth."""
    return f"{viewport}-scroll-{percent}.png"
