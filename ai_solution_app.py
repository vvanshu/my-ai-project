import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime
import re

# ==============================================================================
# 1. PAGE CONFIGURATION & THEME STYLING
# ==============================================================================
st.set_page_config(
    page_title="VIO // Volunteer Intelligent Operator Support",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for high-fidelity FIFA-themed dark UI with deep blue & teal accents
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;600;700&family=Fira+Code:wght@400;600&display=swap');

/* Main container and background override */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #0E1117 !important;
    color: #FFFFFF !important;
    font-family: 'Outfit', sans-serif !important;
}

/* Sidebar Styling - FIFA Dark Blue */
[data-testid="stSidebar"] {
    background-color: #08121E !important;
    border-right: 1px solid #1A2E40 !important;
}

/* Typography styles */
h1, h2, h3, .stHeader {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700;
}

/* Dashboard Metric Cards - Deep Teal/Blue Theme */
.metric-container {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.metric-card {
    flex: 1;
    background-color: #122030;
    border: 1px solid #1E3A52;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
    transition: all 0.3s ease;
}
.metric-card:hover {
    border-color: #00FFCC;
    transform: translateY(-2px);
}
.metric-title {
    font-size: 0.8rem;
    color: #A0C0D0;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.metric-val {
    font-size: 1.8rem;
    color: #FFFFFF;
    font-weight: 700;
    margin: 0.4rem 0;
    font-family: 'Space Grotesk', sans-serif;
}
.metric-desc {
    font-size: 0.75rem;
    color: #00FFCC;
    font-weight: 500;
}
.metric-desc.urgent {
    color: #FF4B4B;
}

/* Operational Registry Grid Cards - Deep Blue with Teal Top Border */
.profile-card {
    background-color: #122030;
    border: 1px solid #1E3A52;
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    border-top: 4px solid #00FFCC;
    transition: transform 0.2s ease;
}
.profile-card:hover {
    transform: scale(1.01);
}
.profile-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
}
.profile-name {
    font-size: 1.15rem;
    font-weight: 600;
    color: #FFFFFF;
}
.profile-role {
    font-size: 0.7rem;
    font-weight: 600;
    background-color: #0F4C81;
    color: #FFFFFF;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    text-transform: uppercase;
}
.profile-info {
    font-size: 0.85rem;
    color: #BEC2CA;
    margin-bottom: 0.4rem;
}
.profile-label {
    font-weight: 500;
    color: #8E929A;
}

/* Custom Status Badges */
.badge {
    display: inline-block;
    padding: 0.25rem 0.6rem;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 6px;
    text-transform: uppercase;
}
.badge-urgent {
    background-color: rgba(255, 75, 75, 0.15);
    color: #FF4B4B;
    border: 1px solid #FF4B4B;
}
.badge-warning {
    background-color: rgba(255, 170, 0, 0.15);
    color: #FFAA00;
    border: 1px solid #FFAA00;
}
.badge-nominal {
    background-color: rgba(0, 255, 204, 0.15);
    color: #00FFCC;
    border: 1px solid #00FFCC;
}

/* Beacon Terminal Feed */
.beacon-terminal {
    background-color: #050E17;
    border: 1px solid #1E3A52;
    border-radius: 8px;
    padding: 1rem;
    font-family: 'Fira Code', monospace;
    font-size: 0.8rem;
    height: 250px;
    overflow-y: auto;
    color: #00FFCC;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.8);
}
.terminal-log {
    margin-bottom: 0.4rem;
    line-height: 1.3;
}

/* Chat Assist Styling */
.chat-container {
    background-color: #122030;
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid #1E3A52;
}
.assistant-reply {
    background-color: #08121E;
    border-left: 4px solid #00FFCC;
    padding: 1rem;
    border-radius: 0 8px 8px 0;
    margin-top: 1rem;
}
.suggested-query-btn {
    text-align: left !important;
}

/* Custom CSS Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-track {
    background: #0E1117;
}
::-webkit-scrollbar-thumb {
    background: #122030;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #00FFCC;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==============================================================================
# 2. LOGISTICAL REFERENCE SYSTEM (VIO AI KNOWLEDGE BASE)
# ==============================================================================
VIO_KNOWLEDGE = {
    "spanish vip wheelchair access path": {
        "title": "♿ Spanish VIP Wheelchair Route (Gate C ➡️ Royal Box)",
        "steps": [
            "Verify that Gate C ramp access is completely clear of media gear.",
            "Greet VIP party at Gate C Lobby (Volunteer Maria Delgado is fluent in Spanish).",
            "Guide through VIP Security Lane 3 (wider clearance for wheelchair passage).",
            "Proceed directly to VIP Elevator West. Secure access to Level 2.",
            "Exit elevator, turn left into VIP Secured Corridor (do not enter the public concourse).",
            "Proceed up the East VIP Corridor Ramp directly into the Royal Box."
        ],
        "tags": ["Spain", "Wheelchair", "Gate C", "Royal Box"]
    },
    "fastest route from gate b to executive box 4": {
        "title": "⚡ Fastest Route: Gate B ➡️ Executive Box 4",
        "steps": [
            "Receive guests at Gate B Ground Reception.",
            "Fast-track through VIP Security Lane 2.",
            "Take VIP Escalator 'Bravo' (east side of lobby) straight to Level 3.",
            "Turn right at Level 3 corridor, walk past the VIP Lounge 1 entry.",
            "Continue down the executive suite corridor for 50 meters.",
            "Executive Box 4 is located on the left side (Suite steward holds access credentials)."
        ],
        "tags": ["Gate B", "Suite 4", "Level 3", "Route"]
    },
    "german vip drop-off": {
        "title": "🚗 German FA VIP Drop-off & Lounge 1 Path",
        "steps": [
            "Instruct driver to enter VIP Access Lane North-West (Gate Code: NW-DE-2026).",
            "Drop off VIP guests at Gate B Lounge Entry. (Samantha Green is designated host).",
            "Check accreditation badges at VIP Reception Desk 1.",
            "Board VIP Elevator 2 (North Lobby) to Level 1.",
            "Turn left, proceed down VIP hallway past the Historical Trophy gallery.",
            "Lounge 1 is located directly at the end of the secure hallway."
        ],
        "tags": ["German", "Gate B", "Lounge 1", "Drop-off"]
    },
    "japanese vip translation": {
        "title": "🇯🇵 Tokyo FC / Japanese VIP Protocol",
        "steps": [
            "Meet Tokyo FC delegation at Gate A Transport Hub (Primary Lead: Mr. Tanaka).",
            "Ensure volunteer Kenji Sato is positioned at Gate A (Bilingual liaison).",
            "Fast-track delegation through VIP Customs Clearance Box 4.",
            "Guide delegation to Executive Suite 4 via Level 3 North Corridor.",
            "Confirm Japanese translated stadium brochures and tablet maps are loaded in Suite 4."
        ],
        "tags": ["Tokyo FC", "Japanese", "Gate A", "Suite 4", "Translation"]
    },
    "emergency medical route": {
        "title": "🚨 Emergency Evacuation: VIP Area ➡️ Ambulance Bay",
        "steps": [
            "Contact Central Command (Sarah Connor) & Medical Dispatch immediately on Radio Channel 1.",
            "Clear VIP Service Elevator 3 using the Emergency Lock Key.",
            "Evacuate patient from Level 2/3 via secure Rear corridor 1B.",
            "Exit building structure at Ground Floor Gate 4 (Ambulance standby zone).",
            "Verify Security details keep path clear of VIP spectators and press."
        ],
        "tags": ["Emergency", "Medical", "Ambulance", "Gate 4"]
    },
    "arabic vip protocol": {
        "title": "🕌 Arabic VIP & Halal Dining Protocol",
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
# 3. MATCHDAY SIMULATION STATE VARIABLES
# ==============================================================================
VIP_SIMULATION_STEPS = {
    0: [
        {"name": "Spain Royal Escort", "affiliation": "Spanish Royal Family", "status": "Urgent Alert", "location_desc": "Approaching Gate C (Vehicle Delay)", "transit_mode": "Private Escort", "eta": "17:45", "language": "Spanish", "target": "Royal Box", "gate": "Gate C", "mandates": "Wheelchair access, high security", "x": 8.0, "y": 2.5, "zone": "Outside"},
        {"name": "German FA President", "affiliation": "DFB Delegation", "status": "Nominal", "location_desc": "En Route (On Highway 1)", "transit_mode": "VIP Shuttle", "eta": "18:30", "language": "German", "target": "VIP Lounge 1", "gate": "Gate B", "mandates": "Halal catering request", "x": 5.0, "y": 1.2, "zone": "Outside"},
        {"name": "Tokyo FC Board", "affiliation": "Tokyo FC Board", "status": "Warning", "location_desc": "At Customs Hub (Language barrier)", "transit_mode": "Charter Bus", "eta": "18:15", "language": "Japanese", "target": "Executive Suite 4", "gate": "Gate A", "mandates": "Needs Japanese translator", "x": 1.8, "y": 3.0, "zone": "Outside"},
        {"name": "FIFA Executive VIPs", "affiliation": "FIFA Comm.", "status": "Nominal", "location_desc": "Arrived at VIP Lounge 2", "transit_mode": "Official Car", "eta": "16:45", "language": "French", "target": "VIP Lounge 2", "gate": "Gate B", "mandates": "Standard accreditations", "x": 7.0, "y": 7.0, "zone": "Inside"},
        {"name": "Ronaldo & Party", "affiliation": "Brazilian Legend", "status": "Nominal", "location_desc": "Arrived at Royal Box", "transit_mode": "Helicopter", "eta": "16:15", "language": "Portuguese", "target": "Royal Box", "gate": "Helipad", "mandates": "Autograph area protection", "x": 5.0, "y": 8.0, "zone": "Inside"}
    ],
    1: [
        {"name": "Spain Royal Escort", "affiliation": "Spanish Royal Family", "status": "Urgent Alert", "location_desc": "At Gate C (Lobby Arrival)", "transit_mode": "Private Escort", "eta": "17:45", "language": "Spanish", "target": "Royal Box", "gate": "Gate C", "mandates": "Wheelchair access, high security", "x": 8.0, "y": 7.5, "zone": "Outside"},
        {"name": "German FA President", "affiliation": "DFB Delegation", "status": "Nominal", "location_desc": "Approaching Gate B Drop-off", "transit_mode": "VIP Shuttle", "eta": "18:25", "language": "German", "target": "VIP Lounge 1", "gate": "Gate B", "mandates": "Halal catering request", "x": 5.0, "y": 4.5, "zone": "Outside"},
        {"name": "Tokyo FC Board", "affiliation": "Tokyo FC Board", "status": "Warning", "location_desc": "Approaching Gate A Hub", "transit_mode": "Charter Bus", "eta": "18:15", "language": "Japanese", "target": "Executive Suite 4", "gate": "Gate A", "mandates": "Needs Japanese translator", "x": 2.0, "y": 6.0, "zone": "Outside"},
        {"name": "FIFA Executive VIPs", "affiliation": "FIFA Comm.", "status": "Nominal", "location_desc": "Settled at VIP Lounge 2", "transit_mode": "Official Car", "eta": "16:45", "language": "French", "target": "VIP Lounge 2", "gate": "Gate B", "mandates": "Standard accreditations", "x": 7.0, "y": 7.0, "zone": "Inside"},
        {"name": "Ronaldo & Party", "affiliation": "Brazilian Legend", "status": "Nominal", "location_desc": "Settled at Royal Box", "transit_mode": "Helicopter", "eta": "16:15", "language": "Portuguese", "target": "Royal Box", "gate": "Helipad", "mandates": "Autograph area protection", "x": 5.0, "y": 8.0, "zone": "Inside"}
    ],
    2: [
        {"name": "Spain Royal Escort", "affiliation": "Spanish Royal Family", "status": "Nominal", "location_desc": "Escorted to Royal Box", "transit_mode": "Private Escort", "eta": "17:45", "language": "Spanish", "target": "Royal Box", "gate": "Gate C", "mandates": "Wheelchair access, high security", "x": 5.0, "y": 8.0, "zone": "Inside"},
        {"name": "German FA President", "affiliation": "DFB Delegation", "status": "Nominal", "location_desc": "At Gate B (Receiving VIP)", "transit_mode": "VIP Shuttle", "eta": "18:25", "language": "German", "target": "VIP Lounge 1", "gate": "Gate B", "mandates": "Halal catering request", "x": 5.0, "y": 7.5, "zone": "Outside"},
        {"name": "Tokyo FC Board", "affiliation": "Tokyo FC Board", "status": "Nominal", "location_desc": "At Gate A (Met by Translator)", "transit_mode": "Charter Bus", "eta": "18:15", "language": "Japanese", "target": "Executive Suite 4", "gate": "Gate A", "mandates": "Needs Japanese translator", "x": 2.0, "y": 7.5, "zone": "Outside"},
        {"name": "FIFA Executive VIPs", "affiliation": "FIFA Comm.", "status": "Nominal", "location_desc": "Settled at VIP Lounge 2", "transit_mode": "Official Car", "eta": "16:45", "language": "French", "target": "VIP Lounge 2", "gate": "Gate B", "mandates": "Standard accreditations", "x": 7.0, "y": 7.0, "zone": "Inside"},
        {"name": "Ronaldo & Party", "affiliation": "Brazilian Legend", "status": "Nominal", "location_desc": "Settled at Royal Box", "transit_mode": "Helicopter", "eta": "16:15", "language": "Portuguese", "target": "Royal Box", "gate": "Helipad", "mandates": "Autograph area protection", "x": 5.0, "y": 8.0, "zone": "Inside"}
    ],
    3: [
        {"name": "Spain Royal Escort", "affiliation": "Spanish Royal Family", "status": "Nominal", "location_desc": "Settled at Royal Box", "transit_mode": "Private Escort", "eta": "17:45", "language": "Spanish", "target": "Royal Box", "gate": "Gate C", "mandates": "Wheelchair access, high security", "x": 5.0, "y": 8.0, "zone": "Inside"},
        {"name": "German FA President", "affiliation": "DFB Delegation", "status": "Nominal", "location_desc": "Arrived at VIP Lounge 1", "transit_mode": "VIP Shuttle", "eta": "18:25", "language": "German", "target": "VIP Lounge 1", "gate": "Gate B", "mandates": "Halal catering request", "x": 3.0, "y": 7.0, "zone": "Inside"},
        {"name": "Tokyo FC Board", "affiliation": "Tokyo FC Board", "status": "Nominal", "location_desc": "Arrived at Executive Suite 4", "transit_mode": "Charter Bus", "eta": "18:15", "language": "Japanese", "target": "Executive Suite 4", "gate": "Gate A", "mandates": "Needs Japanese translator", "x": 3.2, "y": 4.0, "zone": "Inside"},
        {"name": "FIFA Executive VIPs", "affiliation": "FIFA Comm.", "status": "Nominal", "location_desc": "Settled at VIP Lounge 2", "transit_mode": "Official Car", "eta": "16:45", "language": "French", "target": "VIP Lounge 2", "gate": "Gate B", "mandates": "Standard accreditations", "x": 7.0, "y": 7.0, "zone": "Inside"},
        {"name": "Ronaldo & Party", "affiliation": "Brazilian Legend", "status": "Nominal", "location_desc": "Settled at Royal Box", "transit_mode": "Helicopter", "eta": "16:15", "language": "Portuguese", "target": "Royal Box", "gate": "Helipad", "mandates": "Autograph area protection", "x": 5.0, "y": 8.0, "zone": "Inside"}
    ]
}

SIMULATION_TIME_MAPPING = {
    0: "17:00 (Pre-Match Arrival Hub)",
    1: "17:30 (Gates Opening Phase)",
    2: "18:00 (Peak Ingress Peak Flow)",
    3: "18:30 (Kick-off Impending)"
}

# ==============================================================================
# 4. INITIALIZE SESSION STATE
# ==============================================================================
if "initialized" not in st.session_state:
    st.session_state.simulation_step = 0
    st.session_state.vips = VIP_SIMULATION_STEPS[0]
    st.session_state.directory = [
        {"name": "Sarah Connor", "role": "Central Command Director", "zone": "Command Center", "languages": "English, French", "status": "Active", "beep_count": 0, "id": "sarah"},
        {"name": "Ahmed Al-Masri", "role": "Team Lead", "zone": "VIP Lounges", "languages": "English, Arabic", "status": "Active", "beep_count": 0, "id": "ahmed"},
        {"name": "Maria Delgado", "role": "Liaison Officer", "zone": "Gate C VIP Reception", "languages": "Spanish, English", "status": "Active", "beep_count": 0, "id": "maria"},
        {"name": "Kenji Sato", "role": "Bilingual Escort", "zone": "Gate A Logistics", "languages": "Japanese, English", "status": "Active", "beep_count": 0, "id": "kenji"},
        {"name": "Jean-Pierre", "role": "Transit Coordinator", "zone": "Outside Transport Hub", "languages": "French, English", "status": "Active", "beep_count": 0, "id": "jean"},
        {"name": "Samantha Green", "role": "Royal Box Host", "zone": "Royal Box Corridor", "languages": "English, German", "status": "Active", "beep_count": 0, "id": "samantha"}
    ]
    st.session_state.beep_logs = [
        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] SYSTEM INIT // VIO co-pilot online. Secure channels activated."
    ]
    st.session_state.chat_history = []
    st.session_state.selected_contingency = None
    st.session_state.initialized = True

# ==============================================================================
# 5. SIMULATION LOGIC HANDLERS
# ==============================================================================
def update_simulation_step():
    step = st.session_state.simulation_step
    st.session_state.vips = VIP_SIMULATION_STEPS[step]
    log_time = datetime.datetime.now().strftime('%H:%M:%S')
    st.session_state.beep_logs.append(
        f"[{log_time}] SIM UPDATE // Shifted to Step {step} [{SIMULATION_TIME_MAPPING[step]}]. VIP Positions refreshed."
    )

def advance_step():
    if st.session_state.simulation_step < 3:
        st.session_state.simulation_step += 1
        update_simulation_step()
    else:
        st.toast("Simulation is at the final matchday phase.", icon="ℹ️")

def reset_sim():
    st.session_state.simulation_step = 0
    update_simulation_step()
    st.toast("Simulation reset to step 0.", icon="🔄")

def trigger_beep(person_id, name, zone):
    # Find person and increment beep
    for person in st.session_state.directory:
        if person["id"] == person_id:
            person["beep_count"] += 1
            break
    log_time = datetime.datetime.now().strftime('%H:%M:%S')
    st.session_state.beep_logs.append(
        f"[{log_time}] BEACON BEEP // Paged {name} in zone [{zone}] successfully."
    )
    st.toast(f"🚨 Silent beep transmitted to {name}!", icon="📢")

# ==============================================================================
# 6. HEADER & METRIC STYLING (FIFA 2026 BRAND BANNER)
# ==============================================================================
# 2026 FIFA World Cup Custom Gradient Banner (Deep FIFA Blue to Bright Teal Accent)
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #071D49 0%, #104C8A 50%, #00FFCC 100%); 
                padding: 1.8rem; 
                border-radius: 12px; 
                text-align: center; 
                margin-bottom: 1.5rem; 
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
                border-bottom: 3px solid #00FFCC;">
        <h1 style="color: #FFFFFF; margin: 0; font-family: 'Space Grotesk', sans-serif; font-size: 2.3rem; letter-spacing: 2px; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">🏆 2026 FIFA WORLD CUP</h1>
        <h2 style="color: #00FFCC; margin: 6px 0 0 0; font-family: 'Outfit', sans-serif; font-size: 1.35rem; font-weight: 600; letter-spacing: 0.5px;">VIO // Volunteer Intelligent Operator Support</h2>
        <p style="color: #BEC2CA; margin: 6px 0 0 0; font-size: 0.9rem; font-weight: 500; opacity: 0.85;">Frontline Real-Time Decision Support & Spatial Tracking Matrix</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Metrics calculations
total_vips = len(st.session_state.vips)
urgent_vips = len([v for v in st.session_state.vips if v["status"] == "Urgent Alert"])
total_paged = sum([p["beep_count"] for p in st.session_state.directory])
clock_time = SIMULATION_TIME_MAPPING[st.session_state.simulation_step]

# Metric cards using HTML/CSS (Updated with Deep Blue / Teal styles)
st.markdown(f"""
<div class="metric-container">
    <div class="metric-card">
        <div class="metric-title">FIFA Timeline Clock</div>
        <div class="metric-val">{clock_time}</div>
        <div class="metric-desc">Interactive Step {st.session_state.simulation_step} / 3</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Active VIP Delegations</div>
        <div class="metric-val">{total_vips}</div>
        <div class="metric-desc">Monitored in Session</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Urgent Active Alerts</div>
        <div class="metric-val" style="color: {'#FF4B4B' if urgent_vips > 0 else '#00FFCC'}">{urgent_vips}</div>
        <div class="metric-desc {'urgent' if urgent_vips > 0 else ''}">Immediate Action Required</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Active Beacon Beeps</div>
        <div class="metric-val">{total_paged}</div>
        <div class="metric-desc">Volunteers Signalled</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 7. MAIN SIDEBAR NAVIGATION & SIMULATOR CONTROL PANEL
# ==============================================================================
st.sidebar.markdown(
    "<h2 style='color: #00FFCC; font-size: 1.3rem; margin-top: 0px;'>🧭 COMMAND NAVIGATION</h2>", 
    unsafe_allow_html=True
)

tab_selection = st.sidebar.radio(
    "Select Interface Page:",
    [
        "🗺️ Zone Map Command",
        "⚠️ VIP Transit Matrix",
        "📇 Operational Directory",
        "🤖 VIO AI Co-Pilot"
    ],
    label_visibility="collapsed"
)

st.sidebar.write("---")

st.sidebar.markdown(
    "<h3 style='color: #FFFFFF; font-size: 1.1rem;'>⏱️ MATCHDAY TIMELINE SIMULATOR</h3>",
    unsafe_allow_html=True
)
st.sidebar.info(
    "Control the timeline to simulate real-time ingress. VIPs will transition "
    "from incoming transit (Outside Gates) to their designated lounges/suites (Inside Stadium)."
)

# Simulation Buttons
sim_cols = st.sidebar.columns(2)
with sim_cols[0]:
    if st.button("▶️ Advance", use_container_width=True, on_click=advance_step):
        pass
with sim_cols[1]:
    if st.button("🔄 Reset", use_container_width=True, on_click=reset_sim):
        pass

# Add a warning in the sidebar if there's an active urgent alert
urgent_list = [v for v in st.session_state.vips if v["status"] == "Urgent Alert"]
if urgent_list:
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<div style='border: 1px solid #FF4B4B; background-color: rgba(255, 75, 75, 0.1); "
        "padding: 10px; border-radius: 6px; color: #FF4B4B; font-weight: 500; font-size: 0.85rem;'>"
        f"🚨 <b>URGENT ALERT:</b> {urgent_list[0]['name']} is facing a transport issue. "
        "Review VIP Transit tab immediately."
        "</div>",
        unsafe_allow_html=True
    )

# ==============================================================================
# 8. TWO-COLUMN OPERATIONAL LAYOUT (PRIMARY SCREEN + TERMINAL)
# ==============================================================================
col_main, col_logs = st.columns([3, 1])

with col_main:
    # --------------------------------------------------------------------------
    # TAB 1: 🗺️ DUAL-ZONE INTERACTIVE STADIUM MAP
    # --------------------------------------------------------------------------
    if tab_selection == "🗺️ Zone Map Command":
        st.subheader("🗺️ Dual-Zone Interactive Layout Map")
        st.markdown(
            "This dynamic view maps out the movement coordinates of incoming VIP parties. "
            "Toggle between the **Outside Gate Ingress** and the **Inside Suite Layout**."
        )
        
        map_toggle = st.segmented_control(
            "Select Map Zone:",
            options=["Outside Gates & Transport Hub", "Inside Stadium Layout"],
            default="Outside Gates & Transport Hub"
        )

        # Plotly graph creation
        fig = go.Figure()

        if map_toggle == "Outside Gates & Transport Hub":
            # --- OUTSIDE GATE INGRESS HUB LAYOUT DESIGN ---
            # Gates (Rectangles)
            fig.add_shape(type="rect", x0=1.5, y0=7.2, x1=2.5, y1=7.8, fillcolor="#122030", line=dict(color="#1E3A52", width=2))
            fig.add_shape(type="rect", x0=4.5, y0=7.2, x1=5.5, y1=7.8, fillcolor="#122030", line=dict(color="#1E3A52", width=2))
            fig.add_shape(type="rect", x0=7.5, y0=7.2, x1=8.5, y1=7.8, fillcolor="#122030", line=dict(color="#1E3A52", width=2))

            # Transport Hubs (Rectangle & Circle)
            fig.add_shape(type="rect", x0=1.0, y0=2.0, x1=2.2, y1=2.8, fillcolor="#050E17", line=dict(color="#1E3A52", width=1))
            fig.add_shape(type="circle", x0=7.6, y0=1.4, x1=8.4, y1=2.2, fillcolor="#050E17", line=dict(color="#FF4B4B", width=2))

            # VIP Drop-Off Center (Circle)
            fig.add_shape(type="circle", x0=4.6, y0=4.6, x1=5.4, y1=5.4, fillcolor="#0E2333", line=dict(color="#00FFCC", width=1.5))

            # Roads/Path Connectors (Lines)
            fig.add_trace(go.Scatter(
                x=[1.6, 1.6, 5.0, 8.0, 8.0],
                y=[2.8, 5.0, 5.0, 5.0, 2.2],
                mode="lines",
                line=dict(color="#1E3A52", width=5, dash="dash"),
                hoverinfo="skip",
                showlegend=False
            ))
            fig.add_trace(go.Scatter(
                x=[2.0, 2.0], y=[5.0, 7.2], mode="lines", line=dict(color="#1E3A52", width=5, dash="dash"), hoverinfo="skip", showlegend=False
            ))
            fig.add_trace(go.Scatter(
                x=[5.0, 5.0], y=[5.0, 7.2], mode="lines", line=dict(color="#1E3A52", width=5, dash="dash"), hoverinfo="skip", showlegend=False
            ))
            fig.add_trace(go.Scatter(
                x=[8.0, 8.0], y=[5.0, 7.2], mode="lines", line=dict(color="#1E3A52", width=5, dash="dash"), hoverinfo="skip", showlegend=False
            ))

            # Labels & Text Annotations
            fig.add_annotation(x=2.0, y=7.5, text="Gate A Ingress", showarrow=False, font=dict(color="#FFFFFF", size=11, family="Outfit"))
            fig.add_annotation(x=5.0, y=7.5, text="Gate B Ingress", showarrow=False, font=dict(color="#FFFFFF", size=11, family="Outfit"))
            fig.add_annotation(x=8.0, y=7.5, text="Gate C Ingress", showarrow=False, font=dict(color="#FFFFFF", size=11, family="Outfit"))
            fig.add_annotation(x=1.6, y=2.4, text="Transport Hub", showarrow=False, font=dict(color="#BEC2CA", size=9, family="Outfit"))
            fig.add_annotation(x=8.0, y=1.8, text="VIP Helipad (H)", showarrow=False, font=dict(color="#FF4B4B", size=9, family="Outfit"))
            fig.add_annotation(x=5.0, y=5.0, text="VIP Drop-Off Area", showarrow=False, font=dict(color="#00FFCC", size=10, family="Outfit"))
            
            # Filter active VIPs outside
            vips_outside = [v for v in st.session_state.vips if v["zone"] == "Outside"]
            
            # VIP Markers
            if vips_outside:
                colors = []
                for v in vips_outside:
                    if v["status"] == "Urgent Alert": colors.append("#FF4B4B")
                    elif v["status"] == "Warning": colors.append("#FFAA00")
                    else: colors.append("#00FFCC")

                fig.add_trace(go.Scatter(
                    x=[v["x"] for v in vips_outside],
                    y=[v["y"] for v in vips_outside],
                    mode="markers+text",
                    marker=dict(
                        size=20,
                        color=colors,
                        line=dict(color="#FFFFFF", width=2),
                        symbol="circle"
                    ),
                    text=[v["name"] for v in vips_outside],
                    textposition="top center",
                    textfont=dict(color="#FFFFFF", size=12, family="Outfit"),
                    hovertemplate="<b>%{text}</b><br>Affiliation: %{customdata[0]}<br>Status: %{customdata[1]}<br>Location: %{customdata[2]}<br>Language: %{customdata[3]}<extra></extra>",
                    customdata=[[v["affiliation"], v["status"], v["location_desc"], v["language"]] for v in vips_outside],
                    showlegend=False
                ))

        else:
            # --- INSIDE STADIUM VIP SUITES & LOUNGES DESIGN ---
            # Green pitch in center
            fig.add_shape(type="rect", x0=3.2, y0=3.2, x1=6.8, y1=6.8, fillcolor="#103c2f", line=dict(color="#00FFCC", width=1.5))
            fig.add_shape(type="circle", x0=4.5, y0=4.5, x1=5.5, y1=5.5, line=dict(color="#FFFFFF", width=1))
            fig.add_shape(type="line", x0=5.0, y0=3.2, x1=5.0, y1=6.8, line=dict(color="#FFFFFF", width=1))

            # Royal Box (Gold Accent)
            fig.add_shape(type="rect", x0=4.3, y0=7.5, x1=5.7, y1=8.2, fillcolor="#2A2215", line=dict(color="#FFAA00", width=2))
            
            # VIP Lounges (Level 1)
            fig.add_shape(type="rect", x0=1.8, y0=6.8, x1=2.8, y1=7.4, fillcolor="#0F2030", line=dict(color="#1E3A52", width=2))
            fig.add_shape(type="rect", x0=7.2, y0=6.8, x1=8.2, y1=7.4, fillcolor="#0F2030", line=dict(color="#1E3A52", width=2))

            # Executive Suites (Level 3 - bottom sides)
            fig.add_shape(type="rect", x0=1.5, y0=2.0, x1=3.5, y1=2.6, fillcolor="#122030", line=dict(color="#1E3A52", width=1))
            fig.add_shape(type="rect", x0=6.5, y0=2.0, x1=8.5, y1=2.6, fillcolor="#122030", line=dict(color="#1E3A52", width=1))

            # Labels & Text Annotations
            fig.add_annotation(x=5.0, y=5.0, text="PITCH ZONE", showarrow=False, font=dict(color="#FFFFFF", size=14, family="Space Grotesk", weight="bold"))
            fig.add_annotation(x=5.0, y=7.8, text="👑 Royal Box VIP", showarrow=False, font=dict(color="#FFAA00", size=11, family="Outfit"))
            fig.add_annotation(x=2.3, y=7.1, text="VIP Lounge 1", showarrow=False, font=dict(color="#FFFFFF", size=10, family="Outfit"))
            fig.add_annotation(x=7.7, y=7.1, text="VIP Lounge 2", showarrow=False, font=dict(color="#FFFFFF", size=10, family="Outfit"))
            fig.add_annotation(x=2.5, y=2.3, text="Executive Suites 1-5", showarrow=False, font=dict(color="#BEC2CA", size=9, family="Outfit"))
            fig.add_annotation(x=7.5, y=2.3, text="Executive Suites 6-10", showarrow=False, font=dict(color="#BEC2CA", size=9, family="Outfit"))

            # Filter active VIPs inside
            vips_inside = [v for v in st.session_state.vips if v["zone"] == "Inside"]

            # VIP Markers
            if vips_inside:
                colors = []
                for v in vips_inside:
                    if v["status"] == "Urgent Alert": colors.append("#FF4B4B")
                    elif v["status"] == "Warning": colors.append("#FFAA00")
                    else: colors.append("#00FFCC")

                fig.add_trace(go.Scatter(
                    x=[v["x"] for v in vips_inside],
                    y=[v["y"] for v in vips_inside],
                    mode="markers+text",
                    marker=dict(
                        size=20,
                        color=colors,
                        line=dict(color="#FFFFFF", width=2),
                        symbol="circle"
                    ),
                    text=[v["name"] for v in vips_inside],
                    textposition="top center",
                    textfont=dict(color="#FFFFFF", size=12, family="Outfit"),
                    hovertemplate="<b>%{text}</b><br>Affiliation: %{customdata[0]}<br>Status: %{customdata[1]}<br>Location: %{customdata[2]}<br>Target Suite: %{customdata[3]}<extra></extra>",
                    customdata=[[v["affiliation"], v["status"], v["location_desc"], v["target"]] for v in vips_inside],
                    showlegend=False
                ))

        # Apply dark mode styles to plot axes & backgrounds
        fig.update_layout(
            xaxis=dict(range=[0, 10], showgrid=False, zeroline=False, visible=False),
            yaxis=dict(range=[0, 10], showgrid=False, zeroline=False, visible=False),
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117",
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=False,
            height=520,
            dragmode=False
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Mini legend guide
        legend_cols = st.columns(3)
        with legend_cols[0]:
            st.markdown("<span class='badge badge-urgent'>● Urgent Alert</span> — Vehicle blockages/Severe delays", unsafe_allow_html=True)
        with legend_cols[1]:
            st.markdown("<span class='badge badge-warning'>● Delayed/Warning</span> — Delayed in customs/Language friction", unsafe_allow_html=True)
        with legend_cols[2]:
            st.markdown("<span class='badge badge-nominal'>● Nominal/Active</span> — On schedule / Arrived at target destination", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # TAB 2: ⚠️ VIP FLIGHT/TRANSIT & LANGUAGE SYNCHRONIZATION FEED
    # --------------------------------------------------------------------------
    elif tab_selection == "⚠️ VIP Transit Matrix":
        st.subheader("⚠️ VIP Flight, Transit & Language Coordination Feed")
        st.markdown(
            "This synchronization matrix logs flight parameters, languages, and custom guest mandates. "
            "Deploy **Contingency Protocols** immediately for delayed or urgent items."
        )

        # Filters
        filter_cols = st.columns(3)
        with filter_cols[0]:
            status_filter = st.selectbox("Filter Status Urgency:", ["All Statuses", "Urgent Alert", "Warning", "Nominal"])
        with filter_cols[1]:
            lang_filter = st.selectbox("Filter Language Needs:", ["All Languages", "Spanish", "German", "Japanese", "French", "Portuguese"])
        with filter_cols[2]:
            transit_filter = st.selectbox("Filter Transit Mode:", ["All Modes", "Private Escort", "VIP Shuttle", "Charter Bus", "Official Car", "Helicopter"])

        # Compile and Filter VIP Data
        filtered_vips = st.session_state.vips
        if status_filter != "All Statuses":
            filtered_vips = [v for v in filtered_vips if v["status"] == status_filter]
        if lang_filter != "All Languages":
            filtered_vips = [v for v in filtered_vips if v["language"] == lang_filter]
        if transit_filter != "All Modes":
            filtered_vips = [v for v in filtered_vips if v["transit_mode"] == transit_filter]

        if not filtered_vips:
            st.info("No active VIP delegations match your selected filters.")
        else:
            for idx, vip in enumerate(filtered_vips):
                # Assign status CSS classes
                status_class = "badge-nominal"
                if vip["status"] == "Urgent Alert":
                    status_class = "badge-urgent"
                elif vip["status"] == "Warning":
                    status_class = "badge-warning"

                st.markdown(f"""
                <div style='background-color: #122030; border-radius: 10px; border-left: 6px solid {
                    '#FF4B4B' if vip["status"] == 'Urgent Alert' else '#FFAA00' if vip["status"] == 'Warning' else '#00FFCC'
                }; padding: 1.2rem; margin-bottom: 1rem; border-top: 1px solid #1E3A52; border-right: 1px solid #1E3A52; border-bottom: 1px solid #1E3A52;'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <h4 style='margin:0; font-size:1.2rem; font-family:"Space Grotesk";'>{vip["name"]} <span style='font-size:0.9rem; color:#BEC2CA;'>({vip["affiliation"]})</span></h4>
                        <span class="badge {status_class}">{vip["status"]}</span>
                    </div>
                    <div style='display:flex; flex-wrap:wrap; gap:1.5rem; margin-top:0.75rem; font-size:0.9rem; color:#BEC2CA;'>
                        <div><b>📍 Location:</b> {vip["location_desc"]} ({vip["zone"]} Map)</div>
                        <div><b>🛫 Mode:</b> {vip["transit_mode"]}</div>
                        <div><b>⏰ ETA:</b> {vip["eta"]}</div>
                        <div><b>🗣️ Language:</b> {vip["language"]}</div>
                        <div><b>🎯 Target Suite:</b> {vip["target"]}</div>
                        <div><b>🚧 Mandates:</b> {vip["mandates"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show Action Buttons for urgent/warning VIPs
                btn_col1, btn_col2 = st.columns([1, 4])
                with btn_col1:
                    if st.button("Trigger Protocol", key=f"prot_{idx}_{vip['name']}"):
                        st.session_state.selected_contingency = vip
                with btn_col2:
                    st.write("")

        # Contingency Protocol Expandable Guidance Drawer
        if st.session_state.selected_contingency:
            v_ref = st.session_state.selected_contingency
            st.markdown("---")
            st.markdown(
                f"<div style='border: 1px solid #FF4B4B; border-radius: 8px; padding: 1.5rem; background-color: #08121E;'>"
                f"<h4 style='color:#FF4B4B; margin-top:0;'>⚠️ CONTINGENCY PLAN DEPLOYED: {v_ref['name']}</h4>"
                f"<p style='font-size:0.95rem; margin-bottom:15px;'><b>Current Issue:</b> {v_ref['location_desc']}. Target Zone: <b>{v_ref['target']}</b>. Language Barrier: <b>{v_ref['language']}</b>.</p>"
                "</div>",
                unsafe_allow_html=True
            )

            # Match VIO knowledge database to provide contingency instructions
            matched_key = None
            if "spanish" in v_ref["language"].lower() or "wheelchair" in v_ref["mandates"].lower():
                matched_key = "spanish vip wheelchair access path"
            elif "tokyo" in v_ref["affiliation"].lower() or "japanese" in v_ref["language"].lower():
                matched_key = "japanese vip translation"
            elif "german" in v_ref["language"].lower():
                matched_key = "german vip drop-off"
            elif "arabic" in v_ref["language"].lower() or "halal" in v_ref["mandates"].lower():
                matched_key = "arabic vip protocol"
            
            if matched_key and matched_key in VIO_KNOWLEDGE:
                k_data = VIO_KNOWLEDGE[matched_key]
                st.markdown(f"##### 📋 Operational Checklist: {k_data['title']}")
                for step_num, step_desc in enumerate(k_data["steps"], 1):
                    st.markdown(f"**Step {step_num}:** {step_desc}")
                
                # Dynamic suggest contact button
                suggested_staff = None
                for staff in st.session_state.directory:
                    if v_ref["language"] in staff["languages"]:
                        suggested_staff = staff
                        break
                
                if suggested_staff:
                    st.info(f"💡 **Recommended Action:** Click **Silent Beep** on **{suggested_staff['name']}** ({suggested_staff['role']}) in the Operational Directory tab to escort this VIP party.")
            else:
                st.markdown("##### 📋 Standard VIP Reception Protocol")
                st.markdown("1. Contact Central Command via silent beep or secure channel.")
                st.markdown(f"2. Station a coordinator at {v_ref['gate']} immediately to handle arrival.")
                st.markdown(f"3. Clear secure VIP corridor elevators leading to {v_ref['target']}.")

            if st.button("Close Contingency Console"):
                st.session_state.selected_contingency = None
                st.rerun()

    # --------------------------------------------------------------------------
    # TAB 3: 📇 CONTEXT-AWARE OPERATIONAL DIRECTORY & BEACON SYSTEM
    # --------------------------------------------------------------------------
    elif tab_selection == "📇 Operational Directory":
        st.subheader("📇 Stakeholder Operations Directory & Beacon System")
        st.markdown(
            "Search and ping fellow field volunteers, team coordinators, and central command. "
            "Sending a **Silent Beep** signals their wireless handheld receiver, skipping radio frequency jams."
        )

        search_query = st.text_input("🔍 Search stakeholder database (Name, Role, Zone, or Language):", "")

        # Directory Filtration
        filtered_directory = st.session_state.directory
        if search_query:
            q = search_query.lower()
            filtered_directory = [
                p for p in filtered_directory
                if q in p["name"].lower() or q in p["role"].lower() or q in p["zone"].lower() or q in p["languages"].lower()
            ]

        # Roster Grid System
        if not filtered_directory:
            st.warning("No stadium team members found matching search query.")
        else:
            grid_cols = st.columns(2)
            for idx, person in enumerate(filtered_directory):
                # alternate columns
                col_target = grid_cols[idx % 2]
                
                with col_target:
                    # Registry Card
                    st.markdown(f"""
                    <div class="profile-card">
                        <div class="profile-header">
                            <span class="profile-name">{person["name"]}</span>
                            <span class="profile-role">{person["role"]}</span>
                        </div>
                        <div class="profile-info"><span class="profile-label">📍 Allocation:</span> {person["zone"]}</div>
                        <div class="profile-info"><span class="profile-label">🗣️ Languages:</span> {person["languages"]}</div>
                        <div class="profile-info"><span class="profile-label">📶 Status:</span> <span style="color: #00FFCC;">● Active</span></div>
                        <div class="profile-info"><span class="profile-label">🚨 Sent Beeps:</span> <b>{person["beep_count"]}</b> Pings</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Beep Action Trigger Button
                    if st.button(
                        f"🚨 SILENT BEEP: {person['name']}", 
                        key=f"beep_btn_{person['id']}_{idx}", 
                        use_container_width=True
                    ):
                        trigger_beep(person["id"], person["name"], person["zone"])
                        st.rerun()

    # --------------------------------------------------------------------------
    # TAB 4: 🤖 VOLUNTEER'S AI SUPPORT AGENT VIO
    # --------------------------------------------------------------------------
    elif tab_selection == "🤖 VIO AI Co-Pilot":
        st.subheader("🤖 VIO Situational Knowledge Assistant")
        st.markdown(
            "VIO is a specialized offline situational knowledge assistant. Ask VIO for specific logistical guidance, "
            "routes, access paths, and protocols for various VIP scenarios."
        )

        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        st.markdown("💬 **Frequently Searched Instructions:**")
        
        # Clickable quick suggestions grid
        sug_cols = st.columns(3)
        with sug_cols[0]:
            if st.button("♿ Spanish Wheelchair Route", use_container_width=True):
                st.session_state.chat_history.append(
                    ("Spanish VIP wheelchair access path", VIO_KNOWLEDGE["spanish vip wheelchair access path"])
                )
            if st.button("🚗 German FA Drop-off Path", use_container_width=True):
                st.session_state.chat_history.append(
                    ("German VIP drop-off", VIO_KNOWLEDGE["german vip drop-off"])
                )
        with sug_cols[1]:
            if st.button("⚡ Gate B to Suite 4 Route", use_container_width=True):
                st.session_state.chat_history.append(
                    ("Fastest route from Gate B to Executive Box 4", VIO_KNOWLEDGE["fastest route from gate b to executive box 4"])
                )
            if st.button("🇯🇵 Tokyo FC Interpreter Protocol", use_container_width=True):
                st.session_state.chat_history.append(
                    ("Japanese VIP translation", VIO_KNOWLEDGE["japanese vip translation"])
                )
        with sug_cols[2]:
            if st.button("🚨 Emergency Medical Evacuation", use_container_width=True):
                st.session_state.chat_history.append(
                    ("Emergency medical route", VIO_KNOWLEDGE["emergency medical route"])
                )
            if st.button("🕌 Arabic Protocol & Halal", use_container_width=True):
                st.session_state.chat_history.append(
                    ("Arabic VIP protocol", VIO_KNOWLEDGE["arabic vip protocol"])
                )

        st.write("")
        
        # Text input query box
        user_query = st.text_input("💬 Ask VIO Co-Pilot a logistical FAQ (e.g. 'How to route Spanish VIP wheelchair'):")
        
        if st.button("Ask Assistant", type="primary"):
            if user_query:
                # Basic NLP keyword searching logic
                q_clean = user_query.lower()
                matched_key = None
                
                # Check for substring matches
                for key in VIO_KNOWLEDGE.keys():
                    # extract important words
                    keywords = key.split(" ")
                    match_count = sum(1 for kw in keywords if kw in q_clean)
                    # if substantial overlap or exact match
                    if key in q_clean or match_count >= 2:
                        matched_key = key
                        break
                
                # Secondary looser checks for Spanish, German, Japanese, Arabic, medical, route
                if not matched_key:
                    if "spanish" in q_clean or "wheelchair" in q_clean:
                        matched_key = "spanish vip wheelchair access path"
                    elif "gate b" in q_clean or "box 4" in q_clean or "suite 4" in q_clean:
                        matched_key = "fastest route from gate b to executive box 4"
                    elif "german" in q_clean or "deutsch" in q_clean:
                        matched_key = "german vip drop-off"
                    elif "japanese" in q_clean or "tokyo" in q_clean or "translation" in q_clean:
                        matched_key = "japanese vip translation"
                    elif "emergency" in q_clean or "medical" in q_clean or "ambulance" in q_clean:
                        matched_key = "emergency medical route"
                    elif "arabic" in q_clean or "halal" in q_clean or "muslim" in q_clean:
                        matched_key = "arabic vip protocol"

                if matched_key:
                    st.session_state.chat_history.append((user_query, VIO_KNOWLEDGE[matched_key]))
                else:
                    st.session_state.chat_history.append((
                        user_query, 
                        {
                            "title": "🔍 System Logistical Lookup Failed",
                            "steps": [
                                "Query did not match pre-loaded offline logistical guides.",
                                "Available keywords: 'Spanish wheelchair', 'Gate B to Executive Box 4', 'German drop-off', 'Japanese translator', 'Emergency medical', 'Arabic halal'.",
                                "Please refine query or contact Command Lead Sarah Connor (Zone: Command Center)."
                            ]
                        }
                    ))
                st.rerun()

        # Display Chat History log
        if st.session_state.chat_history:
            st.write("---")
            st.markdown("**Assistant Response Feed:**")
            
            # Show last response first
            for query, reply in reversed(st.session_state.chat_history):
                st.markdown(f"**👤 You:** *\"{query}\"*")
                
                # Check if it was a failure or success
                border_color = "#FF4B4B" if "Failed" in reply["title"] else "#00FFCC"
                
                st.markdown(f"""
                <div style='background-color:#08121E; border-left:4px solid {border_color}; padding:1rem; border-radius: 0 8px 8px 0; margin-bottom:1.5rem;'>
                    <h5 style='margin-top:0; color:#FFFFFF; font-size:1.05rem;'>{reply["title"]}</h5>
                    <ol style='margin-bottom:0; padding-left:1.2rem; color:#BEC2CA; font-size:0.9rem;'>
                        {"".join(f"<li style='margin-bottom:0.4rem;'>{step}</li>" for step in reply["steps"])}
                    </ol>
                </div>
                """, unsafe_allow_html=True)
                
            if st.button("Clear Consultation Log"):
                st.session_state.chat_history = []
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

with col_logs:
    # --------------------------------------------------------------------------
    # RIGHT SIDE PANEL: LIVE TERMINAL & BEACON LOGS
    # --------------------------------------------------------------------------
    st.markdown(
        "<h3 style='margin-top: 0px; font-size: 1.15rem; color: #FFFFFF;'>📟 LIVE BEACON LOGS</h3>", 
        unsafe_allow_html=True
    )
    st.markdown(
        "Real-time audit log tracking data packet broadcasts, silent paging pings, "
        "and physical simulation updates."
    )
    
    # Terminal panel
    log_content = ""
    for log in reversed(st.session_state.beep_logs):
        log_content += f"<div class='terminal-log'>{log}</div>"
        
    st.markdown(f"""
    <div class="beacon-terminal">
        {log_content}
    </div>
    """, unsafe_allow_html=True)
    
    # Quick clear logs button
    if st.button("Clear Broadcast Log", use_container_width=True):
        st.session_state.beep_logs = [
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Broadcast log cleared by operator."
        ]
        st.rerun()
        
    # Info panel
    st.write("---")
    st.markdown(
        "<div style='background-color: #122030; border-radius: 8px; padding: 1rem; border: 1px solid #1E3A52; font-size: 0.85rem; color:#BEC2CA;'>"
        "<b>📢 Volunteer Tip:</b> Matchday communication is congested. Use <b>Silent Beep</b> first. "
        "Escort VIPs through security lanes equipped for wide-load wheelchair clearances "
        "to satisfy special mandates."
        "</div>",
        unsafe_allow_html=True
    )
