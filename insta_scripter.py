import streamlit as st
import os
import io
import re
import tempfile
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# ---------------------------------------------------------
# Page Configurations & Setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="InstaScripter // Viral Reel Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# Modern Maximalist Styling (Custom CSS Injection)
# ---------------------------------------------------------
def inject_maximalist_css():
    st.markdown("""
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');

    /* Global Canvas Reset */
    .stApp {
        background-color: #F9F9F9 !important;
        color: #111111 !important;
        font-family: 'Outfit', sans-serif !important;
    }

    /* Chunky Typography styles */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 900 !important;
        color: #111111 !important;
        letter-spacing: -0.5px !important;
        text-transform: uppercase !important;
        margin-top: 10px !important;
        margin-bottom: 15px !important;
    }

    h1 {
        font-size: 3.5rem !important;
        border-bottom: 5px solid #111111;
        padding-bottom: 10px;
        margin-bottom: 30px !important;
        display: inline-block;
    }

    h2 {
        font-size: 2rem !important;
        border-bottom: 3px solid #111111;
        padding-bottom: 5px;
    }

    /* Container blocks with heavy borders */
    .max-card {
        background-color: #FFFFFF !important;
        border: 3px solid #111111 !important;
        padding: 25px !important;
        margin-bottom: 25px !important;
        border-radius: 0px !important;
        box-shadow: 6px 6px 0px 0px #111111 !important;
    }

    /* Highlight card with Instagram Gradients */
    .gradient-header {
        background: linear-gradient(45deg, #833AB4, #E1306C, #F56040) !important;
        color: #FFFFFF !important;
        border: 3px solid #111111 !important;
        padding: 30px !important;
        border-radius: 0px !important;
        box-shadow: 6px 6px 0px 0px #111111 !important;
        margin-bottom: 30px !important;
    }

    .gradient-header h1, .gradient-header p {
        color: #FFFFFF !important;
        border-bottom: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Accent Badges */
    .max-badge {
        display: inline-block;
        padding: 5px 12px;
        background-color: #E1306C;
        color: #FFFFFF;
        font-weight: 700;
        text-transform: uppercase;
        border: 2px solid #111111;
        box-shadow: 2px 2px 0px 0px #111111;
        font-size: 0.8rem;
        margin-right: 10px;
        margin-bottom: 10px;
    }

    .max-badge-purple {
        background-color: #833AB4;
    }

    .max-badge-orange {
        background-color: #F56040;
    }

    /* Custom Streamlit Tabs style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent !important;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        background-color: #FFFFFF !important;
        border: 3px solid #111111 !important;
        border-bottom: none !important;
        border-radius: 0px !important;
        padding: 12px 24px !important;
        color: #111111 !important;
        box-shadow: 3px -3px 0px 0px #111111 !important;
        transition: all 0.15s ease-in-out;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #F56040 !important;
        color: #FFFFFF !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #E1306C, #F56040) !important;
        color: #FFFFFF !important;
        box-shadow: 3px -3px 0px 0px #833AB4 !important;
    }

    /* Custom Input and TextArea widgets */
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        border: 3px solid #111111 !important;
        border-radius: 0px !important;
        color: #111111 !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 1rem !important;
        padding: 15px !important;
        box-shadow: inset 2px 2px 0px 0px rgba(0,0,0,0.1) !important;
    }

    .stTextArea textarea:focus {
        border-color: #E1306C !important;
        box-shadow: 4px 4px 0px 0px #111111 !important;
    }

    /* Button Styling */
    div.stButton > button {
        background-color: #111111 !important;
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        border: 3px solid #111111 !important;
        border-radius: 0px !important;
        padding: 15px 35px !important;
        text-transform: uppercase !important;
        width: 100% !important;
        box-shadow: 5px 5px 0px 0px #F56040 !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button:hover {
        background: linear-gradient(45deg, #833AB4, #E1306C, #F56040) !important;
        color: #FFFFFF !important;
        box-shadow: 5px 5px 0px 0px #111111 !important;
        transform: translate(-3px, -3px) !important;
    }

    div.stButton > button:active {
        transform: translate(2px, 2px) !important;
        box-shadow: 1px 1px 0px 0px #111111 !important;
    }

    /* File uploader custom borders */
    div[data-testid="stFileUploader"] {
        border: 3px dashed #111111 !important;
        background-color: #FFFFFF !important;
        border-radius: 0px !important;
        padding: 20px !important;
        box-shadow: 4px 4px 0px 0px #111111 !important;
    }

    /* Audio Preview container */
    .stAudio {
        border: 3px solid #111111 !important;
        background-color: #FFFFFF !important;
        padding: 10px !important;
        border-radius: 0px !important;
        box-shadow: 4px 4px 0px 0px #833AB4 !important;
    }

    /* Code & Timeline display */
    .timeline-item {
        border-left: 4px solid #111111;
        padding-left: 20px;
        margin-bottom: 20px;
        position: relative;
    }

    .timeline-item::before {
        content: '';
        position: absolute;
        left: -12px;
        top: 0px;
        width: 20px;
        height: 20px;
        background-color: #F56040;
        border: 3px solid #111111;
    }

    /* Footnotes and developer branding */
    .max-footer {
        text-align: center;
        border-top: 3px solid #111111;
        margin-top: 50px;
        padding-top: 20px;
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
    }

    /* High contrast text accessibility rules */
    div[data-testid="stRadio"] label p, 
    div[data-testid="stRadio"] label span, 
    div[data-testid="stRadio"] div,
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stFileUploader"] p,
    div[data-testid="stFileUploader"] span,
    div[data-testid="stFileUploader"] small,
    .max-card p,
    .max-card label,
    .max-card span:not(.max-badge) {
        color: #111111 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
def init_session_state():
    if "raw_context" not in st.session_state:
        st.session_state.raw_context = ""
    if "vibe_format" not in st.session_state:
        st.session_state.vibe_format = "The 3-Second Viral Loop"
    if "uploaded_video_info" not in st.session_state:
        st.session_state.uploaded_video_info = None
    if "script_generated" not in st.session_state:
        st.session_state.script_generated = False
    if "viral_script" not in st.session_state:
        st.session_state.viral_script = ""
    if "storyboard_list" not in st.session_state:
        st.session_state.storyboard_list = []
    if "audio_bytes" not in st.session_state:
        st.session_state.audio_bytes = None

init_session_state()
inject_maximalist_css()

# ---------------------------------------------------------
# Core Reframer & Spelling/Grammar Clean Engine
# ---------------------------------------------------------
def clean_text_grammar(text):
    """
    Cleans common grammar issues, spelling mistakes, run-ons, 
    and handles basic casing rules.
    """
    if not text.strip():
        return ""
    
    # Common slang to standard conversion
    rules = {
        r"\bteh\b": "the",
        r"\brecieve\b": "receive",
        r"\bseperate\b": "separate",
        r"\bgonna\b": "going to",
        r"\bwanna\b": "want to",
        r"\bgotta\b": "got to",
        r"\bi\b": "I",
        r"\burs\b": "yours",
        r"\bu\b": "you",
        r"\br\b": "are",
        r"\by\b": "why",
        r"\btho\b": "though",
    }
    
    cleaned = text
    for pattern, replacement in rules.items():
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
    
    # Clean run-on punctuation
    cleaned = re.sub(r'\.{4,}', '...', cleaned)  # long dots to standard ellipsis
    cleaned = re.sub(r',{2,}', ',', cleaned)      # double commas
    cleaned = re.sub(r'\?{2,}', '?', cleaned)      # double question marks
    cleaned = re.sub(r'!{2,}', '!', cleaned)      # double exclamation marks
    cleaned = re.sub(r'\s+', ' ', cleaned)        # fix double spaces
    
    # Simple Sentence Capitalization
    sentences = re.split(r'([.!?]\s*)', cleaned)
    capitalized_sentences = []
    for i, part in enumerate(sentences):
        if i % 2 == 0 and part:  # actual text, not the delimiter
            # Capitalize first character
            part = part.strip()
            if part:
                part = part[0].upper() + part[1:]
        capitalized_sentences.append(part)
    
    return "".join(capitalized_sentences).strip()

def generate_insta_script(cleaned_context, format_type):
    """
    Reframes clean context into mobile-optimized scripts with explicit pacing/storyboard cues.
    """
    if not cleaned_context.strip():
        cleaned_context = "Create something inspiring out of thin air."

    # Split thoughts into mini fragments to extract hook, value, and loop points
    thoughts = [t.strip() for t in re.split(r'[.!?]', cleaned_context) if t.strip()]
    if len(thoughts) < 1:
        thoughts = [cleaned_context]
    
    hook = thoughts[0]
    core_value = thoughts[1] if len(thoughts) > 1 else thoughts[0]
    cta = thoughts[-1] if len(thoughts) > 2 else "Drop a comment and follow for more!"

    script_parts = []
    storyboard = []

    if format_type == "The 3-Second Viral Loop":
        # Ultra fast loop format
        script_parts = [
            f"[00:00 - HOOK INJECTED (HIGH RETENTION)]\n👉 \"{hook.upper()}...\"",
            f"[00:02 - VALUE REVEAL (FAST PACED)]\n💡 \"This is exactly why {core_value.lower()}\"",
            f"[00:03 - LOOP TRICK]\n🔄 \"...and that's the secret to why you should\""
        ]
        storyboard = [
            {
                "time": "00:00 - 00:01",
                "cue": "Visual text hook on screen. Dynamic zoom-in. Face to camera, high energy.",
                "framing": "Extreme Close-Up (ECU)",
                "pacing": "Immediate cut"
            },
            {
                "time": "00:01 - 00:02",
                "cue": "Quick B-roll transition showcasing key action or data graph overlay.",
                "framing": "Medium Shot (MS)",
                "pacing": "Rapid slide transition"
            },
            {
                "time": "00:02 - 00:03",
                "cue": "Loop transition: Action matches the start frame seamlessly.",
                "framing": "Close-Up (CU)",
                "pacing": "Seamless loop transition"
            }
        ]
        
    elif format_type == "The High-Value Educational Carousel":
        script_parts = [
            f"[00:00 - IMPACT HOOK]\n🔥 \"Listen up: {hook}. Here is the exact checklist you need right now.\"",
            f"[00:08 - INSIGHT 1]\n📌 \"Step 1: Focus on how {core_value.lower()}. Avoid common mistakes.\"",
            f"[00:15 - INSIGHT 2]\n📌 \"Step 2: Take action immediately. Consistency beat talent every time.\"",
            f"[00:22 - STRONG CALL-TO-ACTION]\n📣 \"Save this Reel for later and tap follow for daily updates.\""
        ]
        storyboard = [
            {
                "time": "00:00 - 00:05",
                "cue": "Text overlay reads: 'THE ULTIMATE CHECKLIST FOR CREATORS'. Hand gestures pointing up.",
                "framing": "Medium Close-Up (MCU)",
                "pacing": "Dynamic scale in"
            },
            {
                "time": "00:05 - 00:15",
                "cue": "Point-by-point overlay graphics appearing in sync with audio.",
                "framing": "Wide Shot (WS) with split screen",
                "pacing": "Smooth slide-in"
            },
            {
                "time": "00:15 - 00:22",
                "cue": "Direct address to camera, point to 'Save' button location visually.",
                "framing": "Close-Up (CU)",
                "pacing": "Jump cut"
            }
        ]
        
    else:  # "The Raw Aesthetic Storytelling Vlog"
        script_parts = [
            f"[00:00 - ATMOSPHERIC HOOK]\n✨ \"Let's be honest for a second. {hook}.\"",
            f"[00:07 - NARRATIVE JOURNEY]\n🌿 \"Most people don't see the behind-the-scenes work. But here is the truth: {core_value.lower()}. It takes effort.\"",
            f"[00:20 - CLIMAX / OUTRO]\n💬 \"If this resonated with you, let me know in the comments below. Let's grow together.\""
        ]
        storyboard = [
            {
                "time": "00:00 - 00:07",
                "cue": "Slow cinematic panning shot. Moody color grading (warm tone). Low light.",
                "framing": "Extreme Wide Shot (EWS)",
                "pacing": "Slow cross-dissolve"
            },
            {
                "time": "00:07 - 00:20",
                "cue": "ASMR sound overlay: typing, nature sounds, or coffee pouring. Minimalist background.",
                "framing": "Detail Detail Shot (Macro)",
                "pacing": "Soft cut"
            },
            {
                "time": "00:20 - 00:30",
                "cue": "Writer looking out window, fading out to black with script text watermark.",
                "framing": "Medium Shot (MS)",
                "pacing": "Slow fade-out"
            }
        ]

    full_script = "\n\n".join(script_parts)
    return full_script, storyboard

# ---------------------------------------------------------
# Video File Properties Reader & Mock Parser
# ---------------------------------------------------------
def read_video_properties(uploaded_file):
    if uploaded_file is None:
        return None
    
    # Get basic file attributes
    file_name = uploaded_file.name
    file_size_mb = uploaded_file.size / (1024 * 1024)
    file_type = uploaded_file.type
    
    # Calculate mock video properties based on size to be predictable yet realistic
    # Let's say ~2.5 MB per second for 1080p video at 30fps
    mock_duration = max(3.0, round(file_size_mb * 0.8, 1))
    
    # If the user selected the 3-second loop, clamp the mock duration for realism
    if st.session_state.vibe_format == "The 3-Second Viral Loop":
        mock_duration = min(5.0, mock_duration)
        
    mock_resolution = "1080 x 1920 (Vertical Reels Standard)"
    mock_fps = 30
    
    return {
        "filename": file_name,
        "size_mb": round(file_size_mb, 2),
        "type": file_type,
        "duration": mock_duration,
        "resolution": mock_resolution,
        "fps": mock_fps
    }

# ---------------------------------------------------------
# Layout: Header Banner
# ---------------------------------------------------------
st.markdown("""
<div class="gradient-header">
    <h1 style="font-size: 3rem; margin:0px;">🎬 INSTASCRIPTER</h1>
    <p style="font-family: 'Space Mono', monospace; font-size: 1.1rem; margin-top: 10px; font-weight: bold;">
        RAW CONCEPT TRANSFORMATION ENGINE // MODERN MAXIMALIST INTERFACE
    </p>
</div>
""", unsafe_allow_html=True)

# Create layout tabs
tab1, tab2, tab3 = st.tabs([
    "📤 Creator Ingestion Hub", 
    "📝 Storyboard & Script Studio", 
    "🔊 Audio Preview & Export Lab"
])

# ---------------------------------------------------------
# Tab 1: Creator Ingestion Hub
# ---------------------------------------------------------
with tab1:
    col_left, col_right = st.columns([3, 2], gap="large")
    
    with col_left:
        st.markdown('<div class="max-card">', unsafe_allow_html=True)
        st.markdown("### 1. Ingest Video Footage")
        uploaded_video = st.file_uploader(
            "Drag and drop your raw media assets here", 
            type=["mp4", "mov"],
            help="Strictly restricted to MP4 and MOV formats for standard Reel dimensions."
        )
        
        if uploaded_video:
            info = read_video_properties(uploaded_video)
            st.session_state.uploaded_video_info = info
            st.markdown(f"""
            <div style="background-color: #F9F9F9; border: 2px solid #111111; padding: 15px; margin-top: 15px;">
                <span class="max-badge max-badge-purple">RESOLVED PROPERTIES</span>
                <span class="max-badge max-badge-orange">{info['fps']} FPS</span>
                <span class="max-badge">{info['size_mb']} MB</span>
                <p style="margin: 8px 0 0 0; font-family: 'Space Mono', monospace; font-size: 0.9rem;">
                    <b>File Name:</b> {info['filename']}<br>
                    <b>Duration:</b> {info['duration']} seconds<br>
                    <b>Target Resolution:</b> {info['resolution']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="max-card">', unsafe_allow_html=True)
        st.markdown("### 2. Context Terminal")
        raw_thoughts = st.text_area(
            "Drop Your Raw Unedited Thoughts & Context Here",
            value=st.session_state.raw_context,
            height=180,
            placeholder="Type anything here... typos, messy grammar, broken sentences. The engine corrects and arranges it automatically."
        )
        st.session_state.raw_context = raw_thoughts
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="max-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown("### 3. Vibe Settings")
        
        vibe_selection = st.radio(
            "Select Instagram Reel Format Style:",
            [
                "The 3-Second Viral Loop", 
                "The High-Value Educational Carousel", 
                "The Raw Aesthetic Storytelling Vlog"
            ],
            index=0
        )
        st.session_state.vibe_format = vibe_selection
        
        st.markdown("""
        <div style="margin-top: 25px; border-top: 2px solid #111111; padding-top: 15px;">
            <p style="font-size: 0.95rem; line-height: 1.5;">
                <b>System Rules Applied:</b><br>
                1. Auto-correction of capitalization and double spaces.<br>
                2. Real-time conversion of slang to readable captions.<br>
                3. Timing layout matches standard viewer attention spans.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Giant Trigger Button
        st.markdown("<br><br>", unsafe_allow_html=True)
        trigger_btn = st.button("TRANSFORM INTO VIRAL SCRIPT")
        if trigger_btn:
            if not st.session_state.raw_context.strip():
                st.warning("Hey creator! Drop some thoughts in the context terminal first so we have something to script!")
            else:
                # Run grammar clean & generation
                cleaned = clean_text_grammar(st.session_state.raw_context)
                script, storyboard = generate_insta_script(cleaned, st.session_state.vibe_format)
                
                # Update Session State
                st.session_state.viral_script = script
                st.session_state.storyboard_list = storyboard
                st.session_state.script_generated = True
                
                # Clear stale audio bytes on new generation
                st.session_state.audio_bytes = None
                
                st.success("Boom! Your high-impact script and storyboard are ready in Tab 2!")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Tab 2: Storyboard & Reframed Narrative Studio
# ---------------------------------------------------------
with tab2:
    if not st.session_state.script_generated:
        st.markdown("""
        <div class="max-card" style="text-align: center; padding: 50px !important;">
            <h3>🚧 Dashboard Locked</h3>
            <p style="font-family: 'Space Mono', monospace; font-size: 1rem;">
                Please upload video files, insert context, and click the <b>TRANSFORM INTO VIRAL SCRIPT</b> button in Tab 1 to unlock the studio timeline.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        col_left_studio, col_right_studio = st.columns(2, gap="large")
        
        with col_left_studio:
            st.markdown('<div class="max-card">', unsafe_allow_html=True)
            st.markdown("### 🎬 Visual Storyboard Breakdown")
            
            if st.session_state.uploaded_video_info:
                v = st.session_state.uploaded_video_info
                st.markdown(f"""
                <p style="font-size: 0.9rem; font-family: 'Space Mono', monospace; background: #111111; color: #FFF; padding: 10px; border-radius:0px;">
                    Asset Detected: <b>{v['filename']}</b> ({v['duration']}s @ {v['fps']}fps)
                </p>
                """, unsafe_allow_html=True)
            
            for index, shot in enumerate(st.session_state.storyboard_list):
                st.markdown(f"""
                <div class="timeline-item">
                    <span class="max-badge max-badge-purple">{shot['time']}</span>
                    <span class="max-badge max-badge-orange">{shot['framing']}</span>
                    <h4 style="margin: 5px 0px !important;">Shot {index + 1} ({shot['pacing']})</h4>
                    <p style="font-size: 1rem; color: #333333; margin: 5px 0 0 0;">
                        {shot['cue']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_right_studio:
            st.markdown('<div class="max-card">', unsafe_allow_html=True)
            st.markdown("### 📝 Grammar-Perfect Voiceover Script")
            
            st.markdown("""
            <p style="font-size: 0.85rem; color: #555; font-family: 'Space Mono', monospace; margin-bottom: 15px;">
                Note: Sentence fragments have been restructured, typos eliminated, and pacing cues injected.
            </p>
            """, unsafe_allow_html=True)
            
            # Format display
            st.text_area(
                "Final Script Script Outline:",
                value=st.session_state.viral_script,
                height=450,
                disabled=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Tab 3: Audio Preview & Export Lab
# ---------------------------------------------------------
with tab3:
    if not st.session_state.script_generated:
        st.markdown("""
        <div class="max-card" style="text-align: center; padding: 50px !important;">
            <h3>🚧 Audio Studio Locked</h3>
            <p style="font-family: 'Space Mono', monospace; font-size: 1rem;">
                Complete script reframing in Tab 1 first to compile synthetic previews.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="max-card">', unsafe_allow_html=True)
        st.markdown("### 🔊 Synthetic Voiceover Compilation")
        
        # Audio rendering controller
        if not GTTS_AVAILABLE:
            st.error("The synthetic voice compilation library (`gtts`) is not loaded. Please ensure it is installed in requirements.txt.")
        elif st.session_state.audio_bytes is None:
            with st.spinner("Processing script audio compile... please wait."):
                # Strip out formatting/cues from speech output
                speech_text = re.sub(r'\[.*?\]', '', st.session_state.viral_script)
                speech_text = re.sub(r'👉|💡|🔄|🔥|📌|📣|✨|🌿|💬|"', '', speech_text)
                
                try:
                    tts = gTTS(text=speech_text, lang='en', slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    st.session_state.audio_bytes = fp.read()
                except Exception as e:
                    st.error(f"Failed to generate TTS preview. Error: {str(e)}")
        
        if st.session_state.audio_bytes:
            st.markdown("<p style='font-family: Space Mono, monospace; font-size:0.9rem;'>PLAYBACK PACING TRACK</p>", unsafe_allow_html=True)
            st.audio(st.session_state.audio_bytes, format='audio/mp3')
            
            # Export Columns
            st.markdown("<br><br>", unsafe_allow_html=True)
            col_d1, col_d2 = st.columns(2)
            
            with col_d1:
                st.download_button(
                    label="DOWNLOAD SCRIPT (.TXT)",
                    data=st.session_state.viral_script,
                    file_name="instagram_script.txt",
                    mime="text/plain"
                )
            
            with col_d2:
                st.download_button(
                    label="DOWNLOAD AUDIO VOICEOVER (.MP3)",
                    data=st.session_state.audio_bytes,
                    file_name="instagram_voiceover.mp3",
                    mime="audio/mp3"
                )
        st.markdown('</div>', unsafe_allow_html=True)

# Footer branding
st.markdown("""
<div class="max-footer">
    MADE FOR CREATORS BY CREATORS // INSTASCRIPTER V1.0 // STANDALONE APP
</div>
""", unsafe_allow_html=True)
