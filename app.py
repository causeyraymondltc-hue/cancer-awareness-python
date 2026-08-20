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
# GLOBAL MEDICAL DISCLAIMER (Must be visible everywhere)
# =====================
st.warning("""
⚠️ **MEDICAL DISCLAIMER:** This is an **educational portfolio project only**. 
It is **NOT** a clinical diagnostic device, medical tool, or substitute for professional healthcare advice. 
Always consult qualified medical professionals for diagnosis, screening, and treatment decisions. 
Never rely on this app for real health decisions.
""")

st.title("🩺 Cancer Awareness & Educational Toolkit")
st.subheader("Built with Python • Streamlit • Scikit-Learn • Public Health Data")
st.caption("Portfolio Project — Not for clinical use")

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