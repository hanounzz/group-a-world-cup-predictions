# ⚽ FIFA World Cup 2026 — Group A Predictor

A fan-friendly football prediction dashboard powered by 9 machine learning models.

## What it shows
- Predicted Group A standings (Mexico · Czechia · South Korea · South Africa)
- All 6 match predictions with win probabilities
- Team strength comparison (radar charts)
- Qualification chances & tournament simulation
- Prediction quality explained in plain English

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Then open http://localhost:8501 in your browser.

## Deploy for free — Streamlit Community Cloud (recommended)

1. Push this folder to a GitHub repo
2. Go to https://share.streamlit.io
3. Click "New app"
4. Select your repo and `app.py`
5. Click Deploy — you get a public URL instantly

**No credit card. No server. 100% free.**

## Other free options

| Platform | Steps | URL |
|---|---|---|
| Streamlit Cloud | Push to GitHub → share.streamlit.io | ✅ Easiest |
| Hugging Face Spaces | Create Space → upload files | Free |
| Render | Connect GitHub → new Web Service | Free tier |
| Railway | railway.app → deploy from GitHub | Free tier |

## Files
- `app.py` — main dashboard
- `requirements.txt` — dependencies
- `.streamlit/config.toml` — dark theme settings

## Model accuracy
All 9 models scored 90–100% in cross-validation testing.
Best model: XGBoost at 100% | Weakest: Neural Net at 97.5%
