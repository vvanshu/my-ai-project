import streamlit as st
import json

# ==============================================================================
# 1. PAGE SETUP & MINIMALIST IVORY THEME CONFIG
# ==============================================================================
st.set_page_config(
    page_title="DesignForge // Copywriter Engine",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom light ivory stylesheet with futuristic typography & pastel highlights
IVORY_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Syne:wght@600;700;800&display=swap');

/* Base layout styling */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #FAF9F5 !important;
    color: #2D2D30 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Sidebar styling overrides */
[data-testid="stSidebar"] {
    background-color: #F3F2EC !important;
    border-right: 1px solid #E2E1D8 !important;
}
[data-testid="stSidebar"] .stMarkdown h1, 
[data-testid="stSidebar"] .stMarkdown h2, 
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #2D2D30 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Streamlit form input controls overrides */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E1D8 !important;
    color: #2D2D30 !important;
    border-radius: 6px !important;
}
div[role="listbox"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E1D8 !important;
}
div[role="option"] {
    color: #2D2D30 !important;
    background-color: #FFFFFF !important;
}
div[role="option"]:hover, div[role="option"][aria-selected="true"] {
    background-color: #E8DBFD !important;
    color: #4A1D96 !important;
}
.stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #2D2D30 !important;
    border: 1px solid #E2E1D8 !important;
    border-radius: 6px !important;
}

/* Primary actions button styling */
.stButton>button {
    background-color: #8B5CF6 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.6rem 1.5rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stButton>button:hover {
    background-color: #7C3AED !important;
    box-shadow: 0 4px 14px rgba(139, 92, 246, 0.25) !important;
}

/* Copywriter Headers */
.engine-header {
    margin-bottom: 2rem;
    border-bottom: 1px solid #E2E1D8;
    padding-bottom: 1.5rem;
}
.engine-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #2D2D30 40%, #8B5CF6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.engine-subtitle {
    font-size: 0.95rem;
    color: #7C808C;
    margin-top: 0.2rem;
}

/* Visual Card Surfaces */
.ivory-panel {
    background-color: #FFFFFF;
    border: 1px solid #E2E1D8;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}
.ivory-panel-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: #2D2D30;
    margin-bottom: 12px;
    border-bottom: 1px solid #F3F2EC;
    padding-bottom: 6px;
}

/* Pastel Highlight Containers */
.pastel-badge {
    display: inline-block;
    padding: 2px 8px;
    font-family: 'Fira Code', monospace;
    font-size: 10px;
    border-radius: 4px;
    font-weight: 500;
}
.badge-lavender {
    background-color: #F3E8FF;
    color: #6B21A8;
    border: 1px solid #D8B4FE;
}
.badge-mint {
    background-color: #ECFDF5;
    color: #065F46;
    border: 1px solid #A7F3D0;
}
.badge-sky {
    background-color: #E0F2FE;
    color: #075985;
    border: 1px solid #BAE6FD;
}
.badge-rose {
    background-color: #FFF1F2;
    color: #9F1239;
    border: 1px solid #FECDD3;
}

/* Metric card widgets */
.metric-layout-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 1.5rem;
}
.metric-stat-card {
    padding: 1.2rem;
    border-radius: 8px;
    text-align: center;
}

/* Preformatted Copy Viewport */
.copy-viewport {
    background-color: #FAF9F5;
    border: 1px dashed #E2E1D8;
    border-radius: 6px;
    padding: 1.25rem;
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    color: #2D2D30;
    line-height: 1.6;
    white-space: pre-wrap;
    margin-bottom: 12px;
}
</style>
"""
st.markdown(IVORY_THEME_CSS, unsafe_allow_html=True)

# ==============================================================================
# 2. STATE MANAGEMENT & SESSION SYSTEM
# ==============================================================================
valid_archetypes = ["The Failure-to-Success Journey", "The Unpopular Opinion", "The Tactical Playbook"]
if 'archetype' not in st.session_state or st.session_state.archetype not in valid_archetypes:
    st.session_state.archetype = "The Failure-to-Success Journey"


if 'user_notes' not in st.session_state:
    st.session_state.user_notes = "I spent 3 years trying to build micro-saas tools. Most of them failed to gain users because I focused entirely on design instead of distribution. Finally pivoted to local client services, launched in 2 weeks, and earned $12k in monthly recurring revenue."

if 'transformed_output' not in st.session_state:
    st.session_state.transformed_output = ""

if 'hooks' not in st.session_state:
    st.session_state.hooks = []

if 'ctas' not in st.session_state:
    st.session_state.ctas = []

if 'metrics' not in st.session_state:
    st.session_state.metrics = {
        "characters": 0,
        "words": 0,
        "runtime_seconds": 0,
        "readability_score": 0.0,
        "readability_label": "Uncalculated"
    }

# ==============================================================================
# 3. TEXT TRANSFORMATION ENGINE METRICS & TEMPLATES
# ==============================================================================
# Templates definitions mapping dropdown selections
templates = {
    "The Failure-to-Success Journey": {
        "template": """🚀 I wasted years before figuring this out.

Here is the raw truth about what I learned:

{UserContext}

Here is how you can skip my mistakes:
1. THE MYTH: Build it and they will come.
2. THE PIVOT: Speed-to-market beats aesthetic perfection every single time.
3. THE OUTCOME: Focus on direct feedback loops and build distribution first.

Save this list before starting your next iteration loop.""",
        "hooks": [
            "I spent 36 months failing at this so you can learn it in 30 seconds.",
            "The hardest pill to swallow: perfectionism is just masked fear.",
            "If your project takes more than 3 weeks to launch, you are building the wrong thing."
        ],
        "ctas": [
            "💬 What was your biggest design project failure? Let's discuss in the comments.",
            "🔄 Repost this to save another developer from wasting months."
        ]
    },
    "The Unpopular Opinion": {
        "template": """💡 Unpopular opinion: Most creators are doing this completely backwards.

The mainstream advice is setting you up for failure:

{UserContext}

Stop trying to follow standard manuals.
- Standard guidelines keep your layouts generic.
- Real progress comes from high-impact asymmetric focus.
- Validate the value first, optimize layout code second.

Do you agree or disagree with this workflow?""",
        "hooks": [
            "Most design playbooks are written for massive teams, not solo builders.",
            "Why polishing code syntax is the absolute worst way to start an application.",
            "Quiet distribution beats visual perfection every single week."
        ],
        "ctas": [
            "💬 Agree or disagree? Let me know your thoughts below.",
            "📥 Bookmark this guideline for your next retrospective meeting."
        ]
    },
    "The Tactical Playbook": {
        "template": """🛠️ Stop searching for shortcuts. Here is the step-by-step tactical playbook:

The blueprint logic behind this process:

{UserContext}

Here is the exact checklist to execute:
- PHASE 1: Audit and list baseline bottlenecks.
- PHASE 2: Strip non-essential code buffers.
- PHASE 3: Design a clean layout interface matching active states.
- PHASE 4: Gather feedback, commit variables, and push to main.

Bookmark this guide. You'll need it when you execute:""",
        "hooks": [
            "The exact 4-phase playbook I use to validate and ship layouts.",
            "Stop guessing what works. Use this checklist on your next project.",
            "A repeatable framework to move from raw notes to deployable specs."
        ],
        "ctas": [
            "📌 Save this post so it's handy when you run your next Git sync.",
            "💬 Which phase are you currently stuck on? Let's break it down."
        ]
    }
}

# Core function to execute text transformation and recalculate metrics reactively
def transform_content():
    raw_notes = st.session_state.user_notes.strip()
    
    # Pre-select matching archetype data
    active_archetype = st.session_state.archetype
    archetype_data = templates[active_archetype]
    
    # Default placeholder text if user notes are empty
    if not raw_notes:
        raw_notes = "[Please insert raw notes context in the sidebar input box]"
        
    # Inject context into template
    transformed = archetype_data["template"].format(UserContext=raw_notes)
    
    st.session_state.transformed_output = transformed
    st.session_state.hooks = archetype_data["hooks"]
    st.session_state.ctas = archetype_data["ctas"]
    
    # Calculate word and character metrics
    word_count = len(transformed.split())
    char_count = len(transformed)
    
    # Reading Speed Estimate: Average adult reads ~220 WPM
    runtime_seconds = max(1, int((word_count / 220) * 60))
    
    # Robust readability calculator approximation (Flesch Reading Ease style)
    sentences_count = max(1, transformed.count('.') + transformed.count('!') + transformed.count('?'))
    syllables_count = int(char_count / 4.7)  # Typical syllable multiplier
    
    # Calculate Flesch Reading Ease score
    readability = 206.835 - 1.015 * (word_count / sentences_count) - 84.6 * (syllables_count / word_count)
    readability = max(0.0, min(100.0, readability))
    
    # Mapped readability label classification
    if readability >= 90:
        label = "Very Easy (5th Grade level)"
    elif readability >= 70:
        label = "Easy Conversational"
    elif readability >= 50:
        label = "Standard / Moderate"
    elif readability >= 30:
        label = "Difficult (Academic)"
    else:
        label = "Very Confusing / Technical"
        
    st.session_state.metrics = {
        "characters": char_count,
        "words": word_count,
        "runtime_seconds": runtime_seconds,
        "readability_score": round(readability, 1),
        "readability_label": label
    }

# ==============================================================================
# 4. MAIN PANEL NAVIGATION & DISPLAY
# ==============================================================================
# Sidebar parameters
st.sidebar.write("### 🎛️ Engine Configuration")

selected_archetype = st.sidebar.selectbox(
    "Select Copy Archetype",
    valid_archetypes,
    index=valid_archetypes.index(st.session_state.archetype),
    key="selected_archetype"
)
st.session_state.archetype = selected_archetype

user_notes_input = st.sidebar.text_area(
    "Insert Raw Context Notes",
    value=st.session_state.user_notes,
    height=200,
    key="notes_input"
)
st.session_state.user_notes = user_notes_input

# Transform Action Button inside sidebar
if st.sidebar.button("Transform Content", use_container_width=True):
    transform_content()

# Ensure we run initial transformation if state empty
if not st.session_state.transformed_output:
    transform_content()

# Header display title
st.markdown(f"""
<div class="engine-header">
    <div class="engine-title">DesignForge Copywriter Engine</div>
    <div class="engine-subtitle">Minimalist Ivory Layout • Reactive Transformation Engine</div>
</div>
""", unsafe_allow_html=True)

# Main Grid layout: Left Column = Transformed Copy block, Right Column = Hooks & CTAs
col_output, col_info = st.columns([1.6, 1.0])

with col_output:
    st.markdown("<h3 style='font-family:\"Space Grotesk\", sans-serif; margin-top:0px;'>📝 Transformed Output Blueprint</h3>", unsafe_allow_html=True)
    
    # Renders the dynamic stats metrics inside a pastel horizontal layout grid
    st.markdown(f"""
    <div class="metric-layout-grid">
        <div class="metric-stat-card badge-lavender">
            <span style="font-family:'Fira Code'; font-size:9px; text-transform:uppercase; display:block; margin-bottom:4px;">Composition Metrics</span>
            <span style="font-family:'Space Grotesk'; font-size:18px; font-weight:bold;">{st.session_state.metrics['words']} Words</span>
            <span style="font-size:10px; display:block; margin-top:2px; color:rgba(107,33,168,0.7);">{st.session_state.metrics['characters']} Characters</span>
        </div>
        <div class="metric-stat-card badge-mint">
            <span style="font-family:'Fira Code'; font-size:9px; text-transform:uppercase; display:block; margin-bottom:4px;">Read Time</span>
            <span style="font-family:'Space Grotesk'; font-size:18px; font-weight:bold;">{st.session_state.metrics['runtime_seconds']} Seconds</span>
            <span style="font-size:10px; display:block; margin-top:2px; color:rgba(6,95,70,0.7);">Estimated runtime</span>
        </div>
        <div class="metric-stat-card badge-sky">
            <span style="font-family:'Fira Code'; font-size:9px; text-transform:uppercase; display:block; margin-bottom:4px;">Readability Score</span>
            <span style="font-family:'Space Grotesk'; font-size:18px; font-weight:bold;">{st.session_state.metrics['readability_score']}/100</span>
            <span style="font-size:9px; display:block; margin-top:2px; color:rgba(7,89,133,0.7); font-weight:bold;">{st.session_state.metrics['readability_label']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Output content viewport wrapper
    st.markdown(f"""
    <div class="ivory-panel" style="margin-top:10px;">
        <div class="ivory-panel-title">TRANSFORMED COPY TEXT</div>
        <div class="copy-viewport">{st.session_state.transformed_output}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Download Action for output text
    st.download_button(
        label="Download Text Copy",
        data=st.session_state.transformed_output,
        file_name="designforge_copy_blueprint.txt",
        mime="text/plain"
    )

with col_info:
    # Scroll stopping Hook recommendations
    st.markdown("<h3 style='font-family:\"Space Grotesk\", sans-serif; margin-top:0px;'>⚡ Hook Variants</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px; color:#7C808C; margin-top:-10px;'>Scroll-stopping hook variants generated for active archetype.</p>", unsafe_allow_html=True)
    
    hook_html = ""
    for idx, h in enumerate(st.session_state.hooks, start=1):
        hook_html += f"""
        <div class="ivory-panel" style="padding:1rem; margin-bottom:10px; border-left:4px solid #8B5CF6;">
            <span class="pastel-badge badge-lavender" style="margin-bottom:6px;">Hook Variant 0{idx}</span>
            <div style="font-size:12px; color:#2D2D30; line-height:1.4; font-weight:500;">"{h}"</div>
        </div>
        """
    st.markdown(hook_html, unsafe_allow_html=True)
    
    st.write("")
    
    # Engagement CTAs
    st.markdown("<h3 style='font-family:\"Space Grotesk\", sans-serif; margin-top:10px;'>📣 Engagement CTAs</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px; color:#7C808C; margin-top:-10px;'>Recommended Call-To-Action closures to boost content conversions.</p>", unsafe_allow_html=True)
    
    cta_html = ""
    for idx, c in enumerate(st.session_state.ctas, start=1):
        cta_html += f"""
        <div class="ivory-panel" style="padding:1rem; margin-bottom:10px; border-left:4px solid #34D399;">
            <span class="pastel-badge badge-mint" style="margin-bottom:6px;">CTA Variant 0{idx}</span>
            <div style="font-size:12px; color:#2D2D30; line-height:1.4; font-weight:500;">{c}</div>
        </div>
        """
    st.markdown(cta_html, unsafe_allow_html=True)
    
    # System Details panel
    st.markdown(f"""
    <div class="ivory-panel" style="margin-top:15px; background-color:#F3F2EC; border-color:#E2E1D8;">
        <div class="ivory-panel-title" style="border-bottom:1px solid #E2E1D8;">🔧 Blueprint Engine Metadata</div>
        <div style="font-family:'Fira Code', monospace; font-size:10px; color:#2D2D30; line-height:1.5;">
            <strong>ARCHETYPE:</strong> {st.session_state.archetype}<br>
            <strong>WORDS:</strong> {st.session_state.metrics['words']}<br>
            <strong>READABILITY:</strong> {st.session_state.metrics['readability_score']}<br>
            <strong>RUN TIME:</strong> {st.session_state.metrics['runtime_seconds']}s
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 5. GLOBAL CONFIGURATION PROFILE DUMP (BOTTOM ACTION)
# ==============================================================================
st.write("---")
st.markdown("### 📥 Active Export JSON Spec Map")
json_config = {
    "engineName": "DesignForge Copywriter Engine",
    "version": "1.0.0",
    "configuration": {
        "activeArchetype": st.session_state.archetype,
        "inputWordCount": len(st.session_state.user_notes.split()),
        "outputMetrics": st.session_state.metrics,
        "previewOutput": st.session_state.transformed_output
    }
}
st.code(json.dumps(json_config, indent=2), language="json")
