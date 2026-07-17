import streamlit as st
import json

# ==============================================================================
# 1. PAGE CONFIGURATION & THEME INJECTION
# ==============================================================================
st.set_page_config(
    page_title="DesignForge // Design System Blueprint Engine",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Scandinavian Dark CSS Injection
THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700&family=Lora:ital,wght@0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Syne:wght@500;700;800&display=swap');

/* Main App Container Styling */
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

/* Native input styling overrides */
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

/* Tab selector customization */
button[data-baseweb="tab"] {
    background-color: transparent !important;
    color: #9CA3AF !important;
    border: none !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    padding: 12px 20px !important;
    transition: all 0.2s ease !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #7C3AED !important;
    border-bottom: 2px solid #7C3AED !important;
}

/* Header Container */
.engine-header {
    margin-bottom: 2rem;
    border-bottom: 1px solid #2D2D35;
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

/* Design Card Surface styling */
.blueprint-card {
    background-color: #1A1A1E;
    border: 1px solid #2D2D35;
    border-radius: 8px;
    padding: 1.25rem;
    position: relative;
    box-sizing: border-box;
    height: 100%;
}
.blueprint-card-label {
    position: absolute;
    top: -9px;
    left: 12px;
    font-family: 'Fira Code', monospace;
    font-size: 8px;
    color: #9CA3AF;
    background-color: #121214;
    padding: 0 6px;
    border: 1px solid #2D2D35;
    border-radius: 3px;
    line-height: 1;
    text-transform: uppercase;
    font-weight: 500;
}
.blueprint-card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: #FFFFFF;
    margin-bottom: 6px;
    margin-top: 4px;
}
.blueprint-card-text {
    font-size: 11px;
    color: #9CA3AF;
    line-height: 1.5;
}

/* Color Swatch elements */
.swatch-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: #121214;
    border: 1px solid #2D2D35;
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 8px;
}
.swatch-color-box {
    width: 32px;
    height: 32px;
    border-radius: 4px;
    border: 1px solid #2D2D35;
}

/* Validation banner custom alerts */
.validation-banner {
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13.5px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 10px;
}
</style>
"""
st.markdown(THEME_CSS, unsafe_allow_html=True)

# ==============================================================================
# 2. STATE MANAGEMENT & SESSION SYSTEM
# ==============================================================================
if 'discipline' not in st.session_state:
    st.session_state.discipline = "UX Case Study"

if 'gutter_spacing' not in st.session_state:
    st.session_state.gutter_spacing = 16

if 'archetype' not in st.session_state:
    st.session_state.archetype = "Minimalist Scandinavian"

if 'project_title' not in st.session_state:
    st.session_state.project_title = "Creative Portfolio Framework"

# Checkpoint checklist state
if 'check_research' not in st.session_state:
    st.session_state.check_research = False
if 'check_wireframe' not in st.session_state:
    st.session_state.check_wireframe = False
if 'check_hifi' not in st.session_state:
    st.session_state.check_hifi = False
if 'check_spec' not in st.session_state:
    st.session_state.check_spec = False

# ==============================================================================
# 3. INTERACTIVE SIDEBAR CONTROLS
# ==============================================================================
st.sidebar.markdown("<h2 style='margin-bottom:0px;'>DesignForge</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:0.75rem; color:#9CA3AF; margin-top:0px;'>LAYOUT BLUEPRINT ENGINE // V2.0</p>", unsafe_allow_html=True)
st.sidebar.write("---")

st.sidebar.markdown("### 🛠️ Global Parameters")

# Sidebar parameter selectors
discipline_selection = st.sidebar.selectbox(
    "Design Discipline Router",
    ["UX Case Study", "Industrial Blueprint", "Graphic Editorial"],
    index=["UX Case Study", "Industrial Blueprint", "Graphic Editorial"].index(st.session_state.discipline),
    key="selected_discipline"
)
st.session_state.discipline = discipline_selection

gutter_spacing = st.sidebar.slider(
    "Layout Gutter Spacing (px)",
    min_value=8,
    max_value=32,
    value=st.session_state.gutter_spacing,
    step=2,
    key="selected_gutter"
)
st.session_state.gutter_spacing = gutter_spacing

st.sidebar.write("---")
st.sidebar.markdown("""
<div style="font-size:11px; color:#9CA3AF; line-height:1.5;">
    <strong>Reactive Framework Status:</strong><br>
    The layouts and components on the right dynamically adjust and repaint themselves based on active sidebar and state selections.
</div>
""", unsafe_allow_html=True)

# Inject dynamic spacing variables into CSS root
st.markdown(f"""
<style>
:root {{
    --card-spacing: {st.session_state.gutter_spacing}px;
}}
.blueprint-card {{
    margin-bottom: var(--card-spacing) !important;
}}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. MAIN INTERACTION ENGINE & TABS ROUTER
# ==============================================================================
# Header Area
st.markdown(f"""
<div class="engine-header">
    <div class="engine-title">DesignForge Blueprint Engine</div>
    <div class="engine-subtitle">High-Fidelity Multi-Page Layout & Design Token Simulator</div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab_router, tab_tokens, tab_matrix = st.tabs([
    "📊 Canvas Wireframe Router", 
    "🎨 Active Token Injector", 
    "🗂️ Case Study Sequence Matrix"
])

# ------------------------------------------------------------------------------
# TAB 1: CANVAS WIREFRAME ROUTER
# ------------------------------------------------------------------------------
with tab_router:
    st.markdown("<h3 style='font-family:\"Space Grotesk\", sans-serif; margin-top:0px;'>📐 Dynamic Columns & Wireframe Router</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:12px; color:#9CA3AF; margin-top:-10px;'>Active Wireframe Structure: <strong>{st.session_state.discipline}</strong> • Gutter Spacing: <strong>{st.session_state.gutter_spacing}px</strong></p>", unsafe_allow_html=True)

    # Dynamic layout structure rendering
    if st.session_state.discipline == "UX Case Study":
        # Row 1: Hero Banner (Full Width)
        st.markdown(f"""
        <div class="blueprint-card" style="min-height:120px;">
            <div class="blueprint-card-label">Hero Banner (Col-12)</div>
            <div class="blueprint-card-title">CASE STUDY HERO HEADING // PORTFOLIO INTRO</div>
            <div class="blueprint-card-text">A primary high-impact header introducing the designer's UX philosophy, core research thesis, and the target user persona problems solved. Layout is optimized for wide screens.</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Row 2: Problem Grid (Side-by-side columns)
        col_prob1, col_prob2 = st.columns(2)
        with col_prob1:
            st.markdown(f"""
            <div class="blueprint-card" style="min-height:110px;">
                <div class="blueprint-card-label">Problem Brief (Col-6)</div>
                <div class="blueprint-card-title">Core Friction Challenges</div>
                <div class="blueprint-card-text">Documenting structural friction barriers, high-latency page checkouts, and onboarding step drop-off patterns mapped from user analytics reports.</div>
            </div>
            """, unsafe_allow_html=True)
        with col_prob2:
            st.markdown(f"""
            <div class="blueprint-card" style="min-height:110px;">
                <div class="blueprint-card-label">Target Solution (Col-6)</div>
                <div class="blueprint-card-title">Integrated Stepper System</div>
                <div class="blueprint-card-text">Proposed solution involving single-page state preservation and contextual help modules to lower user drop-off rate by 35%.</div>
            </div>
            """, unsafe_allow_html=True)

        # Row 3: Persona Breakdown (3-column layout)
        col_pers1, col_pers2, col_pers3 = st.columns(3)
        with col_pers1:
            st.markdown(f"""
            <div class="blueprint-card" style="min-height:100px;">
                <div class="blueprint-card-label">Persona 1 (Col-4)</div>
                <div class="blueprint-card-title">The Planner (Age 32)</div>
                <div class="blueprint-card-text">Demands high-density overview widgets, multi-select rows, and fast keyboard accelerators.</div>
            </div>
            """, unsafe_allow_html=True)
        with col_pers2:
            st.markdown(f"""
            <div class="blueprint-card" style="min-height:100px;">
                <div class="blueprint-card-label">Persona 2 (Col-4)</div>
                <div class="blueprint-card-title">The Explorer (Age 24)</div>
                <div class="blueprint-card-text">Requires simplified layout steps, visual progress cues, and deep tooltips.</div>
            </div>
            """, unsafe_allow_html=True)
        with col_pers3:
            st.markdown(f"""
            <div class="blueprint-card" style="min-height:100px;">
                <div class="blueprint-card-label">Persona 3 (Col-4)</div>
                <div class="blueprint-card-title">The Admin (Age 45)</div>
                <div class="blueprint-card-text">Needs export options (CSV/JSON), historical audit feeds, and robust data integrity checks.</div>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.discipline == "Industrial Blueprint":
        # Row 1: Exploded view drawing and technical dimensions
        col_cad, col_specs, col_rad = st.columns([2, 1, 1])
        with col_cad:
            st.markdown(f"""
            <div class="blueprint-card" style="min-height:160px; border-color: #7C3AED;">
                <div class="blueprint-card-label" style="border-color: #7C3AED; color: #7C3AED;">CAD Exploded Assembly Spec (Col-6)</div>
                <div class="blueprint-card-title" style="color: #7C3AED;">ISOMETRIC SCHEMATIC VIEWS</div>
                <div class="blueprint-card-text">
                    Blueprint specs for mechanical casing alignment.<br>
                    <strong>Length:</strong> 180.00mm &bull; <strong>Width:</strong> 120.00mm &bull; <strong>Height:</strong> 42.00mm<br>
                    <strong>Process:</strong> 5-Axis Milling CNC extrusion mapping.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_specs:
            st.markdown(f"""
            <div class="blueprint-card" style="min-height:160px;">
                <div class="blueprint-card-label">PCB Core Specs (Col-3)</div>
                <div class="blueprint-card-title">Electrical Layout</div>
                <div class="blueprint-card-text">
                    Core processor mounting details.<br>
                    <strong>CPU:</strong> ARM Cortex-M4<br>
                    <strong>Power:</strong> 3.3V DC Input<br>
                    <strong>Pins:</strong> 48-Pin QFN package
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_rad:
            st.markdown(f"""
            <div class="blueprint-card" style="min-height:160px;">
                <div class="blueprint-card-label">Dimensions (Col-3)</div>
                <div class="blueprint-card-title">Physical Fillets</div>
                <div class="blueprint-card-text">
                    Enclosure design dimensions.<br>
                    <strong>Corner Fillets:</strong> R8.0mm<br>
                    <strong>Tolerance:</strong> &plusmn;0.05mm<br>
                    <strong>Sealing:</strong> IP67 Silicone
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Row 2: Fabrication schedule & materials table
        st.markdown(f"""
        <div class="blueprint-card" style="min-height:130px;">
            <div class="blueprint-card-label">Fabrication Schedule Grid (Col-12)</div>
            <table style="width: 100%; border-collapse: collapse; font-family: 'Fira Code', monospace; font-size: 11px; margin-top: 8px; text-align: left;">
                <thead>
                    <tr style="border-bottom: 2px solid #7C3AED; color: #7C3AED;">
                        <th style="padding: 6px 0;">PART ID</th>
                        <th style="padding: 6px 0;">MATERIAL SUBSTRATE</th>
                        <th style="padding: 6px 0;">FABRICATION PROCESS</th>
                        <th style="padding: 6px 0; text-align: right;">QUANTITY</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom: 1px solid #2D2D35;">
                        <td style="padding: 6px 0;">DF-CASE-01</td>
                        <td>Aluminum 6061-T6 Case Enclosure</td>
                        <td>CNC Anodized Bead Blast</td>
                        <td style="text-align: right;">1</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #2D2D35;">
                        <td style="padding: 6px 0;">DF-CORE-02</td>
                        <td>Polycarbonate Inner Frame</td>
                        <td>Injection Molding</td>
                        <td style="text-align: right;">1</td>
                    </tr>
                    <tr>
                        <td style="padding: 6px 0;">DF-SEAL-03</td>
                        <td>Fluoroelastomer O-Ring</td>
                        <td>Compression Molded</td>
                        <td style="text-align: right;">2</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

    else:
        # Graphic Editorial: Overlapping asymmetrical column layout grid
        col_ed1, col_ed2, col_ed3 = st.columns([4, 5, 3])
        with col_ed1:
            st.markdown(f"""
            <div class="blueprint-card" style="min-height:180px;">
                <div class="blueprint-card-label">Editorial Statement (Col-4)</div>
                <div class="blueprint-card-title">Typographical Asymmetry</div>
                <div style="font-family: 'Playfair Display', serif; font-size: 20px; line-height: 1.15; color:#F3F4F6; margin: 10px 0 6px 0;">
                    "Form follows function, but style commands emotion."
                </div>
                <div class="blueprint-card-text">Aligning display font sizes with geometric offsets to command the reader's attention focal point.</div>
            </div>
            """, unsafe_allow_html=True)
        with col_ed2:
            st.markdown(f"""
            <div class="blueprint-card" style="min-height:180px; border-color: #7C3AED;">
                <div class="blueprint-card-label" style="border-color: #7C3AED; color: #7C3AED;">Visual Placement (Col-5)</div>
                <div style="border: 1px dashed rgba(156, 163, 175, 0.3); border-radius: 4px; height: 110px; background: linear-gradient(135deg, rgba(26, 26, 30, 0.6) 0%, rgba(124, 58, 237, 0.06) 100%); display: flex; align-items: center; justify-content: center; position: relative;">
                    <svg width="100%" height="100%" style="position: absolute; top:0; left:0;">
                        <line x1="0" y1="0" x2="100%" y2="100%" stroke="rgba(156,163,175,0.1)" />
                        <line x1="100%" y1="0" x2="0" y2="100%" stroke="rgba(156,163,175,0.1)" />
                    </svg>
                    <span style="font-family:'Fira Code'; font-size:10px; color:#9CA3AF; z-index:2;">EDITORIAL_HERO_ASSET.JPG</span>
                </div>
                <div style="font-size: 9px; color:#9CA3AF; margin-top: 6px; text-transform: uppercase;">Image Placeholder Frame (Grid Alignment)</div>
            </div>
            """, unsafe_allow_html=True)
        with col_ed3:
            st.markdown(f"""
            <div class="blueprint-card" style="min-height:180px;">
                <div class="blueprint-card-label">Design Spec (Col-3)</div>
                <div class="blueprint-card-title">Grid Rules</div>
                <div class="blueprint-card-text">
                    Specifying high contrast alignments.<br><br>
                    <strong>Baseline Grid:</strong> 8px Grid<br>
                    <strong>Typographic Scale:</strong> Golden Ratio<br>
                    <strong>Asymmetry Offset:</strong> 15% Left Margin
                </div>
            </div>
            """, unsafe_allow_html=True)

        col_ed_sub1, col_ed_sub2 = st.columns([7, 5])
        with col_ed_sub1:
            st.markdown(f"""
            <div class="blueprint-card" style="min-height:100px;">
                <div class="blueprint-card-label">Caption (Col-7)</div>
                <div class="blueprint-card-title">Editorial Layout Composition</div>
                <div class="blueprint-card-text">
                    By offsetting headers, readers are motivated to navigate through technical tables and text blocks in a progressive hierarchy.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_ed_sub2:
            st.markdown(f"""
            <div class="blueprint-card" style="min-height:100px;">
                <div class="blueprint-card-label">Column Spec (Col-5)</div>
                <div class="blueprint-card-title">Active Colorway Tokens</div>
                <div style="display: flex; gap: 6px; margin-top: 6px;">
                    <div style="width: 16px; height: 16px; background-color: #EF4444; border-radius: 3px;"></div>
                    <div style="width: 16px; height: 16px; background-color: #000000; border-radius: 3px; border:1px solid #2D2D35;"></div>
                    <div style="width: 16px; height: 16px; background-color: #FFFDF9; border-radius: 3px;"></div>
                    <span style="font-family:'Fira Code'; font-size:10px; color:#9CA3AF;">Helvetica Crimson Scheme</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 2: ACTIVE TOKEN INJECTOR (THE VIBE SYSTEM)
# ------------------------------------------------------------------------------
with tab_tokens:
    st.markdown("<h3 style='font-family:\"Space Grotesk\", sans-serif; margin-top:0px;'>🎨 Vibe System Archetype Injector</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:12px; color:#9CA3AF; margin-top:-10px;'>Select a design preset archetype below to inject active colors, typography pairings, and layout rule tokens.</p>", unsafe_allow_html=True)

    # Preset archetype buttons using columns
    col_arc1, col_arc2, col_arc3 = st.columns(3)
    
    with col_arc1:
        if st.button("Futuristic Neo-Tokyo", use_container_width=True):
            st.session_state.archetype = "Futuristic Neo-Tokyo"
    with col_arc2:
        if st.button("Minimalist Scandinavian", use_container_width=True):
            st.session_state.archetype = "Minimalist Scandinavian"
    with col_arc3:
        if st.button("Swiss International", use_container_width=True):
            st.session_state.archetype = "Swiss International"

    # Define the token configurations
    theme_tokens = {
        "Futuristic Neo-Tokyo": {
            "display_font": "Space Grotesk",
            "body_font": "Fira Code",
            "bg_color": "#0F0F13",
            "accent_color": "#D946EF",
            "accent_text": "Neon Magenta",
            "secondary_color": "#06B6D4",
            "secondary_text": "Cyber Cyan",
            "border_style": "1px solid #D946EF",
            "shadow_glow": "box-shadow: 0 0 15px rgba(217, 70, 239, 0.35);",
            "text_shadow": "text-shadow: 0 0 8px rgba(6, 182, 212, 0.6);",
            "rules": "Sharp grid borders, cyberpunk high-contrast highlights, technical matrix monospace layouts."
        },
        "Minimalist Scandinavian": {
            "display_font": "Plus Jakarta Sans",
            "body_font": "Inter",
            "bg_color": "#18181B",
            "accent_color": "#34D399",
            "accent_text": "Soft Forest Green",
            "secondary_color": "#9CA3AF",
            "secondary_text": "Cool Slate",
            "border_style": "1px solid #2D2D35",
            "shadow_glow": "box-shadow: none;",
            "text_shadow": "text-shadow: none;",
            "rules": "Generous letter spacing, organic tones, high white-space ratio, functional content blocks."
        },
        "Swiss International": {
            "display_font": "Playfair Display",
            "body_font": "Lora",
            "bg_color": "#FFFFFF",
            "accent_color": "#EF4444",
            "accent_text": "Helvetica Crimson",
            "secondary_color": "#000000",
            "secondary_text": "Ink Black",
            "border_style": "2px solid #000000",
            "shadow_glow": "box-shadow: 6px 6px 0px #000000;",
            "text_shadow": "text-shadow: none;",
            "rules": "Asymmetrical title alignments, heavy font weighting, minimal borders, architectural content cards."
        }
    }

    active_theme = theme_tokens[st.session_state.archetype]

    # Render Swatch Information & Typography Pairing side-by-side
    col_tinfo, col_tswatch = st.columns([1.2, 1.0])
    
    with col_tinfo:
        st.markdown(f"""
        <div class="blueprint-card" style="margin-top:10px;">
            <div class="blueprint-card-label">Active Archetype</div>
            <div class="blueprint-card-title" style="color:#7C3AED; font-size:18px;">{st.session_state.archetype} Preset</div>
            
            <div style="margin-top: 12px; font-size:12px; line-height:1.6;">
                <strong>Typography Pairing:</strong> {active_theme['display_font']} + {active_theme['body_font']}<br>
                <strong>Active Accent:</strong> <span style="color:{active_theme['accent_color']}; font-weight:600;">{active_theme['accent_text']}</span> ({active_theme['accent_color']})<br>
                <strong>Active Secondary:</strong> <span style="color:{active_theme['secondary_color']}; font-weight:600;">{active_theme['secondary_text']}</span> ({active_theme['secondary_color']})<br>
                <strong>System Layout Rule:</strong> <em>{active_theme['rules']}</em>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_tswatch:
        # Display swatches beautifully
        st.markdown("<h4 style='font-size:1rem; font-family:\"Space Grotesk\", sans-serif; margin-bottom:10px; margin-top:10px;'>🎨 Active Color Token Swatches</h4>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="swatch-item">
            <div>
                <span style="font-size:11px; font-weight:bold; display:block; color:#FFFFFF;">Theme Background</span>
                <span style="font-family:'Fira Code'; font-size:9.5px; color:#9CA3AF;">{active_theme['bg_color']}</span>
            </div>
            <div class="swatch-color-box" style="background-color: {active_theme['bg_color']};"></div>
        </div>
        <div class="swatch-item">
            <div>
                <span style="font-size:11px; font-weight:bold; display:block; color:#FFFFFF;">Primary Accent ({active_theme['accent_text']})</span>
                <span style="font-family:'Fira Code'; font-size:9.5px; color:#9CA3AF;">{active_theme['accent_color']}</span>
            </div>
            <div class="swatch-color-box" style="background-color: {active_theme['accent_color']};"></div>
        </div>
        <div class="swatch-item">
            <div>
                <span style="font-size:11px; font-weight:bold; display:block; color:#FFFFFF;">Secondary Accent ({active_theme['secondary_text']})</span>
                <span style="font-family:'Fira Code'; font-size:9.5px; color:#9CA3AF;">{active_theme['secondary_color']}</span>
            </div>
            <div class="swatch-color-box" style="background-color: {active_theme['secondary_color']};"></div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("<h3 style='font-family:\"Space Grotesk\", sans-serif;'>✍️ Typography Title Injector & Live Preview</h3>", unsafe_allow_html=True)
    
    # Text input field for design title
    project_title_input = st.text_input(
        "Inject Custom Title Spec Text",
        value=st.session_state.project_title,
        key="project_title_input"
    )
    st.session_state.project_title = project_title_input

    # Style mapping and display fonts
    display_family = f"'{active_theme['display_font']}', sans-serif"
    if active_theme['display_font'] in ["Playfair Display"]:
        display_family = f"'{active_theme['display_font']}', serif"
        
    body_family = f"'{active_theme['body_font']}', sans-serif"
    if active_theme['body_font'] in ["Lora"]:
        body_family = f"'{active_theme['body_font']}', serif"
    elif active_theme['body_font'] in ["Fira Code"]:
        body_family = f"'{active_theme['body_font']}', monospace"

    # High fidelity preview card based on active theme
    preview_box_html = f"""
    <div style="background-color: {active_theme['bg_color']}; border: {active_theme['border_style']}; border-radius: 8px; padding: 2.5rem; text-align: center; margin-top: 15px; transition: all 0.3s ease; {active_theme['shadow_glow']}">
        <span style="font-family: 'Fira Code', monospace; font-size: 9px; color: {active_theme['secondary_color']}; text-transform: uppercase; letter-spacing: 0.1em; display: block; margin-bottom: 6px;">[ {st.session_state.archetype.upper()} PREVIEW ]</span>
        <h1 style="font-family: {display_family}; font-size: 2.6rem; font-weight: 700; color: {active_theme['accent_color']}; margin: 0 0 10px 0; line-height: 1.1; {active_theme['text_shadow']}">
            {st.session_state.project_title}
        </h1>
        <p style="font-family: {body_family}; font-size: 11px; color: {active_theme['secondary_color']}; margin: 0 auto; max-width: 60%; line-height: 1.5;">
            This header rendering simulates active font weights, letter heights, and color variables loaded into the local engine memory buffers.
        </p>
    </div>
    """
    
    st.markdown(preview_box_html, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 3: CASE STUDY SEQUENCE MATRIX
# ------------------------------------------------------------------------------
with tab_matrix:
    st.markdown("<h3 style='font-family:\"Space Grotesk\", sans-serif; margin-top:0px;'>🗂️ Sequential Design Timeline Matrix</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:12px; color:#9CA3AF; margin-top:-10px;'>Audit and log portfolio step completions. Toggling tasks dynamically pushes progression percentages.</p>", unsafe_allow_html=True)

    col_chk, col_pbar = st.columns([1.1, 1.0])
    
    with col_chk:
        st.markdown("<h4 style='font-size:1rem; font-family:\"Space Grotesk\", sans-serif; margin-bottom:10px;'>📋 Design Progress Checkpoints</h4>", unsafe_allow_html=True)
        
        # Checkpoint Toggles
        check_research = st.checkbox("Phase 1: Deep User Research Complete", value=st.session_state.check_research, key="chk_research")
        check_wireframe = st.checkbox("Phase 2: Wireframe Systems Validated", value=st.session_state.check_wireframe, key="chk_wireframe")
        check_hifi = st.checkbox("Phase 3: High-Fi Component Spec Defined", value=st.session_state.check_hifi, key="chk_hifi")
        check_spec = st.checkbox("Phase 4: Design Token Spec Approved & Exported", value=st.session_state.check_spec, key="chk_spec")
        
        # Save updates to session state
        st.session_state.check_research = check_research
        st.session_state.check_wireframe = check_wireframe
        st.session_state.check_hifi = check_hifi
        st.session_state.check_spec = check_spec

    # Calculate completion percentage
    total_checks = 4
    completed_checks = sum([
        1 if st.session_state.check_research else 0,
        1 if st.session_state.check_wireframe else 0,
        1 if st.session_state.check_hifi else 0,
        1 if st.session_state.check_spec else 0
    ])
    
    progress_percentage = int((completed_checks / total_checks) * 100)

    with col_pbar:
        st.markdown("<h4 style='font-size:1rem; font-family:\"Space Grotesk\", sans-serif; margin-bottom:10px;'>📊 System Pipeline Progress</h4>", unsafe_allow_html=True)
        
        # Render the streamlit progress bar
        st.progress(progress_percentage / 100.0)
        st.markdown(f"<div style='font-family:\"Fira Code\", monospace; font-size:12px; margin-top:5px; text-align:right;'>COMPLETION RATIO: <strong>{progress_percentage}%</strong></div>", unsafe_allow_html=True)
        
        st.write("")
        
        # Render color-coded validation banners based on status
        if progress_percentage == 0:
            banner_html = """
            <div class="validation-banner" style="background-color: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.4); color: #FCA5A5;">
                🔴 <strong>Pipeline Inactive:</strong> Please initiate phase 1 tasks and log progress to unlock design tokens.
            </div>
            """
        elif progress_percentage <= 50:
            banner_html = f"""
            <div class="validation-banner" style="background-color: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.4); color: #FDE047;">
                🟡 <strong>Pipeline In Progress:</strong> {completed_checks}/{total_checks} phases complete. Foundation design research validated.
            </div>
            """
        elif progress_percentage < 100:
            banner_html = f"""
            <div class="validation-banner" style="background-color: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.4); color: #93C5FD;">
                🔵 <strong>System Spec Stage:</strong> {completed_checks}/{total_checks} phases complete. High-fidelity layouts and font token tables under validation.
            </div>
            """
        else:
            banner_html = """
            <div class="validation-banner" style="background-color: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.4); color: #6EE7B7;">
                🟢 <strong>System Validated:</strong> 100% complete! Design tokens and layouts fully verified for export deployment.
            </div>
            """
            
        st.markdown(banner_html, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 5. GLOBAL CONFIGURATION PROFILE DUMP (BOTTOM ACTION)
# ------------------------------------------------------------------------------
st.write("---")
st.markdown("### 📦 Active Engine Configuration JSON Dump")

# Generate JSON configuration profile mapping active state variables
config_dump = {
    "engineName": "DesignForge Blueprint Engine",
    "version": "2.0.0",
    "state": {
        "discipline": st.session_state.discipline,
        "gutterSpacingPx": st.session_state.gutter_spacing,
        "archetype": st.session_state.archetype,
        "projectTitle": st.session_state.project_title,
        "pipelineProgressPercent": progress_percentage,
        "themeTokens": {
            "displayFont": active_theme["display_font"],
            "bodyFont": active_theme["body_font"],
            "accentHex": active_theme["accent_color"],
            "secondaryHex": active_theme["secondary_color"]
        }
    }
}

st.code(json.dumps(config_dump, indent=2), language="json")
