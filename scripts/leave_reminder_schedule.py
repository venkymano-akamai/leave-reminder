"""Bi-weekly scheduling helpers for the leave reminder job.

This script is intended to gate reminder execution to the 2nd and 4th
weeks of the month in Indian Standard Time.
"""

from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
DEFAULT_TARGET_WEEKS = (2, 4)
DEFAULT_TARGET_WEEKDAY = 0  # Monday (0=Mon, 6=Sun)


def week_of_month(day: date) -> int:
    """Return the week number in month (1-5) for a given date."""
    return (day.day - 1) // 7 + 1


def should_run(
    now: datetime | None = None,
    *,
    target_weeks: tuple[int, ...] = DEFAULT_TARGET_WEEKS,
    target_weekday: int = DEFAULT_TARGET_WEEKDAY,
    tz_name: str = "Asia/Kolkata",
) -> bool:
    """Return True when reminder should be sent.

    Rules:
    - Timezone is IST by default.
    - Only run during the 2nd and 4th weeks of the month.
    - Only run on a specific weekday (Monday by default) to avoid sending
      repeated reminders every day of those weeks.
    """
    tz = ZoneInfo(tz_name)

    if now is None:
        current = datetime.now(tz)
    elif now.tzinfo is None:
        current = now.replace(tzinfo=tz)
    else:
        current = now.astimezone(tz)

    return (
        week_of_month(current.date()) in target_weeks
        and current.weekday() == target_weekday
    )


if __name__ == "__main__":
    print("run" if should_run() else "skip")
