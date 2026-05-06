import streamlit as st
import pandas as pd
import os
import datetime

# ---------------- 1. PAGE CONFIG ----------------
st.set_page_config(
    page_title="FLUX Engine | Cognitive Resource Manager",
    page_icon="⚡",
    layout="wide"
)

# ---------------- 2. STYLING ----------------
# ---------------- 2. NEON DARK THEME STYLING ----------------
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #0E1117;
        color: #00D4FF;
    }

    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #00D4FF;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #1c2128;
        border: 1px solid #00D4FF;
        border-radius: 10px;
        box-shadow: 0 0 10px #00D4FF;
        padding: 15px;
    }

    /* Text Colors */
    h1, h2, h3, p, span, label {
        color: #00D4FF !important;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Button Styling */
    .stButton>button {
        background-color: #0E1117;
        color: #00D4FF;
        border: 2px solid #00D4FF;
        border-radius: 20px;
        box-shadow: 0 0 5px #00D4FF;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #00D4FF;
        color: #0E1117;
        box-shadow: 0 0 20px #00D4FF;
    }

    /* Progress Bar Neon */
    .stProgress > div > div > div > div {
        background-color: #00D4FF;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #161B22;
        border-radius: 5px 5px 0px 0px;
        color: #00D4FF;
    }
    </style>
""", unsafe_allow_html=True) 

# ---------------- 3. SIDEBAR ----------------
with st.sidebar:
    try:
        st.image("logo.png", width=180)
    except:
        st.title("⚡ FLUX ENGINE")

    st.caption("FLUX v1.0 | Engineered by Shreya")
    st.markdown("---")

    st.header("🎮 Control Center")

    subject = st.selectbox("Current Domain", ["Physics", "Math/Coding", "Biology/Chem", "Languages", "Humanities"])
    hours = st.slider("Session Duration (Hrs)", 0.5, 8.0, 2.0)
    focus = st.slider("Focus Efficiency (1-10)", 1, 10, 8)

    st.markdown("---")
    log_btn = st.button("💾 Log Telemetry Data")

# ---------------- 4. ENGINE LOGIC ----------------
drain_factors = {
    "Physics": 1.5,
    "Math/Coding": 1.4,
    "Biology/Chem": 1.2,
    "Languages": 0.9,
    "Humanities": 0.8
}

drain = drain_factors[subject]

energy = (hours * drain) / (focus / 10)
efficiency = focus / (hours * drain) if hours > 0 else 0
battery = max(0, 100 - energy * 10)

# ---------------- 5. DASHBOARD ----------------
st.header("🖥️ System Telemetry Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("ENERGY DRAIN", f"{round(energy, 2)} Units")
col2.metric("SYSTEM EFFICIENCY", f"{round(efficiency * 100, 1)}%")

status = "OPTIMAL" if battery > 45 else "CRITICAL"
col3.metric("BATTERY HEALTH", status, delta=f"{int(battery)}%")

if battery < 45:
    st.error(f"🚨 High load detected. Take a break for {round(energy * 12)} mins.")
else:
    st.success("✅ System stable")

# ---------------- 6. DATA STORAGE ----------------
file_path = "flux_data.csv"

if log_btn:
    new_entry = pd.DataFrame([{
        "Date": str(datetime.date.today()),
        "Subject": subject,
        "Energy": round(energy, 2),
        "Efficiency": round(efficiency * 100, 2)
    }])

    if not os.path.isfile(file_path):
        new_entry.to_csv(file_path, index=False)
    else:
        new_entry.to_csv(file_path, mode='a', header=False, index=False)

    st.success("Data saved successfully!")

# ---------------- 7. ANALYTICS ----------------
st.markdown("---")

if os.path.exists(file_path):
    df = pd.read_csv(file_path)

    tab1, tab2, tab3 = st.tabs(["📈 Load Trends", "📊 Subject Analysis", "📑 Raw Data"])

    with tab1:
        st.subheader("Energy Trend")
        st.line_chart(df["Energy"])

    with tab2:
        st.subheader("Efficiency by Subject")
        subject_stats = df.groupby("Subject")["Efficiency"].mean()
        st.bar_chart(subject_stats)

    with tab3:
        st.subheader("Stored Data")
        st.dataframe(df)

    # ---------------- 8. BURNOUT PREDICTION ----------------
    st.markdown("---")
    st.subheader("🔮 Burnout Prediction Engine")

    if len(df) >= 3:
        recent_data = df.tail(3)

        avg_energy = recent_data["Energy"].mean()
        avg_efficiency = recent_data["Efficiency"].mean()

        st.write(f"Recent Avg Energy: {round(avg_energy,2)}")
        st.write(f"Recent Avg Efficiency: {round(avg_efficiency,2)}%")

        if avg_energy > 6 and avg_efficiency < 60:
            st.error("🔴 HIGH BURNOUT RISK: Immediate rest recommended.")
        elif avg_energy > 4:
            st.warning("🟡 MODERATE RISK: Balance your workload.")
        else:
            st.success("🟢 LOW RISK: System stable.")

    else:
        st.info("Log at least 3 sessions to enable prediction.")

else:
    st.info("No data yet. Click 'Log Telemetry Data' to start.")

# ---------------- 9. FOOTER ----------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("FLUX Engine | Engineering Project")