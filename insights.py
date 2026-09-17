"""
CancerGuard AI - Rule-based personal insights.

All insights describe behaviour, never risk. Nothing here
claims a health outcome or implies a change in cancer risk.
"""

from datetime import date


def generate_insights(record):
    """Return a list of behavioural insight dictionaries."""
    insights = []

    water = record.get("water", 0)
    exercise = record.get("exercise", 0)
    sleep = record.get("sleep", 7.0)
    streak = record.get("streak", 0)
    history = record.get("history", {})

    habits = sum([
        record.get("habit_diet", False),
        record.get("habit_tobacco", False),
        record.get("habit_activity", False),
        record.get("habit_sun", False),
        record.get("habit_screening", False)
    ])

    # --- Today's gaps ---
    if water < 8:
        insights.append({
            "tone": "info",
            "title": "Hydration",
            "text": (
                f"You have logged {water} of 8 glasses. "
                f"{8 - water} more would meet your daily target."
            )
        })
    else:
        insights.append({
            "tone": "success",
            "title": "Hydration",
            "text": "You have met your water target today."
        })

    if exercise == 0:
        insights.append({
            "tone": "info",
            "title": "Movement",
            "text": (
                "No activity logged yet. A ten-minute walk is "
                "enough to start the day's count."
            )
        })
    elif exercise < 30:
        insights.append({
            "tone": "info",
            "title": "Movement",
            "text": (
                f"{exercise} minutes logged. "
                f"{30 - exercise} more reaches the daily target."
            )
        })

    if sleep < 6:
        insights.append({
            "tone": "warning",
            "title": "Rest",
            "text": (
                f"You logged {sleep} hours. Short sleep affects "
                "energy and decision-making. Consider an earlier night."
            )
        })

    # --- Weekly pattern ---
    if len(history) >= 3:

        recent = sorted(history.keys())[-7:]

        water_days = [
            history[day].get("water", 0) for day in recent
        ]
        habit_days = [
            history[day].get("habits", 0) for day in recent
        ]

        avg_water = sum(water_days) / len(water_days)
        avg_habits = sum(habit_days) / len(habit_days)

        if avg_water < 5:
            insights.append({
                "tone": "info",
                "title": "Weekly pattern",
                "text": (
                    f"Your average has been {avg_water:.1f} glasses "
                    "over recent days. Try keeping a bottle at your desk."
                )
            })

        if avg_habits >= 4:
            insights.append({
                "tone": "success",
                "title": "Weekly pattern",
                "text": (
                    f"You are averaging {avg_habits:.1f} of 5 habits. "
                    "That is strong consistency."
                )
            })

        weakest = min(
            recent,
            key=lambda d: history[d].get("habits", 0)
        )

        if history[weakest].get("habits", 0) <= 1:
            insights.append({
                "tone": "info",
                "title": "Quieter day",
                "text": (
                    f"{weakest} was your lightest day. "
                    "Missing a day is normal. What matters is returning."
                )
            })

    # --- Habit-specific nudges ---
    if not record.get("habit_screening", False) and streak >= 3:
        insights.append({
            "tone": "info",
            "title": "Screening",
            "text": (
                "You have been consistent for several days. "
                "This is a good moment to check whether any "
                "age-appropriate screening applies to you."
            )
        })

    if habits == 5:
        insights.append({
            "tone": "success",
            "title": "Full day",
            "text": "All five habits completed today."
        })

    return insights


def daily_prompt(seed_index):
    """Return a reflective prompt that rotates by date."""
    prompts = [
        "What is one small health action you can take today?",
        "What made yesterday easier or harder than expected?",
        "Is there a change in your body you have been meaning to mention?",
        "Who could you encourage to check their own health this week?",
        "What time of day do you find it easiest to be active?",
        "What would make tomorrow slightly better than today?",
        "Have you booked any appointment you have been postponing?"
    ]
    return prompts[seed_index % len(prompts)]


def unlock_content(seed_index, claimed):
    """
    Return today's unlockable educational content.
    Deterministic by date, so it is the same for a given day.
    """
    library = [
        {
            "id": "hydration",
            "title": "Hydration and health",
            "text": (
                "Water supports circulation, temperature regulation "
                "and kidney function. Thirst is a late signal, so "
                "regular small amounts work better than large gaps."
            )
        },
        {
            "id": "fibre",
            "title": "Why fibre matters",
            "text": (
                "Dietary fibre supports bowel health and is associated "
                "with lower colorectal cancer risk in population studies. "
                "Whole grains, beans and vegetables are good sources."
            )
        },
        {
            "id": "uv_index",
            "title": "Reading the UV index",
            "text": (
                "A UV index of 3 or above means sun protection is "
                "advisable. The index is often higher than people "
                "expect on cloudy days."
            )
        },
        {
            "id": "sleep_cycle",
            "title": "Sleep and recovery",
            "text": (
                "Consistent sleep and wake times support better sleep "
                "quality than total hours alone. Aim for regularity "
                "before aiming for duration."
            )
        },
        {
            "id": "family_history",
            "title": "Mapping family history",
            "text": (
                "Knowing which relatives had which conditions, and at "
                "what age, helps a doctor judge whether earlier "
                "screening is appropriate for you."
            )
        },
        {
            "id": "activity_snacks",
            "title": "Activity in small pieces",
            "text": (
                "Three ten-minute walks count the same as one thirty "
                "minute walk. Breaking activity up makes it easier "
                "to sustain."
            )
        },
        {
            "id": "asking_questions",
            "title": "Getting more from an appointment",
            "text": (
                "Writing questions down beforehand and bringing someone "
                "with you both improve how much information you retain "
                "from a consultation."
            )
        }
    ]

    item = library[seed_index % len(library)]
    item = dict(item)
    item["already_claimed"] = item["id"] in claimed

    return item