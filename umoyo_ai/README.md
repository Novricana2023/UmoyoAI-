# 🌸 Umoyo AI – Intelligent PCOS Health Companion

> *Umoyo means "Life" in Chewa*

A premium, production-ready PCOS health companion built with Streamlit. Powered by Google Gemini AI with Groq fallback. Fully deployable on Streamlit Community Cloud.

---

## Features

- **AI Companion** – Warm, evidence-based PCOS chat assistant (Gemini/Groq/Offline)
- **PCOS Risk Assessment** – ML model prediction with personalized recommendations
- **Symptom Tracker** – Daily logging with trend analysis charts
- **Cycle Tracker** – Period logging, cycle prediction, ovulation estimation
- **Nutrition Coach** – Meal plan generator, hydration tracker, PCOS foods guide
- **Fitness Coach** – Weekly exercise plans tailored to PCOS
- **Mental Wellness** – Daily mood check-ins, journaling, emotional support
- **Reports & Data Export** – Wellness reports downloadable as .txt and .csv

---

## Deploy to Streamlit Cloud (Free)

### Step 1 – Push to GitHub
```bash
git init
git add .
git commit -m "Initial Umoyo AI deployment"
git remote add origin https://github.com/YOUR_USERNAME/umoyo-ai.git
git push -u origin main
```

### Step 2 – Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **New app**
3. Select your GitHub repo
4. Set **Main file path**: `app.py`
5. Click **Deploy**

### Step 3 – Add API Keys (Optional – for live AI)
In Streamlit Cloud → **App Settings → Secrets**, add:
```toml
GEMINI_API_KEY = "your_gemini_key_here"
GROQ_API_KEY = "your_groq_key_here"
```

Get **free** Gemini key at: https://aistudio.google.com/app/apikey  
Get **free** Groq key at: https://console.groq.com

> **Note:** Without API keys, the app runs in offline mode with built-in PCOS knowledge responses. All other features (tracking, risk assessment, charts) work fully without any API key.

---

## Local Development

```bash
# Clone and set up
git clone https://github.com/YOUR_USERNAME/umoyo-ai.git
cd umoyo-ai

# Install dependencies
pip install -r requirements.txt

# (Optional) Set API keys
export GEMINI_API_KEY="your_key"
export GROQ_API_KEY="your_key"

# Run
streamlit run app.py
```

---

## Project Structure
```
umoyo-ai/
├── app.py                          # Main application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .streamlit/
│   ├── config.toml                 # Streamlit theme & server config
│   └── secrets.toml.template       # API key template
└── model_artifacts/
    ├── best_svc_model.joblib       # Trained PCOS SVC model
    ├── scaler.joblib               # Feature scaler
    └── feature_names.json          # Model feature names
```

---

## AI Provider Architecture

Priority order (automatic failover):
1. **Google Gemini 1.5 Flash** – Primary (free tier: generous)
2. **Groq (Llama 3)** – Fallback (free tier: fast)
3. **Offline Mode** – Built-in PCOS knowledge base (always available)

No user ever sees a broken experience – the app gracefully falls back.

---

## Disclaimer

Umoyo AI is an educational wellness tool, not a medical device or diagnostic platform.
It does not provide medical diagnoses. Always consult a qualified healthcare provider.

---

© 2025 Umoyo AI Health
