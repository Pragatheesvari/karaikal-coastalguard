import streamlit as st
import pandas as pd
import requests
from utils.risk_engine import (
    calculate_land_risk,
    calculate_marine_risk,
    calculate_compound_risk,
    get_risk_level
)
# -----------------------------
# THEME SELECTION
# -----------------------------

theme = st.sidebar.radio(
    "🎨 Choose Theme",
    ["Light", "Dark"]
)
if theme == "Dark":

    st.markdown("""
    <style>

    .stApp {
        background-color: #0E1117;
        color: white;
    }

    [data-testid="stSidebar"] {
        background-color: #161B22;
    }

    .stMarkdown,
    .stText,
    p,
    label {
        color: white !important;
    }

    .stMetric {
        background-color: #1C2128;
        border-radius: 10px;
        padding: 10px;
    }

    </style>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <style>

    .stApp {
        background-color: #FFFFFF;
        color: #111111;
    }

    [data-testid="stSidebar"] {
        background-color: #F5F7FA;
    }

    .stMarkdown,
    .stText,
    p,
    label {
        color: #111111 !important;
    }

    .stMetric {
        background-color: #F5F7FA;
        border-radius: 10px;
        padding: 10px;
    }

    </style>
    """, unsafe_allow_html=True)

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Karaikal CoastalGuard",
    page_icon="🌊",
    layout="wide"
)


# =========================
# LOAD DATA
# =========================

locations = pd.read_csv(
    "data/karaikal_locations.csv"
)

vulnerability = pd.read_csv(
    "data/vulnerability.csv"
)

historical = pd.read_csv(
    "data/historical_hazards.csv"
)


# =========================
# OPEN-METEO WEATHER
# =========================

def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
        "hourly": "precipitation",
        "forecast_days": 1
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    if response.status_code == 200:

        data = response.json()

        temperature = data["current"]["temperature_2m"]

        wind_speed = data["current"]["wind_speed_10m"]

        rainfall = sum(
            data["hourly"]["precipitation"]
        )

        return temperature, wind_speed, rainfall

    return None, None, None


# =========================
# OPEN-METEO MARINE
# =========================

def get_marine(latitude, longitude):

    url = "https://marine-api.open-meteo.com/v1/marine"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "wave_height,"
            "wave_direction,"
            "wave_period,"
            "sea_level_height_msl"
        ),
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    if response.status_code == 200:

        data = response.json()

        current = data["current"]

        return (
            current["wave_height"],
            current["wave_direction"],
            current["wave_period"],
            current["sea_level_height_msl"]
        )

    return None, None, None, None


# =========================
# HEADER
# =========================

st.title("🌊 Karaikal CoastalGuard")

st.subheader(
    "Hyperlocal Compound Risk & Livelihood Safety System"
)

st.write(
    "Identify combined drainage, agricultural and marine "
    "risks for Karaikal communities."
)


# =========================
# LOCATION
# =========================

st.divider()

st.header("📍 Select Location")

locations["location_name"] = (
    locations["village"].astype(str)
    + " - "
    + locations["water_body"].astype(str)
)

location_list = locations["location_name"].tolist()

selected_location = st.selectbox(
    "Choose a Karaikal location",
    location_list
)


# Get selected location

selected_row = locations[
    locations["location_name"] == selected_location
].iloc[0]

latitude = float(selected_row["latitude"])
longitude = float(selected_row["longitude"])

village = str(selected_row["village"])
water_body = str(selected_row["water_body"])


st.info(
    f"📍 {village} | 💧 {water_body} | "
    f"Latitude: {latitude:.6f} | "
    f"Longitude: {longitude:.6f}"
)


# =========================
# VULNERABILITY
# =========================

vulnerability_row = vulnerability[
    vulnerability["location"].astype(str).str.lower()
    == village.lower()
]


if len(vulnerability_row) > 0:

    vulnerability_row = vulnerability_row.iloc[0]

else:

    st.warning(
        "⚠️ Vulnerability data is not available "
        "for this location yet. Prototype default "
        "values will be used."
    )

    vulnerability_row = pd.Series({
        "drainage_vulnerability": "Medium",
        "agricultural_vulnerability": "Medium",
        "fishing_vulnerability": "Medium"
    })


drainage = vulnerability_row[
    "drainage_vulnerability"
]

agriculture = vulnerability_row[
    "agricultural_vulnerability"
]

fishing = vulnerability_row[
    "fishing_vulnerability"
]


# =========================
# HISTORICAL HAZARDS
# =========================

historical_row = historical[
    historical["location"].astype(str).str.lower()
    == village.lower()
]


if len(historical_row) > 0:

    historical_row = historical_row.iloc[0]

    st.header("📚 Historical Hazard Indicators")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🌊 Flood History",
            historical_row["flood_history"]
        )

    with col2:
        st.metric(
            "🚰 Waterlogging",
            historical_row["waterlogging_history"]
        )

    with col3:
        st.metric(
            "🌾 Crop Damage",
            historical_row["crop_damage_history"]
        )

    with col4:
        st.metric(
            "🌊 Marine Hazards",
            historical_row["marine_hazard_history"]
        )


# =========================
# WEATHER
# =========================

st.header("🌦️ Live Environmental Conditions")

temperature, wind_speed, rainfall = get_weather(
    latitude,
    longitude
)


if temperature is not None:

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🌡️ Temperature",
            f"{temperature} °C"
        )

    with col2:

        st.metric(
            "🌬️ Wind Speed",
            f"{wind_speed} km/h"
        )

    with col3:

        st.metric(
            "🌧️ Forecast Rainfall",
            f"{rainfall:.1f} mm"
        )

else:

    st.error(
        "Unable to fetch weather data. "
        "Please check your internet connection."
    )

    temperature = 0
    wind_speed = 0
    rainfall = 0


# =========================
# MARINE
# =========================

st.header("🌊 Live Marine Conditions")

(
    wave_height,
    wave_direction,
    wave_period,
    sea_level
) = get_marine(
    latitude,
    longitude
)


if wave_height is not None:

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🌊 Wave Height",
            f"{wave_height} m"
        )

    with col2:

        st.metric(
            "🧭 Wave Direction",
            f"{wave_direction}°"
        )

    with col3:

        st.metric(
            "⏱️ Wave Period",
            f"{wave_period} sec"
        )

    with col4:

        st.metric(
            "🌊 Sea Level",
            f"{sea_level} m"
        )

else:

    st.error(
        "Unable to fetch marine data."
    )

    wave_height = 0
    sea_level = 0


# =========================
# VULNERABILITY DISPLAY
# =========================

st.header("🚰🌾🎣 Local Vulnerability")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🚰 Drainage",
        drainage
    )

with col2:

    st.metric(
        "🌾 Agriculture",
        agriculture
    )

with col3:

    st.metric(
        "🎣 Fishing",
        fishing
    )


# =========================
# CALCULATE RISK
# =========================

if st.button(
    "⚠️ Calculate Compound Risk",
    use_container_width=True
):

    # -------------------------
    # LAND RISK
    # -------------------------

    land_risk = calculate_land_risk(
        rainfall,
        drainage,
        agriculture
    )


    # -------------------------
    # MARINE RISK
    # -------------------------

    marine_risk = calculate_marine_risk(
        wind_speed,
        wave_height,
        sea_level,
        fishing
    )


    # -------------------------
    # COMPOUND RISK
    # -------------------------

    compound_risk = calculate_compound_risk(
        land_risk,
        marine_risk
    )


    # -------------------------
    # RISK LEVEL
    # -------------------------

    risk_level = get_risk_level(
        compound_risk
    )


    # =========================
    # RISK ASSESSMENT
    # =========================

    st.divider()

    st.header("⚠️ Risk Assessment")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🌧️ Land Risk",
            f"{land_risk}/100"
        )

    with col2:

        st.metric(
            "🌊 Marine Risk",
            f"{marine_risk}/100"
        )

    with col3:

        st.metric(
            "⚠️ Compound Risk",
            f"{compound_risk}/100"
        )


    st.subheader(
        f"Risk Level: {risk_level}"
    )


    # =========================
    # RISK MESSAGE
    # =========================

    if risk_level == "LOW":

        st.success(
            "🟢 LOW RISK — Normal monitoring recommended."
        )

    elif risk_level == "MODERATE":

        st.info(
            "🟡 MODERATE RISK — Stay alert and monitor conditions."
        )

    elif risk_level == "HIGH":

        st.warning(
            "🟠 HIGH RISK — Take preventive action."
        )

    else:

        st.error(
            "🔴 SEVERE RISK — Immediate precaution is recommended."
        )


    # =========================
    # PROGRESS BAR
    # =========================

    st.progress(
        compound_risk / 100,
        text=f"Overall Compound Risk: {compound_risk}/100"
    )


    # =========================
    # RISK SUMMARY
    # =========================

    st.divider()

    st.header("📋 Risk Summary")

    if compound_risk <= 25:

        summary = (
            "Current environmental conditions indicate "
            "low combined risk. Continue normal monitoring."
        )

    elif compound_risk <= 50:

        summary = (
            "Moderate combined risk detected. "
            "Monitor rainfall, drainage and marine conditions."
        )

    elif compound_risk <= 75:

        summary = (
            "High combined risk detected. "
            "Preventive action is recommended for vulnerable livelihoods."
        )

    else:

        summary = (
            "Severe combined risk detected. "
            "Immediate precautionary action is recommended."
        )

    st.info(summary)


    # =========================
    # MAP
    # =========================

    st.divider()

    st.subheader("📍 Selected Location")

    map_data = pd.DataFrame({
        "latitude": [latitude],
        "longitude": [longitude]
    })

    st.map(
        map_data,
        zoom=12
    )


    # =========================
    # RECOMMENDED ACTIONS
    # =========================

    st.divider()

    st.header("🚨 Recommended Actions")


    # -------------------------
    # DRAINAGE
    # -------------------------

    st.subheader("🚰 Drainage")

    if drainage == "High" and rainfall >= 25:

        st.warning(
            "• High drainage vulnerability with significant rainfall.\n\n"
            "• Monitor drainage channels and water accumulation.\n\n"
            "• Avoid low-lying and waterlogged areas."
        )

    elif drainage == "Medium" and rainfall >= 25:

        st.info(
            "• Monitor drainage conditions.\n\n"
            "• Watch for local water accumulation."
        )

    else:

        st.success(
            "• Continue normal drainage monitoring."
        )


    # -------------------------
    # FARMER + FISHERMAN
    # -------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.subheader("🌾 Farmer")

        if land_risk > 75:

            st.warning(
                "• Protect crops and farm equipment.\n\n"
                "• Monitor water accumulation.\n\n"
                "• Avoid low-lying agricultural areas."
            )

        elif land_risk > 50:

            st.info(
                "• Monitor rainfall and drainage.\n\n"
                "• Prepare crop protection measures."
            )

        else:

            st.success(
                "• Continue normal monitoring."
            )


    with col2:

        st.subheader("🎣 Fisherman")

        if marine_risk > 75:

            st.warning(
                "• Avoid or delay fishing.\n\n"
                "• Monitor updated marine conditions.\n\n"
                "• Avoid entering the sea during severe conditions."
            )

        elif marine_risk > 50:

            st.info(
                "• Check marine forecast before departure.\n\n"
                "• Exercise additional caution."
            )

        else:

            st.success(
                "• Normal monitoring of marine conditions."
            )


# =========================
# DATA SOURCES
# =========================

st.divider()

st.header("📚 Data Sources")

st.markdown("""
- 📍 **Karaikal District Government** — Water-body and location data
- 🌧️ **Open-Meteo Weather API** — Temperature, rainfall and wind
- 🌊 **Open-Meteo Marine API** — Wave and sea-level information
- 🚰🌾🎣 **Local Vulnerability Layer** — Prototype vulnerability indicators
- 📚 **Historical Hazard Layer** — Prototype historical indicators
""")

st.caption(
    "Prototype decision-support system. "
    "Risk thresholds and weights should be calibrated "
    "using validated historical and government datasets "
    "before real-world deployment."
)