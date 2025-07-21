#  Montalban Water Level Monitor

This Streamlit app provides a simple, real-time visualization of river water levels from PAGASA monitoring stations in **Rodriguez** and **Burgos**, Rizal. It helps local users quickly check flood risk by referencing key water level thresholds: **Alert**, **Alarm**, and **Critical**.

## Live App

[Click here to open the live app](https://montalbanwaterlevel.streamlit.app/)  

---

## Features

- **Live water level data** pulled from PAGASA’s public endpoint
- Color-coded water status:
  - ✅ Normal
  - ⚠️ Alert
  - 🚨 Alarm
  - 🔴 Critical
- Simple and data-consumer friendly details 
- Mobile-friendly and fast to load

---

## Data Source

All data is fetched from the official PAGASA website:

[PAGASA Water Level Table](https://pasig-marikina-tullahanffws.pagasa.dost.gov.ph/water/table.do)

---

## Tech Stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Requests](https://docs.python-requests.org/)
- Tailwind-inspired CSS for styling

---

##  Installation

To run the app locally:

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/montalban-water-monitor.git
cd montalban-water-monitor
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the app:**

```bash
streamlit run app.py
```

---

## Threshold Reference

The following are used internally to classify water levels:

| Station   | Alert (⚠️) | Alarm (🚨) | Critical (🔴) |
|-----------|------------|------------|----------------|
| Rodriguez | 28.80 m    | 29.80 m    | 30.70 m        |
| Burgos    | 27.40 m    | 27.90 m    | 28.40 m        |

---

## License

This project is under the [MIT License](LICENSE).  
Data provided by PAGASA is publicly accessible and not modified in any way.

---

## Acknowledgments

- PAGASA for maintaining a public water level data API  
- Streamlit for the lightweight, interactive web app platform