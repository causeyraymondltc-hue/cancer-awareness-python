import streamlit as st
import pandas as pd
import random
import json
import os
import hashlib

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import plotly.express as px


# =====================================================
# PAGE SETUP
# =====================================================
st.set_page_config(
    page_title="CancerGuard AI",
    page_icon="🔐",
    layout="wide"
)


# =====================================================
# STYLING
# =====================================================
st.markdown(
    """
    <style>
    .main {
        background-color: #E91E63;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background-color: #E91E63;
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    h1, h2, h3 {
        font-weight: 700;
    }

    div[data-testid="stMetric"] {
        background-color: #E91E63;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    .app-footer {
        text-align: center;
        padding: 20px;
        color: #666666;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# USER ACCOUNT STORAGE
# =====================================================
USER_FILE = "users.json"


def hash_password(password):
    """Convert a password into a secure hash."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_users():
    """Load users from users.json."""
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r", encoding="utf-8") as file:
                users = json.load(file)

                # Supports older accounts stored as plain text
                converted_users = {}
                for username, password in users.items():
                    if len(password) == 64:
                        converted_users[username] = password
                    else:
                        converted_users[username] = hash_password(password)

                return converted_users

        except Exception:
            return {"demo": hash_password("password")}

    return {"demo": hash_password("password")}


def save_users(users):
    """Save users to users.json."""
    with open(USER_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)


# =====================================================
# SESSION STATE
# =====================================================
default_values = {
    "users": load_users(),
    "logged_in": False,
    "current_user": None,

    "goals": [],
    "score_history": [],
    "badges": [],
    "demo_group": "Prefer not to say",

    "water": 0,
    "exercise": 0,
    "sleep": 7.0,

    "habit_diet": False,
    "habit_tobacco": False,
    "habit_activity": False,
    "habit_sun": False,
    "habit_screening": False,

    "awareness_score": 0,

    "full_name": "",
    "profile_age": 30,
    "health_goal": "Improve my diet",

    "daily_quote": None,
    "challenge_week": 1,
    "challenge_done": False
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# LOGIN AND REGISTRATION
# =====================================================
if not st.session_state.logged_in:

    st.title("🔐 Customer Access Portal")
    st.caption("Early Awareness. Better Health. Brighter Future")

    login_tab, register_tab = st.tabs(
        ["Login", "Sign Up / Register"]
    )

    with login_tab:
        with st.form("login_form"):
            username_input = st.text_input("Username")
            password_input = st.text_input(
                "Password",
                type="password"
            )

            login_button = st.form_submit_button("Login")

            if login_button:
                username_input = username_input.strip()

                password_hash = hash_password(password_input)

                if (
                    username_input in st.session_state.users
                    and st.session_state.users[username_input] == password_hash
                ):
                    st.session_state.logged_in = True
                    st.session_state.current_user = username_input
                    st.success("Login successful.")
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")

    with register_tab:
        with st.form("register_form"):
            new_username = st.text_input("Choose a username")
            new_password = st.text_input(
                "Choose a password",
                type="password"
            )
            confirm_password = st.text_input(
                "Confirm password",
                type="password"
            )

            register_button = st.form_submit_button(
                "Create Account"
            )

            if register_button:
                new_username = new_username.strip()

                if not new_username or not new_password:
                    st.error("Please complete all fields.")

                elif len(new_username) < 3:
                    st.error("Username must contain at least 3 characters.")

                elif len(new_password) < 6:
                    st.error("Password must contain at least 6 characters.")

                elif new_password != confirm_password:
                    st.error("Passwords do not match.")

                elif new_username in st.session_state.users:
                    st.error("Username already exists.")

                else:
                    st.session_state.users[new_username] = hash_password(
                        new_password
                    )

                    save_users(st.session_state.users)

                    st.success(
                        "Account created successfully. Please use the Login tab."
                    )

    st.info(
        "Demo account: username `demo`, password `password`."
    )

    st.warning(
        "This is a portfolio authentication demo. Do not use it for real medical or customer data."
    )

    st.stop()


# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:

    st.title("CancerGuard AI")

    st.write(
        f"Logged in as: {st.session_state.current_user}"
    )

    st.divider()

    st.caption("Your health awareness companion")

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

    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()


# =====================================================
# HEADER
# =====================================================
st.warning(
    """
    CancerGuard AI is an educational portfolio application.
    It does not diagnose cancer, predict personal cancer risk,
    or replace professional medical advice, screening, or treatment.
    """
)

st.title("CancerGuard AI")
st.subheader(
    "Turning Cancer Data Into Prevention, Awareness and Early Action"
)

st.image(
    "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=1000&q=80",
    caption="Medical research and health education"
)

st.caption(
    "CancerGuard AI makes cancer-related information easier to understand and explore."
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
    tab_research,
    tab_profile
) = st.tabs(
    [
        "Dashboard",
        "Prevention",
        "Healthy Living",
        "Goals",
        "Weekly Challenge",
        "Learn",
        "ML Research",
        "Profile"
    ]
)


# =====================================================
# DASHBOARD
# =====================================================
with tab_home:

    st.title("Your Health Dashboard")

    st.subheader(
        f"Welcome back, {st.session_state.current_user}"
    )

    st.write(
        "Track your healthy habits and improve your health awareness."
    )

    st.divider()

    completed_habits = sum(
        [
            st.session_state.habit_diet,
            st.session_state.habit_tobacco,
            st.session_state.habit_activity,
            st.session_state.habit_sun,
            st.session_state.habit_screening
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Awareness Score",
            f"{st.session_state.awareness_score}/100"
        )

    with col2:
        st.metric(
            "Water Intake",
            f"{st.session_state.water} glasses"
        )

    with col3:
        st.metric(
            "Exercise",
            f"{st.session_state.exercise} minutes"
        )

    with col4:
        st.metric(
            "Sleep",
            f"{st.session_state.sleep} hours"
        )

    st.divider()

    st.subheader("Today's Health Tip")

    st.success(
        "Avoid tobacco, stay physically active, maintain a balanced diet, "
        "protect your skin from excessive ultraviolet exposure, and follow "
        "appropriate screening guidance from a healthcare professional."
    )

    st.divider()

    st.subheader("Daily Motivation")

    quotes = [
        "Small steps every day lead to big changes.",
        "Your health is an investment, not an expense.",
        "Prevention today can support a healthier future.",
        "Knowledge helps people make informed decisions.",
        "Every healthy choice matters.",
        "Progress is more important than perfection.",
        "A healthy lifestyle is built one habit at a time."
    ]

    if st.session_state.daily_quote is None:
        st.session_state.daily_quote = random.choice(quotes)

    st.info(st.session_state.daily_quote)

    if st.button("New Quote"):
        st.session_state.daily_quote = random.choice(quotes)
        st.rerun()

    st.divider()

    st.subheader("Healthy Living Progress")

    progress_data = pd.DataFrame(
        {
            "Habit": [
                "Water",
                "Exercise",
                "Sleep",
                "Daily Habits"
            ],
            "Progress": [
                min(st.session_state.water / 8 * 100, 100),
                min(st.session_state.exercise / 30 * 100, 100),
                min(st.session_state.sleep / 7 * 100, 100),
                completed_habits / 5 * 100
            ]
        }
    )

    progress_chart = px.bar(
        progress_data,
        x="Habit",
        y="Progress",
        range_y=[0, 100],
        color="Habit",
        title="Today's Healthy Living Progress"
    )

    st.plotly_chart(
        progress_chart,
        use_container_width=True
    )

    st.caption(
        "Your awareness score updates when you complete the Prevention section."
    )


# =====================================================
# PREVENTION
# =====================================================
with tab_prevention:

    st.title("Prevention Awareness")

    st.write(
        "This calculator provides a general educational awareness profile."
    )

    st.warning(
        "This is not a validated medical risk calculator and does not diagnose cancer."
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
            "Discuss appropriate breast and cervical screening with a healthcare professional.",
            "Ask a healthcare professional about HPV vaccination.",
            "Report unusual breast changes to a healthcare professional.",
            "Reducing alcohol intake may support lower cancer risk."
        ],
        "Man": [
            "Discuss prostate health and screening with a healthcare professional.",
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
            "Ask a caregiver or family member to support appointment tracking if useful."
        ]
    }

    if demographic_choice in demographic_tips:
        st.write(
            f"Information for: {demographic_choice}"
        )

        for tip in demographic_tips[demographic_choice]:
            st.write("-", tip)

    st.divider()

    st.subheader("Basic Awareness Questionnaire")

    col1, col2 = st.columns(2)

    with col1:
        basic_age = st.slider(
            "Age",
            18,
            100,
            40,
            key="basic_age"
        )

        basic_smoking = st.selectbox(
            "Smoking status",
            [
                "Never smoked",
                "Former smoker",
                "Current smoker"
            ],
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
            [
                "Up to date",
                "Sometimes",
                "Not up to date or unsure"
            ],
            key="basic_screening"
        )

    with col2:
        basic_alcohol = st.selectbox(
            "Alcohol use",
            [
                "None or rare",
                "Light",
                "Moderate",
                "Heavy"
            ],
            key="basic_alcohol"
        )

        basic_sun = st.selectbox(
            "Unprotected sun exposure",
            [
                "Rarely",
                "Sometimes",
                "Often"
            ],
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
            "Several awareness areas may need attention. Discuss your questions with a healthcare professional."
        )
    elif awareness_score >= 30:
        st.warning(
            "Some awareness areas may benefit from improvement. Review them with a healthcare professional."
        )
    else:
        st.success(
            "Your answers show fewer flagged awareness areas. Continue healthy habits and follow appropriate screening advice."
        )

    st.divider()

    st.subheader("General Prevention Information")

    prevention_tips = [
        "Avoid tobacco products.",
        "Maintain regular physical activity.",
        "Eat a balanced diet containing vegetables, fruit and whole grains.",
        "Limit alcohol consumption.",
        "Protect your skin from excessive ultraviolet exposure.",
        "Ask a healthcare professional about appropriate screening.",
        "Ask a healthcare professional about HPV and hepatitis B vaccination."
    ]

    for prevention_tip in prevention_tips:
        st.write("-", prevention_tip)

    st.divider()

    st.subheader("Advanced Awareness Questionnaire")

    with st.form("advanced_awareness_form"):

        advanced_col1, advanced_col2, advanced_col3 = st.columns(3)

        with advanced_col1:
            advanced_age = st.slider(
                "Age",
                18,
                90,
                35,
                key="advanced_age"
            )

            advanced_smoking = st.selectbox(
                "Smoking",
                [
                    "Never",
                    "Former smoker",
                    "Current smoker"
                ],
                key="advanced_smoking"
            )

            advanced_family = st.selectbox(
                "Family history",
                [
                    "None",
                    "Second-degree relative",
                    "First-degree relative"
                ],
                key="advanced_family"
            )

        with advanced_col2:
            advanced_alcohol = st.selectbox(
                "Alcohol per week",
                [
                    "None",
                    "1 to 7",
                    "8 to 14",
                    "15 or more"
                ],
                key="advanced_alcohol"
            )

            advanced_weight = st.selectbox(
                "Self-estimated weight category",
                [
                    "Normal",
                    "Overweight",
                    "Obese"
                ],
                key="advanced_weight"
            )

            advanced_fruit_vegetables = st.selectbox(
                "Fruit and vegetables per day",
                [
                    "5 or more",
                    "2 to 4",
                    "Less than 2"
                ],
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
                [
                    "Always",
                    "Sometimes",
                    "Rarely"
                ],
                key="advanced_sun"
            )

            advanced_screening = st.selectbox(
                "Screening",
                [
                    "Up to date",
                    "Partially up to date",
                    "Not up to date"
                ],
                key="advanced_screening"
            )

        advanced_submit = st.form_submit_button(
            "Generate Advanced Profile"
        )

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

        st.subheader(
            f"Advanced Awareness Profile: {advanced_score}/100"
        )

        st.progress(advanced_score / 100)

        if advanced_score >= 50:
            st.error(
                "Several factors were flagged. Discuss them with a healthcare professional."
            )
        elif advanced_score >= 25:
            st.warning(
                "Some factors were flagged. Consider discussing them with a healthcare professional."
            )
        else:
            st.success(
                "Fewer factors were flagged based on your answers. Continue healthy habits and screening discussions."
            )

        if flagged_factors:
            st.write(
                "Factors flagged:",
                ", ".join(flagged_factors)
            )
        else:
            st.write(
                "No major factors were flagged by this educational questionnaire."
            )

        st.subheader("Suggested Actions")

        suggested_actions = [
            "Discuss appropriate screening with a qualified healthcare professional.",
            "Maintain regular physical activity.",
            "Avoid tobacco products.",
            "Eat a balanced diet.",
            "Protect your skin from ultraviolet exposure."
        ]

        for action in suggested_actions:
            st.write("-", action)

        st.warning(
            "This result is educational only. It does not predict cancer or replace medical advice."
        )


# =====================================================
# HEALTHY LIVING
# =====================================================
with tab_lifestyle:

    st.title("Healthy Living")

    st.image(
        "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=1000&q=80",
        caption="Small daily habits support a healthy lifestyle"
    )

    st.write(
        "Track simple daily habits that support general health."
    )

    st.divider()

    st.subheader("Water Intake")

    st.session_state.water = st.slider(
        "Glasses of water today",
        0,
        15,
        key="water"
    )

    st.progress(
        min(st.session_state.water / 15, 1.0)
    )

    if st.session_state.water >= 8:
        st.success("You reached the water target.")
    else:
        st.info(
            f"{8 - st.session_state.water} more glasses to reach the target."
        )

    st.divider()

    st.subheader("Exercise")

    st.session_state.exercise = st.slider(
        "Minutes of exercise today",
        0,
        180,
        key="exercise"
    )

    if st.session_state.exercise >= 30:
        st.success("You completed at least 30 minutes of activity.")
    else:
        st.info(
            f"{30 - st.session_state.exercise} more minutes to reach today's target."
        )

    st.divider()

    st.subheader("Sleep")

    st.session_state.sleep = st.slider(
        "Hours of sleep last night",
        0.0,
        12.0,
        step=0.5,
        key="sleep"
    )

    if st.session_state.sleep >= 7:
        st.success("Your sleep duration meets the general target.")
    else:
        st.warning("Consider improving your sleep routine.")

    st.divider()

    st.subheader("Daily Healthy Habits")

    st.checkbox(
        "Ate fruits and vegetables",
        key="habit_diet"
    )

    st.checkbox(
        "Avoided tobacco",
        key="habit_tobacco"
    )

    st.checkbox(
        "Completed physical activity",
        key="habit_activity"
    )

    st.checkbox(
        "Protected myself from excessive sun exposure",
        key="habit_sun"
    )

    st.checkbox(
        "Stayed up to date with health checks",
        key="habit_screening"
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

    st.write(
        f"Daily Habit Score: {daily_habit_total}/5"
    )

    st.progress(daily_habit_total / 5)

    if daily_habit_total == 5:
        st.success("You completed all your daily habits.")


# =====================================================
# GOALS AND PROGRESS
# =====================================================
with tab_goals:

    st.title("Prevention Goals and Progress")

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

        for selected_goal in selected_goals:
            existing_goal_names = [
                item["goal"]
                for item in st.session_state.goals
            ]

            if selected_goal not in existing_goal_names:
                st.session_state.goals.append(
                    {
                        "goal": selected_goal,
                        "done": False
                    }
                )

        if custom_goal.strip():
            st.session_state.goals.append(
                {
                    "goal": custom_goal.strip(),
                    "done": False
                }
            )

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

            st.session_state.goals[index]["done"] = goal_status

            if goal_status:
                completed_goal_count += 1

        total_goals = len(st.session_state.goals)
        goal_progress = completed_goal_count / total_goals

        st.progress(goal_progress)

        st.write(
            f"{completed_goal_count} of {total_goals} goals completed."
        )

        if completed_goal_count == total_goals:
            st.success("All goals completed.")

        if st.button("Clear All Goals"):
            st.session_state.goals = []
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
                    1,
                    len(st.session_state.score_history) + 1
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

        st.plotly_chart(
            history_chart,
            use_container_width=True
        )


# =====================================================
# WEEKLY CHALLENGE
# =====================================================
with tab_challenge:

    st.title("Weekly Prevention Challenge")

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

    current_challenge_number = (
        (st.session_state.challenge_week - 1)
        % len(challenge_list)
    ) + 1

    challenge_title, challenge_description = challenge_list[
        current_challenge_number
    ]

    st.subheader(
        f"Week {current_challenge_number}: {challenge_title}"
    )

    st.write(challenge_description)

    if not st.session_state.challenge_done:

        if st.button("Mark Challenge Complete"):
            st.session_state.challenge_done = True
            st.success("Challenge completed.")

    else:

        st.success("This challenge is complete.")

        if st.button("Start Next Challenge"):
            st.session_state.challenge_week += 1
            st.session_state.challenge_done = False
            st.rerun()

    st.divider()

    st.write(
        f"Challenges completed: {st.session_state.challenge_week - 1}"
    )


# =====================================================
# LEARN AND QUIZ
# =====================================================
with tab_learn:

    st.title("Cancer Awareness and Education")

    st.image(
        "https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?w=1000&q=80",
        caption="Health education supports informed decisions"
    )

    st.write(
        "Explore general educational information about cancer prevention."
    )

    education_topics = {
        "Cancer Awareness": (
            "Cancer is a group of diseases involving abnormal cell growth. "
            "Prevention, appropriate screening and professional medical advice "
            "can support informed health decisions."
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
            "Regular physical activity supports general wellbeing and can help "
            "maintain a healthy body weight."
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
            "Be aware of unusual lumps, skin changes or other persistent changes. "
            "Discuss concerns and screening with a healthcare professional."
        ),
        "Digestive System": (
            "Persistent bowel changes, blood in stool or unexplained weight loss "
            "should be discussed with a healthcare professional."
        ),
        "Respiratory System": (
            "A persistent cough, chest pain or breathing difficulty should be "
            "discussed with a healthcare professional."
        ),
        "General": (
            "Persistent unexplained symptoms should be discussed with a qualified "
            "healthcare professional."
        )
    }

    if body_area != "Select an area":
        st.info(body_information[body_area])

    st.divider()

    st.subheader("Knowledge Quiz")

    quiz_questions = [
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
            "question": "What does family history mean?",
            "options": [
                "Cancer is guaranteed",
                "It may be useful to discuss screening with a doctor",
                "Screening is never needed",
                "It has no relevance"
            ],
            "answer": "It may be useful to discuss screening with a doctor"
        }
    ]

    with st.form("knowledge_quiz_form"):

        quiz_answers = []

        for question_number, question in enumerate(quiz_questions):

            st.write(
                f"Question {question_number + 1}: "
                f"{question['question']}"
            )

            selected_answer = st.radio(
                "Choose one answer",
                question["options"],
                key=f"quiz_question_{question_number}"
            )

            quiz_answers.append(selected_answer)

        quiz_submit = st.form_submit_button(
            "Submit Quiz"
        )

    if quiz_submit:

        quiz_score = 0

        for question_number, question in enumerate(quiz_questions):

            if quiz_answers[question_number] == question["answer"]:
                quiz_score += 1

        quiz_percentage = quiz_score / len(quiz_questions)

        st.subheader(
            f"Quiz Score: {quiz_score}/{len(quiz_questions)}"
        )

        st.progress(quiz_percentage)

        if quiz_percentage == 1:
            badge = "Gold: Prevention Expert"
        elif quiz_percentage >= 0.5:
            badge = "Silver: Well Informed"
        else:
            badge = "Bronze: Keep Learning"

        if badge not in st.session_state.badges:
            st.session_state.badges.append(badge)

        st.success(
            f"Achievement earned: {badge}"
        )


# =====================================================
# MACHINE LEARNING RESEARCH
# =====================================================
with tab_research:

    st.title("Educational ML Research Lab")

    st.image(
        "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=1000&q=80",
        caption="Data-driven health education"
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

    st.dataframe(
        cancer_dataset.head()
    )

    features = cancer_dataset.drop(
        columns=["diagnosis"]
    )

    target = cancer_dataset["diagnosis"]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42,
        stratify=target
    )

    research_model = RandomForestClassifier(
        n_estimators=150,
        random_state=42
    )

    research_model.fit(
        x_train,
        y_train
    )

    predictions = research_model.predict(x_test)

    model_accuracy = accuracy_score(
        y_test,
        predictions
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Test Accuracy",
            f"{model_accuracy:.2%}"
        )

    with col2:
        st.write("Dataset target meaning:")
        st.write("0 represents malignant.")
        st.write("1 represents benign.")

    st.subheader("Important Features")

    feature_importance_data = pd.DataFrame(
        {
            "Feature": features.columns,
            "Importance": research_model.feature_importances_
        }
    ).sort_values(
        by="Importance",
        ascending=False
    ).head(8)

    importance_chart = px.bar(
        feature_importance_data,
        x="Importance",
        y="Feature",
        orientation="h",
        color="Importance",
        title="Top Features Used by the Model"
    )

    st.plotly_chart(
        importance_chart,
        use_container_width=True
    )

    st.subheader("Interactive Learning Example")

    selected_feature = "mean radius"

    feature_minimum = float(
        features[selected_feature].min()
    )

    feature_maximum = float(
        features[selected_feature].max()
    )

    feature_average = float(
        features[selected_feature].mean()
    )

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

    example_prediction = research_model.predict(
        example_row
    )

    example_probabilities = research_model.predict_proba(
        example_row
    )[0]

    if example_prediction[0] == 1:
        st.success(
            f"Educational output: benign class. "
            f"Estimated model probability: "
            f"{example_probabilities[1]:.1%}"
        )
    else:
        st.error(
            f"Educational output: malignant class. "
            f"Estimated model probability: "
            f"{example_probabilities[0]:.1%}"
        )

    st.warning(
        "This model output is not a diagnosis and must not be used for health decisions."
    )


# =====================================================
# PROFILE
# =====================================================
with tab_profile:

    st.title("My Profile")

    st.success(
        f"Logged in as: {st.session_state.current_user}"
    )

    st.divider()

    st.subheader("Personal Information")

    st.text_input(
        "Full Name",
        key="full_name"
    )

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

    if st.button("Save Profile"):
        st.success("Profile saved for this session.")


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