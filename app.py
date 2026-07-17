import streamlit as st
import json
import base64

# ==============================================================================
# 1. PAGE SETUP & SCANDINAVIAN DARK THEME CONFIG
# ==============================================================================
st.set_page_config(
    page_title="DesignForge // Layout Blueprint Engine",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Scandinavian Dark CSS Injection
THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600;700&family=Lora:ital,wght@0,400;0,600;1,400&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Syne:wght@500;700;800&family=Fira+Code:wght@400;500&display=swap');

/* Main Layout Styles */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #121214 !important;
    color: #F3F4F6 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Sidebar Custom Styling */
[data-testid="stSidebar"] {
    background-color: #1A1A1E !important;
    border-right: 1px solid #2D2D35 !important;
}
[data-testid="stSidebar"] .stMarkdown h1, 
[data-testid="stSidebar"] .stMarkdown h2, 
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #F3F4F6 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Streamlit Native Input Element Overrides */
div[data-baseweb="select"] > div {
    background-color: #1A1A1E !important;
    border: 1px solid #2D2D35 !important;
    color: #F3F4F6 !important;
    border-radius: 6px !important;
}
div[role="listbox"] {
    background-color: #1A1A1E !important;
    border: 1px solid #2D2D35 !important;
}
div[role="option"] {
    color: #F3F4F6 !important;
    background-color: #1A1A1E !important;
}
div[role="option"]:hover, div[role="option"][aria-selected="true"] {
    background-color: #7C3AED !important;
    color: #FFFFFF !important;
}
.stSlider [data-testid="stWidgetLabel"] {
    color: #F3F4F6 !important;
}

/* Tab styling overrides */
button[data-baseweb="tab"] {
    background-color: transparent !important;
    color: #9CA3AF !important;
    border: none !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    padding: 10px 16px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #7C3AED !important;
    border-bottom: 2px solid #7C3AED !important;
}

/* Custom design components */
.engine-header {
    margin-bottom: 2rem;
    border-bottom: 1px solid #2A2A30;
    padding-bottom: 1.5rem;
}
.engine-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #F3F4F6 50%, #7C3AED 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.engine-subtitle {
    font-size: 0.95rem;
    color: #9CA3AF;
    margin-top: 0.2rem;
}

/* Card Surface component */
.designforge-panel {
    background-color: #1A1A1E;
    border: 1px solid #2D2D35;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

/* Wireframe simulation workspace */
.wireframe-workspace {
    position: relative;
    background-color: #0E0E10;
    border: 1px solid var(--slate-color);
    border-radius: var(--border-radius);
    padding: 24px;
    min-height: 520px;
    box-sizing: border-box;
    transition: all 0.3s ease;
    overflow: hidden;
}

/* Grid guide overlay representation */
.grid-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 1;
}
.grid-overlay-12 {
    background-image: repeating-linear-gradient(to right, 
        rgba(124, 58, 237, 0.04) 0px, 
        rgba(124, 58, 237, 0.04) calc((100% - 11 * var(--grid-gap)) / 12), 
        transparent calc((100% - 11 * var(--grid-gap)) / 12), 
        transparent calc((100% - 11 * var(--grid-gap)) / 12 + var(--grid-gap))
    );
}
.grid-overlay-4 {
    background-image: repeating-linear-gradient(to right, 
        rgba(124, 58, 237, 0.04) 0px, 
        rgba(124, 58, 237, 0.04) calc((100% - 3 * var(--grid-gap)) / 4), 
        transparent calc((100% - 3 * var(--grid-gap)) / 4), 
        transparent calc((100% - 3 * var(--grid-gap)) / 4 + var(--grid-gap))
    );
}
.grid-overlay-modular {
    background-image: 
        repeating-linear-gradient(to right, 
            rgba(124, 58, 237, 0.03) 0px, 
            rgba(124, 58, 237, 0.03) 80px, 
            transparent 80px, 
            transparent calc(80px + var(--grid-gap))
        ),
        repeating-linear-gradient(to bottom, 
            rgba(124, 58, 237, 0.03) 0px, 
            rgba(124, 58, 237, 0.03) 80px, 
            transparent 80px, 
            transparent calc(80px + var(--grid-gap))
        );
}

/* Wireframe Elements */
.wireframe-element {
    position: relative;
    border: var(--border-thickness) solid var(--slate-color);
    border-radius: var(--border-radius);
    background-color: rgba(26, 26, 30, 0.6);
    backdrop-filter: blur(2px);
    padding: 14px;
    z-index: 2;
    transition: all 0.3s ease;
}
.wireframe-element:hover {
    border-color: var(--accent-color);
    box-shadow: 0 0 12px rgba(124, 58, 237, calc(var(--accent-opacity) * 0.4));
}
.wireframe-label {
    position: absolute;
    top: -8px;
    left: 8px;
    font-family: 'Fira Code', monospace;
    font-size: 8px;
    color: var(--slate-color);
    background-color: #0E0E10;
    padding: 0 4px;
    border: 1px solid var(--slate-color);
    border-radius: 3px;
    line-height: 1;
    text-transform: uppercase;
}
.wireframe-element:hover .wireframe-label {
    color: var(--accent-color);
    border-color: var(--accent-color);
}

/* SVG Dimension indicator style */
.dim-indicator {
    stroke: var(--slate-color);
    stroke-width: 1;
    stroke-dasharray: 2 2;
}
.dim-text {
    fill: var(--slate-color);
    font-family: 'Fira Code', monospace;
    font-size: 9px;
}

/* Swatch container */
.color-swatch {
    display: inline-block;
    width: 42px;
    height: 42px;
    border-radius: 6px;
    margin-right: 8px;
    border: 1px solid #2D2D35;
    vertical-align: middle;
}

/* Interactive SVG Icon lists */
.icon-list-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-top: 10px;
}
.icon-card {
    background-color: #151518;
    border: 1px solid #2A2A32;
    border-radius: 6px;
    padding: 10px;
    text-align: center;
    transition: all 0.2s ease;
}
.icon-card:hover {
    border-color: #7C3AED;
    background-color: #1A1624;
}
.icon-svg-container {
    color: #7C3AED;
    margin-bottom: 6px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.icon-name {
    font-family: 'Fira Code', monospace;
    font-size: 10px;
    color: #9CA3AF;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
"""

st.markdown(THEME_CSS, unsafe_allow_html=True)

# ==============================================================================
# 2. STATE MANAGEMENT & SESSION SYSTEM
# ==============================================================================
if 'creative_field' not in st.session_state:
    st.session_state.creative_field = "UX/UI Design"

if 'project_type' not in st.session_state:
    st.session_state.project_type = "Case Study"

if 'grid_system' not in st.session_state:
    st.session_state.grid_system = "12-Column Grid"

if 'tone' not in st.session_state:
    st.session_state.tone = "Avant-Garde"

if 'grid_gap' not in st.session_state:
    st.session_state.grid_gap = 16

if 'border_radius' not in st.session_state:
    st.session_state.border_radius = 8

if 'border_thickness' not in st.session_state:
    st.session_state.border_thickness = 1

if 'accent_opacity' not in st.session_state:
    st.session_state.accent_opacity = 70

# Dynamic callbacks or helper resets when Creative Field shifts
def on_field_change():
    field = st.session_state.selected_field
    st.session_state.creative_field = field
    if field == "UX/UI Design":
        st.session_state.project_type = "Case Study"
        st.session_state.grid_system = "12-Column Grid"
    elif field == "Industrial Design":
        st.session_state.project_type = "Physical Prototype"
        st.session_state.grid_system = "Modular Grid"
    else:
        st.session_state.project_type = "Brand Identity"
        st.session_state.grid_system = "4-Column Mobile Grid"

# ==============================================================================
# 3. INTERACTIVE SIDEBAR & PARAMETERS
# ==============================================================================
st.sidebar.markdown("<h2 style='margin-bottom:0px;'>DesignForge</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:0.75rem; color:#9CA3AF; margin-top:0px;'>LAYOUT BLUEPRINT ENGINE // V1.0</p>", unsafe_allow_html=True)
st.sidebar.write("---")

# 1. Creative Discipline Selector
creative_fields = ["UX/UI Design", "Industrial Design", "Graphic Design"]
selected_field = st.sidebar.selectbox(
    "Creative Discipline",
    creative_fields,
    index=creative_fields.index(st.session_state.creative_field),
    key="selected_field",
    on_change=on_field_change
)

# Set dynamic project types list based on selected field
if selected_field == "UX/UI Design":
    project_options = ["Case Study", "Web Application Dashboard", "SaaS Landing Page"]
elif selected_field == "Industrial Design":
    project_options = ["Physical Prototype", "Exploded Tech Assembly", "Ergonomic Schematic"]
else:
    project_options = ["Brand Identity", "Editorial Book Spread", "Asymmetric Exhibition Grid"]

# Ensure selected project type is in the list
current_proj = st.session_state.project_type
if current_proj not in project_options:
    st.session_state.project_type = project_options[0]

project_type = st.sidebar.selectbox(
    "Project Architecture",
    project_options,
    key="project_type"
)

# 2. Tone Selector
tone_options = ["Avant-Garde", "Corporate", "Editorial"]
tone = st.sidebar.selectbox(
    "Typography Tone",
    tone_options,
    index=tone_options.index(st.session_state.tone),
    key="tone"
)

# 3. Target Grid System
grid_options = ["12-Column Grid", "4-Column Mobile Grid", "Modular Grid"]
grid_system = st.sidebar.selectbox(
    "Target Grid Structure",
    grid_options,
    index=grid_options.index(st.session_state.grid_system),
    key="grid_system"
)

st.sidebar.write("---")
st.sidebar.markdown("### Layout Fine-Tuning")

# 4. Spacing sliders
grid_gap = st.sidebar.slider("Grid Gutter Spacing (px)", min_value=4, max_value=32, value=st.session_state.grid_gap, step=2, key="grid_gap")
border_radius = st.sidebar.slider("Wireframe Corner Radius (px)", min_value=0, max_value=24, value=st.session_state.border_radius, step=2, key="border_radius")
border_thickness = st.sidebar.slider("Boundary Thickness (px)", min_value=1, max_value=4, value=st.session_state.border_thickness, step=1, key="border_thickness")
accent_opacity = st.sidebar.slider("Accent Glow Opacity (%)", min_value=10, max_value=100, value=st.session_state.accent_opacity, step=5, key="accent_opacity")

# CSS root variables injection based on sliders
st.markdown(f"""
<style>
:root {{
    --grid-gap: {grid_gap}px;
    --border-radius: {border_radius}px;
    --border-thickness: {border_thickness}px;
    --accent-color: #7C3AED;
    --accent-opacity: {accent_opacity / 100.0};
    --slate-color: #9CA3AF;
}}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. MAIN PANEL LAYOUT & SIMULATION ENGINE
# ==============================================================================
# Header Area
st.markdown(f"""
<div class="engine-header">
    <div class="engine-title">DesignForge Layout Blueprint Engine</div>
    <div class="engine-subtitle">Multidisciplinary Design System Generator • Active Mode: <span style="color:#7C3AED; font-weight:600;">{selected_field}</span></div>
</div>
""", unsafe_allow_html=True)

# Define design token recommendations dynamically based on selection
typography_pairings = {
    "Avant-Garde": {
        "display_name": "Syne",
        "display_url": "https://fonts.googleapis.com/css2?family=Syne:wght@700;800&display=swap",
        "display_css": "'Syne', sans-serif",
        "body_name": "Space Grotesk",
        "body_url": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&display=swap",
        "body_css": "'Space Grotesk', sans-serif",
        "archetype": "Bold, geometric, tech-experimental structure with tight display letter-spacing.",
        "scale": "Display: 38px (h1) / Body: 15px (p) / Leading: 1.1 (Display) & 1.4 (Body)"
    },
    "Corporate": {
        "display_name": "Plus Jakarta Sans",
        "display_url": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700&display=swap",
        "display_css": "'Plus Jakarta Sans', sans-serif",
        "body_name": "Inter",
        "body_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap",
        "body_css": "'Inter', sans-serif",
        "archetype": "Ultra-clean Scandinavian sans-serif pairing optimized for readability and high UI pixel densities.",
        "scale": "Display: 28px (h1) / Body: 14px (p) / Leading: 1.25 (Display) & 1.6 (Body)"
    },
    "Editorial": {
        "display_name": "Playfair Display",
        "display_url": "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&display=swap",
        "display_css": "'Playfair Display', serif",
        "body_name": "Lora",
        "body_url": "https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400&display=swap",
        "body_css": "'Lora', serif",
        "archetype": "High-contrast classy serif pairing drawing reference from Swiss typography layout magazines and art grids.",
        "scale": "Display: 34px (h1) / Body: 16px (p) / Leading: 1.15 (Display) & 1.7 (Body)"
    }
}

active_typography = typography_pairings[tone]

# Color palette token mappings based on Field
color_schemes = {
    "UX/UI Design": {
        "bg": "#121214",
        "surface": "#1A1A1E",
        "accent": "#7C3AED",
        "accent_text": "Electric Purple",
        "neutral_dark": "#1F1F24",
        "neutral_light": "#F3F4F6",
        "accent_secondary": "#06B6D4",
        "accent_secondary_text": "Cyber Cyan",
        "palette_description": "Clean dark UI foundation with purple primary focus for highlights and cyan for interactive hover states."
    },
    "Industrial Design": {
        "bg": "#0D0E10",
        "surface": "#141517",
        "accent": "#7C3AED",
        "accent_text": "Electric Purple",
        "neutral_dark": "#1B1C1E",
        "neutral_light": "#E5E7EB",
        "accent_secondary": "#F97316",
        "accent_secondary_text": "Warning Amber",
        "palette_description": "Engineering blueprint aesthetic. Purple for primary bounding coordinates and Warning Amber for hardware controls."
    },
    "Graphic Design": {
        "bg": "#111111",
        "surface": "#181818",
        "accent": "#7C3AED",
        "accent_text": "Electric Purple",
        "neutral_dark": "#202020",
        "neutral_light": "#FFFFFF",
        "accent_secondary": "#EC4899",
        "accent_secondary_text": "Chroma Pink",
        "palette_description": "Editorial offset. High-contrast white and dark slate spaces using purple and magenta highlights for asymmetrical layouts."
    }
}

active_colors = color_schemes[selected_field]

# Split main workspace: Left Column = Wireframe Simulation, Right Column = System Tokens Panel
col_sim, col_tokens = st.columns([1.6, 1.0])

with col_sim:
    st.markdown("<h3 style='margin-top:0px; font-size:1.25rem; font-family:\"Space Grotesk\", sans-serif;'>📐 Dynamic Wireframe Simulation Canvas</h3>", unsafe_allow_html=True)
    
    # Identify which grid class to use
    if grid_system == "12-Column Grid":
        grid_overlay_class = "grid-overlay grid-overlay-12"
    elif grid_system == "4-Column Mobile Grid":
        grid_overlay_class = "grid-overlay grid-overlay-4"
    else:
        grid_overlay_class = "grid-overlay grid-overlay-modular"

    # Assemble HTML Layout based on creative field
    if selected_field == "UX/UI Design":
        # Render a case study wireframe layout (Hero -> Problem -> Research Grid -> High-Fi Interactive Canvas)
        wireframe_html = f"""
        <div class="wireframe-workspace">
            <div class="{grid_overlay_class}"></div>
            
            <!-- Hero Section -->
            <div class="wireframe-element" style="grid-column: span 12; margin-bottom: var(--grid-gap); display: flex; flex-direction: column; justify-content: center; min-height: 110px;">
                <div class="wireframe-label">HERO CONTAINER (col-12)</div>
                <div style="font-family: {active_typography['display_css']}; font-size: 18px; color: #F3F4F6; margin: 0 0 4px 0; font-weight: bold;">[CASE STUDY HERO HEADING]</div>
                <div style="font-family: {active_typography['body_css']}; font-size: 10px; color: #9CA3AF; margin: 0 0 10px 0; max-width: 70%;">UX Case Study describing core metrics, problem definition, and design process milestones.</div>
                <div style="display: flex; gap: 8px;">
                    <div style="width: 70px; height: 16px; border-radius: 4px; background-color: rgba(124, 58, 237, var(--accent-opacity));"></div>
                    <div style="width: 50px; height: 16px; border-radius: 4px; border: 1px solid #9CA3AF;"></div>
                </div>
            </div>
            
            <!-- Problem & Research Row -->
            <div style="display: grid; grid-template-columns: repeat(12, 1fr); gap: var(--grid-gap); margin-bottom: var(--grid-gap);">
                <div class="wireframe-element" style="grid-column: span 6; min-height: 100px;">
                    <div class="wireframe-label">PROBLEM STATEMENT (col-6)</div>
                    <div style="font-family: {active_typography['display_css']}; font-size: 12px; color: #F3F4F6; margin-bottom: 6px; font-weight: 600;">The Challenge</div>
                    <div style="font-family: {active_typography['body_css']}; font-size: 9px; color: #9CA3AF; line-height: 1.4;">Users encounter friction during onboarding, causing a drop-off rate of 42% in step 2. We designed a modular stepper to resolve information density issues.</div>
                </div>
                <div class="wireframe-element" style="grid-column: span 6; min-height: 100px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div class="wireframe-label">RESEARCH INSIGHTS (col-6)</div>
                    <div style="font-family: {active_typography['display_css']}; font-size: 12px; color: #F3F4F6; margin-bottom: 4px; font-weight: 600;">User Archetype Data</div>
                    <div style="display: flex; gap: 8px; align-items: center;">
                        <div style="flex: 1; height: 35px; border-left: 2px solid #7C3AED; padding-left: 6px; display: flex; flex-direction: column; justify-content: center;">
                            <span style="font-size: 12px; font-weight: bold; color: #F3F4F6; font-family: 'Space Grotesk';">78%</span>
                            <span style="font-size: 7px; color: #9CA3AF; text-transform: uppercase;">Task Success</span>
                        </div>
                        <div style="flex: 1; height: 35px; border-left: 2px solid #06B6D4; padding-left: 6px; display: flex; flex-direction: column; justify-content: center;">
                            <span style="font-size: 12px; font-weight: bold; color: #F3F4F6; font-family: 'Space Grotesk';">-35%</span>
                            <span style="font-size: 7px; color: #9CA3AF; text-transform: uppercase;">Time-on-Task</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Research Cards -->
            <div style="display: grid; grid-template-columns: repeat(12, 1fr); gap: var(--grid-gap); margin-bottom: var(--grid-gap);">
                <div class="wireframe-element" style="grid-column: span 4; min-height: 60px;">
                    <div class="wireframe-label">PERSONA A (col-4)</div>
                    <div style="font-family: {active_typography['body_css']}; font-size: 9px; font-weight: bold; color: #F3F4F6;">The Heavy Planner</div>
                    <div style="font-size: 8px; color: #9CA3AF; margin-top: 2px;">Needs high density grids and multi-task viewports.</div>
                </div>
                <div class="wireframe-element" style="grid-column: span 4; min-height: 60px;">
                    <div class="wireframe-label">PERSONA B (col-4)</div>
                    <div style="font-family: {active_typography['body_css']}; font-size: 9px; font-weight: bold; color: #F3F4F6;">The Casual User</div>
                    <div style="font-size: 8px; color: #9CA3AF; margin-top: 2px;">Requires simplified step navigation and progressive disclosure.</div>
                </div>
                <div class="wireframe-element" style="grid-column: span 4; min-height: 60px;">
                    <div class="wireframe-label">PERSONA C (col-4)</div>
                    <div style="font-family: {active_typography['body_css']}; font-size: 9px; font-weight: bold; color: #F3F4F6;">The Specialist</div>
                    <div style="font-size: 8px; color: #9CA3AF; margin-top: 2px;">Demands technical schematic graphs and rapid keyboard hotkeys.</div>
                </div>
            </div>

            <!-- High-Fi Interactive Canvas -->
            <div class="wireframe-element" style="grid-column: span 12; min-height: 140px; display: flex; flex-direction: column;">
                <div class="wireframe-label">HI-FI INTERACTIVE CANVAS (col-12)</div>
                <div style="display: flex; flex: 1; border: 1px dashed rgba(156, 163, 175, 0.4); border-radius: 4px; background-color: rgba(14, 14, 16, 0.5); overflow: hidden;">
                    <!-- App Mockup Left Sidebar -->
                    <div style="width: 32px; border-right: 1px dashed rgba(156, 163, 175, 0.4); display: flex; flex-direction: column; align-items: center; gap: 8px; padding-top: 8px; background-color: rgba(26, 26, 30, 0.8);">
                        <div style="width: 14px; height: 14px; border-radius: 3px; background-color: rgba(124, 58, 237, 0.3);"></div>
                        <div style="width: 14px; height: 14px; border-radius: 3px; border: 1px solid rgba(156, 163, 175, 0.5);"></div>
                        <div style="width: 14px; height: 14px; border-radius: 3px; border: 1px solid rgba(156, 163, 175, 0.5);"></div>
                    </div>
                    <!-- App Mockup Content Window -->
                    <div style="flex: 1; padding: 10px; display: flex; flex-direction: column; justify-content: space-between;">
                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(156, 163, 175, 0.2); padding-bottom: 6px;">
                            <span style="font-size: 9px; font-family: 'Space Grotesk'; font-weight: 600; color: #FFFFFF;">Workspace Panel</span>
                            <span style="font-size: 8px; color: #7C3AED;">Active Live View</span>
                        </div>
                        <div style="display: flex; gap: 8px; flex: 1; align-items: center; margin-top: 6px;">
                            <div style="flex: 2; height: 50px; border-radius: 4px; background-color: rgba(255, 255, 255, 0.02); border: 1px solid rgba(156, 163, 175, 0.2); padding: 6px; display: flex; flex-direction: column; justify-content: center; gap: 4px;">
                                <div style="width: 80%; height: 6px; background-color: #F3F4F6; border-radius: 2px;"></div>
                                <div style="width: 50%; height: 4px; background-color: #9CA3AF; border-radius: 2px;"></div>
                            </div>
                            <div style="flex: 1; height: 50px; border-radius: 4px; border: 1px dashed rgba(124, 58, 237, 0.5); display: flex; justify-content: center; align-items: center;">
                                <span style="font-size: 8px; color: #7C3AED;">+ Element</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    elif selected_field == "Industrial Design":
        # Render blueprint layout focusing on Hero Renders, 3D Component Exploded Views, and Material Spec Tables
        wireframe_html = f"""
        <div class="wireframe-workspace">
            <div class="{grid_overlay_class}"></div>
            
            <!-- Technical Canvas with SVG Isometric Draw -->
            <div class="wireframe-element" style="grid-column: span 12; margin-bottom: var(--grid-gap); min-height: 180px; position: relative;">
                <div class="wireframe-label">CAD DRAFT & ISOMETRIC HERO SPEC (col-12)</div>
                <!-- Drawing Overlay SVG -->
                <div style="position: absolute; top: 0; left: 0; width:100%; height: 100%; z-index: 1; padding: 20px;">
                    <svg width="100%" height="100%" viewBox="0 0 600 140" fill="none">
                        <!-- Blueprint Crosshair Grid -->
                        <line x1="50" y1="0" x2="50" y2="140" stroke="#7C3AED" stroke-opacity="0.1" />
                        <line x1="300" y1="0" x2="300" y2="140" stroke="#7C3AED" stroke-opacity="0.1" />
                        <line x1="550" y1="0" x2="550" y2="140" stroke="#7C3AED" stroke-opacity="0.1" />
                        <line x1="0" y1="70" x2="600" y2="70" stroke="#7C3AED" stroke-opacity="0.1" />
                        
                        <!-- Isometric Cube Schematic (Chroma Design Concept) -->
                        <path d="M 280,30 L 330,60 L 330,110 L 280,80 Z" stroke="#7C3AED" stroke-width="1.5" stroke-opacity="0.9" />
                        <path d="M 330,60 L 380,30 L 380,80 L 330,110 Z" stroke="#7C3AED" stroke-width="1.5" stroke-opacity="0.9" />
                        <path d="M 280,30 L 330,0 L 380,30 L 330,60 Z" stroke="#7C3AED" stroke-width="1.5" stroke-opacity="0.9" />
                        
                        <!-- Dimension Indicator Lines -->
                        <line x1="280" y1="90" x2="330" y2="120" class="dim-indicator" />
                        <line x1="270" y1="80" x2="270" y2="30" class="dim-indicator" />
                        <text x="290" y="112" class="dim-text">L: 120.00mm</text>
                        <text x="225" y="60" class="dim-text">H: 85.00mm</text>
                        
                        <!-- Radial / callout detail -->
                        <circle cx="330" cy="60" r="10" stroke="#06B6D4" stroke-width="1" stroke-dasharray="2 2" />
                        <line x1="340" y1="60" x2="430" y2="45" stroke="#06B6D4" stroke-width="1" />
                        <text x="435" y="48" fill="#06B6D4" font-family="Fira Code" font-size="9px">FILLET RAD: R10.0</text>
                    </svg>
                </div>
                
                <div style="position: relative; z-index: 2; font-family: {active_typography['display_css']}; font-size: 15px; color: #FFFFFF; font-weight: bold;">[ISOMETRIC BluePrint DRAFT]</div>
                <div style="position: relative; z-index: 2; font-family: {active_typography['body_css']}; font-size: 9px; color: #9CA3AF; width: 40%; margin-top: 4px;">Precision exploded mapping of hardware casing, specifying tolerance boundaries and modular internal layout interfaces.</div>
            </div>
            
            <!-- Exploded Component Specs Row -->
            <div style="display: grid; grid-template-columns: repeat(12, 1fr); gap: var(--grid-gap); margin-bottom: var(--grid-gap);">
                <div class="wireframe-element" style="grid-column: span 4; min-height: 80px;">
                    <div class="wireframe-label">SHELL ASSEMBLY (col-4)</div>
                    <div style="font-family: {active_typography['body_css']}; font-size: 10px; font-weight: bold; color: #F3F4F6; margin-bottom: 2px;">Anodized Shell</div>
                    <div style="font-size: 8px; color: #9CA3AF;">Material: Aluminum 6061-T6<br>Thickness: 1.80mm<br>Surface Finish: Sandblast bead 120</div>
                </div>
                <div class="wireframe-element" style="grid-column: span 4; min-height: 80px;">
                    <div class="wireframe-label">INTERNAL FRAME (col-4)</div>
                    <div style="font-family: {active_typography['body_css']}; font-size: 10px; font-weight: bold; color: #F3F4F6; margin-bottom: 2px;">Polycarbonate Core</div>
                    <div style="font-size: 8px; color: #9CA3AF;">Material: PC-ABS Polymer<br>Fillet Radius: 1.5mm<br>Process: Injection Molded</div>
                </div>
                <div class="wireframe-element" style="grid-column: span 4; min-height: 80px;">
                    <div class="wireframe-label">OPTICAL WINDOW (col-4)</div>
                    <div style="font-family: {active_typography['body_css']}; font-size: 10px; font-weight: bold; color: #F3F4F6; margin-bottom: 2px;">Gorilla Glass Screen</div>
                    <div style="font-size: 8px; color: #9CA3AF;">Material: Aluminosilicate Glass<br>Tolerance: &plusmn;0.05mm<br>Coating: Anti-reflective (AR)</div>
                </div>
            </div>
            
            <!-- Material Specification Table -->
            <div class="wireframe-element" style="grid-column: span 12; min-height: 120px;">
                <div class="wireframe-label">MATERIAL & FABRICATION SCHEDULE (col-12)</div>
                <table style="width: 100%; border-collapse: collapse; font-family: 'Fira Code', monospace; font-size: 8.5px; color: #F3F4F6; margin-top: 10px;">
                    <thead>
                        <tr style="border-bottom: 1.5px solid #7C3AED; text-align: left;">
                            <th style="padding: 4px; color: #7C3AED;">PART ID</th>
                            <th style="padding: 4px;">MATERIAL SUBSTRATE</th>
                            <th style="padding: 4px;">PROCESS/METHOD</th>
                            <th style="padding: 4px; text-align: right;">QTY</th>
                            <th style="padding: 4px; text-align: right;">UNIT MASS</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid rgba(156, 163, 175, 0.2);">
                            <td style="padding: 4px; font-weight: bold; color: #9CA3AF;">DF-01</td>
                            <td style="padding: 4px;">AA 6061 Hard Case</td>
                            <td style="padding: 4px;">5-Axis CNC Milling</td>
                            <td style="padding: 4px; text-align: right;">1</td>
                            <td style="padding: 4px; text-align: right; color:#7C3AED;">142.5 g</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(156, 163, 175, 0.2);">
                            <td style="padding: 4px; font-weight: bold; color: #9CA3AF;">DF-02</td>
                            <td style="padding: 4px;">Neodymium Ring Magnet (N52)</td>
                            <td style="padding: 4px;">Sintering</td>
                            <td style="padding: 4px; text-align: right;">4</td>
                            <td style="padding: 4px; text-align: right; color:#7C3AED;">8.2 g</td>
                        </tr>
                        <tr>
                            <td style="padding: 4px; font-weight: bold; color: #9CA3AF;">DF-03</td>
                            <td style="padding: 4px;">FKM Rubber Seals</td>
                            <td style="padding: 4px;">Compression Molding</td>
                            <td style="padding: 4px; text-align: right;">2</td>
                            <td style="padding: 4px; text-align: right; color:#7C3AED;">1.4 g</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        """
    else:
        # Graphic Design: Render asymmetrical, high-impact typography and mood board gallery alignment layout
        wireframe_html = f"""
        <div class="wireframe-workspace">
            <div class="{grid_overlay_class}"></div>
            
            <!-- Huge typography header banner (Asymmetrical) -->
            <div style="display: grid; grid-template-columns: repeat(12, 1fr); gap: var(--grid-gap); margin-bottom: var(--grid-gap);">
                <div class="wireframe-element" style="grid-column: span 8; min-height: 120px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div class="wireframe-label">TYPOGRAPHIC FOCAL COMPOSITION (col-8)</div>
                    <div style="font-family: {active_typography['display_css']}; font-size: 32px; line-height: 0.95; font-weight: bold; letter-spacing: -0.04em; color: #FFFFFF;">
                        ASYNCH<br><span style="color: #7C3AED; font-style: italic;">METRICAL</span><br>FORM GRID
                    </div>
                    <div style="font-family: {active_typography['body_css']}; font-size: 8px; color: #9CA3AF; margin-top: 6px;">
                        EXPLORING CHROMA PATTERNS AND TYPE CONTRASTS.
                    </div>
                </div>
                <div class="wireframe-element" style="grid-column: span 4; min-height: 120px; display: flex; flex-direction: column; justify-content: space-between; align-items: flex-end; background-color: rgba(124, 58, 237, 0.05); border-color: rgba(124, 58, 237, 0.4);">
                    <div class="wireframe-label">BALANCE CARD (col-4)</div>
                    <div style="font-family: 'Fira Code', monospace; font-size: 9px; color: #7C3AED;">[WEIGHT 01]</div>
                    <div style="text-align: right; font-family: {active_typography['body_css']}; font-size: 10px; color: #F3F4F6;">
                        1:1.618<br><span style="font-size: 7px; color: #9CA3AF;">Golden Ratio Align</span>
                    </div>
                </div>
            </div>

            <!-- Moodboard & Gallery Items -->
            <div style="display: grid; grid-template-columns: repeat(12, 1fr); gap: var(--grid-gap); margin-bottom: var(--grid-gap);">
                <!-- Asymmetric overlapping column elements -->
                <div class="wireframe-element" style="grid-column: span 5; min-height: 140px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div class="wireframe-label">ASSET CONTAINER A (col-5)</div>
                    <!-- Mock diagonal crop lines represent visual media -->
                    <div style="flex: 1; width: 100%; border: 1px dashed rgba(156, 163, 175, 0.3); border-radius: 4px; position: relative; background: linear-gradient(135deg, rgba(26, 26, 30, 0.6) 0%, rgba(124, 58, 237, 0.08) 100%);">
                        <svg width="100%" height="100%" style="position: absolute; top:0; left:0;">
                            <line x1="0" y1="0" x2="100%" y2="100%" stroke="rgba(156, 163, 175, 0.15)" />
                            <line x1="100%" y1="0" x2="0" y2="100%" stroke="rgba(156, 163, 175, 0.15)" />
                        </svg>
                        <div style="position: absolute; bottom: 6px; left: 6px; font-family: 'Fira Code'; font-size: 7.5px; color: #9CA3AF;">MOOD_FRAME_01.PNG</div>
                    </div>
                    <div style="font-family: {active_typography['body_css']}; font-size: 8px; color: #9CA3AF; margin-top: 6px;">Visual identity rendering showing structural branding scale.</div>
                </div>
                
                <div class="wireframe-element" style="grid-column: span 7; min-height: 140px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div class="wireframe-label">ASSET CONTAINER B (col-7)</div>
                    <div style="display: flex; gap: 8px; flex: 1;">
                        <div style="flex: 1; border: 1px dashed rgba(156, 163, 175, 0.3); border-radius: 4px; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 6px; background-color: rgba(6, 182, 212, 0.02);">
                            <span style="font-family: 'Space Grotesk'; font-size: 14px; font-weight: bold; color: #7C3AED;">PANTONE</span>
                            <span style="font-size: 8px; font-family: 'Fira Code'; color: #9CA3AF;">2728 C</span>
                        </div>
                        <div style="flex: 1; border: 1px dashed rgba(156, 163, 175, 0.3); border-radius: 4px; padding: 10px; display: flex; flex-direction: column; justify-content: space-between;">
                            <span style="font-size: 12px; font-family: {active_typography['display_name']}; font-weight: bold;">Chroma System</span>
                            <span style="font-size: 7.5px; color: #9CA3AF; line-height: 1.3;">Primary CMYK offset layout maps target high contrast print finishes.</span>
                        </div>
                    </div>
                    
                    <!-- Bottom Swatch bar -->
                    <div style="display: flex; align-items: center; margin-top: 10px; border-top: 1px solid rgba(156, 163, 175, 0.2); padding-top: 8px;">
                        <div class="color-swatch" style="background-color: #7C3AED;"></div>
                        <div class="color-swatch" style="background-color: #EC4899;"></div>
                        <div class="color-swatch" style="background-color: #1A1A1E;"></div>
                        <div class="color-swatch" style="background-color: #FFFFFF;"></div>
                        <span style="font-family: 'Fira Code', monospace; font-size: 7.5px; color: #9CA3AF;">Palette swatches loaded into branding spec registry.</span>
                    </div>
                </div>
            </div>
        </div>
        """

    # Inject layout & render it
    st.markdown(wireframe_html, unsafe_allow_html=True)
    
    st.write("")
    
    # 5. DESIGN TOKEN EXPORTER MECHANISM (JSON + Markdown)
    st.markdown("<h3 style='font-size:1.25rem; font-family:\"Space Grotesk\", sans-serif;'>💾 Export Design Token Profile</h3>", unsafe_allow_html=True)
    
    # Generate Output Configuration Map (JSON)
    json_config = {
        "engineName": "DesignForge Layout Blueprint Engine",
        "configuration": {
            "creativeField": selected_field,
            "projectType": project_type,
            "tone": tone,
            "gridSystem": grid_system,
            "spacing": {
                "gutterGapPx": grid_gap,
                "cornerRadiusPx": border_radius,
                "borderThicknessPx": border_thickness,
                "accentOpacityPercent": accent_opacity
            },
            "designTokens": {
                "fonts": {
                    "heading": {
                        "family": active_typography["display_name"],
                        "css": active_typography["display_css"]
                    },
                    "body": {
                        "family": active_typography["body_name"],
                        "css": active_typography["body_css"]
                    },
                    "pairingRationale": active_typography["archetype"]
                },
                "colors": {
                    "background": active_colors["bg"],
                    "cardSurface": active_colors["surface"],
                    "accentPrimary": active_colors["accent"],
                    "accentPrimaryName": active_colors["accent_text"],
                    "accentSecondary": active_colors["accent_secondary"],
                    "accentSecondaryName": active_colors["accent_secondary_text"],
                    "paletteDescription": active_colors["palette_description"]
                }
            }
        }
    }
    
    # Generate Markdown Blueprint text
    markdown_blueprint = f"""# DesignForge Portfolio Layout Blueprint
*Generated on behalf of Creative Field: **{selected_field}***
*System Architecture Profile: **{project_type}***

---

## 📐 Grid & Bounding System Configuration
- **Selected Grid Structure:** {grid_system}
- **Layout Spacing Metrics:**
  - Column Gutter Gap: `{grid_gap}px`
  - Container Border Radius: `{border_radius}px`
  - Wireframe Stroke Boundary: `{border_thickness}px`
  - Primary Accent Opacity: `{accent_opacity}%`

## 🔠 Typography Pairing Tokens
- **Tone Profile:** `{tone}`
- **Display Header Typeface:** `{active_typography['display_name']}`
  - *Shorthand CSS:* `font-family: {active_typography['display_css']};`
- **Body Typeface:** `{active_typography['body_name']}`
  - *Shorthand CSS:* `font-family: {active_typography['body_css']};`
- **Recommended Hierarchy Scale:**
  - `{active_typography['scale']}`
- **Archetype Rationale:**
  - *{active_typography['archetype']}*

## 🎨 Color Palette Tokens (Scandinavian Clean Mode)
- **Primary Background:** `{active_colors['bg']}`
- **Card Surfaces & Panels:** `{active_colors['surface']}`
- **Primary Design Accent:** `{active_colors['accent']}` (Hex Mapping for `{active_colors['accent_text']}`)
- **Secondary Interactive Accent:** `{active_colors['accent_secondary']}` (Hex Mapping for `{active_colors['accent_secondary_text']}`)
- **System Theme Palette Rationale:**
  - *{active_colors['palette_description']}*

## 📦 Icon Suit Mapping Recommendation
We map specific SVG icons contextualized for creative tasks in **{selected_field}**. Read the adjacent token registry to view actual SVG structures and configurations.
"""

    tab_json, tab_md = st.tabs(["JSON Layout Map", "Markdown Blueprint Document"])
    
    with tab_json:
        # Prettified JSON code view
        json_str = json.dumps(json_config, indent=2)
        st.code(json_str, language="json")
        
        # Download button
        st.download_button(
            label="Download JSON Profile Map",
            data=json_str,
            file_name=f"designforge_{selected_field.lower().replace(' ', '_').replace('/', '_')}_blueprint.json",
            mime="application/json"
        )
        
    with tab_md:
        st.code(markdown_blueprint, language="markdown")
        
        # Download button
        st.download_button(
            label="Download Markdown Blueprint",
            data=markdown_blueprint,
            file_name=f"designforge_{selected_field.lower().replace(' ', '_').replace('/', '_')}_blueprint.md",
            mime="text/markdown"
        )

# Right Column: Tokens Pane and Icon Suit Recommend
with col_tokens:
    st.markdown("<h3 style='margin-top:0px; font-size:1.25rem; font-family:\"Space Grotesk\", sans-serif;'>🗃️ Active Design Token Registry</h3>", unsafe_allow_html=True)
    
    # 1. Fonts pairing Pane
    st.markdown(f"""
    <div class="designforge-panel">
        <h4 style="margin:0 0 10px 0; color:#7C3AED; font-family:'Space Grotesk'; font-size: 1rem;">🔤 Active Typography Token Pairing</h4>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div>
                <div style="font-size:11px; color:#9CA3AF; text-transform:uppercase; font-family:'Fira Code';">Header Font (Display)</div>
                <div style="font-family:{active_typography['display_css']}; font-size:20px; font-weight:bold; color:#FFFFFF;">{active_typography['display_name']}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:11px; color:#9CA3AF; text-transform:uppercase; font-family:'Fira Code';">Body Font</div>
                <div style="font-family:{active_typography['body_css']}; font-size:16px; color:#FFFFFF;">{active_typography['body_name']}</div>
            </div>
        </div>
        <p style="font-size:11px; color:#9CA3AF; margin: 8px 0 0 0; line-height: 1.4; border-top:1px solid #2D2D35; padding-top:8px;">
            <strong>Archetype:</strong> {active_typography['archetype']}<br>
            <strong>Recommended Hierarchy Scale:</strong> {active_typography['scale']}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. Color Palette Token Pane
    st.markdown(f"""
    <div class="designforge-panel">
        <h4 style="margin:0 0 10px 0; color:#7C3AED; font-family:'Space Grotesk'; font-size: 1rem;">🎨 Color Swatch Palettes</h4>
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center;">
                    <div class="color-swatch" style="background-color: {active_colors['bg']};"></div>
                    <div>
                        <span style="font-size:11px; font-weight:bold; display:block; color:#FFFFFF;">Primary Background</span>
                        <span style="font-family:'Fira Code'; font-size:9.5px; color:#9CA3AF;">{active_colors['bg']}</span>
                    </div>
                </div>
                <span style="font-size: 9px; padding: 2px 6px; background-color: #202020; border-radius: 4px; font-family:'Fira Code'; color: #9CA3AF;">BASE</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center;">
                    <div class="color-swatch" style="background-color: {active_colors['surface']};"></div>
                    <div>
                        <span style="font-size:11px; font-weight:bold; display:block; color:#FFFFFF;">Card Surface</span>
                        <span style="font-family:'Fira Code'; font-size:9.5px; color:#9CA3AF;">{active_colors['surface']}</span>
                    </div>
                </div>
                <span style="font-size: 9px; padding: 2px 6px; background-color: #202020; border-radius: 4px; font-family:'Fira Code'; color: #9CA3AF;">SURFACE</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center;">
                    <div class="color-swatch" style="background-color: {active_colors['accent']};"></div>
                    <div>
                        <span style="font-size:11px; font-weight:bold; display:block; color:#FFFFFF;">Primary Accent</span>
                        <span style="font-family:'Fira Code'; font-size:9.5px; color:#9CA3AF;">{active_colors['accent']}</span>
                    </div>
                </div>
                <span style="font-size: 9px; padding: 2px 6px; background-color: rgba(124,58,237,0.2); border-radius: 4px; font-family:'Fira Code'; color: #7C3AED;">{active_colors['accent_text'].upper()}</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center;">
                    <div class="color-swatch" style="background-color: {active_colors['accent_secondary']};"></div>
                    <div>
                        <span style="font-size:11px; font-weight:bold; display:block; color:#FFFFFF;">Interactive Secondary</span>
                        <span style="font-family:'Fira Code'; font-size:9.5px; color:#9CA3AF;">{active_colors['accent_secondary']}</span>
                    </div>
                </div>
                <span style="font-size: 9px; padding: 2px 6px; background-color: rgba(6,182,212,0.15); border-radius: 4px; font-family:'Fira Code'; color: {active_colors['accent_secondary']};">{active_colors['accent_secondary_text'].upper()}</span>
            </div>
        </div>
        <p style="font-size:11px; color:#9CA3AF; margin: 10px 0 0 0; line-height: 1.4; border-top:1px solid #2D2D35; padding-top:8px;">
            <strong>Palette Rule:</strong> {active_colors['palette_description']}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 3. Interactive SVG Icon Suite recommend pane
    st.markdown("<h4 style='font-size:1.05rem; font-family:\"Space Grotesk\", sans-serif; margin-bottom: 2px;'>📦 Structural Icon Suite Mapping</h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:11px; color:#9CA3AF; margin-top:0px;'>Recommended vector types for active Creative Field: <strong>{selected_field}</strong></p>", unsafe_allow_html=True)

    # Define recommended SVGs for UX/UI
    ux_ui_icons = [
        {"name": "app-window", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="18" rx="2" ry="2"/><line x1="2" y1="8" x2="22" y2="8"/><line x1="6" y1="5" x2="6" y2="5"/><line x1="10" y1="5" x2="10" y2="5"/></svg>'},
        {"name": "smartphone", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>'},
        {"name": "mouse-pointer", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3l7.07 16.97 2.51-7.39 7.39-2.51L3 3z"/><path d="M13 13l6 6"/></svg>'},
        {"name": "layers", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polygon points="2 17 12 22 22 17"/><polygon points="2 12 12 17 22 12"/></svg>'},
        {"name": "layout-grid", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/></svg>'},
        {"name": "app-window-ai", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="18" rx="2" ry="2"/><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>'},
        {"name": "sliders", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>'},
        {"name": "sparkles", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m11.314 11.314l.707.707M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z"/></svg>'}
    ]

    industrial_icons = [
        {"name": "drafting-compass", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v2"/><path d="M12 4l-4 16"/><path d="M12 4l4 16"/><path d="M8 15h8"/><path d="M12 2a2 2 0 1 1 0 4 2 2 0 0 1 0-4z"/></svg>'},
        {"name": "cog-gear", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>'},
        {"name": "caliper-ruler", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3h14c1.1 0 2 .9 2 2v14c0 1.1-.9 2-2 2H5c-1.1 0-2-.9-2-2V5c0-1.1.9-2 2-2z"/><path d="M3 9h4"/><path d="M3 15h4"/><path d="M9 3v4"/><path d="M15 3v4"/></svg>'},
        {"name": "microchip-cpu", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="15" x2="23" y2="15"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="15" x2="4" y2="15"/></svg>'},
        {"name": "box-exploded", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>'},
        {"name": "schematic-node", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>'},
        {"name": "scale-measure", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 3H6a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3h12a3 3 0 0 0 3-3V6a3 3 0 0 0-3-3z"/><line x1="9" y1="3" x2="9" y2="9"/><line x1="15" y1="3" x2="15" y2="9"/><line x1="3" y1="12" x2="21" y2="12"/></svg>'},
        {"name": "wrench-specs", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>'}
    ]

    graphic_icons = [
        {"name": "art-palette", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 14.7255 3.09032 17.1962 4.85857 19C5.03456 19.176 5.28135 19.2435 5.519 19.1818L6.4445 18.941C6.91572 18.8184 7.4116 18.9712 7.73715 19.3392L8.6083 20.3248C8.94821 20.7093 9.45892 20.9167 9.98818 20.8687L11.5362 20.728C11.6888 20.7141 11.8436 20.7141 11.9962 20.728L12 22Z"/><circle cx="7.5" cy="10.5" r="1.5" fill="currentColor"/><circle cx="11.5" cy="7.5" r="1.5" fill="currentColor"/><circle cx="16.5" cy="9.5" r="1.5" fill="currentColor"/></svg>'},
        {"name": "paint-brush", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 22H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8l6 6v12a2 2 0 0 1-2 2z"/><path d="M14 2v6h6"/><path d="M12 18h.01"/><path d="M11 12a1 1 0 1 0 2 0 1 1 0 0 0-2 0z"/></svg>'},
        {"name": "type-tool", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/><line x1="12" y1="4" x2="12" y2="20"/></svg>'},
        {"name": "crop-alignment", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 1v3H1"/><path d="M18 23v-3h5"/><rect x="6" y="4" width="12" height="16" rx="2"/></svg>'},
        {"name": "bezier-pen", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 14.7255 3.09032 17.1962 4.85857 19"/><path d="M12 2v6m0 8v6M2 12h6m8 0h6"/></svg>'},
        {"name": "gallery-image", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>'},
        {"name": "scissors-crop", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="9.8" y1="8.2" x2="20" y2="18.4"/><line x1="9.8" y1="15.8" x2="20" y2="5.6"/></svg>'},
        {"name": "compass-explore", "svg": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>'}
    ]

    active_icons = ux_ui_icons
    if selected_field == "Industrial Design":
        active_icons = industrial_icons
    elif selected_field == "Graphic Design":
        active_icons = graphic_icons

    # Display icons in a beautiful layout
    icon_grid_html = '<div class="icon-list-grid">'
    for ico in active_icons:
        icon_grid_html += f"""
        <div class="icon-card">
            <div class="icon-svg-container">{ico['svg']}</div>
            <div class="icon-name">{ico['name']}</div>
        </div>
        """
    icon_grid_html += '</div>'

    st.markdown(icon_grid_html, unsafe_allow_html=True)
    
    st.write("")
    
    # Render interactive details block explaining the architecture
    st.markdown(f"""
    <div class="designforge-panel" style="margin-top: 10px;">
        <h4 style="margin:0 0 10px 0; color:#7C3AED; font-family:'Space Grotesk'; font-size: 1rem;">🔧 Grid System Details</h4>
        <div style="font-family:'Fira Code', monospace; font-size: 10px; color:#F3F4F6;">
            <strong>GRID SPECIFICATION:</strong> {grid_system}<br>
            <strong>COLUMN GUTTER GAP:</strong> {grid_gap}px<br>
            <strong>INNER CORNER RADIUS:</strong> {border_radius}px<br>
            <strong>ACCENT OVERLAY OPACITY:</strong> {accent_opacity}%<br>
            <strong>BORDER STROKE WEIGHT:</strong> {border_thickness}px
        </div>
        <p style="font-size:11px; color:#9CA3AF; margin: 8px 0 0 0; line-height: 1.4; border-top:1px solid #2D2D35; padding-top:8px;">
            The simulation grid renders repeating linear gradients dynamically matching parameter configurations. Increase Border Radius to soften block enclosures or raise Glow Opacity to enhance hover visual indicators.
        </p>
    </div>
    """, unsafe_allow_html=True)
