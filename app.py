import streamlit as st
import requests
import datetime

# Streamlit setup
st.set_page_config(page_title="Rodriguez & Burgos Water Levels", layout="centered")
st.markdown("<h1 style='text-align: center;'>☔ Montalban Water Level Monitor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'> Data from PAGASA | Monitoring stations in Rodriguez and Burgos</p>", unsafe_allow_html=True)

# Water level thresholds
thresholds = {
    "Rodriguez": {"alert": 28.80, "alarm": 29.80, "critical": 30.70},
    "Burgos": {"alert": 27.40, "alarm": 27.90, "critical": 28.40}
}

# Classification for display
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

# Numeric status for comparison
def get_level_status(station, level):
    t = thresholds[station]
    if level >= t["critical"]:
        return 3
    elif level >= t["alarm"]:
        return 2
    elif level >= t["alert"]:
        return 1
    else:
        return 0

# Compare -1h vs now
def get_trend_note(station, now, past):
    now_rank = get_level_status(station, now)
    past_rank = get_level_status(station, past)
    if now_rank > past_rank:
        return ("🔺 Rising", "red")
    elif now_rank < past_rank:
        return ("🔻 Receding", "green")
    else:
        return ("⏸️ No Significant Change", "orange")

# Fetch data
url = "https://pasig-marikina-tullahanffws.pagasa.dost.gov.ph/water/table_list.do"

try:
    response = requests.post(url, timeout=10)
    if response.status_code == 200:
        stations = response.json()

        delay = 0
        for target in ["Rodriguez", "Burgos"]:
            for station in stations:
                if target.lower() in station["obsnm"].lower():
                    try:
                        wl_now = float(station["wl"])
                        wl30m = float(station["wl30m"])
                        wl1h = float(station["wl1h"])
                        wl2h = float(station["wl2h"])
                        status = classify_status(target, wl_now)

                        # 1-hour trend comparison
                        trend_note, color = get_trend_note(target, wl_now, wl1h)

                        st.markdown(
                            f"""
                            <style>
                            :root {{
                                --div-background-color: #e0f2ff;
                                --text-color: black;
                            }}
                            @media (prefers-color-scheme: dark) {{
                                :root {{
                                    --div-background-color: #1a2b40;
                                    --text-color: white;
                                }}
                            }}
                            .zoom-in {{
                                animation: zoomIn 0.6s ease forwards;
                                transform: scale(0.9);
                                opacity: 0;
                                animation-delay: {delay}s;
                                background-color: var(--div-background-color);
                                color: var(--text-color);
                                margin-bottom: 2em;
                                padding: 1.2em;
                                border-radius: 1em;
                            }}
                            .zoom-in h2, .zoom-in p, .zoom-in b, .zoom-in span {{
                                color: var(--text-color);
                            }}
                            @keyframes zoomIn {{
                                from {{
                                    transform: scale(0.9);
                                    opacity: 0;
                                }}
                                to {{
                                    transform: scale(1);
                                    opacity: 1;
                                }}
                            }}
                            </style>

                            <div class="zoom-in">
                                <h2 style='text-align: center;'>📍 {station['obsnm']}</h2>
                                <div style='text-align: center; font-size: 1.2em; line-height: 1; margin: 0; padding: 0;'>
                                    <p><b>Status:</b> {status}</p>
                                    <p><b><span style="font-size: 1.8em;">Now:</span></b> <span style="font-size: 2em;">{wl_now} m</span></p>
                                    <div style='display: flex; justify-content: center; gap: 1em; margin-top: 0.5em;'>
                                        <p><b>-30 min:</b> <span style="font-size: 1em;">{wl30m} m</span></p>
                                        <p><b>-1 hour:</b> <span style="font-size: 1em;">{wl1h} m</span></p>
                                        <p><b>-2 hours:</b> <span style="font-size: 1em;">{wl2h} m</span></p>
                                    </div>
                                    <p style='margin-top: 1em;'><b>1-hour trend:</b> <span style="color:{color};">{trend_note}</span></p>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        delay += 0.5
                    except:
                        st.error(f"⚠️ Invalid or missing data for {target}.")
    else:
        st.error(f"❌ Failed to fetch data. Status code: {response.status_code}")
except Exception as e:
    st.error(f"❌ Error fetching data: {e}")

# Show date and time
fetch_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(
    f"<p style='text-align: center; color: gray;'>Last updated: <b>{fetch_time}</b></p>",
    unsafe_allow_html=True
)

# Refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()

# Credit
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
