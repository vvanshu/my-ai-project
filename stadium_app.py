import streamlit as st
import plotly.graph_objects as go
import datetime

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="VIO — Volunteer Companion Hub | FIFA 2026",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. GLOBAL CUSTOM CSS — DARK THEME, IGNITION AURA, AVATARS, FLOATING BOT
# ==============================================================================
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;600;700&family=Fira+Code:wght@400;600&display=swap');

/* === BASE DARK THEME === */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #0E1117 !important;
    color: #FFFFFF !important;
    font-family: 'Outfit', sans-serif !important;
}
[data-testid="stSidebar"] {
    background-color: #08121E !important;
    border-right: 1px solid #1A2E40 !important;
}
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; font-weight: 700; }

/* === IGNITION AURA — Active Tab Glow === */
button[data-baseweb="tab"] {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    color: #A0C0D0 !important;
    border-bottom: 3px solid transparent !important;
    padding: 0.7rem 1.2rem !important;
    transition: all 0.3s ease !important;
    background: transparent !important;
}
button[data-baseweb="tab"]:hover {
    color: #FFFFFF !important;
    background: rgba(10, 102, 194, 0.08) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #FFFFFF !important;
    border-bottom: 3px solid #0A66C2 !important;
    background: rgba(10, 102, 194, 0.12) !important;
    box-shadow: 0 4px 12px rgba(10, 102, 194, 0.2) !important;
}
div[data-baseweb="tab-highlight"] {
    background-color: #0A66C2 !important;
}
div[data-baseweb="tab-border"] {
    background-color: #1E3A52 !important;
}

/* === WEATHER STRIP === */
.weather-strip {
    background: linear-gradient(90deg, #122030 0%, #0E1117 100%);
    border: 1px solid #1E3A52;
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    font-size: 0.88rem;
    color: #BEC2CA;
}
.weather-strip .temp { color: #FFAA00; font-weight: 700; font-size: 1.05rem; }
.weather-strip .hydrate { color: #00FFCC; font-weight: 600; }

/* === METRIC CARDS === */
.metric-container { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.metric-card {
    flex: 1;
    background-color: #122030;
    border: 1px solid #1E3A52;
    border-radius: 12px;
    padding: 1.1rem;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.35);
    transition: all 0.3s ease;
}
.metric-card:hover { border-color: #00FFCC; transform: translateY(-2px); }
.metric-title { font-size: 0.78rem; color: #A0C0D0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; }
.metric-val { font-size: 1.7rem; color: #FFFFFF; font-weight: 700; margin: 0.3rem 0; font-family: 'Space Grotesk', sans-serif; }
.metric-desc { font-size: 0.72rem; color: #00FFCC; font-weight: 500; }
.metric-desc.urgent { color: #FF4B4B; }

/* === PROFILE BADGE === */
.profile-badge {
    background-color: #122030;
    border: 1px solid #1E3A52;
    border-radius: 12px;
    padding: 0.8rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.7rem;
}
.profile-badge .avatar-circle {
    width: 42px; height: 42px; border-radius: 50%;
    background: linear-gradient(135deg, #0A66C2, #00FFCC);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; font-weight: 700; color: #FFFFFF;
    flex-shrink: 0;
}
.profile-badge .badge-name { font-size: 0.95rem; font-weight: 600; color: #FFFFFF; }
.profile-badge .badge-role { font-size: 0.72rem; color: #A0C0D0; }

/* === PROFILE CARDS === */
.profile-card {
    background-color: #122030;
    border: 1px solid #1E3A52;
    border-radius: 12px;
    padding: 1.15rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    border-top: 4px solid #00FFCC;
    transition: transform 0.2s ease;
}
.profile-card:hover { transform: scale(1.01); }
.profile-header { display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.7rem; }
.profile-name { font-size: 1.1rem; font-weight: 600; color: #FFFFFF; }
.profile-role-badge { font-size: 0.68rem; font-weight: 600; background-color: #0F4C81; color: #FFFFFF; padding: 0.2rem 0.5rem; border-radius: 4px; text-transform: uppercase; }
.profile-info { font-size: 0.83rem; color: #BEC2CA; margin-bottom: 0.35rem; }
.profile-label { font-weight: 500; color: #8E929A; }

/* === STATUS BADGES === */
.badge { display: inline-block; padding: 0.25rem 0.6rem; font-size: 0.73rem; font-weight: 600; border-radius: 6px; text-transform: uppercase; }
.badge-urgent { background-color: rgba(255,75,75,0.15); color: #FF4B4B; border: 1px solid #FF4B4B; }
.badge-warning { background-color: rgba(255,170,0,0.15); color: #FFAA00; border: 1px solid #FFAA00; }
.badge-nominal { background-color: rgba(0,255,204,0.15); color: #00FFCC; border: 1px solid #00FFCC; }

/* === ACTIVITY FEED TERMINAL === */
.activity-feed {
    background-color: #050E17;
    border: 1px solid #1E3A52;
    border-radius: 8px;
    padding: 1rem;
    font-family: 'Fira Code', monospace;
    font-size: 0.78rem;
    max-height: 220px;
    overflow-y: auto;
    color: #00FFCC;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.8);
}
.feed-entry { margin-bottom: 0.35rem; line-height: 1.3; }

/* === SHIFT SCHEDULE TIMELINE === */
.schedule-item {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 0.9rem 1rem;
    margin-bottom: 0.6rem;
    border-radius: 10px;
    border-left: 4px solid #1E3A52;
    background-color: #122030;
    transition: all 0.2s ease;
}
.schedule-item.completed { border-left-color: #00FFCC; opacity: 0.65; }
.schedule-item.current { border-left-color: #0A66C2; background-color: #0F1E35; box-shadow: 0 0 12px rgba(10,102,194,0.2); }
.schedule-item.upcoming { border-left-color: #1E3A52; }
.schedule-time { font-family: 'Fira Code', monospace; font-size: 0.85rem; color: #FFAA00; font-weight: 600; min-width: 50px; }
.schedule-desc { font-size: 0.9rem; color: #FFFFFF; font-weight: 500; }
.schedule-status { font-size: 0.7rem; text-transform: uppercase; font-weight: 600; margin-top: 2px; }
.schedule-status.done { color: #00FFCC; }
.schedule-status.active { color: #0A66C2; }
.schedule-status.pending { color: #8E929A; }

/* === FLOATING VIO BOT === */
.vio-float-btn {
    position: fixed;
    bottom: 28px;
    right: 28px;
    z-index: 9999;
    background: linear-gradient(135deg, #0A66C2, #00FFCC);
    width: 62px; height: 62px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem;
    box-shadow: 0 6px 20px rgba(0,255,204,0.3);
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid #00FFCC;
}
.vio-float-btn:hover { transform: scale(1.1); box-shadow: 0 8px 28px rgba(0,255,204,0.45); }
.vio-speech-bubble {
    position: fixed;
    bottom: 98px;
    right: 24px;
    z-index: 9998;
    background-color: #122030;
    border: 1px solid #1E3A52;
    border-radius: 12px 12px 0 12px;
    padding: 0.8rem 1rem;
    max-width: 260px;
    font-size: 0.82rem;
    color: #BEC2CA;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}

/* === ONBOARDING CARD === */
.onboard-card {
    max-width: 580px;
    margin: 2rem auto;
    background-color: #122030;
    border: 1px solid #1E3A52;
    border-radius: 16px;
    padding: 2.5rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    border-top: 4px solid #0A66C2;
}

/* === SCROLLBAR === */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0E1117; }
::-webkit-scrollbar-thumb { background: #122030; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #00FFCC; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==============================================================================
# 3. VIO AI KNOWLEDGE BASE
# ==============================================================================
VIO_KNOWLEDGE = {
    "spanish vip wheelchair access path": {
        "title": "♿ Spanish Guest Wheelchair Route (Gate C → Royal Box)",
        "steps": [
            "Verify that Gate C ramp access is completely clear of media gear.",
            "Greet the guest party at Gate C Lobby (Volunteer Maria Delgado speaks fluent Spanish).",
            "Guide through VIP Security Lane 3 (wider clearance for wheelchair passage).",
            "Proceed directly to VIP Elevator West. Secure access to Level 2.",
            "Exit elevator, turn left into VIP Secured Corridor (do not enter the public concourse).",
            "Proceed up the East VIP Corridor Ramp directly into the Royal Box."
        ],
        "tags": ["Spain", "Wheelchair", "Gate C", "Royal Box"]
    },
    "fastest route from gate b to executive box 4": {
        "title": "⚡ Fastest Route: Gate B → Executive Box 4",
        "steps": [
            "Receive guests at Gate B Ground Reception.",
            "Fast-track through VIP Security Lane 2.",
            "Take VIP Escalator 'Bravo' (east side of lobby) straight to Level 3.",
            "Turn right at Level 3 corridor, walk past VIP Lounge 1 entry.",
            "Continue down the executive suite corridor for 50 meters.",
            "Executive Box 4 is on the left side (suite steward holds access credentials)."
        ],
        "tags": ["Gate B", "Suite 4", "Level 3", "Route"]
    },
    "german vip drop-off": {
        "title": "🚗 German FA Guest Drop-off & Lounge 1 Path",
        "steps": [
            "Instruct driver to enter VIP Access Lane North-West (Gate Code: NW-DE-2026).",
            "Drop off guests at Gate B Lounge Entry. (Samantha Green is designated host).",
            "Check accreditation badges at VIP Reception Desk 1.",
            "Board VIP Elevator 2 (North Lobby) to Level 1.",
            "Turn left, proceed down VIP hallway past the Historical Trophy gallery.",
            "Lounge 1 is located directly at the end of the secure hallway."
        ],
        "tags": ["German", "Gate B", "Lounge 1", "Drop-off"]
    },
    "japanese vip translation": {
        "title": "🇯🇵 Tokyo FC / Japanese Guest Protocol",
        "steps": [
            "Meet Tokyo FC delegation at Gate A Transport Hub (Primary Lead: Mr. Tanaka).",
            "Ensure volunteer Kenji Sato is positioned at Gate A (bilingual liaison).",
            "Fast-track delegation through VIP Customs Clearance Box 4.",
            "Guide delegation to Executive Suite 4 via Level 3 North Corridor.",
            "Confirm Japanese translated stadium brochures and tablet maps are loaded in Suite 4."
        ],
        "tags": ["Tokyo FC", "Japanese", "Gate A", "Suite 4", "Translation"]
    },
    "emergency medical route": {
        "title": "🚨 Emergency Evacuation: VIP Area → Ambulance Bay",
        "steps": [
            "Contact Central Command (Sarah Connor) & Medical Dispatch immediately on Radio Channel 1.",
            "Clear VIP Service Elevator 3 using the Emergency Lock Key.",
            "Evacuate patient from Level 2/3 via secure Rear corridor 1B.",
            "Exit building structure at Ground Floor Gate 4 (Ambulance standby zone).",
            "Verify Security keeps path clear of VIP spectators and press."
        ],
        "tags": ["Emergency", "Medical", "Ambulance", "Gate 4"]
    },
    "arabic vip protocol": {
        "title": "🕌 Arabic Guest & Halal Dining Protocol",
        "steps": [
            "Verify with Catering Lead that VIP Lounge 1 Halal-certified menu is active.",
            "Ensure no alcoholic beverages are placed on the main table unless explicitly requested.",
            "Quiet room / Prayer Room is open on Level 2, Room 204 (labeled 'Quiet Room').",
            "Greet guests with traditional formal Arabic respect (hand on heart, head bow).",
            "If any special protocol questions arise, contact Team Lead Ahmed Al-Masri."
        ],
        "tags": ["Arabic", "Halal", "Lounge 1", "Prayer"]
    }
}

# ==============================================================================
# 4. MATCHDAY SIMULATION DATA
# ==============================================================================
VIP_SIMULATION_STEPS = {
    0: [
        {"name": "Spain Royal Escort", "affiliation": "Spanish Royal Family", "status": "Urgent Alert", "location_desc": "Approaching Gate C (Vehicle Delay)", "transit_mode": "Private Escort", "eta": "17:45", "language": "Spanish", "target": "Royal Box", "gate": "Gate C", "mandates": "Wheelchair access, high security", "x": 8.0, "y": 2.5, "zone": "Outside"},
        {"name": "German FA President", "affiliation": "DFB Delegation", "status": "Nominal", "location_desc": "En Route (Highway 1)", "transit_mode": "VIP Shuttle", "eta": "18:30", "language": "German", "target": "VIP Lounge 1", "gate": "Gate B", "mandates": "Halal catering request", "x": 5.0, "y": 1.2, "zone": "Outside"},
        {"name": "Tokyo FC Board", "affiliation": "Tokyo FC Board", "status": "Warning", "location_desc": "Clearing Customs (Language barrier)", "transit_mode": "Charter Bus", "eta": "18:15", "language": "Japanese", "target": "Executive Suite 4", "gate": "Gate A", "mandates": "Needs Japanese translator", "x": 1.8, "y": 3.0, "zone": "Outside"},
        {"name": "FIFA Executive VIPs", "affiliation": "FIFA Committee", "status": "Nominal", "location_desc": "Settled at VIP Lounge 2", "transit_mode": "Official Car", "eta": "16:45", "language": "French", "target": "VIP Lounge 2", "gate": "Gate B", "mandates": "Standard accreditations", "x": 7.7, "y": 7.1, "zone": "Inside"},
        {"name": "Ronaldo & Party", "affiliation": "Brazilian Legend", "status": "Nominal", "location_desc": "Settled at Royal Box", "transit_mode": "Helicopter", "eta": "16:15", "language": "Portuguese", "target": "Royal Box", "gate": "Helipad", "mandates": "Autograph area protection", "x": 5.0, "y": 7.85, "zone": "Inside"}
    ],
    1: [
        {"name": "Spain Royal Escort", "affiliation": "Spanish Royal Family", "status": "Urgent Alert", "location_desc": "At Gate C (Lobby Check-In)", "transit_mode": "Private Escort", "eta": "17:45", "language": "Spanish", "target": "Royal Box", "gate": "Gate C", "mandates": "Wheelchair access, high security", "x": 8.0, "y": 7.5, "zone": "Outside"},
        {"name": "German FA President", "affiliation": "DFB Delegation", "status": "Nominal", "location_desc": "Approaching Gate B Drop-off", "transit_mode": "VIP Shuttle", "eta": "18:25", "language": "German", "target": "VIP Lounge 1", "gate": "Gate B", "mandates": "Halal catering request", "x": 5.0, "y": 4.5, "zone": "Outside"},
        {"name": "Tokyo FC Board", "affiliation": "Tokyo FC Board", "status": "Warning", "location_desc": "Approaching Gate A Hub", "transit_mode": "Charter Bus", "eta": "18:15", "language": "Japanese", "target": "Executive Suite 4", "gate": "Gate A", "mandates": "Needs Japanese translator", "x": 2.0, "y": 6.0, "zone": "Outside"},
        {"name": "FIFA Executive VIPs", "affiliation": "FIFA Committee", "status": "Nominal", "location_desc": "Settled at VIP Lounge 2", "transit_mode": "Official Car", "eta": "16:45", "language": "French", "target": "VIP Lounge 2", "gate": "Gate B", "mandates": "Standard accreditations", "x": 7.7, "y": 7.1, "zone": "Inside"},
        {"name": "Ronaldo & Party", "affiliation": "Brazilian Legend", "status": "Nominal", "location_desc": "Settled at Royal Box", "transit_mode": "Helicopter", "eta": "16:15", "language": "Portuguese", "target": "Royal Box", "gate": "Helipad", "mandates": "Autograph area protection", "x": 5.0, "y": 7.85, "zone": "Inside"}
    ],
    2: [
        {"name": "Spain Royal Escort", "affiliation": "Spanish Royal Family", "status": "Nominal", "location_desc": "Escorted to Royal Box", "transit_mode": "Private Escort", "eta": "17:45", "language": "Spanish", "target": "Royal Box", "gate": "Gate C", "mandates": "Wheelchair access, high security", "x": 5.0, "y": 7.85, "zone": "Inside"},
        {"name": "German FA President", "affiliation": "DFB Delegation", "status": "Nominal", "location_desc": "At Gate B (Receiving Guest)", "transit_mode": "VIP Shuttle", "eta": "18:25", "language": "German", "target": "VIP Lounge 1", "gate": "Gate B", "mandates": "Halal catering request", "x": 5.0, "y": 7.5, "zone": "Outside"},
        {"name": "Tokyo FC Board", "affiliation": "Tokyo FC Board", "status": "Nominal", "location_desc": "At Gate A (Met by Translator)", "transit_mode": "Charter Bus", "eta": "18:15", "language": "Japanese", "target": "Executive Suite 4", "gate": "Gate A", "mandates": "Needs Japanese translator", "x": 2.0, "y": 7.5, "zone": "Outside"},
        {"name": "FIFA Executive VIPs", "affiliation": "FIFA Committee", "status": "Nominal", "location_desc": "Settled at VIP Lounge 2", "transit_mode": "Official Car", "eta": "16:45", "language": "French", "target": "VIP Lounge 2", "gate": "Gate B", "mandates": "Standard accreditations", "x": 7.7, "y": 7.1, "zone": "Inside"},
        {"name": "Ronaldo & Party", "affiliation": "Brazilian Legend", "status": "Nominal", "location_desc": "Settled at Royal Box", "transit_mode": "Helicopter", "eta": "16:15", "language": "Portuguese", "target": "Royal Box", "gate": "Helipad", "mandates": "Autograph area protection", "x": 5.0, "y": 7.85, "zone": "Inside"}
    ],
    3: [
        {"name": "Spain Royal Escort", "affiliation": "Spanish Royal Family", "status": "Nominal", "location_desc": "Settled at Royal Box", "transit_mode": "Private Escort", "eta": "17:45", "language": "Spanish", "target": "Royal Box", "gate": "Gate C", "mandates": "Wheelchair access, high security", "x": 5.0, "y": 7.85, "zone": "Inside"},
        {"name": "German FA President", "affiliation": "DFB Delegation", "status": "Nominal", "location_desc": "Settled at VIP Lounge 1", "transit_mode": "VIP Shuttle", "eta": "18:25", "language": "German", "target": "VIP Lounge 1", "gate": "Gate B", "mandates": "Halal catering request", "x": 2.3, "y": 7.1, "zone": "Inside"},
        {"name": "Tokyo FC Board", "affiliation": "Tokyo FC Board", "status": "Nominal", "location_desc": "Settled at Executive Suite 4", "transit_mode": "Charter Bus", "eta": "18:15", "language": "Japanese", "target": "Executive Suite 4", "gate": "Gate A", "mandates": "Needs Japanese translator", "x": 2.5, "y": 2.3, "zone": "Inside"},
        {"name": "FIFA Executive VIPs", "affiliation": "FIFA Committee", "status": "Nominal", "location_desc": "Settled at VIP Lounge 2", "transit_mode": "Official Car", "eta": "16:45", "language": "French", "target": "VIP Lounge 2", "gate": "Gate B", "mandates": "Standard accreditations", "x": 7.7, "y": 7.1, "zone": "Inside"},
        {"name": "Ronaldo & Party", "affiliation": "Brazilian Legend", "status": "Nominal", "location_desc": "Settled at Royal Box", "transit_mode": "Helicopter", "eta": "16:15", "language": "Portuguese", "target": "Royal Box", "gate": "Helipad", "mandates": "Autograph area protection", "x": 5.0, "y": 7.85, "zone": "Inside"}
    ]
}

TIMELINE_LABELS = {
    0: "17:00 — Pre-Match Guest Reception",
    1: "17:30 — Gates Open, Active Arrivals",
    2: "18:00 — Peak Guest Check-In Window",
    3: "18:30 — Kick-off Approaching"
}

# ==============================================================================
# 5. SHIFT SCHEDULE DATA (PER TIMELINE PHASE)
# ==============================================================================
SHIFT_SCHEDULE = [
    {"time": "15:00", "desc": "Report to your assigned zone and check in with your Team Lead", "phase_complete": 0},
    {"time": "15:30", "desc": "Collect your radio, lanyard badge, and venue map tablet", "phase_complete": 0},
    {"time": "16:00", "desc": "Attend the pre-match volunteer briefing at Command Center", "phase_complete": 0},
    {"time": "16:30", "desc": "Security sweep of VIP corridors — confirm all-clear", "phase_complete": 0},
    {"time": "17:00", "desc": "Gates open — stand by at your assigned entry point", "phase_complete": 1},
    {"time": "17:15", "desc": "First VIP guest arrivals expected — prepare welcome kits", "phase_complete": 1},
    {"time": "17:30", "desc": "Coordinate with Translation Liaisons for language-sensitive arrivals", "phase_complete": 1},
    {"time": "17:45", "desc": "Peak arrival window begins — all hands active", "phase_complete": 2},
    {"time": "18:00", "desc": "Confirm all priority guests are seated in their designated areas", "phase_complete": 2},
    {"time": "18:15", "desc": "Final corridor sweep — clear public areas for kick-off", "phase_complete": 3},
    {"time": "18:25", "desc": "Final security check complete — lock VIP access elevators", "phase_complete": 3},
    {"time": "18:30", "desc": "Kick-off! Transition to in-match standby mode", "phase_complete": 3},
]

# ==============================================================================
# 6. WAYFINDING COORDINATE MAP (FOR ROUTE DRAWING)
# ==============================================================================
LOCATION_COORDS_OUTSIDE = {
    "Gate A": (2.0, 7.5),
    "Gate B": (5.0, 7.5),
    "Gate C": (8.0, 7.5),
    "Transport Hub": (1.6, 2.4),
    "VIP Helipad": (8.0, 1.8),
    "VIP Drop-Off": (5.0, 5.0),
}
LOCATION_COORDS_INSIDE = {
    "VIP Lounge 1": (2.3, 7.1),
    "VIP Lounge 2": (7.7, 7.1),
    "Royal Box": (5.0, 7.85),
    "Executive Suites 1-5": (2.5, 2.3),
    "Executive Suites 6-10": (7.5, 2.3),
    "Pitch Centre": (5.0, 5.0),
}

# ==============================================================================
# 7. AVATAR SVG GENERATOR
# ==============================================================================
AVATAR_STYLES = {
    "Central Command Director": {"bg": "#071D49", "hair": "#A0C0D0", "uniform": "#0A66C2"},
    "Team Lead": {"bg": "#0E2333", "hair": "#FFAA00", "uniform": "#00FFCC"},
    "Liaison Officer": {"bg": "#2A1520", "hair": "#FF6B8A", "uniform": "#FF6B8A"},
    "Bilingual Escort": {"bg": "#0E2820", "hair": "#00FFCC", "uniform": "#2ECC71"},
    "Transit Coordinator": {"bg": "#2A1E0E", "hair": "#FFAA00", "uniform": "#FF8C00"},
    "Royal Box Host": {"bg": "#2A2215", "hair": "#FFD700", "uniform": "#FFD700"},
}

def make_avatar_svg(name, role):
    style = AVATAR_STYLES.get(role, {"bg": "#122030", "hair": "#A0C0D0", "uniform": "#0A66C2"})
    initials = "".join([w[0].upper() for w in name.split()[:2]])
    return f"""<svg width="44" height="44" viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg">
        <circle cx="22" cy="22" r="22" fill="{style['bg']}"/>
        <circle cx="22" cy="16" r="8" fill="{style['hair']}"/>
        <circle cx="22" cy="16" r="7" fill="#D4A574"/>
        <ellipse cx="22" cy="36" rx="13" ry="10" fill="{style['uniform']}"/>
        <text x="22" y="40" text-anchor="middle" fill="#FFFFFF" font-size="8" font-family="Outfit" font-weight="700">{initials}</text>
    </svg>"""

# ==============================================================================
# 8. INITIALIZE SESSION STATE
# ==============================================================================
if "app_init" not in st.session_state:
    st.session_state.onboarded = False
    st.session_state.volunteer_profile = {}
    st.session_state.timeline_phase = 0
    st.session_state.vips = VIP_SIMULATION_STEPS[0]
    st.session_state.directory = [
        {"name": "Sarah Connor", "role": "Central Command Director", "zone": "Command Center", "languages": "English, French", "status": "Active", "beep_count": 0, "id": "sarah"},
        {"name": "Ahmed Al-Masri", "role": "Team Lead", "zone": "VIP Lounges", "languages": "English, Arabic", "status": "Active", "beep_count": 0, "id": "ahmed"},
        {"name": "Maria Delgado", "role": "Liaison Officer", "zone": "Gate C VIP Reception", "languages": "Spanish, English", "status": "Active", "beep_count": 0, "id": "maria"},
        {"name": "Kenji Sato", "role": "Bilingual Escort", "zone": "Gate A Logistics", "languages": "Japanese, English", "status": "Active", "beep_count": 0, "id": "kenji"},
        {"name": "Jean-Pierre", "role": "Transit Coordinator", "zone": "Transport Hub", "languages": "French, English", "status": "Active", "beep_count": 0, "id": "jean"},
        {"name": "Samantha Green", "role": "Royal Box Host", "zone": "Royal Box Corridor", "languages": "English, German", "status": "Active", "beep_count": 0, "id": "samantha"}
    ]
    st.session_state.activity_feed = [
        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] System online — VIO Companion Hub is ready."
    ]
    st.session_state.chat_history = []
    st.session_state.selected_contingency = None
    st.session_state.show_vio_chat = False
    st.session_state.app_init = True

# ==============================================================================
# 9. HELPER FUNCTIONS
# ==============================================================================
def update_timeline():
    phase = st.session_state.timeline_phase
    st.session_state.vips = VIP_SIMULATION_STEPS[phase]
    t = datetime.datetime.now().strftime('%H:%M:%S')
    st.session_state.activity_feed.append(
        f"[{t}] Timeline updated to Phase {phase} — {TIMELINE_LABELS[phase]}"
    )

def advance_timeline():
    if st.session_state.timeline_phase < 3:
        st.session_state.timeline_phase += 1
        update_timeline()
    else:
        st.toast("You're at the final matchday phase.", icon="ℹ️")

def reset_timeline():
    st.session_state.timeline_phase = 0
    update_timeline()
    st.toast("Timeline reset to Phase 0.", icon="🔄")

def send_alert(person_id, name, zone):
    for p in st.session_state.directory:
        if p["id"] == person_id:
            p["beep_count"] += 1
            break
    t = datetime.datetime.now().strftime('%H:%M:%S')
    st.session_state.activity_feed.append(f"[{t}] Quick Alert sent to {name} (Zone: {zone})")
    st.toast(f"✅ Alert sent to {name}!", icon="📢")

# ==============================================================================
# 10. ONBOARDING GATE — COMPULSORY VOLUNTEER REGISTRATION
# ==============================================================================
if not st.session_state.onboarded:
    st.markdown("""
    <div style="text-align:center; margin-top: 2rem;">
        <h1 style="font-size: 2.5rem; margin-bottom: 0;">🏆 2026 FIFA World Cup</h1>
        <h2 style="color: #00FFCC; font-weight: 600; margin-top: 4px;">Volunteer Companion Hub</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='onboard-card'>", unsafe_allow_html=True)
    st.markdown("#### 🔐 Volunteer Credential Registration")
    st.markdown("Welcome! Please register your details below to access your personalised matchday dashboard.")
    st.write("")

    ob_name = st.text_input("Full Name", placeholder="e.g. Alex Johnson")
    ob_role = st.selectbox("Active Role", [
        "Guest Relations Specialist",
        "Logistics Lead",
        "VIP Escort Coordinator",
        "Accessibility Officer",
        "Translation Liaison"
    ])
    ob_langs = st.multiselect("Language Proficiency", [
        "English", "Spanish", "French", "German", "Japanese", "Arabic", "Portuguese"
    ], default=["English"])
    ob_zone = st.selectbox("Assigned Stadium Zone", [
        "Gate A", "Gate B", "Gate C",
        "VIP Lounges", "Royal Box Corridor",
        "Transport Hub", "Command Center"
    ])

    st.write("")
    if st.button("✅  Begin My Shift", type="primary", use_container_width=True):
        if ob_name.strip():
            st.session_state.volunteer_profile = {
                "full_name": ob_name.strip(),
                "active_role": ob_role,
                "language_proficiency": ", ".join(ob_langs),
                "assigned_zone": ob_zone
            }
            st.session_state.onboarded = True
            t = datetime.datetime.now().strftime('%H:%M:%S')
            st.session_state.activity_feed.append(
                f"[{t}] Volunteer {ob_name.strip()} ({ob_role}) checked in at zone: {ob_zone}"
            )
            st.rerun()
        else:
            st.warning("Please enter your full name to continue.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==============================================================================
# 11. MAIN DASHBOARD — WEATHER STRIP
# ==============================================================================
st.markdown("""
<div class="weather-strip">
    <div>⛅ <span class="temp">34°C</span> — Partly Cloudy | Humidity 62% | Wind 12 km/h NW</div>
    <div class="hydrate">💧 Stay Hydrated — Water stations at every gate</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 12. HERO BANNER + TOP-RIGHT PROFILE BADGE
# ==============================================================================
prof = st.session_state.volunteer_profile
initials = "".join([w[0].upper() for w in prof["full_name"].split()[:2]])

col_banner, col_profile = st.columns([4, 1])

with col_banner:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #071D49 0%, #0A3D7A 40%, #0A66C2 70%, #00FFCC 100%);
                padding: 1.6rem 2rem; border-radius: 14px; margin-bottom: 0.5rem;
                box-shadow: 0 6px 20px rgba(0,0,0,0.4); border-bottom: 3px solid #00FFCC;">
        <h1 style="color: #FFFFFF; margin: 0; font-size: 2.1rem; letter-spacing: 1.5px;
                   text-shadow: 0 2px 4px rgba(0,0,0,0.5);">🏆 2026 FIFA World Cup</h1>
        <h2 style="color: #00FFCC; margin: 4px 0 0 0; font-size: 1.2rem; font-weight: 600;
                   font-family: 'Outfit', sans-serif;">Volunteer Companion Hub</h2>
        <p style="color: #C0D8E8; margin: 6px 0 0 0; font-size: 0.85rem; opacity: 0.9;">
            Your personal matchday command center — track guest arrivals, coordinate with your team, and navigate the venue with confidence.</p>
    </div>
    """, unsafe_allow_html=True)

with col_profile:
    st.markdown(f"""
    <div class="profile-badge">
        <div class="avatar-circle">{initials}</div>
        <div>
            <div class="badge-name">{prof["full_name"]}</div>
            <div class="badge-role">{prof["active_role"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("📋 View My Profile"):
        st.markdown(f"**Role:** {prof['active_role']}")
        st.markdown(f"**Languages:** {prof['language_proficiency']}")
        st.markdown(f"**Zone:** {prof['assigned_zone']}")

# ==============================================================================
# 13. METRIC CARDS ROW
# ==============================================================================
total_vips = len(st.session_state.vips)
urgent_vips = len([v for v in st.session_state.vips if v["status"] == "Urgent Alert"])
total_alerts = sum(p["beep_count"] for p in st.session_state.directory)
phase_label = TIMELINE_LABELS[st.session_state.timeline_phase]

st.markdown(f"""
<div class="metric-container">
    <div class="metric-card">
        <div class="metric-title">Matchday Phase</div>
        <div class="metric-val" style="font-size:1.2rem;">{phase_label}</div>
        <div class="metric-desc">Phase {st.session_state.timeline_phase} of 3</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Expected Guests</div>
        <div class="metric-val">{total_vips}</div>
        <div class="metric-desc">Actively Monitored</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Urgent Arrivals</div>
        <div class="metric-val" style="color: {'#FF4B4B' if urgent_vips > 0 else '#00FFCC'}">{urgent_vips}</div>
        <div class="metric-desc {'urgent' if urgent_vips > 0 else ''}">{"Needs Attention" if urgent_vips > 0 else "All Clear"}</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Alerts Sent Today</div>
        <div class="metric-val">{total_alerts}</div>
        <div class="metric-desc">Team Members Pinged</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 14. SIDEBAR — MATCHDAY TIMELINE CONTROLS
# ==============================================================================
st.sidebar.markdown("<h2 style='color:#00FFCC; font-size:1.2rem;'>⏱️ Matchday Timeline</h2>", unsafe_allow_html=True)
st.sidebar.markdown(f"**Current Phase:** {st.session_state.timeline_phase} / 3")
st.sidebar.markdown(f"*{phase_label}*")
st.sidebar.write("")
st.sidebar.info("Advance the timeline to see guest movements update in real time on the venue map.")
sc1, sc2 = st.sidebar.columns(2)
with sc1:
    st.button("▶️ Advance", use_container_width=True, on_click=advance_timeline)
with sc2:
    st.button("🔄 Reset", use_container_width=True, on_click=reset_timeline)

# Sidebar urgent callout
urgent_list = [v for v in st.session_state.vips if v["status"] == "Urgent Alert"]
if urgent_list:
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"<div style='border:1px solid #FF4B4B; background:rgba(255,75,75,0.1); padding:10px; border-radius:6px; color:#FF4B4B; font-size:0.83rem;'>"
        f"🚨 <b>ATTENTION:</b> {urgent_list[0]['name']} — {urgent_list[0]['location_desc']}. Check <b>Expected Client Arrivals</b> for details."
        "</div>", unsafe_allow_html=True
    )

# ==============================================================================
# 15. CENTRAL TABS NAVIGATION (IGNITION AURA)
# ==============================================================================
tab_map, tab_arrivals, tab_team, tab_schedule = st.tabs([
    "📍 Venue Map & Wayfinding",
    "👥 Expected Client Arrivals",
    "📇 Team Directory & Alerts",
    "🗓️ Your Shift Schedule"
])

# ==============================================================================
# TAB 1: VENUE MAP & WAYFINDING
# ==============================================================================
with tab_map:
    st.subheader("📍 Venue Map & Wayfinding")
    st.markdown("Use this interactive map to locate guests, find your way around the venue, and plan the best walking routes between stations.")

    map_view = st.segmented_control(
        "Select venue zone:",
        options=["Outside — Gates & Transport", "Inside — Suites & Lounges"],
        default="Outside — Gates & Transport"
    )

    # Route selector dropdowns
    rc1, rc2 = st.columns(2)
    is_outside = map_view == "Outside — Gates & Transport"
    loc_options = list(LOCATION_COORDS_OUTSIDE.keys()) if is_outside else list(LOCATION_COORDS_INSIDE.keys())
    with rc1:
        route_from = st.selectbox("📍 My Current Station", ["— Select —"] + loc_options, key="route_from")
    with rc2:
        route_to = st.selectbox("🎯 Client Destination", ["— Select —"] + loc_options, key="route_to")

    fig = go.Figure()
    coord_map = LOCATION_COORDS_OUTSIDE if is_outside else LOCATION_COORDS_INSIDE

    if is_outside:
        # Gates
        for gx, label in [(2.0, "Gate A"), (5.0, "Gate B"), (8.0, "Gate C")]:
            fig.add_shape(type="rect", x0=gx-0.5, y0=7.2, x1=gx+0.5, y1=7.8, fillcolor="#122030", line=dict(color="#1E3A52", width=2))
            fig.add_annotation(x=gx, y=7.5, text=label, showarrow=False, font=dict(color="#FFFFFF", size=11, family="Outfit"))
        # Transport Hub
        fig.add_shape(type="rect", x0=1.0, y0=2.0, x1=2.2, y1=2.8, fillcolor="#050E17", line=dict(color="#1E3A52", width=1))
        fig.add_annotation(x=1.6, y=2.4, text="Transport Hub", showarrow=False, font=dict(color="#BEC2CA", size=9, family="Outfit"))
        # Helipad
        fig.add_shape(type="circle", x0=7.6, y0=1.4, x1=8.4, y1=2.2, fillcolor="#050E17", line=dict(color="#FF4B4B", width=2))
        fig.add_annotation(x=8.0, y=1.8, text="VIP Helipad", showarrow=False, font=dict(color="#FF4B4B", size=9, family="Outfit"))
        # Drop-Off
        fig.add_shape(type="circle", x0=4.6, y0=4.6, x1=5.4, y1=5.4, fillcolor="#0E2333", line=dict(color="#00FFCC", width=1.5))
        fig.add_annotation(x=5.0, y=5.0, text="VIP Drop-Off", showarrow=False, font=dict(color="#00FFCC", size=10, family="Outfit"))
        # Footpaths (dashed)
        for xs, ys in [([2.0,2.0],[5.0,7.2]), ([5.0,5.0],[5.0,7.2]), ([8.0,8.0],[5.0,7.2]), ([1.6,1.6,5.0,8.0,8.0],[2.8,5.0,5.0,5.0,2.2])]:
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="#1E3A52", width=4, dash="dash"), hoverinfo="skip", showlegend=False))
        # VIP markers
        vips_zone = [v for v in st.session_state.vips if v["zone"] == "Outside"]
    else:
        # Pitch
        fig.add_shape(type="rect", x0=3.2, y0=3.2, x1=6.8, y1=6.8, fillcolor="#103c2f", line=dict(color="#00FFCC", width=1.5))
        fig.add_shape(type="circle", x0=4.5, y0=4.5, x1=5.5, y1=5.5, line=dict(color="#FFFFFF", width=1))
        fig.add_shape(type="line", x0=5.0, y0=3.2, x1=5.0, y1=6.8, line=dict(color="#FFFFFF", width=1))
        fig.add_annotation(x=5.0, y=5.0, text="PITCH", showarrow=False, font=dict(color="#FFFFFF", size=14, family="Space Grotesk"))
        # Royal Box
        fig.add_shape(type="rect", x0=4.3, y0=7.5, x1=5.7, y1=8.2, fillcolor="#2A2215", line=dict(color="#FFAA00", width=2))
        fig.add_annotation(x=5.0, y=7.85, text="👑 Royal Box", showarrow=False, font=dict(color="#FFAA00", size=11, family="Outfit"))
        # VIP Lounges
        fig.add_shape(type="rect", x0=1.8, y0=6.8, x1=2.8, y1=7.4, fillcolor="#0F2030", line=dict(color="#1E3A52", width=2))
        fig.add_annotation(x=2.3, y=7.1, text="Lounge 1", showarrow=False, font=dict(color="#FFFFFF", size=10, family="Outfit"))
        fig.add_shape(type="rect", x0=7.2, y0=6.8, x1=8.2, y1=7.4, fillcolor="#0F2030", line=dict(color="#1E3A52", width=2))
        fig.add_annotation(x=7.7, y=7.1, text="Lounge 2", showarrow=False, font=dict(color="#FFFFFF", size=10, family="Outfit"))
        # Exec Suites
        fig.add_shape(type="rect", x0=1.5, y0=2.0, x1=3.5, y1=2.6, fillcolor="#122030", line=dict(color="#1E3A52", width=1))
        fig.add_annotation(x=2.5, y=2.3, text="Suites 1-5", showarrow=False, font=dict(color="#BEC2CA", size=9, family="Outfit"))
        fig.add_shape(type="rect", x0=6.5, y0=2.0, x1=8.5, y1=2.6, fillcolor="#122030", line=dict(color="#1E3A52", width=1))
        fig.add_annotation(x=7.5, y=2.3, text="Suites 6-10", showarrow=False, font=dict(color="#BEC2CA", size=9, family="Outfit"))
        vips_zone = [v for v in st.session_state.vips if v["zone"] == "Inside"]

    # Draw VIP markers
    if vips_zone:
        colors = []
        for v in vips_zone:
            if v["status"] == "Urgent Alert": colors.append("#FF4B4B")
            elif v["status"] == "Warning": colors.append("#FFAA00")
            else: colors.append("#00FFCC")
        fig.add_trace(go.Scatter(
            x=[v["x"] for v in vips_zone], y=[v["y"] for v in vips_zone],
            mode="markers+text",
            marker=dict(size=20, color=colors, line=dict(color="#FFFFFF", width=2), symbol="circle"),
            text=[v["name"] for v in vips_zone], textposition="top center",
            textfont=dict(color="#FFFFFF", size=11, family="Outfit"),
            hovertemplate="<b>%{text}</b><br>Status: %{customdata[0]}<br>Location: %{customdata[1]}<br>Destination: %{customdata[2]}<extra></extra>",
            customdata=[[v["status"], v["location_desc"], v["target"]] for v in vips_zone],
            showlegend=False
        ))

    # Draw route line if both locations are selected
    if route_from != "— Select —" and route_to != "— Select —" and route_from != route_to:
        if route_from in coord_map and route_to in coord_map:
            fx, fy = coord_map[route_from]
            tx, ty = coord_map[route_to]
            mid_x = (fx + tx) / 2
            mid_y = (fy + ty) / 2 + 0.5
            fig.add_trace(go.Scatter(
                x=[fx, mid_x, tx], y=[fy, mid_y, ty], mode="lines+markers",
                line=dict(color="#0A66C2", width=4), marker=dict(size=12, color="#0A66C2", symbol=["circle", "diamond", "star"]),
                hoverinfo="skip", showlegend=False
            ))
            fig.add_annotation(x=mid_x, y=mid_y+0.3, text="Suggested Route", showarrow=False,
                font=dict(color="#0A66C2", size=10, family="Outfit"))

    fig.update_layout(
        xaxis=dict(range=[0, 10], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[0, 10], showgrid=False, zeroline=False, visible=False),
        plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
        margin=dict(l=0, r=0, t=10, b=0), showlegend=False, height=500, dragmode=False
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    lc1, lc2, lc3 = st.columns(3)
    with lc1: st.markdown("<span class='badge badge-urgent'>● Urgent</span> — Delays or blockages", unsafe_allow_html=True)
    with lc2: st.markdown("<span class='badge badge-warning'>● Delayed</span> — Customs or language issues", unsafe_allow_html=True)
    with lc3: st.markdown("<span class='badge badge-nominal'>● On Track</span> — Arrived or on schedule", unsafe_allow_html=True)

# ==============================================================================
# TAB 2: EXPECTED CLIENT ARRIVALS
# ==============================================================================
with tab_arrivals:
    st.subheader("👥 Expected Client Arrivals")
    st.markdown("Monitor all incoming VIP guests. Use the filters to focus on specific urgency levels, languages, or travel modes.")

    fc1, fc2, fc3 = st.columns(3)
    with fc1: f_status = st.selectbox("Filter by Status:", ["All", "Urgent Alert", "Warning", "Nominal"])
    with fc2: f_lang = st.selectbox("Filter by Language:", ["All", "Spanish", "German", "Japanese", "French", "Portuguese"])
    with fc3: f_mode = st.selectbox("Filter by Travel Mode:", ["All", "Private Escort", "VIP Shuttle", "Charter Bus", "Official Car", "Helicopter"])

    filtered = st.session_state.vips
    if f_status != "All": filtered = [v for v in filtered if v["status"] == f_status]
    if f_lang != "All": filtered = [v for v in filtered if v["language"] == f_lang]
    if f_mode != "All": filtered = [v for v in filtered if v["transit_mode"] == f_mode]

    if not filtered:
        st.info("No guest arrivals match your filters.")
    else:
        for idx, vip in enumerate(filtered):
            border_color = "#FF4B4B" if vip["status"] == "Urgent Alert" else "#FFAA00" if vip["status"] == "Warning" else "#00FFCC"
            status_class = "badge-urgent" if vip["status"] == "Urgent Alert" else "badge-warning" if vip["status"] == "Warning" else "badge-nominal"
            st.markdown(f"""
            <div style='background:#122030; border-radius:10px; border-left:6px solid {border_color};
                        padding:1.2rem; margin-bottom:0.8rem; border:1px solid #1E3A52; border-left:6px solid {border_color};'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <h4 style='margin:0; font-size:1.15rem;'>{vip["name"]} <span style='font-size:0.88rem; color:#BEC2CA;'>({vip["affiliation"]})</span></h4>
                    <span class="badge {status_class}">{vip["status"]}</span>
                </div>
                <div style='display:flex; flex-wrap:wrap; gap:1.2rem; margin-top:0.65rem; font-size:0.88rem; color:#BEC2CA;'>
                    <div>📍 <b>Location:</b> {vip["location_desc"]}</div>
                    <div>🚗 <b>Travel:</b> {vip["transit_mode"]}</div>
                    <div>⏰ <b>ETA:</b> {vip["eta"]}</div>
                    <div>🗣️ <b>Language:</b> {vip["language"]}</div>
                    <div>🎯 <b>Destination:</b> {vip["target"]}</div>
                    <div>📋 <b>Notes:</b> {vip["mandates"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            bc1, bc2 = st.columns([1, 5])
            with bc1:
                if st.button("📋 View Arrival Checklist", key=f"checklist_{idx}_{vip['name']}"):
                    st.session_state.selected_contingency = vip

    if st.session_state.selected_contingency:
        v = st.session_state.selected_contingency
        st.markdown("---")
        st.markdown(f"""
        <div style='border:1px solid #0A66C2; border-radius:10px; padding:1.3rem; background:#0F1E35;'>
            <h4 style='color:#0A66C2; margin-top:0;'>📋 Guest Arrival Action Plan: {v['name']}</h4>
            <p style='font-size:0.9rem;'><b>Current situation:</b> {v['location_desc']} | <b>Destination:</b> {v['target']} | <b>Language:</b> {v['language']}</p>
        </div>
        """, unsafe_allow_html=True)

        matched_key = None
        if "spanish" in v["language"].lower() or "wheelchair" in v["mandates"].lower():
            matched_key = "spanish vip wheelchair access path"
        elif "tokyo" in v["affiliation"].lower() or "japanese" in v["language"].lower():
            matched_key = "japanese vip translation"
        elif "german" in v["language"].lower():
            matched_key = "german vip drop-off"
        elif "arabic" in v["language"].lower() or "halal" in v["mandates"].lower():
            matched_key = "arabic vip protocol"

        if matched_key and matched_key in VIO_KNOWLEDGE:
            k = VIO_KNOWLEDGE[matched_key]
            st.markdown(f"##### {k['title']}")
            for i, step in enumerate(k["steps"], 1):
                st.markdown(f"**Step {i}:** {step}")
            suggested = None
            for s in st.session_state.directory:
                if v["language"] in s["languages"]:
                    suggested = s
                    break
            if suggested:
                st.info(f"💡 **Suggested contact:** Send a Quick Alert to **{suggested['name']}** ({suggested['role']}) in the Team Directory tab.")
        else:
            st.markdown("**Standard Reception Protocol:**")
            st.markdown(f"1. Station a coordinator at {v['gate']} to receive this guest.")
            st.markdown(f"2. Escort them through the nearest VIP corridor to **{v['target']}**.")
            st.markdown("3. Confirm dietary or accessibility requirements with Catering/Facilities.")

        if st.button("✅ Close Action Plan"):
            st.session_state.selected_contingency = None
            st.rerun()

# ==============================================================================
# TAB 3: TEAM DIRECTORY & ALERTS
# ==============================================================================
with tab_team:
    st.subheader("📇 Team Directory & Quick Alerts")
    st.markdown("Find and contact your fellow volunteers instantly. Sending a **Quick Alert** silently pages their handheld device — no radio needed.")

    search = st.text_input("🔍 Search by name, role, zone, or language:", "")
    filtered_dir = st.session_state.directory
    if search:
        q = search.lower()
        filtered_dir = [p for p in filtered_dir if q in p["name"].lower() or q in p["role"].lower() or q in p["zone"].lower() or q in p["languages"].lower()]

    if not filtered_dir:
        st.warning("No team members found matching your search.")
    else:
        grid = st.columns(2)
        for idx, person in enumerate(filtered_dir):
            with grid[idx % 2]:
                avatar_svg = make_avatar_svg(person["name"], person["role"])
                st.markdown(f"""
                <div class="profile-card">
                    <div class="profile-header">
                        {avatar_svg}
                        <div style="flex:1;">
                            <span class="profile-name">{person["name"]}</span><br/>
                            <span class="profile-role-badge">{person["role"]}</span>
                        </div>
                    </div>
                    <div class="profile-info"><span class="profile-label">📍 Zone:</span> {person["zone"]}</div>
                    <div class="profile-info"><span class="profile-label">🗣️ Languages:</span> {person["languages"]}</div>
                    <div class="profile-info"><span class="profile-label">📶 Status:</span> <span style="color:#00FFCC;">● Active</span></div>
                    <div class="profile-info"><span class="profile-label">📨 Alerts Sent:</span> <b>{person["beep_count"]}</b></div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"📨 Send Quick Alert: {person['name']}", key=f"alert_{person['id']}_{idx}", use_container_width=True):
                    send_alert(person["id"], person["name"], person["zone"])
                    st.rerun()

# ==============================================================================
# TAB 4: YOUR SHIFT SCHEDULE
# ==============================================================================
with tab_schedule:
    st.subheader("🗓️ Your Shift Schedule")
    st.markdown("A chronological overview of your matchday responsibilities. Milestones update automatically as the timeline advances.")

    current_phase = st.session_state.timeline_phase
    for item in SHIFT_SCHEDULE:
        if item["phase_complete"] < current_phase:
            css_class = "completed"
            status_label = "✓ Done"
            status_css = "done"
        elif item["phase_complete"] == current_phase:
            css_class = "current"
            status_label = "● Active Now"
            status_css = "active"
        else:
            css_class = "upcoming"
            status_label = "○ Upcoming"
            status_css = "pending"

        st.markdown(f"""
        <div class="schedule-item {css_class}">
            <div class="schedule-time">{item["time"]}</div>
            <div>
                <div class="schedule-desc">{item["desc"]}</div>
                <div class="schedule-status {status_css}">{status_label}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 16. LIVE ACTIVITY TIMELINE (BELOW TABS)
# ==============================================================================
st.markdown("---")
act_col1, act_col2 = st.columns([3, 1])
with act_col1:
    st.markdown("<h3 style='font-size:1.1rem; margin-bottom:0.5rem;'>📋 Live Activity Timeline</h3>", unsafe_allow_html=True)
    feed_html = "".join(f"<div class='feed-entry'>{e}</div>" for e in reversed(st.session_state.activity_feed))
    st.markdown(f'<div class="activity-feed">{feed_html}</div>', unsafe_allow_html=True)
with act_col2:
    st.markdown("<h3 style='font-size:1.1rem; margin-bottom:0.5rem;'>🛠️ Quick Actions</h3>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Activity Log", use_container_width=True):
        st.session_state.activity_feed = [f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Activity log cleared."]
        st.rerun()
    st.markdown(
        "<div style='background:#122030; border-radius:8px; padding:0.8rem; border:1px solid #1E3A52; font-size:0.82rem; color:#BEC2CA; margin-top:0.5rem;'>"
        "<b>💡 Tip:</b> Use <b>Quick Alerts</b> to silently page teammates when radio channels are busy."
        "</div>", unsafe_allow_html=True
    )

# ==============================================================================
# 17. FLOATING VIO AI BOT — TAP TO OPEN CHAT PANEL
# ==============================================================================

# Show the floating bot bubble only when chat is closed
if not st.session_state.show_vio_chat:
    st.markdown("""
    <div class="vio-speech-bubble">🤖 Need help with directions or guest protocols?</div>
    <div class="vio-float-btn">🤖</div>
    """, unsafe_allow_html=True)
    st.write("")
    _vio_spacer, _vio_btn_col = st.columns([5, 1])
    with _vio_btn_col:
        if st.button("🤖 Ask VIO", use_container_width=True, key="vio_open_btn"):
            st.session_state.show_vio_chat = True
            st.rerun()

# When chat is open, render a compact right-aligned chat panel
if st.session_state.show_vio_chat:
    st.markdown("---")
    _chat_spacer, _chat_panel = st.columns([2, 3])
    with _chat_panel:
        # Chat panel header
        st.markdown("""
        <div style='background:linear-gradient(135deg, #0A66C2, #00FFCC); padding:0.9rem 1.2rem;
                    border-radius:12px 12px 0 0; display:flex; align-items:center; gap:0.7rem;'>
            <span style='font-size:1.6rem;'>🤖</span>
            <div>
                <div style='font-size:1.05rem; font-weight:700; color:#FFFFFF;'>VIO Assistant</div>
                <div style='font-size:0.75rem; color:rgba(255,255,255,0.8);'>Your matchday routing & protocol guide</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Chat body container
        st.markdown("""
        <div style='background:#0A1020; border:1px solid #1E3A52; border-top:none;
                    border-radius:0 0 12px 12px; padding:1rem;'>
        """, unsafe_allow_html=True)

        st.markdown("**💬 Suggested Questions:**")
        vq1, vq2 = st.columns(2)
        with vq1:
            if st.button("♿ Spanish Wheelchair Route", use_container_width=True, key="vio_q1"):
                st.session_state.chat_history.append(("Spanish VIP wheelchair access path", VIO_KNOWLEDGE["spanish vip wheelchair access path"]))
                st.rerun()
            if st.button("🚗 German FA Drop-off", use_container_width=True, key="vio_q2"):
                st.session_state.chat_history.append(("German VIP drop-off", VIO_KNOWLEDGE["german vip drop-off"]))
                st.rerun()
            if st.button("🚨 Emergency Medical", use_container_width=True, key="vio_q5"):
                st.session_state.chat_history.append(("Emergency medical route", VIO_KNOWLEDGE["emergency medical route"]))
                st.rerun()
        with vq2:
            if st.button("⚡ Gate B → Suite 4", use_container_width=True, key="vio_q3"):
                st.session_state.chat_history.append(("Fastest route from Gate B to Executive Box 4", VIO_KNOWLEDGE["fastest route from gate b to executive box 4"]))
                st.rerun()
            if st.button("🇯🇵 Tokyo FC Protocol", use_container_width=True, key="vio_q4"):
                st.session_state.chat_history.append(("Japanese VIP translation", VIO_KNOWLEDGE["japanese vip translation"]))
                st.rerun()
            if st.button("🕌 Arabic / Halal Protocol", use_container_width=True, key="vio_q6"):
                st.session_state.chat_history.append(("Arabic VIP protocol", VIO_KNOWLEDGE["arabic vip protocol"]))
                st.rerun()

        st.write("")
        user_q = st.text_input("Type your question here...", key="vio_input", placeholder="e.g. 'How do I get to Executive Box 4?'")
        aq1, aq2 = st.columns([3, 1])
        with aq1:
            send_pressed = st.button("Send ➤", type="primary", use_container_width=True, key="vio_send")
        with aq2:
            if st.button("✕ Close", use_container_width=True, key="vio_close_btn"):
                st.session_state.show_vio_chat = False
                st.rerun()

        if send_pressed and user_q:
            q_clean = user_q.lower()
            matched = None
            for key in VIO_KNOWLEDGE:
                kws = key.split()
                if key in q_clean or sum(1 for kw in kws if kw in q_clean) >= 2:
                    matched = key
                    break
            if not matched:
                if "spanish" in q_clean or "wheelchair" in q_clean: matched = "spanish vip wheelchair access path"
                elif "gate b" in q_clean or "box 4" in q_clean or "suite 4" in q_clean: matched = "fastest route from gate b to executive box 4"
                elif "german" in q_clean: matched = "german vip drop-off"
                elif "japanese" in q_clean or "tokyo" in q_clean: matched = "japanese vip translation"
                elif "emergency" in q_clean or "medical" in q_clean: matched = "emergency medical route"
                elif "arabic" in q_clean or "halal" in q_clean: matched = "arabic vip protocol"
            if matched:
                st.session_state.chat_history.append((user_q, VIO_KNOWLEDGE[matched]))
            else:
                st.session_state.chat_history.append((user_q, {
                    "title": "🔍 No Matching Guide Found",
                    "steps": [
                        "Your query didn't match any pre-loaded guides.",
                        "Try keywords like: 'Spanish wheelchair', 'Gate B Suite 4', 'German drop-off', 'Japanese translator', 'emergency medical', 'Arabic halal'.",
                        "Or contact your Team Lead for live assistance."
                    ]
                }))
            st.rerun()

        # Chat history display
        if st.session_state.chat_history:
            st.markdown("---")
            # Show the latest 4 conversations to keep the panel compact
            for query, reply in list(reversed(st.session_state.chat_history))[:4]:
                bc = "#FF4B4B" if "No Matching" in reply["title"] else "#00FFCC"
                st.markdown(f"**You:** *\"{query}\"*")
                st.markdown(f"""
                <div style='background:#08121E; border-left:4px solid {bc}; padding:0.8rem; border-radius:0 8px 8px 0; margin-bottom:0.8rem;'>
                    <div style='margin-top:0; color:#FFFFFF; font-size:0.92rem; font-weight:600;'>{reply["title"]}</div>
                    <ol style='margin-bottom:0; padding-left:1.1rem; color:#BEC2CA; font-size:0.82rem;'>
                        {"".join(f"<li style='margin-bottom:0.2rem;'>{s}</li>" for s in reply["steps"])}
                    </ol>
                </div>
                """, unsafe_allow_html=True)
            if st.button("🗑️ Clear Chat", key="vio_clear", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
