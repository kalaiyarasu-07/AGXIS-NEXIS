
import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(
    page_title="Agri Nexus Dashboard",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AGRI NEXUS")
st.caption("Environmental Sensor Monitoring Dashboard")

# Initialize sensor data
if "history" not in st.session_state:
    st.session_state.history = []

if "reading" not in st.session_state:
    st.session_state.reading = {
        "Temperature": 29.5,
        "Humidity": 65.0,
        "Gas Level": 220,
        "Ultrasonic Distance": 45.0
    }

# Generate simulated readings
def generate_data():
    old = st.session_state.reading

    return {
        "Temperature": round(
            max(15, min(45, old["Temperature"] +
                        random.uniform(-0.8, 0.8))), 1
        ),
        "Humidity": round(
            max(20, min(100, old["Humidity"] +
                        random.uniform(-2, 2))), 1
        ),
        "Gas Level": max(
            0, old["Gas Level"] + random.randint(-30, 30)
        ),
        "Ultrasonic Distance": round(
            max(2, min(400, old["Ultrasonic Distance"] +
                        random.uniform(-5, 5))), 1
        )
    }

# Refresh dashboard every 3 seconds
@st.fragment(run_every="3s")
def dashboard():

    st.session_state.reading = generate_data()
    data = st.session_state.reading

    # Save readings for visualization
    st.session_state.history.append({
        "Time": datetime.now(),
        **data
    })

    st.session_state.history = (
        st.session_state.history[-100:]
    )

    st.subheader("Live Sensor Readings")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🌡️ Temperature",
        f"{data['Temperature']} °C"
    )

    col2.metric(
        "💧 Humidity",
        f"{data['Humidity']} %"
    )

    col3.metric(
        "☁️ Gas Level",
        data["Gas Level"]
    )

    col4.metric(
        "📡 Ultrasonic Distance",
        f"{data['Ultrasonic Distance']} cm"
    )

    st.caption(
        "Last updated: " +
        datetime.now().strftime("%H:%M:%S")
    )

    # Environmental warnings
    st.subheader("Environmental Status")

    a, b, c = st.columns(3)

    if data["Temperature"] >= 35:
        a.error("High Temperature")
    else:
        a.success("Temperature Normal")

    if data["Gas Level"] >= 400:
        b.error("High Gas Level")
    else:
        b.success("Gas Level Normal")

    if data["Ultrasonic Distance"] <= 20:
        c.warning("Object Detected Nearby")
    else:
        c.success("Area Clear")

    # Sensor charts
    st.subheader("Sensor Analytics")

    history = pd.DataFrame(
        st.session_state.history
    )

    tabs = st.tabs([
        "Temperature",
        "Humidity",
        "Gas Level",
        "Ultrasonic"
    ])

    with tabs[0]:
        st.line_chart(
            history.set_index("Time")[["Temperature"]]
        )

    with tabs[1]:
        st.line_chart(
            history.set_index("Time")[["Humidity"]]
        )

    with tabs[2]:
        st.line_chart(
            history.set_index("Time")[["Gas Level"]]
        )

    with tabs[3]:
        st.line_chart(
            history.set_index("Time")[
                ["Ultrasonic Distance"]
            ]
        )

    st.caption(
        "Demo Mode: Sensor readings are simulated. "
        "No physical hardware is connected."
    )

dashboard()
