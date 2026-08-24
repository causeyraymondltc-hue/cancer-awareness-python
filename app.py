import streamlit as st
import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import plotly.express as px

# =====================
# PAGE SETUP
# =====================
st.set_page_config(
    page_title="Cancer Awareness & Research Toolkit",
    page_icon="🩺",
    layout="centered"
)
# =====================
# CUSTOMER LOGIN / REGISTER (Demo Only)
# =====================
if 'users' not in st.session_state:
    # Pre-loaded demo account + empty storage for new sign-ups
    st.session_state.users = {"demo": "password"}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

# If not logged in, show only the login/register screen and stop everything else
if not st.session_state.logged_in:
    st.title("🔐 Customer Access Portal")
    st.caption("Demo authentication for portfolio — not a secure production system")
    
    login_tab, reg_tab = st.tabs(["Login", "Sign Up / Register"])
    
    with login_tab:
        st.write("**Existing Customer Login**")
        with st.form("login_form"):
            user_in = st.text_input("Username")
            pass_in = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login")
            
            if login_btn:
                if user_in in st.session_state.users and st.session_state.users[user_in] == pass_in:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user_in
                    st.success("Login successful! Loading app...")
                    st.rerun()
                else:
                    st.error("Wrong username or password. Try: demo / password")
    
    with reg_tab:
        st.write("**New Customer Sign Up**")
        with st.form("register_form"):
            new_user = st.text_input("Choose a username")
            new_pass = st.text_input("Choose a password", type="password")
            reg_btn = st.form_submit_button("Create Account")
            
            if reg_btn:
                if new_user in st.session_state.users:
                    st.error("Username already taken.")
                elif not new_user or not new_pass:
                    st.error("Please fill both fields.")
                elif len(new_pass) < 4:
                    st.warning("For demo only: password must be at least 4 characters.")
                else:
                    st.session_state.users[new_user] = new_pass
                    st.success(f"Account '{new_user}' created! Now log in with the Login tab.")
    
    st.info("💡 **Demo credentials:** username `demo` | password `password`")
    st.stop()  # This stops the cancer app from loading until login succeeds

# =====================
# LOGGED IN STATE: Show app + Logout option in sidebar
# =====================
# Show welcome message and logout button in sidebar
with st.sidebar:
    st.write(f"👤 Welcome, **{st.session_state.current_user}**")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
    st.divider()
    st.caption("Customer Portal Active")
# =====================
# GLOBAL MEDICAL DISCLAIMER (Must be visible everywhere)
# =====================
st.warning("""
 **CancerGuard AI, health data, and machine learning to help people understand cancer risk factors, discover prevention strategies, explore cancer research, and recognize when professional screening may be important..
""")

st.title("🩺 Cancer Awareness & Educational Guard AI")
st.subheader(" Turning Cancer Data Into Prevention, Awareness & Early Action") 
st.image("https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800&q=80", 
         caption="Medical Research & Education — Source: Unsplash (Free)")
st.caption("CancerGuard AI was created to make cancer-related information easier to understand and explore.")

# =====================
# NAVIGATION TABS
# =====================
tab_prevention, tab_research = st.tabs([
    "🛡️ Protection & Prevention Awareness",
    "🔬 Educational ML Research Demo"
])

# ==========================================
# TAB 1: PROTECTION & PREVENTION
# ==========================================
with tab_prevention:
    st.header("Know Your Risk Factors")
    st.write("This educational calculator uses general lifestyle inputs. **It does not diagnose anything.**")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 18, 100, 40)
        smoking = st.selectbox("Smoking Status", [
            "Never smoked", "Former smoker", "Current smoker"
        ])
        family_hist = st.selectbox("Family History", [
            "No", "Yes — 1st degree relative", "Yes — 2nd degree"
        ])
        screening = st.selectbox("Regular Screenings", [
            "Up to date", "Sometimes", "Not up to date / Unsure"
        ])

    with col2:
        alcohol = st.selectbox("Alcohol Use", [
            "None / Rare", "Light", "Moderate", "Heavy"
        ])
        sun = st.selectbox("Regular Unprotected Sun Exposure", [
            "Rarely", "Sometimes", "Often"
        ])
        diet = st.selectbox("Diet Quality (self-rated)", [
            "Mostly whole foods / plants", "Average / Mixed", "High processed foods"
        ])
        exercise = st.selectbox("Weekly Exercise", [
            "Active (150+ min)", "Moderate (some)", "Mostly sedentary"
        ])

    # Simple educational scoring logic (arbitrary weights for demo)
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

    if exercise == "Mostly sedentary": score += 10
    elif exercise == "Moderate (some)": score += 4

    awareness_score = min(score, 100)

    st.divider()
    st.subheader(f"Awareness Score: {awareness_score} / 100")
    st.progress(awareness_score / 100.0)

    if awareness_score >= 55:
        st.error("🔴 Higher awareness profile based on inputs. Please discuss risk reduction and screening schedules with a healthcare provider.")
    elif awareness_score >= 30:
        st.warning("🟡 Moderate awareness. Review habits with a doctor or qualified health professional.")
    else:
        st.success("🟢 Lower awareness profile based on inputs. Maintain healthy practices and stay up to date with screenings.")

    st.divider()
    st.subheader("Evidence-Based Protection Tips")
    tips = [
        "🚭 Avoid all tobacco products.",
        "🥗 Eat a diet rich in vegetables, fruits, whole grains; limit processed meats.",
        "🏃 Maintain regular physical activity.",
        "☀️ Protect skin from UV radiation (sunscreen, shade, clothing).",
        "🍷 Limit alcohol; avoid heavy drinking.",
        "🩺 Follow age-appropriate cancer screening guidelines (consult your doctor).",
        "💉 Consider vaccinations (e.g., HPV, Hepatitis B) where medically appropriate."
    ]
    for t in tips:
        st.write("•", t)

    st.caption("References for display: WHO, CDC, NCI. Used for education only.")

# ==========================================
# TAB 2: EDUCATIONAL ML DEMO
# ==========================================

    # ==========================================
    # NEW ADDED FEATURE: Multi-Factor Risk Questionnaire
    # ==========================================
    st.divider()
    st.subheader("🔍 Advanced Awareness Calculator")
    st.info("Answer these questions for an expanded educational profile. Not clinical.")

    with st.form("advanced_risk"):
        st.write("**Lifestyle & Health Factors**")
        c1, c2, c3 = st.columns(3)
        with c1:
            a_age = st.slider("Age", 18, 90, 35)
            a_smoke = st.selectbox("Smoking", ["Never", "Former (quit >10yr)", "Former (<10yr)", "Current"])
            a_family = st.selectbox("Family History", ["None", "2nd degree", "1st degree"])
        with c2:
            a_alc = st.selectbox("Alcohol / Week", ["None", "1-7", "8-14", "15+"])
            a_weight = st.selectbox("Weight (self-est)", ["Normal", "Overweight", "Obese"])
            a_veg = st.selectbox("Veg/Fruit Daily", ["5+", "2-4", "<2"])
        with c3:
            a_meat = st.selectbox("Processed Meat", ["Rare/None", "1-2x/wk", "3-5x/wk", "Most days"])
            a_sun = st.selectbox("Sun Protection", ["Always", "Sometimes", "Rarely / Burn"])
            a_screen = st.selectbox("Screenings", ["Up to date", "Partial", "Not up to date"])
        
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

        score = min(pts, 100)
        
        if score >= 50:
            level, color = "Higher Awareness Profile", "red"
        elif score >= 25:
            level, color = "Moderate Awareness", "orange"
        else:
            level, color = "Lower Awareness Profile", "green"
        
        st.subheader(f"Profile: {level}")
        st.progress(score / 100.0)
        st.write(f"Score: **{score}/100**")
        st.write("Factors noted:", ", ".join(flags) if flags else "None major flagged")
        
        st.subheader("Evidence-Based Actions")
        tips = []
        if a_smoke != "Never": tips.append(("🚭 Tobacco", "Quitting at any age reduces risk. Seek support."))
        if "15+" in a_alc or "8-14" in a_alc: tips.append(("🍷 Alcohol", "Lower intake reduces multiple cancer risks."))
        if "Obese" in a_weight or "Overweight" in a_weight: tips.append(("⚖️ Weight", "Healthy weight lowers risk for 13 cancer types."))
        if "<2" in a_veg or "Most days" in a_meat or "3-5x/wk" in a_meat: tips.append(("🥗 Diet", "More plants/whole grains; less processed meat."))
        if "Rarely" in a_sun or "Sometimes" in a_sun: tips.append(("☀️ Sun", "SPF 30+, shade, protective clothing."))
        if "Not up to date" in a_screen: tips.append(("🩺 Screening", "Consult your GP for age-appropriate tests."))
        if "1st degree" in a_family or "2nd degree" in a_family: tips.append(("👨‍👩‍👧 Family", "Discuss earlier/additional screening with doctor."))
        tips.append(("💉 Vaccines", "HPV / Hep B vaccines where appropriate."))
        tips.append(("📚 Source", "Cancer Council Australia, WHO, NCI — for education only."))
        
        for title, body in tips:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.write(body)
        
        st.warning("⚠️ **Not clinical.** This is an educational portfolio tool. Always see a healthcare provider for real risk assessment and screening.")
with tab_research:
    st.header("Breast Cancer Dataset Explorer")
    st.info("""
    This loads the public **Wisconsin Breast Cancer Dataset** (built into `scikit-learn`). 
    The model predicts based on anonymized cell measurements. **This is NOT a real diagnostic tool.**
    """)

    @st.cache_data
    def get_data():
        data = load_breast_cancer()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df["diagnosis"] = data.target  # 0 = Malignant, 1 = Benign
        return df, data

    df, cancer_data = get_data()

    st.write(f"**Dataset:** {df.shape[0]} samples | {df.shape[1] - 1} features")
    st.write("Sample of anonymized measurements:")
    st.dataframe(df.head())

    # Train / Test split
    X = df.drop("diagnosis", axis=1)
    y = df["diagnosis"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

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

    # Feature importance chart
    st.subheader("Top Features Driving This Educational Model")
    importance_df = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=False).head(8)

    fig = px.bar(
        importance_df,
        x="Importance",
        y="Feature",
        orientation="h",
        color="Importance",
        color_continuous_scale="Tealgrn",
        title="What measurements influence this learning model?"
    )
    fig.update_layout(yaxis_categoryorder="total ascending")
    st.plotly_chart(fig, use_container_width=True)

    # Interactive educational prediction
    st.subheader("Interactive Learning: Adjust a Feature")
    st.write("Move the slider to see how one feature changes the model's output. **This is hypothetical.**")

    feature_choice = "mean radius"
    min_val = float(X[feature_choice].min())
    max_val = float(X[feature_choice].max())
    mean_val = float(X[feature_choice].mean())

    user_value = st.slider(
        feature_choice.replace(" ", " ").title(),
        min_value=min_val,
        max_value=max_val,
        value=mean_val,
        step=0.1
    )

    # Make a single-row copy of first row and change just this feature
    sample_row = X.iloc[[0]].copy()
    sample_row[feature_choice] = user_value

    prediction = model.predict(sample_row)
    probabilities = model.predict_proba(sample_row)[0]

    st.write("**Model Output for This Hypothetical Input:**")
    if prediction[0] == 1:
        st.success(
            f"Predicted Class: **Benign** | "
            f"Confidence: Benign {probabilities[1]:.1%} | Malignant {probabilities[0]:.1%}"
        )
    else:
        st.error(
            f"Predicted Class: **Malignant** | "
            f"Confidence: Malignant {probabilities[0]:.1%} | Benign {probabilities[1]:.1%}"
        )

    st.caption("Reminder: Real diagnosis requires biopsy, imaging, and expert pathologist review. This demo is for code/portfolio demonstration only.")

# Footer
st.divider()
st.caption("Portfolio Project • Not a medical product • Data source: sklearn.datasets.load_breast_cancer")