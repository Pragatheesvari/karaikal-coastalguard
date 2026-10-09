import streamlit as st
import pandas as pd
import requests

from utils.risk_engine import (
    calculate_land_risk,
    calculate_marine_risk,
    calculate_compound_risk,
    get_risk_level
)


# -------------------------
# PAGE SETTINGS
# -------------------------

st.set_page_config(
    page_title="Karaikal CoastalGuard",
    page_icon="🌊",
    layout="wide"
)


# -------------------------
# LOAD DATA
# -------------------------

locations = pd.read_csv(
    "data/karaikal_locations.csv"
)

vulnerability = pd.read_csv(
    "data/vulnerability.csv"
)
historical = pd.read_csv(
    "data/historical_hazards.csv"
)

# -------------------------
# OPEN-METEO FUNCTION
# -------------------------

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

def get_marine(latitude, longitude):

    url = "https://marine-api.open-meteo.com/v1/marine"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "wave_height,wave_direction,wave_period,sea_level_height_msl",
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
# -------------------------
# HEADER
# -------------------------

st.title("🌊 Karaikal CoastalGuard")

st.subheader(
    "Hyperlocal Compound Risk & Livelihood Safety System"
)

st.write(
    "Identify combined drainage, agricultural and marine "
    "risks for Karaikal communities."
)





st.markdown("""<style>
.stApp{background:radial-gradient(circle at 10% 0%,rgba(0,180,216,.12),transparent 28%),radial-gradient(circle at 90% 10%,rgba(0,119,182,.12),transparent 25%),#071A2B;color:#F5F9FC}.block-container{max-width:1450px;padding-top:2rem;padding-bottom:3rem}section[data-testid="stSidebar"]{background:linear-gradient(180deg,#061522,#0A2235);border-right:1px solid rgba(0,180,216,.22)}h1,h2,h3{color:#F5F9FC!important}p,li,label,.stMarkdown{color:#D7E6EF} .hero{padding:2rem 2.2rem;border-radius:22px;background:linear-gradient(135deg,#0B3048,#082033 55%,#061522);border:1px solid rgba(0,180,216,.30);box-shadow:0 15px 45px rgba(0,0,0,.25);margin-bottom:1.5rem}.hero-title{font-size:2.45rem;font-weight:800}.hero-subtitle{font-size:1.08rem;color:#A9DCEB;margin:.35rem 0 .8rem}.badge{display:inline-block;padding:.35rem .8rem;border-radius:999px;background:rgba(0,180,216,.13);border:1px solid rgba(0,180,216,.35);color:#7DE7FF;font-size:.82rem;font-weight:700}.section-title{font-size:1.35rem;font-weight:750;color:#F5F9FC;margin:1.2rem 0 .8rem}div[data-testid="stMetric"]{background:linear-gradient(145deg,#0D2A40,#0A2235);border:1px solid rgba(0,180,216,.20);border-radius:16px;padding:1rem;box-shadow:0 8px 25px rgba(0,0,0,.16)}div[data-testid="stMetricLabel"]{color:#A9C8D6!important}div[data-testid="stMetricValue"]{color:#F5F9FC!important}.stButton>button{border-radius:14px;border:1px solid #00B4D8;background:linear-gradient(90deg,#0077B6,#00B4D8);color:white;font-weight:800;padding:.75rem 1rem;box-shadow:0 8px 22px rgba(0,180,216,.18)}.risk-panel{background:linear-gradient(145deg,#0D2A40,#071A2B);border:1px solid rgba(0,180,216,.30);border-radius:22px;padding:1.5rem;text-align:center;box-shadow:0 12px 35px rgba(0,0,0,.20)}.risk-score{font-size:3.5rem;font-weight:900;line-height:1;margin:.5rem 0}.risk-low{color:#55D187}.risk-moderate{color:#FFD166}.risk-high{color:#FF9F43}.risk-severe{color:#FF5C5C}.action-card{background:#0D2A40;border:1px solid rgba(255,255,255,.08);border-radius:17px;padding:1.2rem;min-height:150px;box-shadow:0 8px 25px rgba(0,0,0,.14)}.action-title{font-size:1.1rem;font-weight:800;color:#F5F9FC;margin-bottom:.55rem}.action-text{color:#C9DCE6;line-height:1.65}.source-panel{background:#081E30;border:1px solid rgba(0,180,216,.16);border-radius:16px;padding:1.2rem 1.4rem}#MainMenu,footer{visibility:hidden}
</style>""",unsafe_allow_html=True)

st.markdown("""<div class="hero"><div class="hero-title">🌊 Karaikal CoastalGuard</div><div class="hero-subtitle">Hyperlocal Compound Risk &amp; Livelihood Safety System</div><div>One location • Multiple hazards • One actionable risk picture</div></div>""",unsafe_allow_html=True)
with st.sidebar:
    st.markdown("## 🌊 CoastalGuard")
    st.caption("Hyperlocal risk intelligence")
    st.divider()
    st.markdown("### 📌 Risk Layers")
    st.markdown("🌧️ Rainfall  \n🚰 Drainage  \n🌾 Agriculture  \n🌬️ Wind  \n🌊 Waves  \n🌊 Sea level  \n🎣 Fishing vulnerability")
    st.divider()
    st.markdown("### 📊 Risk Scale")
    st.markdown("🟢 **0–25** — Low  \n🟡 **26–50** — Moderate  \n🟠 **51–75** — High  \n🔴 **76–100** — Severe")
    st.divider()
    st.caption("Prototype decision-support system")
# -------------------------
# LOCATION
# -------------------------

st.divider()

st.markdown('<div class="section-title">📍 Select Monitoring Location</div>',unsafe_allow_html=True)

# Create a readable location name
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

# Get selected location row
selected_row = locations[
    locations["location_name"] == selected_location
].iloc[0]

latitude = float(selected_row["latitude"])
longitude = float(selected_row["longitude"])

village = selected_row["village"]
water_body = selected_row["water_body"]

st.info(
    f"📍 {village} | 💧 {water_body} | "
    f"Latitude: {latitude:.6f} | "
    f"Longitude: {longitude:.6f}"
)


# -------------------------
# GET VULNERABILITY
# -------------------------

vulnerability_row = vulnerability[
    vulnerability["location"].str.lower()
    == village.lower()
]
if len(vulnerability_row) > 0:

    vulnerability_row = vulnerability_row.iloc[0]

else:

    st.warning(
        "⚠️ Vulnerability data is not available "
        "for this location yet. Prototype default values will be used."
    )

    vulnerability_row = pd.Series({
        "drainage_vulnerability": "Medium",
        "agricultural_vulnerability": "Medium",
        "fishing_vulnerability": "Medium"
    })
# -------------------------
# HISTORICAL HAZARD
# -------------------------

historical_row = historical[
    historical["location"].str.lower()
    == village.lower()
]

if len(historical_row) > 0:

    historical_row = historical_row.iloc[0]

    st.markdown('<div class="section-title">📚 Historical Hazard Indicators</div>',unsafe_allow_html=True)

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

# -------------------------
# FETCH WEATHER
# -------------------------

temperature, wind_speed, rainfall = get_weather(
    latitude,
    longitude
)


# -------------------------
# ENVIRONMENTAL CONDITIONS
# -------------------------

st.markdown('<div class="section-title">🌦️ Live Environmental Conditions</div>',unsafe_allow_html=True)


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


# -------------------------
# MARINE CONDITIONS
# -------------------------

st.markdown('<div class="section-title">🌊 Live Marine Conditions</div>',unsafe_allow_html=True)

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

# -------------------------
# VULNERABILITY
# -------------------------

st.markdown('<div class="section-title">🚰🌾🎣 Local Vulnerability</div>',unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)


with col1:

    drainage = vulnerability_row[
        "drainage_vulnerability"
    ]

    st.metric(
        "🚰 Drainage",
        drainage
    )


with col2:

    agriculture = vulnerability_row[
        "agricultural_vulnerability"
    ]

    st.metric(
        "🌾 Agriculture",
        agriculture
    )


with col3:

    fishing = vulnerability_row[
        "fishing_vulnerability"
    ]

    st.metric(
        "🎣 Fishing",
        fishing
    )
# -------------------------
# COMPOUND RISK
# -------------------------
st.divider()
st.markdown('<div class="section-title">⚠️ Compound Risk Assessment</div>',unsafe_allow_html=True)
if st.button("⚠️ CALCULATE COMPOUND RISK",use_container_width=True):
    land_risk=calculate_land_risk(rainfall,drainage,agriculture)
    marine_risk=calculate_marine_risk(wind_speed,wave_height,sea_level,fishing)
    compound_risk=calculate_compound_risk(land_risk,marine_risk)
    risk_level=get_risk_level(compound_risk)
    cls={"LOW":"risk-low","MODERATE":"risk-moderate","HIGH":"risk-high","SEVERE":"risk-severe"}[risk_level]
    msg={"LOW":"🟢 LOW RISK — Normal monitoring recommended.","MODERATE":"🟡 MODERATE RISK — Stay alert and monitor conditions.","HIGH":"🟠 HIGH RISK — Take preventive action.","SEVERE":"🔴 SEVERE RISK — Immediate precaution is recommended."}[risk_level]
    st.markdown(f'<div class="risk-panel"><div style="color:#A9C8D6;font-weight:700">OVERALL COMPOUND RISK</div><div class="risk-score {cls}">{compound_risk}/100</div><div class="{cls}" style="font-size:1.35rem;font-weight:850">{risk_level}</div><div style="color:#BFD3DE;margin-top:.5rem">{msg}</div></div>',unsafe_allow_html=True)
    st.progress(compound_risk/100,text=f"Compound Risk Score: {compound_risk}/100")
    c1,c2=st.columns(2)
    c1.metric("🌧️ Land Risk",f"{land_risk}/100")
    c2.metric("🌊 Marine Risk",f"{marine_risk}/100")
    if compound_risk<=25: summary="Current environmental conditions indicate low combined risk. Continue normal monitoring."
    elif compound_risk<=50: summary="Moderate combined risk detected. Monitor rainfall, drainage and marine conditions."
    elif compound_risk<=75: summary="High combined risk detected. Preventive action is recommended for vulnerable livelihoods."
    else: summary="Severe combined risk detected. Immediate precautionary action is recommended."
    st.info(f"📋 **Risk Summary:** {summary}")
    st.divider()
    st.markdown('<div class="section-title">📍 Monitoring Location</div>',unsafe_allow_html=True)
    st.map(pd.DataFrame({"latitude":[latitude],"longitude":[longitude]}),zoom=12)
    st.divider()
    st.markdown('<div class="section-title">🚨 Recommended Actions</div>',unsafe_allow_html=True)
    if drainage=="High" and rainfall>=25: da="• Monitor drainage channels and water accumulation.<br>• Avoid low-lying and waterlogged areas.<br>• Prepare for possible drainage overflow."
    elif drainage=="Medium" and rainfall>=25: da="• Monitor drainage conditions.<br>• Watch for local water accumulation."
    else: da="• Continue normal drainage monitoring."
    if land_risk>75: fa="• Protect crops and farm equipment.<br>• Monitor water accumulation.<br>• Avoid low-lying agricultural areas."
    elif land_risk>50: fa="• Monitor rainfall and drainage.<br>• Prepare crop protection measures."
    else: fa="• Continue normal agricultural monitoring."
    if marine_risk>75: fi="• Avoid or delay fishing.<br>• Monitor updated marine conditions.<br>• Avoid entering the sea during severe conditions."
    elif marine_risk>50: fi="• Check marine forecast before departure.<br>• Exercise additional caution."
    else: fi="• Continue normal monitoring of marine conditions."
    c1,c2,c3=st.columns(3)
    c1.markdown(f'<div class="action-card"><div class="action-title">🚰 Drainage</div><div class="action-text">{da}</div></div>',unsafe_allow_html=True)
    c2.markdown(f'<div class="action-card"><div class="action-title">🌾 Farmer</div><div class="action-text">{fa}</div></div>',unsafe_allow_html=True)
    c3.markdown(f'<div class="action-card"><div class="action-title">🎣 Fisherman</div><div class="action-text">{fi}</div></div>',unsafe_allow_html=True)
else:
    st.markdown('<div class="risk-panel"><div style="font-size:2rem">🌊</div><div style="font-size:1.25rem;font-weight:800;color:#F5F9FC">Ready for Risk Assessment</div><div style="color:#A9C8D6;margin-top:.4rem">Select a location and calculate the compound risk using the live environmental conditions above.</div></div>',unsafe_allow_html=True)

st.divider()
with st.expander("🧠 How is Compound Risk Calculated?"):
    st.markdown("**Land Risk**  \n`Rainfall + Drainage Vulnerability + Agricultural Vulnerability`  \n↓  \n**Land Risk / 100**  \n\n---\n\n**Marine Risk**  \n`Wind + Wave Height + Sea Level + Fishing Vulnerability`  \n↓  \n**Marine Risk / 100**  \n\n---\n\n**Compound Risk**  \n`Land Risk × 55% + Marine Risk × 45%`  \n↓  \n**LOW → MODERATE → HIGH → SEVERE**")

st.divider()
st.markdown('<div class="section-title">📚 Data Sources & Data Status</div>',unsafe_allow_html=True)
st.markdown("<div class='source-panel'><b>✅ Real / Live Data</b><br>📍 <b>Karaikal District Government</b> — Water-body and location coordinates<br>🌧️ <b>Open-Meteo Weather API</b> — Temperature, rainfall and wind<br>🌊 <b>Open-Meteo Marine API</b> — Wave and sea-level information<br><br><b>⚠️ Prototype Data</b><br>🚰🌾🎣 <b>Local Vulnerability Layer</b> — Prototype indicators<br>📚 <b>Historical Hazard Layer</b> — Prototype indicators<br><br><b>🚀 Future Enhancement</b><br>Prototype vulnerability and historical indicators can be replaced or calibrated using validated government and historical datasets.</div>",unsafe_allow_html=True)
st.caption("Karaikal CoastalGuard is a prototype decision-support system. It is not an official disaster warning system.")
st.markdown('<div style="text-align:center;color:#7693A3;font-size:.82rem;padding-top:1rem">🌊 Karaikal CoastalGuard • AI for Karaikal Hackathon 2026</div>',unsafe_allow_html=True)
