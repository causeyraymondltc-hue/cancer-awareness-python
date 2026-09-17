import streamlit as st
import pandas as pd
import json
import os
import hashlib
import secrets
from datetime import date

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

import plotly.express as px

from cancer_content import (
    CANCER_LIBRARY,
    SYMPTOM_GUIDE,
    EMERGENCY_SIGNS,
    NEXT_STEPS,
    MYTHS,
    screening_guidance,
    CARE_JOURNEY,
    DOCTOR_QUESTIONS,
    SUPPORT_TOPICS,
    CARE_FACILITIES,
    CARE_PATHWAY,
    DISCLAIMER,
    SOURCES
)

from assistant import answer_question

try:
    from assistant import search_knowledge
except ImportError:
    def search_knowledge(query):
        return []

from visuals import (
    GLOBAL_CSS,
    ANIMATED_BACKGROUND,
    dashboard_strip,
    hero_banner,
    react_stat_cards,
    react_progress_rings,
    style_chart,
    render_table
)

from storage import (
    load_progress,
    save_progress,
    apply_daily_rollover,
    daily_index,
    award_xp,
    xp_level,
    personal_comparison,
    update_best_streak,
    weekly_summary,
    DEFAULT_PROGRESS
)

from insights import (
    generate_insights,
    daily_prompt,
    unlock_content
)

from images import image_banner, framed_image


# =====================================================
# PAGE SETUP
# =====================================================
st.set_page_config(
    page_title="CancerGuard AI",
    page_icon="🔐",
    layout="wide"
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown(ANIMATED_BACKGROUND, unsafe_allow_html=True)


# =====================================================
# USER ACCOUNT STORAGE
# =====================================================
USER_FILE = "users.json"

SECURITY_QUESTIONS = [
    "What was the name of your first school?",
    "What is your mother's maiden name?",
    "What was the name of your first pet?",
    "What city were you born in?",
    "What is your favourite book?"
]


def hash_value(value):
    """Hash a security answer."""
    return hashlib.sha256(
        value.strip().lower().encode("utf-8")
    ).hexdigest()


def hash_password(password, salt=None):
    """PBKDF2 with a random salt. Returns 'salt$hash'."""
    if salt is None:
        salt = secrets.token_hex(16)

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        200_000
    ).hex()

    return f"{salt}${digest}"


def verify_password(password, stored):
    """Check a password. Supports legacy unsalted SHA-256 records."""
    if not stored:
        return False

    if "$" not in stored:
        legacy = hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()
        return secrets.compare_digest(legacy, stored)

    salt = stored.split("$", 1)[0]
    return secrets.compare_digest(
        hash_password(password, salt),
        stored
    )


def default_users():
    return {
        "demo": {
            "password": hash_password("password"),
            "question": SECURITY_QUESTIONS[0],
            "answer": hash_value("demo school"),
            "token": ""
        }
    }


def load_users():
    """Load users. Supports old string format and new dict format."""
    if not os.path.exists(USER_FILE):
        return default_users()

    try:
        with open(USER_FILE, "r", encoding="utf-8") as file:
            saved = json.load(file)

        converted = {}

        for username, record in saved.items():

            if isinstance(record, str):
                converted[username] = {
                    "password": record,
                    "question": SECURITY_QUESTIONS[0],
                    "answer": "",
                    "token": ""
                }
            else:
                converted[username] = {
                    "password": record.get("password", ""),
                    "question": record.get(
                        "question", SECURITY_QUESTIONS[0]
                    ),
                    "answer": record.get("answer", ""),
                    "token": record.get("token", "")
                }

        return converted

    except Exception:
        return default_users()


def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)


def issue_token(username):
    """Create and store a remember-me token."""
    token = secrets.token_urlsafe(24)
    st.session_state.users[username]["token"] = token
    save_users(st.session_state.users)
    return token


def find_user_by_token(token):
    """Return username matching a remember-me token."""
    if not token:
        return None

    for username, record in st.session_state.users.items():
        if record.get("token") and record["token"] == token:
            return username

    return None


def clear_token(username):
    if username in st.session_state.users:
        st.session_state.users[username]["token"] = ""
        save_users(st.session_state.users)


# =====================================================
# SESSION STATE
# =====================================================
session_defaults = {
    "users": load_users(),
    "logged_in": False,
    "current_user": None,
    "loaded_for": None,
    "chat_history": [],
    "demo_group": "Prefer not to say"
}

for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

for key, value in DEFAULT_PROGRESS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# REMEMBER ME RESTORE
# =====================================================
if not st.session_state.get("logged_in", False):

    saved_token = st.query_params.get("t", "")
    matched_user = find_user_by_token(saved_token)

    if matched_user:
        st.session_state.logged_in = True
        st.session_state.current_user = matched_user


# =====================================================
# LOGIN, REGISTER AND PASSWORD RESET
# =====================================================
if not st.session_state.get("logged_in", False):

    image_banner(
        "sunrise",
        "CancerGuard AI",
        "Early awareness. Better health. A brighter future.",
        height=240
    )

    st.title("Customer Access Portal")

    login_tab, register_tab, reset_tab = st.tabs(
        ["Login", "Create Account", "Forgot Password"]
    )

    # -------------------------------------------------
    # LOGIN
    # -------------------------------------------------
    with login_tab:

        with st.form("login_form"):

            username_input = st.text_input(
                "Username",
                key="login_username"
            )

            password_input = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            remember_me = st.checkbox(
                "Keep me signed in on this device",
                value=False,
                key="remember_me"
            )

            login_button = st.form_submit_button("Login")

            if login_button:

                username = username_input.strip()
                record = st.session_state.users.get(username)

                if record and verify_password(
                    password_input, record.get("password", "")
                ):

                    if "$" not in record.get("password", ""):
                        st.session_state.users[username]["password"] = (
                            hash_password(password_input)
                        )
                        save_users(st.session_state.users)

                    st.session_state.logged_in = True
                    st.session_state.current_user = username

                    if remember_me:
                        token = issue_token(username)
                        st.query_params["t"] = token

                    st.rerun()

                else:
                    st.error("Incorrect username or password.")

        st.divider()

        st.caption(
            "CancerGuard AI uses username and password authentication. "
            "Single sign-on with Google is documented in the project "
            "roadmap as a planned enhancement."
        )

    # -------------------------------------------------
    # REGISTER
    # -------------------------------------------------
    with register_tab:

        with st.form("register_form"):

            new_username = st.text_input(
                "Choose a username",
                key="register_username"
            )

            new_password = st.text_input(
                "Choose a password",
                type="password",
                key="register_password"
            )

            confirm_password = st.text_input(
                "Confirm password",
                type="password",
                key="confirm_password"
            )

            chosen_question = st.selectbox(
                "Security question for password recovery",
                SECURITY_QUESTIONS,
                key="register_question"
            )

            chosen_answer = st.text_input(
                "Your answer",
                key="register_answer"
            )

            register_button = st.form_submit_button("Create Account")

            if register_button:

                new_username = new_username.strip()

                if not new_username or not new_password:
                    st.error("Please complete all fields.")

                elif len(new_username) < 3:
                    st.error(
                        "Username must contain at least 3 characters."
                    )

                elif len(new_password) < 6:
                    st.error(
                        "Password must contain at least 6 characters."
                    )

                elif new_password != confirm_password:
                    st.error("Passwords do not match.")

                elif not chosen_answer.strip():
                    st.error(
                        "Please answer the security question so you can "
                        "recover your account later."
                    )

                elif new_username in st.session_state.users:
                    st.error("Username already exists.")

                else:
                    st.session_state.users[new_username] = {
                        "password": hash_password(new_password),
                        "question": chosen_question,
                        "answer": hash_value(chosen_answer),
                        "token": ""
                    }

                    save_users(st.session_state.users)

                    st.success(
                        "Account created. You can now log in."
                    )

    # -------------------------------------------------
    # FORGOT PASSWORD
    # -------------------------------------------------
    with reset_tab:

        st.write(
            "Reset your password by answering your security question."
        )

        reset_username = st.text_input(
            "Your username",
            key="reset_username"
        )

        reset_target = st.session_state.get("users", {}).get(
            reset_username.strip()
        )

        if reset_username.strip() and not reset_target:
            st.error("No account found with that username.")

        elif reset_target:

            if not reset_target.get("answer"):
                st.warning(
                    "This account has no security question set, so it "
                    "cannot be recovered. Please create a new account."
                )

            else:

                with st.form("reset_form"):

                    st.info(reset_target["question"])

                    reset_answer = st.text_input(
                        "Your answer",
                        key="reset_answer"
                    )

                    reset_new = st.text_input(
                        "New password",
                        type="password",
                        key="reset_new"
                    )

                    reset_confirm = st.text_input(
                        "Confirm new password",
                        type="password",
                        key="reset_confirm"
                    )

                    reset_button = st.form_submit_button(
                        "Reset Password"
                    )

                    if reset_button:

                        if hash_value(reset_answer) != reset_target["answer"]:
                            st.error("That answer does not match.")

                        elif len(reset_new) < 6:
                            st.error(
                                "Password must contain at least "
                                "6 characters."
                            )

                        elif reset_new != reset_confirm:
                            st.error("Passwords do not match.")

                        else:
                            username_clean = reset_username.strip()

                            st.session_state.users[username_clean][
                                "password"
                            ] = hash_password(reset_new)

                            st.session_state.users[username_clean][
                                "token"
                            ] = ""

                            save_users(st.session_state.users)

                            st.success(
                                "Password reset. Please log in with your "
                                "new password."
                            )

    st.divider()

    st.info(
        "Demo account: username `demo`, password `password`. "
        "Security answer: `demo school`"
    )

    st.warning(
        "This is a portfolio authentication demo. It does not use "
        "production-grade security. Do not enter real medical or "
        "sensitive personal data."
    )

    st.stop()


# =====================================================
# CURRENT USER AND SAVED PROGRESS
# =====================================================
current_user = st.session_state.get("current_user", "User")

if st.session_state.loaded_for != current_user:

    saved_record = load_progress(current_user)
    saved_record, rolled_over = apply_daily_rollover(saved_record)
    saved_record = update_best_streak(saved_record)

    for key, value in saved_record.items():
        st.session_state[key] = value

    st.session_state.loaded_for = current_user
    st.session_state.chat_history = []

    save_progress(current_user, saved_record)

    if rolled_over:
        st.toast("New day. Daily habits have been reset.")


def persist():
    """Write current session values back to disk."""
    record = {
        key: st.session_state.get(key, default)
        for key, default in DEFAULT_PROGRESS.items()
    }

    record = update_best_streak(record)

    st.session_state.best_streak = record.get("best_streak", 0)

    save_progress(current_user, record)


def current_record():
    """Snapshot the current progress values."""
    return {
        key: st.session_state.get(key, default)
        for key, default in DEFAULT_PROGRESS.items()
    }


# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:

    st.title("CancerGuard AI")

    st.write(f"Logged in as: {current_user}")

    st.caption(date.today().strftime("%A, %d %B %Y"))

    st.divider()

    streak_days = st.session_state.get("streak", 0)
    best_days = st.session_state.get("best_streak", 0)
    total_xp = st.session_state.get("xp", 0)

    st.metric(
        "Daily Streak",
        f"{streak_days} day{'s' if streak_days != 1 else ''}",
        f"Best: {best_days}"
    )

    st.caption(
        personal_comparison({
            "streak": streak_days,
            "best_streak": best_days
        })
    )

    st.metric(
        "Level",
        xp_level(total_xp),
        f"{total_xp} XP"
    )

    st.divider()

    st.subheader("Quick Statistics")

    st.metric(
        "Awareness Score",
        f"{st.session_state.awareness_score}/100"
    )

    st.metric(
        "Water Intake",
        f"{st.session_state.water}/8 glasses"
    )

    st.metric(
        "Exercise",
        f"{st.session_state.exercise} minutes"
    )

    st.divider()

    st.caption("Built by Toluwalope")

    st.divider()

    if st.button("Logout", width="stretch"):

        persist()

        if st.session_state.current_user:
            clear_token(st.session_state.current_user)

        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.loaded_for = None

        st.query_params.clear()

        st.rerun()


# =====================================================
# HEADER
# =====================================================
hero_banner(
    title="CancerGuard AI",
    subtitle=(
        "Turning cancer data into prevention, awareness and early action. "
        "Educational tools built for underserved communities."
    ),
    tagline="Prevent · Understand · Detect Early · Navigate Care"
)

st.warning(
    """
    CancerGuard AI is an educational portfolio application.
    It does not diagnose cancer, predict personal cancer risk,
    or replace professional medical advice, screening, or treatment.
    """
)


# =====================================================
# NAVIGATION
# =====================================================
(
    tab_home,
    tab_prevention,
    tab_lifestyle,
    tab_goals,
    tab_challenge,
    tab_learn,
    tab_detect,
    tab_assistant,
    tab_care,
    tab_research,
    tab_profile
) = st.tabs(
    [
        "Dashboard",
        "Prevent",
        "Healthy Living",
        "Goals",
        "Weekly Challenge",
        "Learn",
        "Detect",
        "AI Assistant",
        "Care",
        "ML Research",
        "Profile"
    ]
)


# =====================================================
# DASHBOARD
# =====================================================
with tab_home:

    completed_habits = sum(
        [
            st.session_state.habit_diet,
            st.session_state.habit_tobacco,
            st.session_state.habit_activity,
            st.session_state.habit_sun,
            st.session_state.habit_screening
        ]
    )

    dashboard_strip(
        current_user,
        [
            {
                "label": "Streak",
                "value": f"{st.session_state.get('streak', 0)}d",
                "percent": min(
                    st.session_state.get("streak", 0) / 7 * 100, 100
                )
            },
            {
                "label": "Awareness",
                "value": f"{st.session_state.awareness_score}",
                "percent": st.session_state.awareness_score
            },
            {
                "label": "Water",
                "value": f"{st.session_state.water}/8",
                "percent": min(st.session_state.water / 8 * 100, 100)
            },
            {
                "label": "Habits",
                "value": f"{completed_habits}/5",
                "percent": completed_habits / 5 * 100
            }
        ]
    )

    st.caption(date.today().strftime("%A, %d %B %Y"))

    st.divider()

    # -------------------------------------------------
    # DAILY CHECK-IN
    # -------------------------------------------------
    today_iso = date.today().isoformat()

    already_checked_in = (
        st.session_state.get("checked_in_date") == today_iso
    )

    if not already_checked_in:

        with st.container(border=True):

            st.subheader("Daily Check-In")

            st.caption(
                "Optional. Takes about thirty seconds and earns 10 XP."
            )

            with st.form("daily_checkin"):

                mood = st.select_slider(
                    "How are you feeling today?",
                    options=[
                        "Struggling",
                        "Low",
                        "Okay",
                        "Good",
                        "Strong"
                    ],
                    value="Okay"
                )

                took_action = st.checkbox(
                    "I took at least one health action today"
                )

                st.write(daily_prompt(daily_index()))

                priority = st.text_input(
                    "Your answer (optional)"
                )

                checkin_submit = st.form_submit_button(
                    "Complete Check-In"
                )

                if checkin_submit:

                    st.session_state.mood_log[today_iso] = mood
                    st.session_state.priority_today = priority.strip()
                    st.session_state.checked_in_date = today_iso
                    st.session_state.total_checkins = (
                        st.session_state.get("total_checkins", 0) + 1
                    )

                    award_xp(st.session_state, 10)

                    if took_action:
                        award_xp(st.session_state, 5)

                    persist()

                    st.rerun()

    else:

        with st.container(border=True):

            st.subheader("Check-In Complete")

            st.write(
                "Mood today: "
                f"{st.session_state.mood_log.get(today_iso, 'Not set')}"
            )

            if st.session_state.get("priority_today"):
                st.write(
                    f"Your focus: {st.session_state.priority_today}"
                )

            st.caption(
                personal_comparison({
                    "streak": st.session_state.get("streak", 0),
                    "best_streak": st.session_state.get("best_streak", 0)
                })
            )

    st.divider()

    # -------------------------------------------------
    # TODAY'S UNLOCK
    # -------------------------------------------------
    st.subheader("Today's Unlock")

    todays_content = unlock_content(
        daily_index(),
        st.session_state.get("rewards_claimed", [])
    )

    if todays_content["already_claimed"]:

        with st.container(border=True):
            st.write(f"**{todays_content['title']}**")
            st.write(todays_content["text"])
            st.caption("Unlocked. A new topic appears tomorrow.")

    else:

        with st.container(border=True):

            st.write(f"**{todays_content['title']}**")

            st.caption("Available today. Unlocking earns 5 XP.")

            if st.button("Unlock this topic"):

                st.session_state.rewards_claimed.append(
                    todays_content["id"]
                )

                award_xp(st.session_state, 5)
                persist()
                st.rerun()

    st.divider()

    # -------------------------------------------------
    # TODAY'S FOCUS
    # -------------------------------------------------
    st.subheader("Today's Focus")

    quotes = [
        "Small steps every day lead to big changes.",
        "Your health is an investment, not an expense.",
        "Prevention today can support a healthier future.",
        "Knowledge helps people make informed decisions.",
        "Every healthy choice matters.",
        "Progress is more important than perfection.",
        "A healthy lifestyle is built one habit at a time."
    ]

    micro_tips = [
        "Swap one sugary drink for water today.",
        "Take a ten-minute walk after a meal.",
        "Add one extra vegetable to dinner.",
        "Check the UV forecast before going outside.",
        "Note any body change you have noticed this week.",
        "Ask a family member about their health history.",
        "Set a reminder for your next check-up."
    ]

    today_index = daily_index()

    st.info(quotes[today_index % len(quotes)])

    st.caption(
        f"Today's action: {micro_tips[today_index % len(micro_tips)]}"
    )

    st.divider()

    react_stat_cards([
        {
            "label": "Awareness Score",
            "value": st.session_state.awareness_score,
            "unit": "/100",
            "percent": st.session_state.awareness_score,
            "color": "linear-gradient(135deg,#EC4899,#BE185D)"
        },
        {
            "label": "Water Intake",
            "value": st.session_state.water,
            "unit": "glasses",
            "percent": min(st.session_state.water / 8 * 100, 100),
            "color": "linear-gradient(135deg,#38BDF8,#0284C7)"
        },
        {
            "label": "Exercise",
            "value": st.session_state.exercise,
            "unit": "min",
            "percent": min(st.session_state.exercise / 30 * 100, 100),
            "color": "linear-gradient(135deg,#34D399,#059669)"
        },
        {
            "label": "Sleep",
            "value": int(st.session_state.sleep),
            "unit": "hrs",
            "percent": min(st.session_state.sleep / 7 * 100, 100),
            "color": "linear-gradient(135deg,#A78BFA,#6D28D9)"
        }
    ])

    st.divider()

    st.subheader("Healthy Living Progress")

    react_progress_rings([
        {
            "label": "Water",
            "percent": min(st.session_state.water / 8 * 100, 100),
            "color": "#0EA5E9"
        },
        {
            "label": "Exercise",
            "percent": min(st.session_state.exercise / 30 * 100, 100),
            "color": "#10B981"
        },
        {
            "label": "Sleep",
            "percent": min(st.session_state.sleep / 7 * 100, 100),
            "color": "#8B5CF6"
        },
        {
            "label": "Habits",
            "percent": completed_habits / 5 * 100,
            "color": "#EC4899"
        }
    ])

    st.divider()

    # -------------------------------------------------
    # INSIGHTS
    # -------------------------------------------------
    st.subheader("Your Insights")

    st.caption(
        "These describe your logged behaviour. They do not assess "
        "or predict any medical outcome."
    )

    insight_list = generate_insights(current_record())

    for insight in insight_list:

        with st.container(border=True):

            st.write(f"**{insight['title']}**")

            if insight["tone"] == "success":
                st.success(insight["text"])
            elif insight["tone"] == "warning":
                st.warning(insight["text"])
            else:
                st.info(insight["text"])

    st.divider()

    # -------------------------------------------------
    # WEEKLY SUMMARY
    # -------------------------------------------------
    st.subheader("Your Week")

    summary = weekly_summary(current_record())

    if not summary:
        st.info(
            "Your weekly summary appears after your first full "
            "day of tracking."
        )
    else:

        week_col1, week_col2, week_col3 = st.columns(3)

        with week_col1:
            st.metric(
                "Average water",
                f"{summary['avg_water']} glasses"
            )

        with week_col2:
            st.metric(
                "Total exercise",
                f"{summary['total_exercise']} min"
            )

        with week_col3:
            st.metric(
                "Average habits",
                f"{summary['avg_habits']}/5"
            )

        st.caption(
            f"Your strongest day was {summary['best_day']}."
        )

    st.divider()

    st.subheader("Recent Days")

    history = st.session_state.get("history", {})

    if not history:
        st.info(
            "Your daily history will appear here after your first "
            "full day of tracking."
        )
    else:
        recent_days = sorted(history.keys())[-7:]

        history_frame = pd.DataFrame([
            {
                "Date": day,
                "Water": history[day].get("water", 0),
                "Exercise": history[day].get("exercise", 0),
                "Habits": history[day].get("habits", 0)
            }
            for day in recent_days
        ])

        render_table(history_frame)

        weekly_chart = px.bar(
            history_frame,
            x="Date",
            y="Habits",
            range_y=[0, 5],
            title="Daily Habits Completed This Week"
        )

        weekly_chart = style_chart(weekly_chart)

        st.plotly_chart(weekly_chart, width="stretch")


# =====================================================
# PREVENTION
# =====================================================
with tab_prevention:

    image_banner(
        "prevention",
        "Prevention Awareness",
        "Around four in ten cancers are linked to preventable causes."
    )

    st.write(
        "This calculator provides a general educational awareness profile."
    )

    st.warning(
        "This is not a validated medical risk calculator and does not "
        "diagnose cancer."
    )

    st.divider()

    st.subheader("Personalize Your Content")

    demographic_choice = st.selectbox(
        "Select a content group",
        [
            "Prefer not to say",
            "Woman",
            "Man",
            "Youth or Young Adult",
            "Older Adult"
        ],
        key="demographic_choice"
    )

    st.session_state.demo_group = demographic_choice

    demographic_tips = {
        "Woman": [
            "Discuss appropriate breast and cervical screening with a "
            "healthcare professional.",
            "Ask a healthcare professional about HPV vaccination.",
            "Report unusual breast changes to a healthcare professional.",
            "Reducing alcohol intake may support lower cancer risk."
        ],
        "Man": [
            "Discuss prostate health and screening with a healthcare "
            "professional.",
            "Avoid tobacco products and ask for help quitting if needed.",
            "Use sun protection regularly.",
            "A balanced, high-fibre diet supports general health."
        ],
        "Youth or Young Adult": [
            "Avoid tobacco and vaping products.",
            "Ask a healthcare professional about HPV vaccination.",
            "Protect your skin from sunburn.",
            "Build healthy exercise and nutrition habits early."
        ],
        "Older Adult": [
            "Keep up with age-appropriate screening recommendations.",
            "Discuss family history with a healthcare professional.",
            "Stay physically active according to your ability.",
            "Ask a caregiver or family member to support appointment "
            "tracking if useful."
        ]
    }

    if demographic_choice in demographic_tips:

        st.write(f"Information for: {demographic_choice}")

        for tip in demographic_tips[demographic_choice]:
            st.write("-", tip)

    st.divider()

    st.subheader("Basic Awareness Questionnaire")

    basic_col1, basic_col2 = st.columns(2)

    with basic_col1:

        basic_age = st.slider("Age", 18, 100, 40, key="basic_age")

        basic_smoking = st.selectbox(
            "Smoking status",
            ["Never smoked", "Former smoker", "Current smoker"],
            key="basic_smoking"
        )

        basic_family_history = st.selectbox(
            "Family history",
            [
                "No close family history",
                "Second-degree relative",
                "First-degree relative"
            ],
            key="basic_family_history"
        )

        basic_screening = st.selectbox(
            "Screening status",
            ["Up to date", "Sometimes", "Not up to date or unsure"],
            key="basic_screening"
        )

    with basic_col2:

        basic_alcohol = st.selectbox(
            "Alcohol use",
            ["None or rare", "Light", "Moderate", "Heavy"],
            key="basic_alcohol"
        )

        basic_sun = st.selectbox(
            "Unprotected sun exposure",
            ["Rarely", "Sometimes", "Often"],
            key="basic_sun"
        )

        basic_diet = st.selectbox(
            "Diet quality",
            [
                "Mostly whole foods and plants",
                "Average or mixed",
                "High processed foods"
            ],
            key="basic_diet"
        )

        basic_exercise = st.selectbox(
            "Weekly exercise",
            [
                "Active, 150 or more minutes",
                "Some activity",
                "Mostly sedentary"
            ],
            key="basic_exercise"
        )

    awareness_points = 0

    if basic_age > 60:
        awareness_points += 20
    elif basic_age > 45:
        awareness_points += 12

    if basic_smoking == "Current smoker":
        awareness_points += 22
    elif basic_smoking == "Former smoker":
        awareness_points += 8

    if basic_family_history == "First-degree relative":
        awareness_points += 18
    elif basic_family_history == "Second-degree relative":
        awareness_points += 8

    if basic_alcohol == "Heavy":
        awareness_points += 14
    elif basic_alcohol == "Moderate":
        awareness_points += 6

    if basic_sun == "Often":
        awareness_points += 12
    elif basic_sun == "Sometimes":
        awareness_points += 5

    if basic_screening == "Not up to date or unsure":
        awareness_points += 10

    if basic_diet == "High processed foods":
        awareness_points += 10
    elif basic_diet == "Average or mixed":
        awareness_points += 5

    if basic_exercise == "Mostly sedentary":
        awareness_points += 10
    elif basic_exercise == "Some activity":
        awareness_points += 4

    awareness_score = min(awareness_points, 100)

    st.session_state.awareness_score = awareness_score

    st.divider()

    st.subheader(
        f"Prevention Awareness Score: {awareness_score}/100"
    )

    st.progress(awareness_score / 100)

    if awareness_score >= 55:
        st.error(
            "Several awareness areas may need attention. "
            "Discuss your questions with a healthcare professional."
        )
    elif awareness_score >= 30:
        st.warning(
            "Some awareness areas may benefit from improvement. "
            "Review them with a healthcare professional."
        )
    else:
        st.success(
            "Your answers show fewer flagged awareness areas. "
            "Continue healthy habits and follow appropriate screening advice."
        )

    st.divider()

    st.subheader("General Prevention Information")

    for tip in [
        "Avoid tobacco products.",
        "Maintain regular physical activity.",
        "Eat a balanced diet containing vegetables, fruit and whole grains.",
        "Limit alcohol consumption.",
        "Protect your skin from excessive ultraviolet exposure.",
        "Ask a healthcare professional about appropriate screening.",
        "Ask a healthcare professional about HPV and hepatitis B vaccination."
    ]:
        st.write("-", tip)

    st.divider()

    st.subheader("Advanced Awareness Questionnaire")

    with st.form("advanced_awareness_form"):

        advanced_col1, advanced_col2, advanced_col3 = st.columns(3)

        with advanced_col1:

            advanced_age = st.slider("Age", 18, 90, 35, key="advanced_age")

            advanced_smoking = st.selectbox(
                "Smoking",
                ["Never", "Former smoker", "Current smoker"],
                key="advanced_smoking"
            )

            advanced_family = st.selectbox(
                "Family history",
                ["None", "Second-degree relative", "First-degree relative"],
                key="advanced_family"
            )

        with advanced_col2:

            advanced_alcohol = st.selectbox(
                "Alcohol per week",
                ["None", "1 to 7", "8 to 14", "15 or more"],
                key="advanced_alcohol"
            )

            advanced_weight = st.selectbox(
                "Self-estimated weight category",
                ["Normal", "Overweight", "Obese"],
                key="advanced_weight"
            )

            advanced_fruit_vegetables = st.selectbox(
                "Fruit and vegetables per day",
                ["5 or more", "2 to 4", "Less than 2"],
                key="advanced_fruit_vegetables"
            )

        with advanced_col3:

            advanced_meat = st.selectbox(
                "Processed meat",
                [
                    "Rarely or never",
                    "1 to 2 times per week",
                    "3 to 5 times per week",
                    "Most days"
                ],
                key="advanced_meat"
            )

            advanced_sun = st.selectbox(
                "Sun protection",
                ["Always", "Sometimes", "Rarely"],
                key="advanced_sun"
            )

            advanced_screening = st.selectbox(
                "Screening",
                ["Up to date", "Partially up to date", "Not up to date"],
                key="advanced_screening"
            )

        advanced_submit = st.form_submit_button("Generate Advanced Profile")

    if advanced_submit:

        advanced_points = 0
        flagged_factors = []

        if advanced_age > 60:
            advanced_points += 15
            flagged_factors.append("Age above 60")
        elif advanced_age > 45:
            advanced_points += 7
            flagged_factors.append("Age above 45")

        if advanced_smoking == "Current smoker":
            advanced_points += 25
            flagged_factors.append("Current smoking")
        elif advanced_smoking == "Former smoker":
            advanced_points += 5
            flagged_factors.append("Former smoking")

        if advanced_family == "First-degree relative":
            advanced_points += 14
            flagged_factors.append("First-degree family history")
        elif advanced_family == "Second-degree relative":
            advanced_points += 7
            flagged_factors.append("Second-degree family history")

        if advanced_alcohol == "15 or more":
            advanced_points += 15
            flagged_factors.append("High alcohol intake")
        elif advanced_alcohol == "8 to 14":
            advanced_points += 8
            flagged_factors.append("Moderate alcohol intake")

        if advanced_weight == "Obese":
            advanced_points += 12
            flagged_factors.append("Obesity category")
        elif advanced_weight == "Overweight":
            advanced_points += 6
            flagged_factors.append("Overweight category")

        if advanced_fruit_vegetables == "Less than 2":
            advanced_points += 8
            flagged_factors.append("Low fruit and vegetable intake")

        if advanced_meat == "Most days":
            advanced_points += 10
            flagged_factors.append("Frequent processed meat")
        elif advanced_meat == "3 to 5 times per week":
            advanced_points += 5
            flagged_factors.append("Regular processed meat")

        if advanced_sun == "Rarely":
            advanced_points += 10
            flagged_factors.append("Low sun protection")
        elif advanced_sun == "Sometimes":
            advanced_points += 4
            flagged_factors.append("Inconsistent sun protection")

        if advanced_screening == "Not up to date":
            advanced_points += 12
            flagged_factors.append("Screening gap")

        advanced_score = min(advanced_points, 100)

        st.session_state.awareness_score = advanced_score
        st.session_state.score_history.append(advanced_score)

        award_xp(st.session_state, 15)

        persist()

        st.subheader(
            f"Advanced Awareness Profile: {advanced_score}/100"
        )

        st.progress(advanced_score / 100)

        if advanced_score >= 50:
            st.error(
                "Several factors were flagged. "
                "Discuss them with a healthcare professional."
            )
        elif advanced_score >= 25:
            st.warning(
                "Some factors were flagged. "
                "Consider discussing them with a healthcare professional."
            )
        else:
            st.success(
                "Fewer factors were flagged based on your answers. "
                "Continue healthy habits and screening discussions."
            )

        if flagged_factors:
            st.write("Factors flagged:", ", ".join(flagged_factors))
        else:
            st.write(
                "No major factors were flagged by this educational "
                "questionnaire."
            )

        st.subheader("Suggested Actions")

        for action in [
            "Discuss appropriate screening with a qualified healthcare "
            "professional.",
            "Maintain regular physical activity.",
            "Avoid tobacco products.",
            "Eat a balanced diet.",
            "Protect your skin from ultraviolet exposure."
        ]:
            st.write("-", action)

        st.warning(
            "This result is educational only. "
            "It does not predict cancer or replace medical advice."
        )


# =====================================================
# HEALTHY LIVING
# =====================================================
with tab_lifestyle:

    image_banner(
        "walking",
        "Healthy Living",
        "Small daily habits build lasting protection."
    )

    st.write("Track simple daily habits that support general health.")

    st.caption(
        "Daily values reset each morning. "
        f"Current streak: {st.session_state.get('streak', 0)} day(s)."
    )

    st.divider()

    st.subheader("Water Intake")

    framed_image(
        "water",
        "Hydration supports overall health",
        height=230
    )

    st.slider(
        "Glasses of water today",
        min_value=0,
        max_value=15,
        key="water",
        on_change=persist
    )

    water_value = st.session_state.water

    st.progress(min(water_value / 15, 1.0))

    if water_value >= 8:
        st.success("You reached the water target.")
    else:
        st.info(
            f"{8 - water_value} more glasses to reach the target."
        )

    st.divider()

    st.subheader("Exercise")

    framed_image(
        "running",
        "Aim for 150 minutes of activity each week",
        height=230
    )

    st.slider(
        "Minutes of exercise today",
        min_value=0,
        max_value=180,
        key="exercise",
        on_change=persist
    )

    exercise_value = st.session_state.exercise

    if exercise_value >= 30:
        st.success("You completed at least 30 minutes of activity.")
    else:
        st.info(
            f"{30 - exercise_value} more minutes to reach today's target."
        )

    st.divider()

    st.subheader("Sleep")

    framed_image(
        "sleep",
        "Consistent rest supports recovery and wellbeing",
        height=230
    )

    st.slider(
        "Hours of sleep last night",
        min_value=0.0,
        max_value=12.0,
        step=0.5,
        key="sleep",
        on_change=persist
    )

    sleep_value = st.session_state.sleep

    if sleep_value >= 7:
        st.success("Your sleep duration meets the general target.")
    else:
        st.warning("Consider improving your sleep routine.")

    st.divider()

    st.subheader("Daily Healthy Habits")

    st.checkbox(
        "Ate fruits and vegetables",
        key="habit_diet",
        on_change=persist
    )

    st.checkbox(
        "Avoided tobacco",
        key="habit_tobacco",
        on_change=persist
    )

    st.checkbox(
        "Completed physical activity",
        key="habit_activity",
        on_change=persist
    )

    st.checkbox(
        "Protected myself from excessive sun exposure",
        key="habit_sun",
        on_change=persist
    )

    st.checkbox(
        "Stayed up to date with health checks",
        key="habit_screening",
        on_change=persist
    )

    daily_habit_total = sum(
        [
            st.session_state.habit_diet,
            st.session_state.habit_tobacco,
            st.session_state.habit_activity,
            st.session_state.habit_sun,
            st.session_state.habit_screening
        ]
    )

    st.write(f"Daily Habit Score: {daily_habit_total}/5")

    st.progress(daily_habit_total / 5)

    if daily_habit_total == 5:
        st.success("You completed all your daily habits.")


# =====================================================
# GOALS AND PROGRESS
# =====================================================
with tab_goals:

    image_banner(
        "goals",
        "Prevention Goals and Progress",
        "Set achievable steps and track your progress over time."
    )

    goal_options = [
        "Exercise for 30 minutes",
        "Eat more vegetables",
        "Book a recommended screening appointment",
        "Reduce alcohol intake",
        "Use sun protection",
        "Learn about HPV vaccination",
        "Discuss family history with a doctor"
    ]

    st.subheader("Add Goals")

    selected_goals = st.multiselect(
        "Choose goals",
        goal_options,
        key="selected_goals"
    )

    custom_goal = st.text_input(
        "Add a custom goal",
        key="custom_goal"
    )

    if st.button("Add Selected Goals"):

        existing_goal_names = [
            item["goal"] for item in st.session_state.goals
        ]

        for selected_goal in selected_goals:
            if selected_goal not in existing_goal_names:
                st.session_state.goals.append(
                    {"goal": selected_goal, "done": False}
                )

        if custom_goal.strip():
            st.session_state.goals.append(
                {"goal": custom_goal.strip(), "done": False}
            )

        persist()

        st.success("Goals added.")
        st.rerun()

    st.divider()

    st.subheader("Active Goals")

    if not st.session_state.goals:
        st.info("You have not added any goals yet.")

    else:

        completed_goal_count = 0

        for index, goal_item in enumerate(st.session_state.goals):

            goal_status = st.checkbox(
                goal_item["goal"],
                value=goal_item["done"],
                key=f"goal_status_{index}"
            )

            if goal_status != st.session_state.goals[index]["done"]:
                st.session_state.goals[index]["done"] = goal_status
                persist()

            if goal_status:
                completed_goal_count += 1

        total_goals = len(st.session_state.goals)

        st.progress(completed_goal_count / total_goals)

        st.write(
            f"{completed_goal_count} of {total_goals} goals completed."
        )

        if completed_goal_count == total_goals:
            st.success("All goals completed.")

        if st.button("Clear All Goals"):
            st.session_state.goals = []
            persist()
            st.rerun()

    st.divider()

    st.subheader("Awareness Score History")

    if not st.session_state.score_history:
        st.info(
            "Complete the advanced questionnaire to create a score history."
        )

    else:

        history_data = pd.DataFrame(
            {
                "Attempt": range(
                    1, len(st.session_state.score_history) + 1
                ),
                "Score": st.session_state.score_history
            }
        )

        history_chart = px.line(
            history_data,
            x="Attempt",
            y="Score",
            markers=True,
            range_y=[0, 100],
            title="Awareness Score Trend"
        )

        history_chart = style_chart(history_chart)

        st.plotly_chart(history_chart, width="stretch")


# =====================================================
# WEEKLY CHALLENGE
# =====================================================
with tab_challenge:

    image_banner(
        "sunrise",
        "Weekly Prevention Challenge",
        "One small change each week builds a lasting habit."
    )

    challenge_list = {
        1: (
            "Healthy Food Challenge",
            "Add one extra serving of vegetables to your meals this week."
        ),
        2: (
            "Movement Challenge",
            "Take a ten-minute walk each day this week."
        ),
        3: (
            "Sun Protection Challenge",
            "Use shade, protective clothing or sunscreen when outdoors."
        ),
        4: (
            "Hydration Challenge",
            "Work toward your daily water target."
        ),
        5: (
            "Screening Awareness Challenge",
            "Learn which screenings may be appropriate for your age group."
        )
    }

    challenge_images = {
        1: "vegetables",
        2: "walking",
        3: "sunlight",
        4: "water",
        5: "clinic"
    }

    current_challenge_number = (
        (st.session_state.challenge_week - 1) % len(challenge_list)
    ) + 1

    challenge_title, challenge_description = challenge_list[
        current_challenge_number
    ]

    st.subheader(
        f"Week {current_challenge_number}: {challenge_title}"
    )

    framed_image(
        challenge_images[current_challenge_number],
        challenge_description,
        height=280
    )

    if not st.session_state.challenge_done:

        if st.button("Mark Challenge Complete"):
            st.session_state.challenge_done = True
            award_xp(st.session_state, 25)
            persist()
            st.success("Challenge completed. 25 XP earned.")

    else:

        st.success("This challenge is complete.")

        if st.button("Start Next Challenge"):
            st.session_state.challenge_week += 1
            st.session_state.challenge_done = False
            persist()
            st.rerun()

    st.divider()

    st.write(
        f"Challenges completed: {st.session_state.challenge_week - 1}"
    )


# =====================================================
# LEARN AND QUIZ
# =====================================================
with tab_learn:

    image_banner(
        "education",
        "Cancer Awareness and Education",
        "Reliable information supports informed health decisions."
    )

    st.write(
        "Explore general educational information about cancer prevention."
    )

    education_topics = {
        "Cancer Awareness": (
            "Cancer is a group of diseases involving abnormal cell growth. "
            "Prevention, appropriate screening and professional medical "
            "advice can support informed health decisions."
        ),
        "Tobacco": (
            "Avoiding tobacco products can reduce the risk of several cancers "
            "and other serious health conditions."
        ),
        "Healthy Diet": (
            "A balanced diet that includes vegetables, fruit, whole grains "
            "and appropriate protein sources supports general health."
        ),
        "Physical Activity": (
            "Regular physical activity supports general wellbeing and can "
            "help maintain a healthy body weight."
        ),
        "Sun Protection": (
            "Excessive ultraviolet exposure can damage the skin. Shade, "
            "protective clothing and sunscreen can reduce exposure."
        ),
        "Vaccination": (
            "Some infections are associated with cancer. Ask a healthcare "
            "professional about HPV and hepatitis B vaccination."
        ),
        "Screening": (
            "Screening recommendations depend on factors such as age, sex, "
            "family history and personal health history."
        )
    }

    for topic_name, topic_content in education_topics.items():
        with st.expander(topic_name):
            st.write(topic_content)

    st.divider()

    st.subheader("Cancer Awareness Centre")

    framed_image(
        "library",
        "Plain-language information on common cancer types",
        height=250
    )

    cancer_choice = st.selectbox(
        "Select a cancer type to learn about",
        ["Select a cancer type"] + list(CANCER_LIBRARY.keys()),
        key="cancer_choice"
    )

    if cancer_choice != "Select a cancer type":

        entry = CANCER_LIBRARY[cancer_choice]

        st.write("**What it is**")
        st.write(entry["what_it_is"])

        library_col1, library_col2 = st.columns(2)

        with library_col1:

            st.write("**Risk factors**")
            for factor in entry["risk_factors"]:
                st.write("-", factor)

            st.write("**Prevention**")
            for step in entry["prevention"]:
                st.write("-", step)

        with library_col2:

            st.write("**Possible warning signs**")
            for sign in entry["warning_signs"]:
                st.write("-", sign)

            st.write("**Screening**")
            st.write(entry["screening"])

        st.warning(entry["seek_care"])

        st.caption(SOURCES)

    st.divider()

    st.subheader("General Body Awareness Guide")

    body_area = st.selectbox(
        "Select an area",
        [
            "Select an area",
            "Skin",
            "Breast or Chest",
            "Digestive System",
            "Respiratory System",
            "General"
        ],
        key="body_area"
    )

    body_information = {
        "Skin": (
            "Be aware of new or changing moles and sores that do not heal. "
            "Contact a healthcare professional about concerning changes."
        ),
        "Breast or Chest": (
            "Be aware of unusual lumps, skin changes or other persistent "
            "changes. Discuss concerns and screening with a healthcare "
            "professional."
        ),
        "Digestive System": (
            "Persistent bowel changes, blood in stool or unexplained weight "
            "loss should be discussed with a healthcare professional."
        ),
        "Respiratory System": (
            "A persistent cough, chest pain or breathing difficulty should be "
            "discussed with a healthcare professional."
        ),
        "General": (
            "Persistent unexplained symptoms should be discussed with a "
            "qualified healthcare professional."
        )
    }

    if body_area != "Select an area":
        st.info(body_information[body_area])

    st.divider()

    st.subheader("Myth Buster")

    myth_search = st.text_input(
        "Search a claim you have heard",
        key="myth_search"
    )

    for myth in MYTHS:

        if myth_search.strip():
            if myth_search.lower() not in myth["claim"].lower():
                continue

        with st.expander(myth["claim"]):
            st.write(f"**Verdict:** {myth['verdict']}")
            st.write(myth["explanation"])
            st.caption(SOURCES)

    st.divider()

    st.subheader("Knowledge Quiz")

    st.caption(
        "Questions rotate daily. Correct answers earn XP every time."
    )

    quiz_bank = [
        {
            "question": "Which habit can reduce the risk of several cancers?",
            "options": [
                "Using tobacco",
                "Regular physical activity",
                "Using tanning beds",
                "Avoiding all screening"
            ],
            "answer": "Regular physical activity"
        },
        {
            "question": "What does the HPV vaccine help prevent?",
            "options": [
                "Some HPV-related cancers",
                "All cancers",
                "All infections",
                "Broken bones"
            ],
            "answer": "Some HPV-related cancers"
        },
        {
            "question": "What is a useful sun protection strategy?",
            "options": [
                "Tanning regularly",
                "Using shade and protective clothing",
                "Avoiding water",
                "Using sunscreen only after sunburn"
            ],
            "answer": "Using shade and protective clothing"
        },
        {
            "question": "What does a family history of cancer mean?",
            "options": [
                "Cancer is guaranteed",
                "It may be useful to discuss screening with a doctor",
                "Screening is never needed",
                "It has no relevance"
            ],
            "answer": "It may be useful to discuss screening with a doctor"
        },
        {
            "question": "What is the largest preventable cause of cancer?",
            "options": [
                "Tobacco use",
                "Drinking tea",
                "Using a mobile phone",
                "Eating breakfast"
            ],
            "answer": "Tobacco use"
        },
        {
            "question": "What is the purpose of cancer screening?",
            "options": [
                "To treat cancer",
                "To find changes before symptoms appear",
                "To replace a doctor",
                "To confirm a cure"
            ],
            "answer": "To find changes before symptoms appear"
        },
        {
            "question": "How long should a mouth ulcer be checked after?",
            "options": [
                "Two days",
                "One week",
                "Three weeks or more",
                "Never"
            ],
            "answer": "Three weeks or more"
        },
        {
            "question": "Which infection is linked to liver cancer risk?",
            "options": [
                "Hepatitis B",
                "Common cold",
                "Chickenpox",
                "Measles"
            ],
            "answer": "Hepatitis B"
        },
        {
            "question": "Does a biopsy cause cancer to spread?",
            "options": [
                "Yes, always",
                "No, it is a standard diagnostic procedure",
                "Only in adults",
                "Only in children"
            ],
            "answer": "No, it is a standard diagnostic procedure"
        },
        {
            "question": "Can cancer be passed from person to person?",
            "options": [
                "Yes, by touching",
                "Yes, by sharing food",
                "No, cancer is not contagious",
                "Yes, by talking"
            ],
            "answer": "No, cancer is not contagious"
        },
        {
            "question": "Which reduces bowel cancer risk?",
            "options": [
                "A high-fibre diet",
                "Eating processed meat daily",
                "Avoiding all vegetables",
                "Skipping screening"
            ],
            "answer": "A high-fibre diet"
        },
        {
            "question": "Is pain always present in early cancer?",
            "options": [
                "Yes, always",
                "No, many early cancers cause no pain",
                "Only at night",
                "Only after exercise"
            ],
            "answer": "No, many early cancers cause no pain"
        }
    ]

    quiz_seed = daily_index()
    quiz_start = quiz_seed % len(quiz_bank)

    quiz_questions = [
        quiz_bank[(quiz_start + offset) % len(quiz_bank)]
        for offset in range(4)
    ]

    with st.form("knowledge_quiz_form"):

        quiz_answers = []

        for question_number, question in enumerate(quiz_questions):

            st.write(
                f"Question {question_number + 1}: {question['question']}"
            )

            selected_answer = st.radio(
                "Choose one answer",
                question["options"],
                key=f"quiz_{quiz_seed}_{question_number}"
            )

            quiz_answers.append(selected_answer)

        quiz_submit = st.form_submit_button("Submit Quiz")

    if quiz_submit:

        quiz_score = 0

        for question_number, question in enumerate(quiz_questions):
            if quiz_answers[question_number] == question["answer"]:
                quiz_score += 1

        quiz_percentage = quiz_score / len(quiz_questions)

        earned_xp = quiz_score * 10

        new_level = award_xp(st.session_state, earned_xp)

        if quiz_percentage == 1:
            badge = "Perfect Score"
        elif quiz_percentage >= 0.5:
            badge = "Well Informed"
        else:
            badge = "Keep Learning"

        if badge not in st.session_state.badges:
            st.session_state.badges.append(badge)

        persist()

        st.subheader(
            f"Quiz Score: {quiz_score}/{len(quiz_questions)}"
        )

        st.progress(quiz_percentage)

        st.success(
            f"{earned_xp} XP earned. Current level: {new_level}."
        )

        st.subheader("Correct Answers")

        for question in quiz_questions:
            st.write(f"Question: {question['question']}")
            st.write(f"Correct answer: {question['answer']}")


# =====================================================
# DETECT
# =====================================================
with tab_detect:

    image_banner(
        "clinic",
        "Detect Early",
        "Recognising changes early supports timely medical assessment."
    )

    st.warning(
        "This section provides symptom education only. It cannot tell you "
        "whether you have cancer. Only a qualified healthcare professional "
        "can assess your symptoms."
    )

    detect_warning, detect_screening = st.tabs(
        ["Early Warning Guide", "Screening Navigator"]
    )

    with detect_warning:

        st.subheader("Urgent symptoms")

        st.error(
            "Seek emergency care immediately for any of the following."
        )

        for sign in EMERGENCY_SIGNS:
            st.write("-", sign)

        st.divider()

        st.subheader("Learn about a change you have noticed")

        symptom_choice = st.selectbox(
            "Select what you have noticed",
            ["Select a change"] + list(SYMPTOM_GUIDE.keys()),
            key="symptom_choice"
        )

        if symptom_choice != "Select a change":

            info = SYMPTOM_GUIDE[symptom_choice]

            st.info(info["explanation"])

            st.write("**Suggested action**")
            st.write(info["action"])

            st.write("**What to do next**")

            for step in NEXT_STEPS:
                st.write("-", step)

            st.caption(DISCLAIMER)

    with detect_screening:

        st.subheader("Screening awareness")

        st.write(
            "Answer a few questions to see which screening topics may be "
            "worth discussing with a healthcare professional."
        )

        with st.form("screening_form"):

            screen_col1, screen_col2 = st.columns(2)

            with screen_col1:

                screen_age = st.slider(
                    "Age",
                    18,
                    90,
                    35,
                    key="screen_age"
                )

                screen_sex = st.selectbox(
                    "Sex",
                    ["Prefer not to say", "Female", "Male"],
                    key="screen_sex"
                )

                screen_country = st.text_input(
                    "Country or state",
                    key="screen_country"
                )

            with screen_col2:

                screen_smoking = st.selectbox(
                    "Smoking history",
                    ["Never smoked", "Former smoker", "Current smoker"],
                    key="screen_smoking"
                )

                screen_family = st.selectbox(
                    "Family history of cancer",
                    ["No", "Yes"],
                    key="screen_family"
                )

                screen_hepatitis = st.selectbox(
                    "Chronic hepatitis B or C",
                    ["No", "Yes", "Unsure"],
                    key="screen_hepatitis"
                )

            screening_submit = st.form_submit_button(
                "Show screening awareness"
            )

        if screening_submit:

            results = screening_guidance(
                screen_age,
                screen_sex,
                screen_smoking,
                screen_family,
                screen_hepatitis
            )

            screening_table = pd.DataFrame(results)

            render_table(screening_table)

            if screen_country.strip():
                st.info(
                    "Screening programmes differ by location. Confirm what "
                    f"applies in {screen_country.strip()} with a local "
                    "healthcare professional."
                )

            st.warning(
                "This tool provides educational guidance only. It is not a "
                "medical screening recommendation."
            )


# =====================================================
# AI ASSISTANT
# =====================================================
with tab_assistant:

    image_banner(
        "data",
        "CancerGuard AI Assistant",
        "Answers grounded in a curated cancer education knowledge base."
    )

    st.info(
        "This assistant answers from a curated cancer education knowledge "
        "base. It does not diagnose, and it does not generate medical "
        "opinions."
    )

    st.subheader("Search the knowledge base")

    search_term = st.text_input(
        "Enter any word or phrase",
        key="kb_search"
    )

    if search_term.strip():

        matches = search_knowledge(search_term)

        if matches:
            st.caption(f"{len(matches)} result(s) found.")

            for match in matches:
                with st.expander(
                    f"{match['kind']}: {match['title']}"
                ):
                    st.write(match["text"])
                    st.caption(SOURCES)
        else:
            st.info(
                "No matches found. Try a different word, such as "
                "'screening', 'lump', 'tobacco' or 'HPV'."
            )

    st.divider()

    st.subheader("Example questions")

    example_questions = [
        "What are breast cancer warning signs?",
        "How can I reduce my cancer risk?",
        "What is HPV?",
        "Does sugar cause cancer?",
        "What is the difference between screening and diagnosis?",
        "I found a lump, what should I do?",
        "Explain chemotherapy in simple language.",
        "What questions should I ask my doctor?"
    ]

    for example in example_questions:
        st.write("-", example)

    st.divider()

    user_question = st.chat_input(
        "Ask a cancer education question"
    )

    if user_question:
        reply = answer_question(user_question)
        st.session_state.chat_history.append((user_question, reply))

    for asked, reply in st.session_state.chat_history:

        with st.chat_message("user"):
            st.write(asked)

        with st.chat_message("assistant"):

            if reply["type"] == "crisis":
                st.error(reply["text"])

            elif reply["type"] == "emergency":
                st.error(reply["text"])
                for item in reply.get("list", []):
                    st.write("-", item)

            elif reply["type"] == "myth":
                st.write(f"**Claim:** {reply['claim']}")
                st.write(f"**Verdict:** {reply['verdict']}")
                st.write(reply["text"])

            elif reply["type"] == "symptom":
                st.write(f"**Topic:** {reply['topic']}")
                st.write(reply["text"])
                st.write(f"**Action:** {reply['action']}")
                for item in reply.get("list", []):
                    st.write("-", item)

            else:
                if "topic" in reply:
                    st.write(f"**Topic:** {reply['topic']}")
                st.write(reply["text"])
                for item in reply.get("list", []):
                    st.write("-", item)

            st.caption(DISCLAIMER)

    if st.session_state.chat_history:
        if st.button("Clear conversation"):
            st.session_state.chat_history = []
            st.rerun()


# =====================================================
# CARE NAVIGATION AND SUPPORT
# =====================================================
with tab_care:

    image_banner(
        "support",
        "Navigate Care",
        "Understanding the pathway from awareness to survivorship."
    )

    care_journey_tab, care_find_tab, care_support_tab = st.tabs(
        ["Care Journey", "Find Care", "Support Centre"]
    )

    with care_journey_tab:

        st.subheader("From awareness to survivorship")

        framed_image(
            "path",
            "Each stage of the care pathway explained",
            height=250
        )

        st.write(
            "Understanding the pathway can reduce uncertainty after a symptom "
            "or an abnormal result."
        )

        for stage_number, (stage, description) in enumerate(
            CARE_JOURNEY, start=1
        ):
            with st.expander(f"Stage {stage_number}: {stage}"):
                st.write(description)

        st.divider()

        st.subheader("Questions to ask your doctor")

        for question in DOCTOR_QUESTIONS:
            st.write("-", question)

    with care_find_tab:

        st.subheader("Find care")

        framed_image(
            "clinic",
            "Confirm services before travelling",
            height=250
        )

        st.write(
            "This pilot directory covers selected Nigerian states. Always "
            "confirm services and opening hours before travelling."
        )

        st.warning(
            "Facilities listed here are curated, not self-registered. "
            "CancerGuard AI does not verify individual practitioners and "
            "does not provide consultations."
        )

        state_choice = st.selectbox(
            "Select a state",
            list(CARE_FACILITIES.keys()),
            key="state_choice"
        )

        facilities = CARE_FACILITIES[state_choice]

        facility_table = pd.DataFrame(facilities)

        render_table(facility_table)

        st.divider()

        st.subheader("Typical referral pathway")

        for step_number, step in enumerate(CARE_PATHWAY, start=1):
            st.write(f"{step_number}. {step}")

        st.info(
            "If you cannot reach a large hospital, start at your nearest "
            "primary health centre. They can arrange referral."
        )

        st.divider()

        st.subheader("Prepare for your appointment")

        st.write(
            "Write these down before you go. Taking notes to a "
            "consultation helps you remember what to ask."
        )

        appointment_notes = st.text_area(
            "What have you noticed, and when did it start?",
            key="appointment_notes",
            height=120
        )

        if appointment_notes.strip():

            summary_text = "CancerGuard AI - Appointment Notes\n\n"
            summary_text += f"Date prepared: {date.today().isoformat()}\n\n"
            summary_text += "What I have noticed:\n"
            summary_text += appointment_notes.strip() + "\n\n"
            summary_text += "Questions to ask:\n"

            for question in DOCTOR_QUESTIONS:
                summary_text += f"- {question}\n"

            summary_text += (
                "\nThis note was prepared using an educational app. "
                "It is not a medical assessment."
            )

            st.download_button(
                "Download notes for your appointment",
                data=summary_text,
                file_name="appointment_notes.txt",
                mime="text/plain"
            )

    with care_support_tab:

        st.subheader("Support centre")

        framed_image(
            "hands",
            "Support matters at every stage",
            height=250
        )

        support_choice = st.selectbox(
            "Select a topic",
            ["Select a topic"] + list(SUPPORT_TOPICS.keys()),
            key="support_choice"
        )

        if support_choice != "Select a topic":
            st.info(SUPPORT_TOPICS[support_choice])

        st.divider()

        st.write(
            "If distress is affecting your daily life, speak with a "
            "healthcare professional. If you are in immediate danger, "
            "contact local emergency services."
        )


# =====================================================
# MACHINE LEARNING RESEARCH
# =====================================================
with tab_research:

    image_banner(
        "laboratory",
        "Educational ML Research Lab",
        "Machine learning demonstrated on public research data."
    )

    st.info(
        """
        This section demonstrates machine learning using the public
        Wisconsin Breast Cancer Dataset. It is an educational demonstration
        and is not a medical diagnostic system.
        """
    )

    @st.cache_data
    def load_dataset():
        cancer_data = load_breast_cancer()
        dataset = pd.DataFrame(
            cancer_data.data,
            columns=cancer_data.feature_names
        )
        dataset["diagnosis"] = cancer_data.target
        return dataset

    cancer_dataset = load_dataset()

    st.write(
        f"Dataset size: {cancer_dataset.shape[0]} samples and "
        f"{cancer_dataset.shape[1] - 1} features."
    )

    render_table(
        cancer_dataset.head(),
        max_columns=8
    )

    st.divider()

    st.subheader("Configure the experiment")

    config_col1, config_col2 = st.columns(2)

    with config_col1:
        test_fraction = st.slider(
            "Test set size",
            min_value=0.1,
            max_value=0.4,
            value=0.2,
            step=0.05,
            key="ml_test_size"
        )

    with config_col2:
        tree_count = st.slider(
            "Number of trees",
            min_value=20,
            max_value=300,
            value=150,
            step=10,
            key="ml_trees"
        )

    features = cancer_dataset.drop(columns=["diagnosis"])
    target = cancer_dataset["diagnosis"]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=test_fraction,
        random_state=42,
        stratify=target
    )

    research_model = RandomForestClassifier(
        n_estimators=tree_count,
        random_state=42
    )

    research_model.fit(x_train, y_train)

    predictions = research_model.predict(x_test)

    model_accuracy = accuracy_score(y_test, predictions)

    true_positive = int(
        ((predictions == 1) & (y_test == 1)).sum()
    )
    true_negative = int(
        ((predictions == 0) & (y_test == 0)).sum()
    )
    false_positive = int(
        ((predictions == 1) & (y_test == 0)).sum()
    )
    false_negative = int(
        ((predictions == 0) & (y_test == 1)).sum()
    )

    malignant_recall = (
        true_negative / (true_negative + false_positive)
        if (true_negative + false_positive) else 0
    )

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        st.metric("Test Accuracy", f"{model_accuracy:.2%}")

    with metric_col2:
        st.metric("Malignant Recall", f"{malignant_recall:.2%}")

    with metric_col3:
        st.metric("Missed Malignant", false_positive)

    st.caption(
        "In a medical context, recall on the malignant class matters more "
        "than overall accuracy. A missed malignant case is far more "
        "serious than a false alarm."
    )

    st.subheader("Confusion Matrix")

    confusion_frame = pd.DataFrame(
        {
            "Predicted Malignant": [true_negative, false_negative],
            "Predicted Benign": [false_positive, true_positive]
        },
        index=["Actually Malignant", "Actually Benign"]
    ).reset_index().rename(columns={"index": ""})

    render_table(confusion_frame)

    st.subheader("Important Features")

    feature_importance_data = pd.DataFrame(
        {
            "Feature": features.columns,
            "Importance": research_model.feature_importances_
        }
    ).sort_values(by="Importance", ascending=False).head(8)

    importance_chart = px.bar(
        feature_importance_data,
        x="Importance",
        y="Feature",
        orientation="h",
        color="Importance",
        title="Top Features Used by the Model"
    )

    importance_chart = style_chart(importance_chart)

    st.plotly_chart(importance_chart, width="stretch")

    st.subheader("Interactive Learning Example")

    selected_feature = "mean radius"

    feature_minimum = float(features[selected_feature].min())
    feature_maximum = float(features[selected_feature].max())
    feature_average = float(features[selected_feature].mean())

    selected_value = st.slider(
        "Adjust mean radius",
        min_value=feature_minimum,
        max_value=feature_maximum,
        value=feature_average,
        step=0.1,
        key="research_feature_slider"
    )

    example_row = features.iloc[[0]].copy()
    example_row[selected_feature] = selected_value

    example_prediction = research_model.predict(example_row)
    example_probabilities = research_model.predict_proba(example_row)[0]

    if example_prediction[0] == 1:
        st.success(
            "Educational output: benign class. Estimated model probability: "
            f"{example_probabilities[1]:.1%}"
        )
    else:
        st.error(
            "Educational output: malignant class. Estimated model "
            f"probability: {example_probabilities[0]:.1%}"
        )

    st.warning(
        "This model output is not a diagnosis and must not be used "
        "for health decisions."
    )


# =====================================================
# PROFILE
# =====================================================
with tab_profile:

    image_banner(
        "community",
        "My Profile",
        "Your personal details and achievements."
    )

    st.success(f"Logged in as: {current_user}")

    st.divider()

    profile_col1, profile_col2, profile_col3, profile_col4 = st.columns(4)

    with profile_col1:
        st.metric(
            "Level",
            xp_level(st.session_state.get("xp", 0))
        )

    with profile_col2:
        st.metric(
            "Total XP",
            st.session_state.get("xp", 0)
        )

    with profile_col3:
        st.metric(
            "Streak",
            f"{st.session_state.get('streak', 0)} days"
        )

    with profile_col4:
        st.metric(
            "Check-ins",
            st.session_state.get("total_checkins", 0)
        )

    st.caption(
        personal_comparison({
            "streak": st.session_state.get("streak", 0),
            "best_streak": st.session_state.get("best_streak", 0)
        })
    )

    st.divider()

    st.subheader("Personal Information")

    st.text_input("Full Name", key="full_name")

    st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        key="profile_age"
    )

    st.selectbox(
        "Main Health Goal",
        [
            "Improve my diet",
            "Exercise more",
            "Improve my sleep",
            "Drink more water",
            "Learn about cancer prevention",
            "Stay up to date with screening"
        ],
        key="health_goal"
    )

    st.text_input(
        "Email for future digests",
        key="email",
        help="Stored locally. Daily digests are planned for v2."
    )

    if st.button("Save Profile"):
        persist()
        st.success("Profile saved to your account.")

    st.divider()

    st.subheader("Mood History")

    mood_log = st.session_state.get("mood_log", {})

    if not mood_log:
        st.info(
            "Your mood history appears after your first daily check-in."
        )
    else:

        recent_moods = sorted(mood_log.keys())[-7:]

        mood_frame = pd.DataFrame([
            {"Date": day, "Mood": mood_log[day]}
            for day in recent_moods
        ])

        render_table(mood_frame)

    st.divider()

    st.subheader("Your Badges")

    if st.session_state.badges:
        for badge in st.session_state.badges:
            st.write("-", badge)
    else:
        st.write("No badges yet. Complete the quiz in the Learn tab.")

    st.divider()

    st.subheader("Unlocked Topics")

    claimed = st.session_state.get("rewards_claimed", [])

    if claimed:
        st.write(f"You have unlocked {len(claimed)} topic(s).")
    else:
        st.write("No topics unlocked yet. Check the Dashboard.")

    st.divider()

    st.subheader("Your Data")

    st.caption(
        "Your progress is stored in a JSON file on the server running "
        "this app. It is not encrypted and is not shared. "
        "Do not enter sensitive medical information."
    )

    export_payload = current_record()

    st.download_button(
        "Download my data",
        data=json.dumps(export_payload, indent=4),
        file_name=f"cancerguard_{current_user}.json",
        mime="application/json"
    )


# =====================================================
# FOOTER
# =====================================================
st.divider()

st.caption(
    "Educational awareness application. Not a medical product."
)

st.markdown(
    """
    <div class="app-footer">
        Built by <strong>Toluwalope</strong><br>
        CancerGuard AI
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="app-footer">
        Built by <strong>Toluwalope</strong><br>
        CancerGuard AI
    </div>
    """,
    unsafe_allow_html=True
)