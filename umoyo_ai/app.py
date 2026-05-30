import streamlit as st
import joblib
import json
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time
import datetime
import requests
from streamlit_option_menu import option_menu

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Umoyo AI – PCOS Health Companion",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  PREMIUM CSS THEME
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }
.stApp { background-color: #FDFBFA; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFF0F3 0%, #FDF6FF 100%);
    border-right: 1px solid #F2D9E4;
}
section[data-testid="stSidebar"] * { color: #3D2B3E !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #E8708A 0%, #C9508C 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    opacity: 0.9;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(200,80,140,0.35) !important;
}

/* ── Cards ── */
.umoyo-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 2px 16px rgba(200, 120, 160, 0.10);
    border: 1px solid #F5E6EE;
    margin-bottom: 20px;
}
.metric-card {
    background: linear-gradient(135deg, #FFFFFF 0%, #FFF5F8 100%);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 12px rgba(200,120,160,0.12);
    border: 1px solid #F5E6EE;
}
.metric-value { font-size: 2rem; font-weight: 800; color: #C9508C; line-height: 1.1; }
.metric-label { font-size: 0.85rem; color: #7A5C6E; font-weight: 500; margin-top: 4px; }

/* ── Headers ── */
.page-title {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #C9508C, #8A4FBB);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}
.page-subtitle { color: #8A7087; font-size: 1rem; margin-bottom: 1.5rem; }

/* ── Chat ── */
.chat-bubble-ai {
    background: linear-gradient(135deg, #FFF0F8 0%, #F8F0FF 100%);
    border: 1px solid #F0D5EC;
    border-radius: 0 16px 16px 16px;
    padding: 14px 18px;
    margin: 8px 0;
    max-width: 85%;
    color: #2D1F2E !important;
    line-height: 1.6;
}
.chat-bubble-user {
    background: linear-gradient(135deg, #C9508C 0%, #8A4FBB 100%);
    border-radius: 16px 0 16px 16px;
    padding: 14px 18px;
    margin: 8px 0 8px auto;
    max-width: 75%;
    color: white !important;
    float: right;
    clear: both;
    line-height: 1.6;
}
.chat-container { clear: both; }
.ai-name { font-size: 0.75rem; color: #B07898; font-weight: 600; margin-bottom: 4px; }

/* ── Risk gauge ── */
.risk-low { color: #2E7D32; font-weight: 700; }
.risk-medium { color: #F57F17; font-weight: 700; }
.risk-high { color: #C62828; font-weight: 700; }

/* ── Section dividers ── */
.section-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #F0C8DC, transparent);
    margin: 24px 0;
}

/* ── Inputs ── */
.stSlider > div > div > div { background: #E8708A !important; }
.stSelectbox > div > div { border-color: #F0C8DC !important; }
.stTextInput > div > div > input { border-color: #F0C8DC !important; }
.stNumberInput > div > div > input { border-color: #F0C8DC !important; }
div[data-testid="stChatInput"] textarea { border: 1.5px solid #F0C8DC !important; border-radius: 12px !important; }

/* ── Progress bars ── */
.stProgress > div > div > div { background: linear-gradient(90deg, #E8708A, #C9508C) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab"] { color: #8A7087 !important; }
.stTabs [aria-selected="true"] { color: #C9508C !important; border-bottom-color: #C9508C !important; }

/* ── Welcome hero ── */
.hero-box {
    background: linear-gradient(135deg, #FFF0F8 0%, #F5EEFF 50%, #FFF0F8 100%);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    border: 1px solid #F0D5EC;
    margin-bottom: 24px;
}
.hero-title { font-size: 2.4rem; font-weight: 800; color: #C9508C; margin-bottom: 8px; }
.hero-subtitle { font-size: 1.1rem; color: #7A5C6E; }

/* ── Nav menu ── */
.nav-link-selected { background-color: #F0D5EC !important; color: #C9508C !important; border-radius: 8px; }

/* ── Wellness chips ── */
.symptom-chip {
    display: inline-block;
    background: #FFF0F6;
    border: 1px solid #F0C8DC;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.82rem;
    color: #9B4F7A;
    margin: 3px;
}
.tip-box {
    background: linear-gradient(135deg, #FFF5F8, #F8F0FF);
    border-left: 4px solid #E8708A;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 12px 0;
    color: #3D2B3E;
}

/* ── Footer ── */
.app-footer {
    text-align: center;
    color: #B097A8;
    font-size: 0.8rem;
    padding: 20px 0 8px;
    border-top: 1px solid #F5E6EE;
    margin-top: 40px;
}

/* Hide Streamlit branding */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MODEL LOADING
# ─────────────────────────────────────────────
@st.cache_resource
def load_model_artifacts():
    base = os.path.join(os.path.dirname(__file__), "model_artifacts")
    model   = joblib.load(os.path.join(base, "best_svc_model.joblib"))
    scaler  = joblib.load(os.path.join(base, "scaler.joblib"))
    with open(os.path.join(base, "feature_names.json")) as f:
        features = json.load(f)
    return model, scaler, features

try:
    model, scaler, feature_names = load_model_artifacts()
    MODEL_OK = True
except Exception as e:
    MODEL_OK = False
    st.sidebar.error(f"Model load error: {e}")

# ─────────────────────────────────────────────
#  AI PROVIDER – MULTI-PROVIDER ABSTRACTION
#  Priority: Gemini → Groq → Fallback responses
# ─────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY", "")

UMOYO_SYSTEM_PROMPT = """You are Umoyo, a warm, knowledgeable, and compassionate AI health companion specializing in PCOS (Polycystic Ovary Syndrome) support.

Your personality:
- Empathetic, professional, and supportive
- Evidence-based but approachable
- Never dismissive of concerns
- Encouraging professional medical consultation when appropriate
- You NEVER claim to be a doctor or diagnose conditions

Your expertise areas:
- PCOS symptoms, causes, and management
- Hormonal health and menstrual cycles
- Nutrition and anti-inflammatory eating for PCOS
- Exercise recommendations for hormone balance
- Mental health and emotional wellbeing with PCOS
- Fertility and reproductive health education
- Medication awareness (Metformin, birth control, etc.) – education only
- Lifestyle interventions and natural support

Always:
- End sensitive responses by recommending consulting a healthcare provider
- Be inclusive and sensitive to body diversity
- Use clear, non-medical jargon where possible
- Provide actionable, practical advice

Never:
- Diagnose or prescribe
- Share dangerous medical misinformation
- Be dismissive of symptoms
"""

PCOS_FALLBACK_RESPONSES = {
    "default": """Thank you for reaching out. PCOS affects approximately 1 in 10 women of reproductive age and is one of the most common hormonal disorders.

Key things to know about PCOS:
• **Symptoms vary widely** – irregular periods, acne, hair changes, weight fluctuations, and mood changes are common
• **It's manageable** – with the right lifestyle, nutrition, and medical support, most women live well with PCOS
• **Early intervention helps** – tracking symptoms and working with your doctor can significantly improve quality of life

I'm here to help you understand your symptoms, nutrition, fitness, and wellness strategies. What specific aspect of PCOS would you like to explore?

*Please consult a healthcare provider for personalized medical advice.*""",

    "nutrition": """**PCOS-Friendly Nutrition Guide:**

The best dietary approach for PCOS focuses on:

**Blood Sugar Balance:**
• Choose low-glycemic foods (whole grains, legumes, non-starchy vegetables)
• Pair carbohydrates with protein and healthy fats
• Avoid refined sugars and processed foods

**Anti-inflammatory Foods:**
• Berries, leafy greens, fatty fish, olive oil, turmeric
• These help reduce the chronic low-grade inflammation common in PCOS

**Key Nutrients:**
• Inositol (found in citrus, nuts, whole grains) – supports insulin sensitivity
• Magnesium (dark chocolate, spinach, almonds) – helps with sleep and mood
• Zinc (pumpkin seeds, chickpeas) – supports hormone regulation

**Meal Timing:**
• Eating within a consistent window can help regulate cortisol and insulin
• Don't skip breakfast – it sets your metabolic tone for the day

*Always work with a registered dietitian for a personalized nutrition plan.*""",

    "exercise": """**Exercise for PCOS – What Works Best:**

**Recommended:**
• **Walking** – 30 minutes daily is highly effective for insulin sensitivity
• **Strength training** – 2-3x per week helps build muscle and regulate metabolism
• **Yoga & Pilates** – excellent for stress reduction and cortisol management
• **Swimming** – low-impact, full-body, great for inflammation

**Avoid Overtraining:**
• High-intensity exercise daily can spike cortisol and worsen hormonal imbalance
• Rest days are essential for hormone recovery

**Tips:**
• Aim for 150 minutes of moderate activity per week
• Consistency matters more than intensity
• Movement you enjoy is the best movement

*Please consult your doctor before starting any new exercise program.*"""
}

def call_gemini(messages: list, api_key: str) -> str:
    """Call Google Gemini API."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # Build contents from messages
    contents = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})
    
    payload = {
        "system_instruction": {"parts": [{"text": UMOYO_SYSTEM_PROMPT}]},
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 800,
            "topP": 0.9
        },
        "safetySettings": [
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"}
        ]
    }
    
    resp = requests.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def call_groq(messages: list, api_key: str) -> str:
    """Call Groq API (OpenAI-compatible)."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "system", "content": UMOYO_SYSTEM_PROMPT}] + messages,
        "max_tokens": 800,
        "temperature": 0.7
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def get_ai_response(messages: list) -> tuple[str, str]:
    """Try providers in order. Returns (response_text, provider_name)."""
    # Gemini first
    if GEMINI_API_KEY:
        try:
            return call_gemini(messages, GEMINI_API_KEY), "Gemini"
        except Exception:
            pass
    
    # Groq fallback
    if GROQ_API_KEY:
        try:
            return call_groq(messages, GROQ_API_KEY), "Groq"
        except Exception:
            pass
    
    # Smart keyword fallback
    last_msg = messages[-1]["content"].lower() if messages else ""
    if any(w in last_msg for w in ["eat", "food", "diet", "nutrition", "meal"]):
        return PCOS_FALLBACK_RESPONSES["nutrition"], "Offline"
    elif any(w in last_msg for w in ["exercise", "workout", "gym", "walk", "sport"]):
        return PCOS_FALLBACK_RESPONSES["exercise"], "Offline"
    else:
        return PCOS_FALLBACK_RESPONSES["default"], "Offline"

# ─────────────────────────────────────────────
#  SESSION STATE DEFAULTS
# ─────────────────────────────────────────────
defaults = {
    "messages": [],
    "symptom_log": [],
    "cycle_log": [],
    "mood_log": [],
    "weight_log": [],
    "wellness_scores": [],
    "user_name": "Wellness Warrior",
    "onboarded": False,
    "risk_result": None,
    "current_page": "Home",
    "last_assessment": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 8px'>
        <div style='font-size:2.5rem'>🌸</div>
        <div style='font-size:1.4rem; font-weight:800; color:#C9508C;'>Umoyo AI</div>
        <div style='font-size:0.75rem; color:#9B7A8E; margin-top:2px;'>Your Intelligent PCOS Companion</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    selected = option_menu(
        menu_title=None,
        options=["Home", "AI Companion", "Risk Assessment", "Symptom Tracker",
                 "Cycle Tracker", "Nutrition Coach", "Fitness Coach",
                 "Mental Wellness", "Reports", "Settings"],
        icons=["house-heart", "chat-heart", "activity", "journal-medical",
               "calendar3", "egg-fried", "bicycle", "emoji-smile",
               "file-earmark-pdf", "gear"],
        default_index=0,
        styles={
            "container": {"background-color": "transparent", "padding": "0"},
            "icon": {"color": "#C9508C", "font-size": "16px"},
            "nav-link": {
                "font-size": "0.88rem", "color": "#5A3D4E",
                "border-radius": "8px", "margin": "2px 0",
                "padding": "8px 12px"
            },
            "nav-link-selected": {
                "background-color": "#F5E0ED",
                "color": "#C9508C", "font-weight": "700"
            },
        }
    )
    
    st.divider()
    
    # AI provider status
    if GEMINI_API_KEY:
        st.markdown("<div style='font-size:0.75rem; color:#2E7D32;'>● AI: Gemini Connected</div>", unsafe_allow_html=True)
    elif GROQ_API_KEY:
        st.markdown("<div style='font-size:0.75rem; color:#1565C0;'>● AI: Groq Connected</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size:0.75rem; color:#E65100;'>● AI: Offline Mode</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='font-size:0.72rem; color:#B097A8; margin-top:8px;'>Umoyo means 'Life' in Chewa</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.72rem; color:#B097A8;'>© 2025 Umoyo AI Health</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HELPER: WELLNESS SCORE
# ─────────────────────────────────────────────
def compute_wellness_score() -> int:
    score = 50  # baseline
    logs = st.session_state.symptom_log
    moods = st.session_state.mood_log
    weights = st.session_state.weight_log
    
    if logs:
        recent = logs[-7:] if len(logs) >= 7 else logs
        avg_severity = sum(l.get("severity", 3) for l in recent) / len(recent)
        score -= int((avg_severity - 1) * 5)
    
    if moods:
        recent_mood = moods[-7:] if len(moods) >= 7 else moods
        avg_mood = sum(m.get("score", 5) for m in recent_mood) / len(recent_mood)
        score += int((avg_mood - 5) * 3)
    
    if len(weights) >= 2:
        delta = weights[-1]["value"] - weights[-2]["value"]
        if -0.5 <= delta <= 0:
            score += 5
    
    score = max(10, min(100, score))
    return score

# ─────────────────────────────────────────────
#  PAGE: HOME
# ─────────────────────────────────────────────
if selected == "Home":
    name = st.session_state.user_name
    today = datetime.date.today()
    
    st.markdown(f"""
    <div class='hero-box'>
        <div class='hero-title'>Welcome back, {name}</div>
        <div class='hero-subtitle'>{today.strftime('%A, %B %d, %Y')} — Your health journey continues</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick metrics row
    wellness = compute_wellness_score()
    sym_count = len([l for l in st.session_state.symptom_log
                     if l.get("date") == str(today)])
    cycle_day = len(st.session_state.cycle_log) % 28 + 1 if st.session_state.cycle_log else "—"
    mood_today = next((m["label"] for m in reversed(st.session_state.mood_log)
                       if m.get("date") == str(today)), "Not logged")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-value'>{wellness}</div>
            <div class='metric-label'>Wellness Score</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-value'>Day {cycle_day}</div>
            <div class='metric-label'>Cycle Day</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-value'>{sym_count}</div>
            <div class='metric-label'>Symptoms Today</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-value' style='font-size:1.2rem'>{mood_today}</div>
            <div class='metric-label'>Today's Mood</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        # Wellness score gauge
        st.markdown("### Wellness Overview")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=wellness,
            number={"suffix": "/100", "font": {"size": 32, "color": "#C9508C"}},
            title={"text": "Current Wellness Score", "font": {"size": 14, "color": "#7A5C6E"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#D4B8C8"},
                "bar": {"color": "#C9508C", "thickness": 0.3},
                "bgcolor": "#FFF5F8",
                "bordercolor": "#F0C8DC",
                "steps": [
                    {"range": [0, 40], "color": "#FFE0EC"},
                    {"range": [40, 70], "color": "#FFC8DC"},
                    {"range": [70, 100], "color": "#FFB0CC"},
                ],
                "threshold": {
                    "line": {"color": "#8A4FBB", "width": 3},
                    "thickness": 0.75,
                    "value": wellness
                }
            }
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=240,
            margin={"t": 40, "b": 10, "l": 20, "r": 20}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent symptoms chart
        if st.session_state.symptom_log:
            df_sym = pd.DataFrame(st.session_state.symptom_log[-14:])
            if "date" in df_sym.columns and "severity" in df_sym.columns:
                fig2 = px.line(df_sym, x="date", y="severity",
                               title="Symptom Severity Trend (Last 14 Entries)",
                               color_discrete_sequence=["#E8708A"],
                               labels={"severity": "Severity", "date": "Date"})
                fig2.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(255,240,248,0.5)",
                    height=200, margin={"t": 40, "b": 10, "l": 10, "r": 10},
                    font={"color": "#3D2B3E"}
                )
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Start logging symptoms to see your trend chart.")
    
    with col_right:
        # AI Companion shortcut
        st.markdown("### Quick Chat with Umoyo")
        st.markdown("""
        <div class='umoyo-card'>
            <div class='ai-name'>UMOYO AI</div>
            <div class='chat-bubble-ai'>
                Hello.<br><br>
                I'm <strong>Umoyo</strong>.<br>
                Your intelligent PCOS health companion.<br><br>
                How can I support you today?
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open AI Companion →", use_container_width=True):
            st.session_state["_nav"] = "AI Companion"
            st.rerun()
        
        st.markdown("---")
        
        # Daily tips
        tips = [
            "Stay hydrated – aim for 8 glasses of water today.",
            "A 20-minute walk can boost insulin sensitivity.",
            "Magnesium-rich foods support sleep and hormones.",
            "Stress management is key – try 5 minutes of deep breathing.",
            "Consistent sleep times help regulate cortisol and hunger hormones.",
            "Anti-inflammatory spices like turmeric and ginger support PCOS.",
        ]
        tip_idx = today.day % len(tips)
        st.markdown(f"""
        <div class='tip-box'>
            <strong>Daily Wellness Tip</strong><br>
            {tips[tip_idx]}
        </div>
        """, unsafe_allow_html=True)
        
        # Last risk result
        if st.session_state.risk_result:
            r = st.session_state.risk_result
            color = "#C62828" if r > 65 else ("#F57F17" if r > 40 else "#2E7D32")
            st.markdown(f"""
            <div class='umoyo-card'>
                <strong>Last Risk Assessment</strong><br>
                <span style='color:{color}; font-size:1.5rem; font-weight:800;'>{r:.1f}%</span>
                <span style='color:#9B7A8E; font-size:0.8rem;'> PCOS Risk Index</span>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: AI COMPANION
# ─────────────────────────────────────────────
elif selected == "AI Companion":
    st.markdown("<div class='page-title'>AI Companion</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Chat with Umoyo – your evidence-based PCOS health guide</div>", unsafe_allow_html=True)
    
    # Initialize chat with opening message
    if not st.session_state.messages:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Hello.\n\nI'm **Umoyo**.\n\nYour intelligent PCOS health companion.\n\nHow can I support you today?"
        }]
    
    # Render chat history
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            with st.chat_message("assistant", avatar="🌸"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])
    
    # Suggested questions (shown when chat is new)
    if len(st.session_state.messages) <= 1:
        st.markdown("**Suggested questions:**")
        cols = st.columns(3)
        suggestions = [
            "What are common PCOS symptoms?",
            "What should I eat with PCOS?",
            "How does PCOS affect fertility?",
            "What exercises help with PCOS?",
            "How do I manage PCOS naturally?",
            "Tell me about PCOS and weight",
        ]
        for i, sug in enumerate(suggestions):
            if cols[i % 3].button(sug, key=f"sug_{i}"):
                prompt = sug
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user", avatar="👤"):
                    st.markdown(prompt)
                with st.chat_message("assistant", avatar="🌸"):
                    with st.spinner("Umoyo is thinking..."):
                        response, provider = get_ai_response(st.session_state.messages)
                    st.markdown(response)
                    if provider == "Offline":
                        st.caption("(Offline knowledge base – add GEMINI_API_KEY for live AI)")
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
    
    # Chat input
    if prompt := st.chat_input("Ask Umoyo anything about PCOS..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        with st.chat_message("assistant", avatar="🌸"):
            with st.spinner("Umoyo is thinking..."):
                history = [{"role": m["role"], "content": m["content"]}
                           for m in st.session_state.messages]
                response, provider = get_ai_response(history)
            
            # Streaming word-by-word effect
            placeholder = st.empty()
            words = response.split(" ")
            shown = ""
            for word in words:
                shown += word + " "
                placeholder.markdown(shown + "▌")
                time.sleep(0.025)
            placeholder.markdown(response)
            
            if provider == "Offline":
                st.caption("Offline mode – add GEMINI_API_KEY in Settings for live AI")
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear chat button
    if st.session_state.messages and len(st.session_state.messages) > 1:
        if st.button("Clear conversation"):
            st.session_state.messages = []
            st.rerun()

# ─────────────────────────────────────────────
#  PAGE: RISK ASSESSMENT
# ─────────────────────────────────────────────
elif selected == "Risk Assessment":
    st.markdown("<div class='page-title'>PCOS Risk Assessment</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>A personalized wellness analysis using your health profile</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='tip-box'>
        <strong>Important:</strong> This assessment is an educational wellness tool – not a medical diagnosis.
        Results indicate relative risk levels based on common PCOS indicators. Always consult a healthcare provider.
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("risk_form"):
        st.markdown("#### Personal Information")
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.number_input("Age (years)", min_value=12, max_value=60, value=26)
        with c2:
            weight = st.number_input("Weight (kg)", min_value=35.0, max_value=200.0, value=65.0, step=0.5)
        with c3:
            height = st.number_input("Height (cm)", min_value=100.0, max_value=220.0, value=165.0, step=0.5)
        
        bmi = weight / ((height / 100) ** 2)
        st.markdown(f"**Calculated BMI:** `{bmi:.1f}` — "
                    f"{'Underweight' if bmi < 18.5 else 'Normal' if bmi < 25 else 'Overweight' if bmi < 30 else 'Obese'}")
        
        st.markdown("#### Menstrual Health")
        c4, c5 = st.columns(2)
        with c4:
            menstrual_irregularity = st.selectbox(
                "Menstrual Cycle Regularity",
                options=[0, 1],
                format_func=lambda x: "Regular (21–35 day cycles)" if x == 0 else "Irregular (outside 21–35 days)"
            )
        with c5:
            period_duration = st.selectbox("Period Duration", ["Normal (3–7 days)", "Short (<3 days)", "Long (>7 days)"])
        
        st.markdown("#### Symptoms (select all that apply)")
        sym_cols = st.columns(4)
        symptoms = {
            "Acne": sym_cols[0].checkbox("Acne"),
            "Excess hair growth": sym_cols[1].checkbox("Excess hair growth"),
            "Hair thinning": sym_cols[2].checkbox("Hair thinning"),
            "Unexplained weight gain": sym_cols[3].checkbox("Unexplained weight gain"),
            "Fatigue": sym_cols[0].checkbox("Fatigue"),
            "Mood changes": sym_cols[1].checkbox("Mood changes"),
            "Pelvic pain": sym_cols[2].checkbox("Pelvic pain"),
            "Skin darkening": sym_cols[3].checkbox("Skin darkening"),
        }
        
        st.markdown("#### Lifestyle & Family History")
        c6, c7, c8 = st.columns(3)
        with c6:
            family_history = st.selectbox("Family history of PCOS", ["No", "Yes", "Unknown"])
        with c7:
            exercise_freq = st.selectbox("Exercise frequency", ["Daily", "3-4x/week", "1-2x/week", "Rarely", "Never"])
        with c8:
            stress_level = st.slider("Stress level (1–10)", 1, 10, 5)
        
        submitted = st.form_submit_button("Analyze My Risk Profile", use_container_width=True)
    
    if submitted and MODEL_OK:
        # Run model prediction
        input_df = pd.DataFrame({
            "age": [float(age)],
            "bmi": [float(bmi)],
            "menstrual_irregularity": [float(menstrual_irregularity)]
        })[feature_names]
        
        scale_cols = [c for c in ["age", "bmi"] if c in feature_names]
        input_df[scale_cols] = scaler.transform(input_df[scale_cols])
        
        risk_proba = model.predict_proba(input_df)[0][1] * 100
        
        # Adjust with additional factors
        sym_count_pos = sum(1 for v in symptoms.values() if v)
        risk_proba += sym_count_pos * 2
        if family_history == "Yes":
            risk_proba += 8
        if exercise_freq in ["Rarely", "Never"]:
            risk_proba += 4
        if stress_level >= 8:
            risk_proba += 3
        risk_proba = min(95.0, max(5.0, risk_proba))
        
        st.session_state.risk_result = risk_proba
        st.session_state.last_assessment = str(datetime.date.today())
        
        st.markdown("---")
        st.markdown("### Your Risk Assessment Results")
        
        # Determine level
        if risk_proba >= 65:
            level, color, desc = "High Risk", "#C62828", "Several indicators suggest elevated PCOS likelihood. We strongly recommend consulting a gynecologist or endocrinologist."
        elif risk_proba >= 40:
            level, color, desc = "Moderate Risk", "#F57F17", "Some indicators present. A healthcare consultation is recommended to rule out or confirm PCOS."
        else:
            level, color, desc = "Low Risk", "#2E7D32", "Few indicators detected. Continue maintaining healthy lifestyle habits and monitor any changes."
        
        res_col1, res_col2 = st.columns([1, 1])
        
        with res_col1:
            # Gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk_proba,
                number={"suffix": "%", "font": {"size": 40, "color": color}},
                title={"text": "PCOS Risk Index", "font": {"size": 16, "color": "#5A3D4E"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#D4B8C8"},
                    "bar": {"color": color, "thickness": 0.3},
                    "bgcolor": "#FFF5F8",
                    "bordercolor": "#F0C8DC",
                    "steps": [
                        {"range": [0, 40], "color": "#E8F5E9"},
                        {"range": [40, 65], "color": "#FFF8E1"},
                        {"range": [65, 100], "color": "#FFEBEE"},
                    ]
                }
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                height=280,
                margin={"t": 50, "b": 20, "l": 20, "r": 20}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with res_col2:
            st.markdown(f"""
            <div class='umoyo-card'>
                <div style='font-size:1.4rem; font-weight:800; color:{color};'>{level}</div>
                <div style='color:#5A3D4E; margin: 8px 0;'>{desc}</div>
                <hr style='border:none; border-top:1px solid #F0C8DC; margin:12px 0'>
                <strong>Key Contributing Factors:</strong>
                <ul style='color:#5A3D4E; margin-top:8px;'>
                    {'<li>Menstrual irregularity detected</li>' if menstrual_irregularity else ''}
                    {'<li>BMI above optimal range</li>' if bmi >= 25 else ''}
                    {'<li>' + str(sym_count_pos) + ' active symptoms reported</li>' if sym_count_pos else ''}
                    {'<li>Family history of PCOS</li>' if family_history == "Yes" else ''}
                    {'<li>Low physical activity</li>' if exercise_freq in ["Rarely","Never"] else ''}
                    {'<li>High stress levels</li>' if stress_level >= 8 else ''}
                    <li>Age: {age} years (typical PCOS onset: 15–35)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Personalized recommendations
        st.markdown("#### Personalized Wellness Recommendations")
        recs = []
        if menstrual_irregularity:
            recs.append(("Hormonal Support", "Track your cycle consistently for 3 months and share the data with your gynecologist."))
        if bmi >= 25:
            recs.append(("Weight Management", "Even a 5–10% weight reduction can significantly improve PCOS symptoms and hormone levels."))
        if sym_count_pos >= 3:
            recs.append(("Comprehensive Testing", "Request full hormonal panel: LH, FSH, testosterone, AMH, insulin, and pelvic ultrasound."))
        if stress_level >= 7:
            recs.append(("Stress Reduction", "Chronic stress raises cortisol, worsening insulin resistance. Explore yoga, meditation, or therapy."))
        recs.append(("Nutrition", "Adopt a low-glycemic, anti-inflammatory diet rich in whole foods, fiber, and lean protein."))
        recs.append(("Exercise", "150 minutes of moderate exercise weekly, combining cardio and strength training, improves insulin sensitivity."))
        
        rec_cols = st.columns(3)
        for i, (title, body) in enumerate(recs[:6]):
            rec_cols[i % 3].markdown(f"""
            <div class='umoyo-card' style='margin-bottom:12px;'>
                <div style='font-weight:700; color:#C9508C; margin-bottom:6px;'>{title}</div>
                <div style='color:#5A3D4E; font-size:0.88rem;'>{body}</div>
            </div>
            """, unsafe_allow_html=True)
    
    elif submitted and not MODEL_OK:
        st.error("Model not loaded. Please ensure model_artifacts/ folder is present.")

# ─────────────────────────────────────────────
#  PAGE: SYMPTOM TRACKER
# ─────────────────────────────────────────────
elif selected == "Symptom Tracker":
    st.markdown("<div class='page-title'>Symptom Tracker</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Log and monitor your daily PCOS symptoms</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Log Today", "View Trends"])
    
    with tab1:
        with st.form("symptom_form"):
            st.markdown("#### Today's Symptom Check-in")
            today_str = str(datetime.date.today())
            
            SYMPTOM_LIST = [
                "Irregular periods", "Acne", "Hair loss/thinning",
                "Excess hair growth", "Mood changes", "Fatigue",
                "Food cravings", "Sleep issues", "Pelvic pain",
                "Bloating", "Headaches", "Brain fog"
            ]
            
            sel_symptoms = st.multiselect("Which symptoms are you experiencing today?", SYMPTOM_LIST)
            severity = st.slider("Overall symptom severity", 1, 10, 3,
                                  help="1 = very mild, 10 = very severe")
            notes = st.text_area("Additional notes (optional)", placeholder="Any patterns, triggers, or observations...")
            
            log_btn = st.form_submit_button("Log Symptoms", use_container_width=True)
        
        if log_btn:
            entry = {
                "date": today_str,
                "symptoms": sel_symptoms,
                "severity": severity,
                "notes": notes,
                "timestamp": datetime.datetime.now().isoformat()
            }
            st.session_state.symptom_log.append(entry)
            st.success(f"Symptoms logged for {today_str}")
    
    with tab2:
        if not st.session_state.symptom_log:
            st.info("No symptom data yet. Start logging to see your trends.")
        else:
            df = pd.DataFrame(st.session_state.symptom_log)
            
            # Severity trend
            fig = px.area(df, x="date", y="severity",
                          title="Symptom Severity Over Time",
                          color_discrete_sequence=["#E8708A"],
                          labels={"severity": "Severity (1–10)", "date": "Date"})
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                               plot_bgcolor="rgba(255,240,248,0.4)",
                               font={"color": "#3D2B3E"}, height=280)
            st.plotly_chart(fig, use_container_width=True)
            
            # Symptom frequency
            all_syms = [s for entry in st.session_state.symptom_log for s in entry.get("symptoms", [])]
            if all_syms:
                freq = pd.Series(all_syms).value_counts().reset_index()
                freq.columns = ["Symptom", "Count"]
                fig2 = px.bar(freq, x="Symptom", y="Count",
                              title="Most Frequent Symptoms",
                              color_discrete_sequence=["#C9508C"])
                fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                                    plot_bgcolor="rgba(255,240,248,0.4)",
                                    font={"color": "#3D2B3E"}, height=280,
                                    xaxis_tickangle=-30)
                st.plotly_chart(fig2, use_container_width=True)
            
            # Recent log table
            st.markdown("#### Recent Logs")
            display_df = df[["date", "severity", "symptoms", "notes"]].tail(10).copy()
            display_df["symptoms"] = display_df["symptoms"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
            st.dataframe(display_df, use_container_width=True)

# ─────────────────────────────────────────────
#  PAGE: CYCLE TRACKER
# ─────────────────────────────────────────────
elif selected == "Cycle Tracker":
    st.markdown("<div class='page-title'>Cycle Tracker</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Track your menstrual cycle, predict patterns, and understand your hormones</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Log Period", "Calendar & Analysis"])
    
    with tab1:
        with st.form("cycle_form"):
            c1, c2 = st.columns(2)
            with c1:
                period_start = st.date_input("Period start date", datetime.date.today())
                period_end = st.date_input("Period end date", datetime.date.today() + datetime.timedelta(days=5))
            with c2:
                flow_intensity = st.selectbox("Flow intensity", ["Light", "Moderate", "Heavy", "Very Heavy"])
                period_pain = st.slider("Pain level (1–10)", 1, 10, 3)
            
            cycle_notes = st.text_area("Cycle notes", placeholder="PMS symptoms, mood, clotting, etc.")
            log_cycle = st.form_submit_button("Log Period", use_container_width=True)
        
        if log_cycle:
            duration = (period_end - period_start).days + 1
            entry = {
                "start": str(period_start),
                "end": str(period_end),
                "duration": duration,
                "flow": flow_intensity,
                "pain": period_pain,
                "notes": cycle_notes
            }
            st.session_state.cycle_log.append(entry)
            st.success(f"Period logged: {period_start} to {period_end} ({duration} days)")
    
    with tab2:
        if not st.session_state.cycle_log:
            st.info("Log at least one period to see cycle analysis.")
        else:
            df_cy = pd.DataFrame(st.session_state.cycle_log)
            df_cy["start"] = pd.to_datetime(df_cy["start"])
            df_cy = df_cy.sort_values("start")
            
            # Compute cycle lengths
            if len(df_cy) >= 2:
                df_cy["cycle_length"] = df_cy["start"].diff().dt.days
                avg_cycle = df_cy["cycle_length"].dropna().mean()
                next_period = df_cy["start"].iloc[-1] + datetime.timedelta(days=int(avg_cycle))
                ovulation_est = next_period - datetime.timedelta(days=14)
                
                col1, col2, col3 = st.columns(3)
                col1.markdown(f"<div class='metric-card'><div class='metric-value'>{avg_cycle:.0f}</div><div class='metric-label'>Avg Cycle Length (days)</div></div>", unsafe_allow_html=True)
                col2.markdown(f"<div class='metric-card'><div class='metric-value' style='font-size:1.2rem'>{next_period.strftime('%b %d')}</div><div class='metric-label'>Next Period (est.)</div></div>", unsafe_allow_html=True)
                col3.markdown(f"<div class='metric-card'><div class='metric-value' style='font-size:1.2rem'>{ovulation_est.strftime('%b %d')}</div><div class='metric-label'>Ovulation (est.)</div></div>", unsafe_allow_html=True)
                
                # Regularity insight
                std_dev = df_cy["cycle_length"].dropna().std()
                if pd.notna(std_dev):
                    if std_dev <= 3:
                        st.success(f"Your cycles are **regular** (variation: ±{std_dev:.1f} days). This is a positive sign.")
                    elif std_dev <= 7:
                        st.warning(f"Your cycles show **mild irregularity** (variation: ±{std_dev:.1f} days). Monitor trends.")
                    else:
                        st.error(f"Your cycles are **irregular** (variation: ±{std_dev:.1f} days). Consider consulting a gynecologist.")
                
                # Cycle length chart
                fig = px.bar(df_cy.dropna(subset=["cycle_length"]),
                             x="start", y="cycle_length",
                             title="Cycle Length History",
                             color_discrete_sequence=["#E8708A"],
                             labels={"cycle_length": "Days", "start": "Period Start"})
                fig.add_hline(y=28, line_dash="dot", line_color="#8A4FBB",
                               annotation_text="Avg 28 days")
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                                   plot_bgcolor="rgba(255,240,248,0.4)",
                                   font={"color": "#3D2B3E"}, height=280)
                st.plotly_chart(fig, use_container_width=True)
            
            # Period history table
            st.markdown("#### Period History")
            disp = df_cy[["start", "end", "duration", "flow", "pain"]].copy()
            disp["start"] = disp["start"].dt.strftime("%Y-%m-%d")
            st.dataframe(disp, use_container_width=True)

# ─────────────────────────────────────────────
#  PAGE: NUTRITION COACH
# ─────────────────────────────────────────────
elif selected == "Nutrition Coach":
    st.markdown("<div class='page-title'>Nutrition Coach</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>PCOS-optimized meal plans, hydration tracking, and nutrition guidance</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Meal Plan Generator", "Hydration Tracker", "PCOS Foods Guide"])
    
    with tab1:
        st.markdown("#### Generate Your PCOS Meal Plan")
        c1, c2, c3 = st.columns(3)
        with c1:
            diet_pref = st.selectbox("Dietary preference", ["No restriction", "Vegetarian", "Vegan", "Gluten-free", "Dairy-free", "Low-carb"])
        with c2:
            calorie_goal = st.select_slider("Daily calorie goal", options=[1400, 1600, 1800, 2000, 2200, 2400], value=1800)
        with c3:
            goal = st.selectbox("Primary goal", ["Balance hormones", "Lose weight", "Manage insulin", "Boost energy", "Improve fertility"])
        
        if st.button("Generate My Meal Plan", use_container_width=True):
            MEAL_PLANS = {
                "Balance hormones": {
                    "Breakfast": "Greek yogurt with berries, chia seeds & a drizzle of honey | Spearmint tea",
                    "Mid-morning": "Handful of almonds + apple slices",
                    "Lunch": "Quinoa salad with grilled salmon, cucumber, cherry tomatoes & olive oil dressing",
                    "Afternoon snack": "Hummus with carrot sticks & celery",
                    "Dinner": "Baked chicken breast with roasted sweet potato & steamed broccoli",
                    "Evening": "Warm chamomile or spearmint tea"
                },
                "Manage insulin": {
                    "Breakfast": "Eggs (2) scrambled with spinach on wholegrain toast | Green tea",
                    "Mid-morning": "Low-GI fruit (pear or berries) + 10 walnuts",
                    "Lunch": "Lentil soup with a side salad & whole grain bread",
                    "Afternoon snack": "Celery + almond butter",
                    "Dinner": "Turkey mince stir-fry with cauliflower rice & mixed vegetables",
                    "Evening": "Chamomile tea + magnesium supplement (consult doctor)"
                },
                "Lose weight": {
                    "Breakfast": "Overnight oats with flaxseeds, cinnamon & a few blueberries",
                    "Mid-morning": "1 boiled egg + cucumber slices",
                    "Lunch": "Large green salad with grilled tuna, avocado & lemon vinaigrette",
                    "Afternoon snack": "Protein shake (low sugar) or cottage cheese",
                    "Dinner": "Baked cod with asparagus & a small portion of brown rice",
                    "Evening": "Herbal tea"
                }
            }
            
            plan_key = "Manage insulin" if "insulin" in goal.lower() else ("Lose weight" if "weight" in goal.lower() else "Balance hormones")
            plan = MEAL_PLANS[plan_key]
            
            st.markdown(f"""
            <div class='umoyo-card'>
                <div style='font-size:1.2rem; font-weight:700; color:#C9508C; margin-bottom:16px;'>
                    Your {goal} Meal Plan (~{calorie_goal} kcal/day)
                </div>
            """, unsafe_allow_html=True)
            
            meal_icons = {"Breakfast": "☀️", "Mid-morning": "🍎", "Lunch": "🥗",
                          "Afternoon snack": "🥜", "Dinner": "🍽️", "Evening": "🌙"}
            
            for meal, content in plan.items():
                icon = meal_icons.get(meal, "🥄")
                st.markdown(f"**{icon} {meal}:** {content}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Grocery essentials
            st.markdown("#### PCOS Grocery Essentials")
            grocery_cols = st.columns(4)
            grocery = {
                "Proteins": ["Salmon", "Chicken breast", "Turkey mince", "Greek yogurt", "Eggs", "Lentils", "Chickpeas"],
                "Complex Carbs": ["Quinoa", "Brown rice", "Sweet potato", "Whole grain bread", "Oats", "Cauliflower"],
                "Healthy Fats": ["Avocado", "Almonds", "Walnuts", "Olive oil", "Chia seeds", "Flaxseeds"],
                "Anti-inflammatory": ["Berries", "Spinach", "Broccoli", "Turmeric", "Ginger", "Green tea", "Spearmint"],
            }
            for i, (cat, items) in enumerate(grocery.items()):
                with grocery_cols[i]:
                    st.markdown(f"**{cat}**")
                    for item in items:
                        st.markdown(f"• {item}")
    
    with tab2:
        st.markdown("#### Daily Hydration Tracker")
        
        if "hydration" not in st.session_state:
            st.session_state.hydration = 0
        
        glasses = st.session_state.hydration
        goal_glasses = 8
        
        progress = min(glasses / goal_glasses, 1.0)
        st.progress(progress)
        st.markdown(f"**{glasses} / {goal_glasses} glasses today** ({glasses * 250} ml / {goal_glasses * 250} ml)")
        
        c1, c2, c3 = st.columns(3)
        if c1.button("+ 1 Glass (250ml)"):
            st.session_state.hydration = min(glasses + 1, 16)
            st.rerun()
        if c2.button("+ 500ml Bottle"):
            st.session_state.hydration = min(glasses + 2, 16)
            st.rerun()
        if c3.button("Reset Today"):
            st.session_state.hydration = 0
            st.rerun()
        
        if glasses >= goal_glasses:
            st.success("Daily hydration goal reached! Great work.")
        elif glasses >= goal_glasses * 0.5:
            st.info(f"You're halfway there – {goal_glasses - glasses} more glasses to go!")
        else:
            st.warning("Remember to stay hydrated – water supports hormone balance and metabolism.")
    
    with tab3:
        st.markdown("#### Best Foods for PCOS")
        cols = st.columns(2)
        
        with cols[0]:
            st.markdown("**Foods to Embrace**")
            best_foods = [
                ("Spearmint Tea", "May reduce androgen levels naturally"),
                ("Cinnamon", "Improves insulin sensitivity"),
                ("Turmeric", "Powerful anti-inflammatory"),
                ("Berries", "Low-GI, rich in antioxidants"),
                ("Leafy Greens", "Magnesium & folate for hormones"),
                ("Fatty Fish", "Omega-3s reduce inflammation"),
                ("Walnuts", "Supports hormone production"),
                ("Flaxseeds", "Lignans support estrogen balance"),
            ]
            for food, benefit in best_foods:
                st.markdown(f"**{food}** – {benefit}")
        
        with cols[1]:
            st.markdown("**Foods to Limit**")
            avoid_foods = [
                ("Refined Sugar", "Spikes insulin, worsens PCOS"),
                ("White bread/pasta", "High glycemic, raises blood sugar"),
                ("Processed meats", "Pro-inflammatory"),
                ("Dairy (for some)", "May increase androgen in sensitive individuals"),
                ("Alcohol", "Disrupts liver metabolism of hormones"),
                ("Caffeine (excess)", "Can worsen anxiety & cortisol"),
                ("Trans fats", "Increase insulin resistance"),
                ("Soy in excess", "May affect estrogen balance"),
            ]
            for food, reason in avoid_foods:
                st.markdown(f"**{food}** – {reason}")

# ─────────────────────────────────────────────
#  PAGE: FITNESS COACH
# ─────────────────────────────────────────────
elif selected == "Fitness Coach":
    st.markdown("<div class='page-title'>Fitness Coach</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Exercise plans designed to support hormonal balance and PCOS management</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Weekly Plan", "Exercise Library"])
    
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            fitness_level = st.selectbox("Fitness level", ["Beginner", "Intermediate", "Advanced"])
        with c2:
            focus = st.selectbox("Primary focus", ["Hormone balance", "Weight loss", "Build strength", "Reduce stress", "Improve energy"])
        
        if st.button("Generate My Weekly Plan", use_container_width=True):
            plans = {
                "Beginner": [
                    ("Monday", "30-min brisk walk + 10-min stretching"),
                    ("Tuesday", "Rest or gentle yoga (20 min)"),
                    ("Wednesday", "Bodyweight circuit: 3×10 squats, push-ups (modified), lunges"),
                    ("Thursday", "30-min walk + 5-min deep breathing"),
                    ("Friday", "Beginner Pilates or yoga video (30 min)"),
                    ("Saturday", "Fun activity: dancing, swimming, cycling"),
                    ("Sunday", "Full rest + self-care"),
                ],
                "Intermediate": [
                    ("Monday", "45-min moderate run/jog + core work (15 min)"),
                    ("Tuesday", "Strength: Upper body (dumbbell press, rows, shoulder press) – 45 min"),
                    ("Wednesday", "Yoga or stretching (30 min) + 20-min walk"),
                    ("Thursday", "Strength: Lower body (squats, deadlifts, hip thrusts) – 45 min"),
                    ("Friday", "HIIT (20 min) – keep sessions short to manage cortisol"),
                    ("Saturday", "Outdoor activity: hiking, cycling, swimming"),
                    ("Sunday", "Rest + foam rolling"),
                ],
                "Advanced": [
                    ("Monday", "Heavy strength: Lower body (barbell squats, RDLs) – 60 min"),
                    ("Tuesday", "Run 5km + core circuit – 60 min"),
                    ("Wednesday", "Upper body strength (bench, rows, OHP) – 60 min"),
                    ("Thursday", "Active recovery: yoga or light swim – 40 min"),
                    ("Friday", "Full body compound lifts + conditioning – 60 min"),
                    ("Saturday", "Long walk/hike or sport (2 hrs)"),
                    ("Sunday", "Complete rest – prioritize sleep"),
                ]
            }
            
            plan = plans[fitness_level]
            st.markdown(f"### Your {fitness_level} Weekly Plan – Focus: {focus}")
            day_cols = st.columns(7)
            for i, (day, activity) in enumerate(plan):
                with day_cols[i]:
                    bg = "#FFF0F6" if i % 2 == 0 else "#F5F0FF"
                    st.markdown(f"""
                    <div style='background:{bg}; border-radius:10px; padding:10px; border:1px solid #F0C8DC; min-height:140px;'>
                        <div style='font-weight:700; color:#C9508C; margin-bottom:6px;'>{day}</div>
                        <div style='font-size:0.82rem; color:#3D2B3E;'>{activity}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='tip-box' style='margin-top:20px;'>
                <strong>PCOS Exercise Tips:</strong><br>
                • Keep HIIT sessions to max 2x/week – too much raises cortisol<br>
                • Strength training is highly beneficial for insulin sensitivity<br>
                • Walking after meals (10–20 min) significantly reduces blood sugar spikes<br>
                • Prioritize sleep – it's when your hormones repair and reset
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        exercises = {
            "Walking": {"benefit": "Improves insulin sensitivity, low cortisol impact", "frequency": "Daily", "duration": "30–45 min"},
            "Yoga": {"benefit": "Reduces cortisol, improves sleep, balances hormones", "frequency": "3–4x/week", "duration": "30–60 min"},
            "Strength Training": {"benefit": "Builds muscle, boosts metabolism, improves insulin", "frequency": "2–3x/week", "duration": "45–60 min"},
            "Swimming": {"benefit": "Full body, low impact, anti-inflammatory effect", "frequency": "2–3x/week", "duration": "30–45 min"},
            "Cycling": {"benefit": "Great cardio, low joint stress", "frequency": "3–4x/week", "duration": "30–60 min"},
            "Pilates": {"benefit": "Core strength, posture, stress reduction", "frequency": "2–3x/week", "duration": "30–45 min"},
        }
        
        ex_cols = st.columns(3)
        for i, (ex, info) in enumerate(exercises.items()):
            with ex_cols[i % 3]:
                st.markdown(f"""
                <div class='umoyo-card'>
                    <div style='font-weight:700; color:#C9508C; font-size:1.05rem;'>{ex}</div>
                    <div style='color:#5A3D4E; font-size:0.85rem; margin-top:8px;'>{info['benefit']}</div>
                    <div style='color:#9B7A8E; font-size:0.8rem; margin-top:8px;'>
                        Frequency: {info['frequency']}<br>Duration: {info['duration']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: MENTAL WELLNESS
# ─────────────────────────────────────────────
elif selected == "Mental Wellness":
    st.markdown("<div class='page-title'>Mental Wellness</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Your emotional wellbeing matters – track, reflect, and grow</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Daily Check-in", "Mood Journal", "Wellness Resources"])
    
    with tab1:
        st.markdown("#### How are you feeling today?")
        
        mood_emojis = {"Wonderful": 10, "Good": 8, "Okay": 6, "Low": 4, "Struggling": 2}
        mood_choice = st.select_slider(
            "Overall mood",
            options=list(mood_emojis.keys()),
            value="Okay"
        )
        
        energy = st.slider("Energy level (1–10)", 1, 10, 5)
        anxiety = st.slider("Anxiety level (1–10)", 1, 10, 3)
        sleep_quality = st.selectbox("Last night's sleep", ["Excellent", "Good", "Fair", "Poor", "Very poor"])
        
        gratitude = st.text_area("One thing you're grateful for today", placeholder="Even something small counts...")
        intention = st.text_area("Your intention for today", placeholder="What do you want to focus on?")
        
        if st.button("Save Check-in", use_container_width=True):
            entry = {
                "date": str(datetime.date.today()),
                "label": mood_choice,
                "score": mood_emojis[mood_choice],
                "energy": energy,
                "anxiety": anxiety,
                "sleep": sleep_quality,
                "gratitude": gratitude,
                "intention": intention,
                "timestamp": datetime.datetime.now().isoformat()
            }
            st.session_state.mood_log.append(entry)
            st.success("Check-in saved. Taking care of your mental health is powerful.")
            
            # Affirmation based on mood
            affirmations = {
                "Wonderful": "You're radiating wellness today. Keep nurturing that energy.",
                "Good": "You're doing well. Small consistent steps lead to big changes.",
                "Okay": "It's okay to be okay. Every day doesn't have to be perfect.",
                "Low": "Be gentle with yourself today. Rest is productive too.",
                "Struggling": "You showed up for yourself today – that's courage. You're not alone."
            }
            st.info(f"**Daily Affirmation:** {affirmations[mood_choice]}")
    
    with tab2:
        if not st.session_state.mood_log:
            st.info("Complete your first check-in to see your mood journal.")
        else:
            df_mood = pd.DataFrame(st.session_state.mood_log)
            
            # Mood trend chart
            fig = px.line(df_mood, x="date", y="score",
                          title="Mood Trend",
                          color_discrete_sequence=["#C9508C"],
                          labels={"score": "Mood Score", "date": "Date"},
                          markers=True)
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(255,240,248,0.4)",
                yaxis={"range": [0, 11]},
                font={"color": "#3D2B3E"}, height=260
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Energy vs anxiety
            if "energy" in df_mood.columns and "anxiety" in df_mood.columns:
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(x=df_mood["date"], y=df_mood["energy"],
                                          name="Energy", line={"color": "#E8708A"}))
                fig2.add_trace(go.Scatter(x=df_mood["date"], y=df_mood["anxiety"],
                                          name="Anxiety", line={"color": "#8A4FBB"}))
                fig2.update_layout(title="Energy vs Anxiety Levels",
                                    paper_bgcolor="rgba(0,0,0,0)",
                                    plot_bgcolor="rgba(255,240,248,0.4)",
                                    font={"color": "#3D2B3E"}, height=260)
                st.plotly_chart(fig2, use_container_width=True)
            
            # Recent journal entries
            st.markdown("#### Recent Journal Entries")
            for entry in reversed(st.session_state.mood_log[-5:]):
                with st.expander(f"{entry['date']} – {entry['label']}"):
                    if entry.get("gratitude"):
                        st.markdown(f"**Grateful for:** {entry['gratitude']}")
                    if entry.get("intention"):
                        st.markdown(f"**Intention:** {entry['intention']}")
                    st.markdown(f"Sleep: {entry.get('sleep','—')} | Energy: {entry.get('energy','—')}/10 | Anxiety: {entry.get('anxiety','—')}/10")
    
    with tab3:
        st.markdown("#### Managing Mental Health with PCOS")
        
        resources = [
            ("Anxiety & PCOS", "PCOS increases anxiety risk due to hormonal fluctuations. Techniques: diaphragmatic breathing, progressive muscle relaxation, journaling."),
            ("Depression", "Low serotonin and hormonal imbalance can contribute to depression. Regular exercise, social connection, and therapy are evidence-based interventions."),
            ("Body Image", "PCOS symptoms like weight gain and hair changes can affect self-esteem. Practice body neutrality and focus on what your body can do, not just how it looks."),
            ("Stress & Cortisol", "Chronic stress raises cortisol, which worsens insulin resistance and inflammation in PCOS. Prioritize sleep, boundaries, and relaxation."),
            ("Seeking Help", "Therapy (especially CBT) is highly effective. Don't hesitate to seek professional support – mental health IS physical health."),
        ]
        
        for title, content in resources:
            with st.expander(f"**{title}**"):
                st.markdown(content)
        
        st.markdown("""
        <div class='tip-box'>
            <strong>Crisis Resources:</strong><br>
            If you are struggling with severe depression or crisis, please reach out to a mental health professional or crisis helpline in your country.
            You are not alone, and support is available.
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: REPORTS
# ─────────────────────────────────────────────
elif selected == "Reports":
    st.markdown("<div class='page-title'>Health Reports</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Generate comprehensive summaries of your wellness journey</div>", unsafe_allow_html=True)
    
    today = datetime.date.today()
    
    # Summary stats
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='metric-card'><div class='metric-value'>{len(st.session_state.symptom_log)}</div><div class='metric-label'>Symptom Logs</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><div class='metric-value'>{len(st.session_state.cycle_log)}</div><div class='metric-label'>Periods Logged</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card'><div class='metric-value'>{len(st.session_state.mood_log)}</div><div class='metric-label'>Mood Check-ins</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='metric-card'><div class='metric-value'>{compute_wellness_score()}</div><div class='metric-label'>Wellness Score</div></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("Generate Wellness Report (Text)", use_container_width=True):
        report_lines = [
            f"UMOYO AI – WELLNESS REPORT",
            f"Generated: {today.strftime('%B %d, %Y')}",
            f"User: {st.session_state.user_name}",
            "=" * 50,
            "",
            "WELLNESS SUMMARY",
            f"Current Wellness Score: {compute_wellness_score()}/100",
            f"Total Symptom Logs: {len(st.session_state.symptom_log)}",
            f"Total Period Logs: {len(st.session_state.cycle_log)}",
            f"Total Mood Check-ins: {len(st.session_state.mood_log)}",
            "",
        ]
        
        if st.session_state.risk_result:
            risk = st.session_state.risk_result
            level = "High" if risk >= 65 else ("Moderate" if risk >= 40 else "Low")
            report_lines += [
                "PCOS RISK ASSESSMENT",
                f"Last Risk Score: {risk:.1f}% ({level} Risk)",
                f"Assessment Date: {st.session_state.last_assessment or 'Unknown'}",
                "",
            ]
        
        if st.session_state.symptom_log:
            recent = st.session_state.symptom_log[-7:]
            avg_sev = sum(l.get("severity", 0) for l in recent) / len(recent)
            report_lines += [
                "SYMPTOM SUMMARY (Last 7 Logs)",
                f"Average Severity: {avg_sev:.1f}/10",
                "",
            ]
        
        if st.session_state.cycle_log and len(st.session_state.cycle_log) >= 2:
            df_cy = pd.DataFrame(st.session_state.cycle_log)
            df_cy["start"] = pd.to_datetime(df_cy["start"])
            df_cy = df_cy.sort_values("start")
            df_cy["cycle_length"] = df_cy["start"].diff().dt.days
            avg_cyc = df_cy["cycle_length"].dropna().mean()
            report_lines += [
                "CYCLE SUMMARY",
                f"Average Cycle Length: {avg_cyc:.0f} days",
                f"Total Periods Logged: {len(st.session_state.cycle_log)}",
                "",
            ]
        
        report_lines += [
            "─" * 50,
            "DISCLAIMER: This report is for personal wellness tracking only.",
            "It does not constitute medical advice or diagnosis.",
            "Please consult a qualified healthcare provider for medical guidance.",
            "─" * 50,
        ]
        
        report_text = "\n".join(report_lines)
        st.download_button(
            label="Download Report as .txt",
            data=report_text,
            file_name=f"umoyo_wellness_report_{today}.txt",
            mime="text/plain",
            use_container_width=True
        )
        st.text_area("Report Preview", value=report_text, height=400)
    
    # CSV export
    st.markdown("---")
    st.markdown("#### Export Your Data")
    col_a, col_b = st.columns(2)
    
    if col_a.button("Export Symptom Log (CSV)"):
        if st.session_state.symptom_log:
            df = pd.DataFrame(st.session_state.symptom_log)
            csv = df.to_csv(index=False)
            st.download_button("Download Symptom CSV", csv,
                                f"symptoms_{today}.csv", "text/csv")
        else:
            st.info("No symptom data to export yet.")
    
    if col_b.button("Export Mood Log (CSV)"):
        if st.session_state.mood_log:
            df = pd.DataFrame(st.session_state.mood_log)
            csv = df.to_csv(index=False)
            st.download_button("Download Mood CSV", csv,
                                f"mood_log_{today}.csv", "text/csv")
        else:
            st.info("No mood data to export yet.")

# ─────────────────────────────────────────────
#  PAGE: SETTINGS
# ─────────────────────────────────────────────
elif selected == "Settings":
    st.markdown("<div class='page-title'>Settings</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Configure your Umoyo AI experience</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Profile & AI Keys", "Data Management"])
    
    with tab1:
        st.markdown("#### Your Profile")
        name = st.text_input("Your name", value=st.session_state.user_name)
        if st.button("Update Name"):
            st.session_state.user_name = name
            st.success("Name updated!")
        
        st.markdown("---")
        st.markdown("#### AI Provider Configuration")
        st.markdown("""
        <div class='tip-box'>
            Umoyo AI works with multiple AI providers. Add your free API key to enable live AI conversations.
            <br><strong>Gemini is recommended</strong> – Google offers a generous free tier.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Google Gemini (Recommended – Free)**")
        st.markdown("Get your free API key at: [aistudio.google.com](https://aistudio.google.com/app/apikey)")
        gemini_key = st.text_input("Gemini API Key", value=GEMINI_API_KEY,
                                    type="password", placeholder="AIza...")
        
        st.markdown("**Groq (Fallback – Free)**")
        st.markdown("Get your free API key at: [console.groq.com](https://console.groq.com)")
        groq_key = st.text_input("Groq API Key", value=GROQ_API_KEY,
                                  type="password", placeholder="gsk_...")
        
        if st.button("Save AI Keys (Session Only)"):
            os.environ["GEMINI_API_KEY"] = gemini_key
            os.environ["GROQ_API_KEY"] = groq_key
            st.success("Keys saved for this session. For permanent deployment, add to Streamlit Secrets or .env file.")
        
        st.markdown("---")
        st.markdown("#### Deployment Note")
        st.info("To permanently configure API keys on Streamlit Cloud, add them in **App Settings → Secrets** as:\n```\nGEMINI_API_KEY = \"your_key_here\"\nGROQ_API_KEY = \"your_key_here\"\n```")
    
    with tab2:
        st.markdown("#### Data Management")
        st.warning("Session data is stored in memory only. Refreshing the page will clear all data.")
        
        col_a, col_b = st.columns(2)
        if col_a.button("Clear Symptom Logs", use_container_width=True):
            st.session_state.symptom_log = []
            st.success("Symptom logs cleared.")
        if col_b.button("Clear Mood Logs", use_container_width=True):
            st.session_state.mood_log = []
            st.success("Mood logs cleared.")
        
        c1, c2 = st.columns(2)
        if c1.button("Clear Cycle Logs", use_container_width=True):
            st.session_state.cycle_log = []
            st.success("Cycle logs cleared.")
        if c2.button("Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.success("Chat cleared.")
        
        if st.button("Reset All Data", use_container_width=True, type="primary"):
            for k in ["messages", "symptom_log", "cycle_log", "mood_log",
                      "weight_log", "wellness_scores", "risk_result"]:
                st.session_state[k] = [] if k != "risk_result" else None
            st.success("All data reset.")

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class='app-footer'>
    Umoyo AI is an educational wellness tool, not a medical device.<br>
    Always consult a qualified healthcare provider for medical advice.<br>
    © 2025 Umoyo AI Health · Umoyo means 'Life' in Chewa
</div>
""", unsafe_allow_html=True)
