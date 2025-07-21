import streamlit as st
import requests

# Streamlit setup
st.set_page_config(page_title="Rodriguez & Burgos Water Levels", layout="centered")
st.markdown("<h1 style='text-align: center;'>☔ Montalban Water Level Monitor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'> Data from PAGASA | Monitoring stations in Rodriguez and Burgos</p>", unsafe_allow_html=True)

# Water level thresholds (used for internal classification)
thresholds = {
    "Rodriguez": {"alert": 28.80, "alarm": 29.80, "critical": 30.70},
    "Burgos": {"alert": 27.40, "alarm": 27.90, "critical": 28.40}
}

# Classification function
def classify_status(station, level):
    t = thresholds[station]
    if level >= t["critical"]:
        return "🔴 Critical"
    elif level >= t["alarm"]:
        return "🚨 Alarm"
    elif level >= t["alert"]:
        return "⚠️ Alert"
    else:
        return "✅ Normal"

# Fetch data
url = "https://pasig-marikina-tullahanffws.pagasa.dost.gov.ph/water/table_list.do"

try:
    response = requests.post(url, timeout=10)
    if response.status_code == 200:
        stations = response.json()

        for target in ["Rodriguez", "Burgos"]:
            for station in stations:
                if target.lower() in station["obsnm"].lower():
                    try:
                        wl_now = float(station["wl"])
                        wl30m = station["wl30m"]
                        wl1h = station["wl1h"]
                        wl2h = station["wl2h"]
                        status = classify_status(target, wl_now)

                        st.markdown(f"<h1 style='text-align: center;'>📍 {station['obsnm']}</h2>", unsafe_allow_html=True)
                        st.markdown(
                            f"""
                            <div style='text-align: center; font-size: 1.2em;line-height: 1; margin: 0; padding: 0;'>
                                <p><b>Status:</b> {status}</p>
                                <p><b><span style="font-size: 1.8em;">Now:</span></b> <span style="font-size: 2em;">{wl_now} m</span></p>
                                <p><b>-30 min:</b> <span style="font-size: 1.5em;">{wl30m} m</span></p>
                                <p><b>-1 hour:</b> <span style="font-size: 1.5em;">{wl1h} m</span></p>
                                <p><b>-2 hours:</b> <span style="font-size: 1.5em;">{wl2h} m</span></p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    except:
                        st.error(f"⚠️ Invalid or missing data for {target}.")
    else:
        st.error(f"❌ Failed to fetch data. Status code: {response.status_code}")
except Exception as e:
    st.error(f"❌ Error fetching data: {e}")
st.markdown(
    f"""
    <div style="text-align: center; font-size: 0.9em; margin-top: 1em;">
    <p>Data source: 
        <a href="https://pasig-marikina-tullahanffws.pagasa.dost.gov.ph/water/table.do" 
        target="_blank" 
        rel="noopener noreferrer"
        style="color: #2563eb; text-decoration: underline;">
        PAGASA - Pasig-Marikina-Tullahan River Water Level Table
        </a>
    </p>
    </div>
    """,
    unsafe_allow_html=True
    )