import streamlit as st
import pandas as pd
import numpy as np
import random
import json
import os
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import plotly.express as px

# =====================
# PAGE SETUP
# =====================
st.set_page_config(
    page_title="CancerGuard AI",
    page_icon="🩺",
    layout="wide"
)

# =====================
# USER PERSISTENCE (File-Based)
# =====================
USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {"demo": "password"}

def save_users(users_dict):
    with open(USER_FILE, "w") as f:
        json.dump(users_dict, f)

# =====================
# CUSTOM STYLING
# =====================
st.markdown("""
<style>
.main { background-color: #E91E63; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; }
[data-testid="stSidebar"] { background-color: #E91E63; }
h1 { font-weight: 700; }
h2 { font-weight: 650; }
h3 { font-weight: 600; }
div[data-testid="stMetric"] {
    background-color:#E91E63;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.stButton > button { border-radius: 10px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# =====================
# SESSION STATE INITIALIZATION
# =====================
defaults = {
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
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =====================
# LOGIN / REGISTER GATE
# =====================
if not st.session_state.logged_in:
    st.title("🔐 Customer Access Portal")
    st.caption("Early Awareness. Better Health. Brighter Future")

    login_tab, reg_tab = st.tabs(["Login", "Sign Up / Register"])

    with login_tab:
        with st.form("login_form"):
            user_in = st.text_input("Username")
            pass_in = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login")
            if login_btn:
                if user_in in st.session_state.users and st.session_state.users[user_in] == pass_in:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user_in
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Wrong username or password. Try: demo / password")

    with reg_tab:
        with st.form("register_form"):
            new_user = st.text_input("Choose a username")
            new_pass = st.text_input("Choose a password", type="password")
            reg_btn = st.form_submit_button("Create Account")
            if reg_btn:
                if new_user in st.session_state.users:
                    st.error("Username already taken.")
                elif not new_user or not new_pass:
                    st.error("Please fill both fields.")
                else:
                    st.session_state.users[new_user] = new_pass
                    save_users(st.session_state.users)
                    st.success(f"Account '{new_user}' created! Now log in.")

    st.info(" **Healthy Choices. Stronger Future | password `password`")
    st.stop()

# =====================
# SIDEBAR
# =====================
with st.sidebar:
    st.title("🩺 CancerGuard AI")
    st.write(f" **{st.session_state.current_user}**")
    st.divider()
    st.caption("Your health awareness companion")
    st.divider()
    st.write("### Quick Stats")
    st.metric("Awareness", f"{st.session_state.awareness_score}/100")
    st.metric("Water", f"{st.session_state.water}/8")
    st.metric("Exercise", f"{st.session_state.exercise} min")
    st.divider()
    st.caption(" Built by [Toluwalope]")
    st.divider()
    if st.button(" Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

# =====================
# GLOBAL MEDICAL DISCLAIMER
# =====================
st.warning("""
**CancerGuard AI** uses health data and machine learning to help people understand cancer risk factors, discover prevention strategies, explore cancer research, and recognize when professional screening may be important.
""")

st.title("🩺 CancerGuard AI")
st.subheader("Turning Cancer Data Into Prevention, Awareness & Early Action")
st.image("https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800&q=80",
         caption="Medical Research & Education — Source: Unsplash (Free)")
st.caption("CancerGuard AI was created to make cancer-related information easier to understand and explore.")

# =====================
# NAVIGATION TABS
# =====================
tab_home, tab_prevention, tab_lifestyle, tab_goals, tab_challenge, tab_learn, tab_research, tab_profile = st.tabs([
    " Dashboard",
    " Prevention",
    " Healthy Living",
    " Goals",
    " Weekly Challenge",
    " Learn",
    " ML Research",
    " Profile"
])

# ==========================================
# TAB 1: DASHBOARD
# ==========================================
with tab_home:
    st.title(" Your Health Dashboard")
    st.subheader(f"Welcome back, {st.session_state.current_user} 👋")
    st.write("Track your healthy habits and improve your health awareness.")
    st.divider()

    completed_habits = sum([
        st.session_state.habit_diet,
        st.session_state.habit_tobacco,
        st.session_state.habit_activity,
        st.session_state.habit_sun,
        st.session_state.habit_screening
    ])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        score_color = " if st.session_state.awareness_score < 30 else " if st.session_state.awareness_score < 55 else "🔴"
        st.metric(f"{score_color} Awareness", f"{st.session_state.awareness_score}/100")

    with col2:
        water_emoji = " if st.session_state.water < 8 else "
        st.metric(f"{water_emoji} Water", f"{st.session_state.water} glasses")

    with col3:
        exercise_emoji = " if st.session_state.exercise < 30 else "
        st.metric(f"{exercise_emoji} Exercise", f"{st.session_state.exercise} min")

    with col4:
        sleep_emoji = " if st.session_state.sleep < 7 else "
        st.metric(f"{sleep_emoji} Sleep", f"{st.session_state.sleep} hrs")

    st.divider()
    st.subheader(" Today's Health Tip")
    st.success(
        "Avoid tobacco, stay physically active, maintain a healthy diet, "
        "protect your skin from excessive UV exposure, and keep up with "
        "appropriate health screenings."
    )

    st.divider()
    st.subheader("💬 Daily Motivation")

    quotes = [
        "Small steps every day lead to big changes. ",
        "Your health is an investment, not an expense. ",
        "Prevention today is protection tomorrow. 🛡️",
        "Knowledge about your body is power. ",
        "Every healthy choice matters, no matter how small. ",
        "You can't pour from an empty cup — take care of yourself. ☕",
        "Progress, not perfection. "
    ]

    if st.session_state.daily_quote is None:
        st.session_state.daily_quote = random.choice(quotes)

    st.info(f"*{st.session_state.daily_quote}*")

    if st.button(" New Quote"):
        st.session_state.daily_quote = random.choice(quotes)
        st.rerun()

    st.subheader(" Quick Actions")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info(" Check your prevention awareness")
    with c2:
        st.info(" Track today's healthy habits")
    with c3:
        st.info(" Learn about cancer prevention")

    st.divider()
    st.subheader(" Your Healthy Living Progress")
    progress_data = pd.DataFrame({
        "Habit": ["Water", "Exercise", "Sleep", "Daily Habits"],
        "Progress": [
            min(st.session_state.water / 8 * 100, 100),
            min(st.session_state.exercise / 30 * 100, 100),
            min(st.session_state.sleep / 7 * 100, 100),
            completed_habits / 5 * 100
        ]
    })
    fig_dash = px.bar(progress_data, x="Habit", y="Progress", range_y=[0, 100],
                       title="Today's Health Progress", color="Habit")
    st.plotly_chart(fig_dash, use_container_width=True)

    st.caption("Note: Awareness Score updates after you complete the calculator in the Prevention tab.")

# ==========================================
# TAB 2: PREVENTION
# ==========================================
with tab_prevention:
    st.header(" Prevention Awareness")
    st.divider()
    st.subheader(" Personalize Your Content")
    demo_choice = st.selectbox(
        "I'm filling this out primarily as:",
        ["Prefer not to say", "Woman", "Man", "Youth / Young Adult (under 25)", "Older Adult (65+)"],
        key="demo_select"
    )
    st.session_state.demo_group = demo_choice

    demo_tips = {
        "Woman": [
            "🎗️ Discuss mammogram scheduling with your doctor based on age and family history.",
            " HPV vaccination and regular cervical screening significantly reduce cervical cancer risk.",
            " Breast self-awareness: know what's normal for you and report changes promptly.",
            " Alcohol has a strong link to breast cancer risk — even small reductions help."
        ],
        "Man": [
            " Talk to your doctor about prostate health discussions appropriate for your age.",
            " Smoking cessation dramatically reduces lung and other cancer risks.",
            " Men have higher rates of skin cancer diagnosis — daily sun protection matters.",
            " Reducing processed/red meat and increasing fiber supports colorectal health."
        ],
        "Youth / Young Adult (under 25)": [
            " HPV vaccination is most effective when given younger — ask if not yet done.",
            " Never starting tobacco/vaping is the single best prevention step.",
            " Sunburns in youth significantly raise lifetime skin cancer risk — protect early.",
            " Building lifelong activity and healthy eating habits now pays off for decades."
        ],
        "Older Adult (65+)": [
            " Stay current with age-appropriate screenings (colorectal, breast, prostate, skin checks).",
            " Involve family or caregivers in tracking appointments and health goals.",
            " Nutrient-dense foods support overall health alongside cancer prevention.",
            " Discuss any new or unusual symptoms with your doctor promptly."
        ]
    }

    if demo_choice in demo_tips:
        st.write(f"**Tailored tips for: {demo_choice}**")
        for tip in demo_tips[demo_choice]:
            st.write("•", tip)

    st.divider()
    st.write("This educational calculator uses general lifestyle inputs. **It does not diagnose anything.**")

    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("Age", 18, 100, 40, key="basic_age")
        smoking = st.selectbox("Smoking Status", ["Never smoked", "Former smoker", "Current smoker"], key="basic_smoke")
        family_hist = st.selectbox("Family History", ["No", "Yes — 1st degree relative", "Yes — 2nd degree"], key="basic_family")
        screening = st.selectbox("Regular Screenings", ["Up to date", "Sometimes", "Not up to date / Unsure"], key="basic_screen")

    with col2:
        alcohol = st.selectbox("Alcohol Use", ["None / Rare", "Light", "Moderate", "Heavy"], key="basic_alc")
        sun = st.selectbox("Regular Unprotected Sun Exposure", ["Rarely", "Sometimes", "Often"], key="basic_sun")
        diet = st.selectbox("Diet Quality (self-rated)", ["Mostly whole foods / plants", "Average / Mixed", "High processed foods"], key="basic_diet")
        exercise_input = st.selectbox("Weekly Exercise", ["Active (150+ min)", "Moderate (some)", "Mostly sedentary"], key="basic_exercise")

    score = 0
    if age > 60: score += 20
    elif age > 45: score += 12
    if smoking == "Current smoker": score += 22
    elif smoking == "Former smoker": score += 8
    if family_hist.startswith("Yes — 1st"): score += 18
    elif family_hist.startswith("Yes — 2nd"): score += 8
    if alcohol == "Heavy": score += 14
    elif alcohol == "Moderate": score += 6
    if sun == "Often": score += 12
    elif sun == "Sometimes": score += 5
    if screening == "Not up to date / Unsure": score += 10
    if diet == "High processed foods": score += 10
    elif diet == "Average / Mixed": score += 5
    if exercise_input == "Mostly sedentary": score += 10
    elif exercise_input == "Moderate (some)": score += 4

    awareness_score = min(score, 100)
    st.session_state.awareness_score = awareness_score

    st.divider()
    st.subheader(f" Prevention Awareness Score: {awareness_score} / 100")
    st.progress(awareness_score / 100.0)

    if awareness_score >= 55:
        st.error(" Higher awareness profile based on inputs. Please discuss risk reduction and screening schedules with a healthcare provider.")
    elif awareness_score >= 30:
        st.warning(" Moderate awareness. Review habits with a doctor or qualified health professional.")
    else:
        st.success(" Lower awareness profile based on inputs. Maintain healthy practices and stay up to date with screenings.")
        st.snow()

    st.divider()
    st.subheader("Evidence-Based Protection Tips")
    tips = [
        " Avoid all tobacco products.",
        " Eat a diet rich in vegetables, fruits, whole grains; limit processed meats.",
        " Maintain regular physical activity.",
        " Protect skin from UV radiation (sunscreen, shade, clothing).",
        " Limit alcohol; avoid heavy drinking.",
        " Follow age-appropriate cancer screening guidelines (consult your doctor).",
        " Consider vaccinations (e.g., HPV, Hepatitis B) where medically appropriate."
    ]
    for t in tips:
        st.write("•", t)
    st.caption("References for display: WHO, CDC, NCI. Used for education only.")

    st.divider()
    st.subheader(" Advanced Awareness Calculator")
    st.info("Answer these questions for an expanded educational profile. Not clinical.")

    with st.form("advanced_risk"):
        st.write("**Lifestyle & Health Factors**")
        c1, c2, c3 = st.columns(3)
        with c1:
            a_age = st.slider("Age", 18, 90, 35, key="adv_age")
            a_smoke = st.selectbox("Smoking", ["Never", "Former (quit >10yr)", "Former (<10yr)", "Current"], key="adv_smoke")
            a_family = st.selectbox("Family History", ["None", "2nd degree", "1st degree"], key="adv_family")
        with c2:
            a_alc = st.selectbox("Alcohol / Week", ["None", "1-7", "8-14", "15+"], key="adv_alc")
            a_weight = st.selectbox("Weight (self-est)", ["Normal", "Overweight", "Obese"], key="adv_weight")
            a_veg = st.selectbox("Veg/Fruit Daily", ["5+", "2-4", "<2"], key="adv_veg")
        with c3:
            a_meat = st.selectbox("Processed Meat", ["Rare/None", "1-2x/wk", "3-5x/wk", "Most days"], key="adv_meat")
            a_sun = st.selectbox("Sun Protection", ["Always", "Sometimes", "Rarely / Burn"], key="adv_sun")
            a_screen = st.selectbox("Screenings", ["Up to date", "Partial", "Not up to date"], key="adv_screen")

        btn = st.form_submit_button("Generate Awareness Profile")

    if btn:
        pts = 0
        flags = []
        if a_age > 60: pts += 15; flags.append("Age 60+")
        elif a_age > 45: pts += 7; flags.append("Age 45+")
        if a_smoke == "Current": pts += 25; flags.append("Smoking")
        elif "<10yr" in a_smoke: pts += 10; flags.append("Recent former smoker")
        if "15+" in a_alc: pts += 15; flags.append("High alcohol")
        elif "8-14" in a_alc: pts += 8; flags.append("Moderate alcohol")
        if "Obese" in a_weight: pts += 12; flags.append("Obesity")
        elif "Overweight" in a_weight: pts += 6; flags.append("Overweight")
        if "<2" in a_veg: pts += 8; flags.append("Low veg")
        if "Most days" in a_meat: pts += 10; flags.append("High processed meat")
        elif "3-5x/wk" in a_meat: pts += 5
        if "Rarely" in a_sun: pts += 10; flags.append("Low sun protection")
        elif "Sometimes" in a_sun: pts += 4
        if "Not up to date" in a_screen: pts += 12; flags.append("Screening gap")
        if "1st degree" in a_family: pts += 14; flags.append("1st degree family")
        elif "2nd degree" in a_family: pts += 7

        score2 = min(pts, 100)
        st.session_state.score_history.append(score2)

        if score2 >= 50:
            level = "Higher Awareness Profile"
        elif score2 >= 25:
            level = "Moderate Awareness"
        else:
            level = "Lower Awareness Profile"

        st.subheader(f"Profile: {level}")
        st.progress(score2 / 100.0)
        st.write(f"Score: **{score2}/100**")
        st.write("Factors noted:", ", ".join(flags) if flags else "None major flagged")

        st.subheader("Evidence-Based Actions")
        adv_tips = []
        if a_smoke != "Never": adv_tips.append((" Tobacco", "Quitting at any age reduces risk. Seek support."))
        if "15+" in a_alc or "8-14" in a_alc: adv_tips.append(("🍷 Alcohol", "Lower intake reduces multiple cancer risks."))
        if "Obese" in a_weight or "Overweight" in a_weight: adv_tips.append(("⚖️ Weight", "Healthy weight lowers risk for 13 cancer types."))
        if "<2" in a_veg or "Most days" in a_meat or "3-5x/wk" in a_meat: adv_tips.append(("🥗 Diet", "More plants/whole grains; less processed meat."))
        if "Rarely" in a_sun or "Sometimes" in a_sun: adv_tips.append(("☀️ Sun", "SPF 30+, shade, protective clothing."))
        if "Not up to date" in a_screen: adv_tips.append(("🩺 Screening", "Consult your GP for age-appropriate tests."))
        if "1st degree" in a_family or "2nd degree" in a_family: adv_tips.append(("👨‍👩‍👧 Family", "Discuss earlier/additional screening with doctor."))
        adv_tips.append((" Vaccines", "HPV / Hep B vaccines where appropriate."))
        adv_tips.append((" Source", "Cancer Council Australia, WHO, NCI — for education only."))

        for title, body in adv_tips:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.write(body)

        st.warning(" **Not clinical.** This is an educational portfolio tool. Always see a healthcare provider for real risk assessment and screening.")

# ==========================================
# TAB 3: HEALTHY LIVING
# ==========================================
with tab_lifestyle:
    st.title(" Healthy Living")
    st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800&q=80",
              caption="Small daily habits create lasting change")
    st.write("Track simple daily habits that support a healthier lifestyle.")
    st.divider()

    st.subheader("💧 Water Intake")
    water = st.slider("How many glasses of water have you taken today?", 0, 15, key="water")
    st.progress(min(water / 15, 1.0))
    if water >= 8:
        st.success("Great! You've reached your daily water goal.")
        st.toast(" Water goal reached!", icon="🎉")
    else:
        st.info(f"You need about {8 - water} more glasses to reach 8.")

    st.divider()
    st.subheader(" Exercise")
    exercise = st.slider("Minutes of exercise today", 0, 180, key="exercise")
    if exercise >= 30:
        st.success("Excellent! You've completed 30+ minutes of activity.")
    else:
        st.info(f"{30 - exercise} more minutes to reach today's goal.")

    st.divider()
    st.subheader(" Sleep")
    sleep = st.slider("Hours of sleep last night", 0.0, 12.0, step=0.5, key="sleep")
    if sleep >= 7:
        st.success("Good sleep duration!")
    else:
        st.warning("Try to improve your sleep routine.")

    st.divider()
    st.subheader(" Today's Healthy Habits")
    st.checkbox(" Ate fruits and vegetables", key="habit_diet")
    st.checkbox(" Avoided tobacco", key="habit_tobacco")
    st.checkbox(" Completed physical activity", key="habit_activity")
    st.checkbox(" Protected myself from excessive sun exposure", key="habit_sun")
    st.checkbox(" Stayed up to date with health checks", key="habit_screening")

    completed = sum([
        st.session_state.habit_diet,
        st.session_state.habit_tobacco,
        st.session_state.habit_activity,
        st.session_state.habit_sun,
        st.session_state.habit_screening
    ])
    st.write(f"### Daily Habit Score: {completed}/5")
    st.progress(completed / 5)
    if completed == 5:
        st.success(" Excellent! You completed all your habits today.")
        st.balloons()

# ==========================================
# TAB 4: GOALS & PROGRESS
# ==========================================
with tab_goals:
    st.header(" Your Prevention Goals & Progress")
    st.caption("Set simple, achievable goals based on your awareness profile.")

    preset_goals = [
        "Walk or exercise 30 min, 5x this week",
        "Add 2 extra servings of vegetables daily",
        "Book/attend a recommended screening",
        "Reduce alcohol by 1-2 drinks this week",
        "Apply sunscreen daily",
        "Research HPV or Hepatitis B vaccination",
        "Have a 10-min conversation with my doctor about family history"
    ]

    st.subheader("Choose Goals to Track")
    selected = st.multiselect("Select goals you want to work on:", preset_goals, key="goal_select")
    custom_goal = st.text_input("Or add your own custom goal:", key="custom_goal_input")
    if st.button(" Add Goals"):
        for g in selected:
            if g not in [x["goal"] for x in st.session_state.goals]:
                st.session_state.goals.append({"goal": g, "done": False})
        if custom_goal:
            st.session_state.goals.append({"goal": custom_goal, "done": False})
        st.success("Goals added!")
        st.rerun()

    st.divider()
    st.subheader("Your Active Goals")
    if not st.session_state.goals:
        st.write("No goals yet. Add some above to get started!")
    else:
        completed_goals = 0
        for i, g in enumerate(st.session_state.goals):
            checked = st.checkbox(g["goal"], value=g["done"], key=f"goal_{i}")
            st.session_state.goals[i]["done"] = checked
            if checked:
                completed_goals += 1

        total = len(st.session_state.goals)
        pct = completed_goals / total if total > 0 else 0
        st.progress(pct)
        st.write(f"**{completed_goals} / {total} goals completed** ({pct:.0%})")

        if pct == 1 and total > 0:
            st.balloons()
            st.success(" All goals completed! Great work on your prevention journey.")

        if st.button(" Clear All Goals"):
            st.session_state.goals = []
            st.rerun()

    st.divider()
    st.subheader(" Your Awareness Score Trend")
    if len(st.session_state.score_history) == 0:
        st.write("No score history yet. Complete the Advanced Calculator in the Prevention tab to start tracking.")
    else:
        trend_df = pd.DataFrame({
            "Attempt": list(range(1, len(st.session_state.score_history) + 1)),
            "Score": st.session_state.score_history
        })
        fig_trend = px.line(trend_df, x="Attempt", y="Score", markers=True,
                             title="Your Awareness Score Over Time")
        fig_trend.update_yaxes(range=[0, 100])
        st.plotly_chart(fig_trend, use_container_width=True)

# ==========================================
# TAB 5: WEEKLY CHALLENGE
# ==========================================
with tab_challenge:
    st.title(" Weekly Prevention Challenge")
    st.image("https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&q=80",
              caption="Small challenges, big impact")

    st.info("Complete this week's challenge to build lasting prevention habits!")

    challenges = {
        1: (" Veggie Week", "Add one extra serving of vegetables to every meal this week."),
        2: (" Move More", "Take a 10-minute walk every day this week."),
        3: (" Sun Smart", "Apply sunscreen every day this week, even indoors near windows."),
        4: (" Hydration Hero", "Drink at least 8 glasses of water daily this week."),
        5: (" Screening Check", "Research what screenings are recommended for your age group."),
    }

    current_week = ((st.session_state.challenge_week - 1) % len(challenges)) + 1
    title, description = challenges[current_week]

    st.subheader(f"Week {current_week}: {title}")
    st.write(description)

    if not st.session_state.challenge_done:
        if st.button(" Mark Challenge Complete"):
            st.session_state.challenge_done = True
            st.balloons()
            st.success("🎉 Amazing! Challenge completed!")
    else:
        st.success(" This week's challenge is complete!")
        if st.button(" Start Next Week's Challenge"):
            st.session_state.challenge_week += 1
            st.session_state.challenge_done = False
            st.rerun()

    st.divider()
    st.caption(f"Challenges completed: {st.session_state.challenge_week - 1}")

# ==========================================
# TAB 6: LEARN & QUIZ
# ==========================================
with tab_learn:
    st.title(" Cancer Awareness & Education")
    st.image("https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?w=800&q=80",
              caption="Knowledge is prevention")
    st.write("Explore simple educational information about cancer prevention and healthy living.")
    st.divider()

    topics = {
        " Cancer Awareness": "Cancer refers to a group of diseases involving abnormal cell growth. Learning about prevention, risk factors and appropriate screening can help people make informed health decisions.",
        " Tobacco": "Avoiding tobacco is an important way to reduce the risk of several cancers and other serious health problems.",
        " Healthy Diet": "A balanced diet that includes vegetables, fruits, whole grains and appropriate protein sources supports overall health.",
        " Physical Activity": "Regular physical activity supports overall wellbeing and can help maintain a healthy body weight.",
        " Sun Protection": "Excessive ultraviolet exposure can damage the skin. Protective clothing, shade and appropriate sunscreen can help reduce UV exposure.",
        " Vaccination": "Some infections are associated with cancer. Vaccines such as HPV and hepatitis B vaccines can help prevent certain infections where medically appropriate.",
        " Screening": "Cancer screening recommendations depend on factors such as age, sex, family history and personal health history. Speak with a qualified healthcare professional about appropriate screening."
    }

    for title, content in topics.items():
        with st.expander(title):
            st.write(content)

    st.divider()
    st.subheader(" General Body Awareness Guide")
    st.caption("Educational overview only — always consult a doctor for any concerns.")

    body_area = st.selectbox(
        "Select an area to learn general awareness info:",
        ["Select an area...", "Skin", "Breast/Chest", "Digestive System", "Respiratory System", "General/Whole Body"]
    )

    body_info = {
        "Skin": " **What to watch for:** New moles, changes in existing moles (size, color, border), sores that don't heal. **Action:** See a dermatologist for any changes.",
        "Breast/Chest": " **What to watch for:** Lumps, changes in size/shape, skin dimpling, unusual discharge. **Action:** Regular self-awareness + age-appropriate screening.",
        "Digestive System": " **What to watch for:** Persistent changes in bowel habits, unexplained weight loss, blood in stool. **Action:** Discuss with your doctor, especially if symptoms persist >2 weeks.",
        "Respiratory System": " **What to watch for:** Persistent cough, shortness of breath, chest pain. **Action:** See a doctor, especially if you have a smoking history.",
        "General/Whole Body": " **What to watch for:** Unexplained fatigue, unexplained weight loss, persistent pain, fever. **Action:** Any persistent unusual symptom warrants a doctor visit."
    }

    if body_area != "Select an area...":
        st.warning(body_info[body_area])
        st.caption(" This is general educational information, not a diagnostic tool. Many symptoms have simple, non-cancer explanations.")

    st.divider()
    st.subheader(" Test Your Knowledge")
    st.caption("Short quiz based on public health prevention guidelines. Earn badges as you learn!")

    quiz_questions = [
        {
            "q": "What percentage of cancers are estimated to be preventable through lifestyle changes?",
            "options": ["About 10%", "About 40%", "About 90%", "None are preventable"],
            "answer": 1
        },
        {
            "q": "Which of these is a proven way to reduce cancer risk?",
            "options": ["Tanning beds", "Regular physical activity", "Skipping screenings", "Heavy alcohol use"],
            "answer": 1
        },
        {
            "q": "The HPV vaccine primarily helps prevent which cancer?",
            "options": ["Lung cancer", "Cervical cancer", "Skin cancer", "Bone cancer"],
            "answer": 1
        },
        {
            "q": "What is the best way to protect skin from UV-related cancer risk?",
            "options": ["Only wear sunscreen at the beach", "Avoid all sunlight forever",
                        "Use SPF 30+, seek shade, wear protective clothing", "Tanning in moderation is fine"],
            "answer": 2
        },
        {
            "q": "Family history of cancer means:",
            "options": ["You will definitely develop cancer",
                        "You may benefit from earlier or additional screening",
                        "Nothing, it has no impact",
                        "You should stop all screenings"],
            "answer": 1
        }
    ]

    with st.form("quiz_form"):
        user_answers = []
        for idx, q in enumerate(quiz_questions):
            st.write(f"**Q{idx+1}. {q['q']}**")
            ans = st.radio("Select one:", q["options"], key=f"quiz_{idx}", index=None)
            user_answers.append(ans)
        quiz_submit = st.form_submit_button("Submit Quiz")

    if quiz_submit:
        quiz_score = 0
        for idx, q in enumerate(quiz_questions):
            correct_text = q["options"][q["answer"]]
            if user_answers[idx] == correct_text:
                quiz_score += 1

        total_q = len(quiz_questions)
        pct_score = quiz_score / total_q

        st.subheader(f"You scored {quiz_score} / {total_q}")
        st.progress(pct_score)

        if pct_score == 1.0:
            badge = " Gold — Cancer Prevention Expert"
        elif pct_score >= 0.6:
            badge = " Silver — Well Informed"
        else:
            badge = " Bronze — Keep Learning"

        if badge not in st.session_state.badges:
            st.session_state.badges.append(badge)

        st.success(f"Badge earned: {badge}")

        with st.expander("See Correct Answers & Explanations"):
            explanations = [
                "Around 30-50% of cancers are preventable through lifestyle and known risk factor reduction (WHO estimate).",
                "Regular physical activity is linked to lower risk of several cancer types.",
                "The HPV vaccine significantly reduces cervical cancer risk and some other HPV-related cancers.",
                "Combining SPF, shade, and protective clothing offers the best evidence-based UV protection.",
                "Family history increases risk for some cancers, so earlier/more frequent screening may be recommended."
            ]
            for idx, q in enumerate(quiz_questions):
                correct_text = q["options"][q["answer"]]
                st.write(f"**Q{idx+1}:** Correct answer: *{correct_text}*")
                st.caption(explanations[idx])

    st.divider()
    st.subheader(" Your Badges")
    if st.session_state.badges:
        for b in st.session_state.badges:
            st.write("•", b)
    else:
        st.write("No badges yet — complete the quiz above!")

# ==========================================
# TAB 7: ML RESEARCH
# ==========================================
with tab_research:
    st.header(" Educational ML Research Lab")
    st.image("https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&q=80",
              caption="Data-driven research and education")
    st.info("""
    This section demonstrates how machine learning can be applied to an anonymized breast cancer dataset.

    ⚠️ This is an educational and CancerGuardAI demonstration. It is **NOT** a medical diagnostic system.
    """)

    @st.cache_data
    def get_data():
        data = load_breast_cancer()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df["diagnosis"] = data.target
        return df, data

    df, cancer_data = get_data()

    st.write(f"**Dataset:** {df.shape[0]} samples | {df.shape[1] - 1} features")
    st.write("Sample of anonymized measurements:")
    st.dataframe(df.head())

    X = df.drop("diagnosis", axis=1)
    y = df["diagnosis"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=150, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Model Accuracy (Test Set)", f"{acc:.2%}")
    with col_b:
        st.write("Target Meaning:")
        st.write("**0** = Malignant")
        st.write("**1** = Benign")

    st.subheader("Top Features Driving This Educational Model")
    importance_df = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=False).head(8)

    fig = px.bar(importance_df, x="Importance", y="Feature", orientation="h",
                 color="Importance", color_continuous_scale="Tealgrn",
                 title="What measurements influence this learning model?")
    fig.update_layout(yaxis_categoryorder="total ascending")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Interactive Learning: Adjust a Feature")
    st.write("Move the slider to see how one feature changes the model's output. **This is hypothetical.**")

    feature_choice = "mean radius"
    min_val = float(X[feature_choice].min())
    max_val = float(X[feature_choice].max())
    mean_val = float(X[feature_choice].mean())

    user_value = st.slider(feature_choice.title(), min_value=min_val, max_value=max_val,
                            value=mean_val, step=0.1, key="ml_slider")

    sample_row = X.iloc[[0]].copy()
    sample_row[feature_choice] = user_value

    prediction = model.predict(sample_row)
    probabilities = model.predict_proba(sample_row)[0]

    st.write("**Model Output for This Hypothetical Input:**")
    if prediction[0] == 1:
        st.success(f"Predicted Class: **Benign** | Confidence: Benign {probabilities[1]:.1%} | Malignant {probabilities[0]:.1%}")
    else:
        st.error(f"Predicted Class: **Malignant** | Confidence: Malignant {probabilities[0]:.1%} | Benign {probabilities[1]:.1%}")

    st.caption("Reminder: Real diagnosis requires biopsy, imaging, and expert pathologist review. This demo is for code/portfolio demonstration only.")

# ==========================================
# TAB 8: PROFILE
# ==========================================
with tab_profile:
    st.title(" My Profile")
    st.success(f"Logged in as: **{st.session_state.current_user}**")
    st.divider()

    st.subheader("Personal Information")
    name = st.text_input("Full Name", key="full_name")
    age_profile = st.number_input("Age", min_value=18, max_value=100, key="profile_age")
    goal = st.selectbox(
        "Main Health Goal",
        ["Improve my diet", "Exercise more", "Improve my sleep",
         "Drink more water", "Learn about cancer prevention", "Stay up to date with screening"],
        key="health_goal"
    )

    if st.button(" Save Profile"):
        st.success("Profile updated successfully!")

# =====================
# FOOTER
# =====================
st.divider()
st.caption("Educational Awareness • Not a medical product • Data source: sklearn.datasets.load_breast_cancer")
st.markdown(
    "<div style='text-align: center; padding: 10px; color: gray; font-size: 14px;'>"
    "Built by <strong>[Toluwalope]</strong> | CancerGuard AI © 2026"
    "</div>",
    unsafe_allow_html=True
)