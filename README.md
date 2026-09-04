# Helicopter Rescue Simulator 🚁

A modern desktop application built with **wxPython** simulating a Search & Rescue (SAR) tactical dispatch and helicopter flight operations center.

Designed with an immersive dark tactical cockpit theme (`#111317`), high-visibility **Safety Orange** accents (`#FF5E13`), custom double-buffered tab controls, top status bar, and modular view architecture.

---

## 🖥️ User Interface & Layout

- **Standard Window Frame**: `1366 x 768` (Centered, minimum size `1024 x 600`, fully responsive).
- **Top Title Bar (`Controls/title_bar.py`)**:
  - Live UTC Zulu clock.
  - SATCOM telemetry link status (`99.8%`).
  - Active SAR alert level badge (`DEFCON 1 / READY FOR DISPATCH`).
- **Custom Modern Sidebar (`Controls/sidebar.py` & `Controls/tab_button.py`)**:
  - Tactical SAR emblem header badge.
  - 4 Custom owner-drawn tab controls with animated hover states, vector icons, and active Safety Orange indicator bars.
  - Callsign & Transponder status readout card (`RESCUE-01 • XPDR: 7700`).
- **Modular Content Area (`Views/`)**:
  - **Tab 1: Flight Ops & Telemetry**: Flight avionics bars (Altitude, Airspeed, Rotor RPM, Turboshaft Torque, Winch Cable), active status cards, and live SAR incident dispatch logs.
  - **Tab 2: Rescue Missions**: Active emergency incidents (Maritime Mayday, Mountain Avalanche, Offshore Medevac), GPS coordinates, victim status, and tactical scramble controls.
  - **Tab 3: Fleet & Gear**: Aircraft hangar inventory (Sikorsky S-92, Airbus H145, Leonardo AW139), dual hoist specifications (90m / 272kg), thermal FLIR payloads, and airworthiness maintenance records.
  - **Tab 4: Weather & Radar**: Animated 360° circular Doppler radar sweep, simulated storm cells, official METAR observations, sea state wave heights, and flight hazard advisories.

---

## 📁 Project Architecture

```
HelicopterRescueSimulator/
├── Assets/
│   ├── __init__.py
│   ├── theme.py          # Dark theme palette, Safety Orange accents, fonts & styling
│   └── icons.py          # Vector icon renderers using wx.GraphicsContext
├── Controls/
│   ├── __init__.py
│   ├── tab_button.py     # Custom double-buffered tab button with Safety Orange indicator
│   ├── sidebar.py        # Vertical navigation sidebar with 4 tab buttons & status
│   └── title_bar.py      # Compact header bar with live UTC clock and SAR badges
├── Views/
│   ├── __init__.py
│   ├── dashboard_view.py # Tab 1: Flight Ops & Telemetry Overview
│   ├── missions_view.py  # Tab 2: Search & Rescue Missions & Incident Dossier
│   ├── fleet_view.py     # Tab 3: Helicopter Fleet, Hoists & Maintenance
│   └── weather_view.py   # Tab 4: Animated Doppler Weather Radar & Conditions
├── main.py               # Application entry point & 1366x768 frame coordinator
├── requirements.txt      # Dependencies (wxPython, pygame)
├── .gitignore            # Git ignore configuration
└── README.md             # Project documentation
```

---

## 🚀 Installation & Setup

### 1. Create & Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

*(Packages: `wxPython==4.2.5`, `pygame==2.6.1`)*

### 3. Run the Application

```bash
python main.py
```

### 4. Run Automated UI Verification Test

```bash
python main.py --test
```