"""
CancerGuard AI - Per-user persistence.
Stores progress keyed by username, mirroring the users.json pattern.
"""

import json
import os
from datetime import date

PROGRESS_DIR = "user_data"

DEFAULT_PROGRESS = {
    "water": 0,
    "exercise": 0,
    "sleep": 7.0,

    "habit_diet": False,
    "habit_tobacco": False,
    "habit_activity": False,
    "habit_sun": False,
    "habit_screening": False,

    "awareness_score": 0,
    "goals": [],
    "score_history": [],
    "badges": [],
    "xp": 0,

    "full_name": "",
    "profile_age": 30,
    "health_goal": "Improve my diet",
    "email": "",

    "challenge_week": 1,
    "challenge_done": False,

    "last_active": "",
    "streak": 0,
    "best_streak": 0,
    "history": {},

    "mood_log": {},
    "priority_today": "",
    "checked_in_date": "",
    "rewards_claimed": [],
    "total_checkins": 0
}

DAILY_KEYS = [
    "water",
    "exercise",
    "habit_diet",
    "habit_tobacco",
    "habit_activity",
    "habit_sun",
    "habit_screening"
]


def _safe_name(username):
    """Strip characters that could escape the data directory."""
    return "".join(
        char for char in str(username)
        if char.isalnum() or char in ("-", "_")
    ).lower() or "user"


def _path(username):
    os.makedirs(PROGRESS_DIR, exist_ok=True)
    return os.path.join(
        PROGRESS_DIR,
        f"progress_{_safe_name(username)}.json"
    )


def load_progress(username):
    """Load a user's saved progress, filling any missing keys."""
    record = dict(DEFAULT_PROGRESS)

    file_path = _path(username)

    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                saved = json.load(file)

            for key, value in saved.items():
                if key in DEFAULT_PROGRESS:
                    record[key] = value

        except Exception:
            pass

    return record


def save_progress(username, record):
    """Write a user's progress to disk."""
    try:
        with open(_path(username), "w", encoding="utf-8") as file:
            json.dump(record, file, indent=4)
    except Exception:
        pass


def apply_daily_rollover(record):
    """
    Reset daily habits if the last visit was not today.
    Updates the streak and archives yesterday's totals.
    """
    today = date.today().isoformat()
    last = record.get("last_active", "")

    if last == today:
        return record, False

    if last:

        habits_done = sum(
            1 for key in DAILY_KEYS
            if key.startswith("habit_") and record.get(key)
        )

        history = record.get("history", {})

        history[last] = {
            "water": record.get("water", 0),
            "exercise": record.get("exercise", 0),
            "habits": habits_done
        }

        record["history"] = history

        try:
            gap = (
                date.fromisoformat(today)
                - date.fromisoformat(last)
            ).days
        except ValueError:
            gap = 99

        if gap == 1:
            record["streak"] = record.get("streak", 0) + 1
        else:
            record["streak"] = 1

    else:
        record["streak"] = 1

    for key in DAILY_KEYS:
        if key in ("water", "exercise"):
            record[key] = 0
        else:
            record[key] = False

    record["last_active"] = today

    return record, True


def update_best_streak(record):
    """Keep the all-time best streak up to date."""
    if record.get("streak", 0) > record.get("best_streak", 0):
        record["best_streak"] = record["streak"]
    return record


def personal_comparison(record):
    """Compare current streak against the user's own best."""
    current = record.get("streak", 0)
    best = record.get("best_streak", 0)

    if best == 0:
        return "This is your first streak. Every day counts."

    if current > best:
        return f"New personal best. Your previous record was {best} days."

    if current == best:
        return f"You have matched your personal best of {best} days."

    remaining = best - current

    return (
        f"Your best streak is {best} days. "
        f"{remaining} more to match it."
    )


def weekly_summary(record):
    """Aggregate the last seven recorded days."""
    history = record.get("history", {})

    if not history:
        return None

    recent = sorted(history.keys())[-7:]

    total_water = sum(
        history[day].get("water", 0) for day in recent
    )
    total_exercise = sum(
        history[day].get("exercise", 0) for day in recent
    )
    total_habits = sum(
        history[day].get("habits", 0) for day in recent
    )

    days = len(recent)

    return {
        "days": days,
        "avg_water": round(total_water / days, 1),
        "total_exercise": total_exercise,
        "avg_habits": round(total_habits / days, 1),
        "best_day": max(
            recent,
            key=lambda day: history[day].get("habits", 0)
        )
    }


def daily_index(seed_offset=0):
    """Stable index for date-seeded content."""
    return date.today().toordinal() + seed_offset


def xp_level(xp):
    """Return the level name for a given XP total."""
    if xp >= 500:
        return "Platinum"
    if xp >= 250:
        return "Gold"
    if xp >= 100:
        return "Silver"
    return "Bronze"


def award_xp(record, points):
    """Add XP and return the new level."""
    current = record.get("xp", 0) or 0
    record["xp"] = current + points
    return xp_level(record["xp"])