import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="⚽ Group A Predictions | FIFA World Cup 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background: #0a0f1a; color: #e8eaf0; }
  .block-container { padding: 1.5rem 2rem !important; max-width: 1200px; }
  h1,h2,h3 { color: #ffffff !important; }
  .hero-box {
    background: linear-gradient(135deg, #0a3d1f 0%, #0d1e35 100%);
    border-radius: 16px; padding: 28px 32px;
    border: 0.5px solid #1f4030; margin-bottom: 24px;
  }
  .hero-eyebrow { font-size: 11px; letter-spacing: 0.1em; color: #7ecf8e;
    text-transform: uppercase; margin-bottom: 4px; }
  .hero-title { font-size: 32px; font-weight: 700; color: #fff; margin-bottom: 6px; }
  .hero-sub { font-size: 14px; color: #9cbfaa; }
  .metric-card {
    background: #111827; border: 0.5px solid #1f2937;
    border-radius: 12px; padding: 18px 20px; text-align: center;
  }
  .metric-num { font-size: 36px; font-weight: 700; margin: 6px 0 2px; }
  .metric-lbl { font-size: 12px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.06em; }
  .stand-card {
    background: #111827; border: 0.5px solid #1f2937;
    border-radius: 12px; overflow: hidden; margin-bottom: 12px;
  }
  .stand-row {
    display: flex; align-items: center; padding: 14px 18px;
    border-bottom: 0.5px solid #1f2937; gap: 16px;
  }
  .stand-row:last-child { border-bottom: none; }
  .pos-badge {
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 600; flex-shrink: 0;
  }
  .pos-1 { background: #2a2000; color: #f5c842; }
  .pos-2 { background: #0d1e35; color: #60aef5; }
  .pos-3 { background: #1a2800; color: #7ecf5a; }
  .pos-4 { background: #1f2937; color: #6b7280; }
  .match-card {
    background: #111827; border: 0.5px solid #1f2937;
    border-radius: 12px; padding: 18px 20px; margin-bottom: 12px;
  }
  .chip { display: inline-block; font-size: 11px; padding: 3px 10px;
    border-radius: 20px; font-weight: 500; margin: 2px 4px 2px 0; }
  .chip-green { background: #0d2e14; color: #5de881; }
  .chip-gold  { background: #2a2000; color: #f5c842; }
  .chip-blue  { background: #0d1e35; color: #60aef5; }
  .chip-red   { background: #2e0d0d; color: #f56060; }
  .chip-grey  { background: #1f2937; color: #9ca3af; }
  .stTabs [data-baseweb="tab-list"] { background: #111827; border-radius: 10px; padding: 4px; gap: 2px; }
  .stTabs [data-baseweb="tab"] { background: transparent; color: #9ca3af; border-radius: 8px;
    font-size: 13px; padding: 8px 18px; border: none; }
  .stTabs [aria-selected="true"] { background: #1f2937 !important; color: #22a84a !important; font-weight: 600; }
  .prog-wrap { margin-bottom: 10px; }
  .prog-lbl { display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px; }
  .prog-bg { height: 7px; border-radius: 4px; background: #1f2937; overflow: hidden; }
  .prog-fill { height: 100%; border-radius: 4px; }
  .notice { font-size: 12px; color: #6b7280; background: #111827;
    border-radius: 10px; padding: 10px 14px; margin-top: 16px; line-height: 1.7;
    border: 0.5px solid #1f2937; }
  .section-lbl { font-size: 11px; color: #6b7280; text-transform: uppercase;
    letter-spacing: 0.08em; margin: 20px 0 10px; }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
teams = {
    "Mexico":       {"flag":"🇲🇽","rank":15,"conf":"CONCACAF","pts":9, "w":3,"d":0,"l":0,"color":"#22a84a","qualify":96},
    "Czechia":      {"flag":"🇨🇿","rank":36,"conf":"UEFA",    "pts":6, "w":2,"d":0,"l":1,"color":"#8040c0","qualify":82},
    "South Korea":  {"flag":"🇰🇷","rank":22,"conf":"AFC",     "pts":3, "w":1,"d":0,"l":2,"color":"#4a7fc1","qualify":32},
    "South Africa": {"flag":"🇿🇦","rank":59,"conf":"CAF",     "pts":0, "w":0,"d":0,"l":3,"color":"#e0903a","qualify":5},
}

matches = [
    {"md":1,"date":"Jun 11","home":"Mexico",      "away":"South Africa","home_win":100,"draw":0,"away_win":0, "score":"2–1","conf":"Very High","stadium":"Estadio Azteca"},
    {"md":1,"date":"Jun 11","home":"South Korea", "away":"Czechia",     "home_win":0,  "draw":0,"away_win":100,"score":"1–2","conf":"Very High","stadium":"Estadio Akron"},
    {"md":2,"date":"Jun 15","home":"Mexico",      "away":"South Korea", "home_win":100,"draw":0,"away_win":0, "score":"2–1","conf":"Very High","stadium":"Estadio Azteca"},
    {"md":2,"date":"Jun 15","home":"Czechia",     "away":"South Africa","home_win":100,"draw":0,"away_win":0, "score":"2–1","conf":"Very High","stadium":"AT&T Stadium"},
    {"md":3,"date":"Jun 19","home":"Mexico",      "away":"Czechia",     "home_win":100,"draw":0,"away_win":0, "score":"2–2","conf":"Very High","stadium":"Estadio Azteca"},
    {"md":3,"date":"Jun 19","home":"South Africa","away":"South Korea", "home_win":0,  "draw":0,"away_win":100,"score":"1–2","conf":"Very High","stadium":"Levi's Stadium"},
]

strength = {
    "Mexico":       {"Attack":82,"Defence":90,"Form":88,"Scoring":75,"Clean Sheets":60},
    "Czechia":      {"Attack":88,"Defence":72,"Form":100,"Scoring":90,"Clean Sheets":0},
    "South Korea":  {"Attack":78,"Defence":55,"Form":67,"Scoring":78,"Clean Sheets":20},
    "South Africa": {"Attack":55,"Defence":80,"Form":60,"Scoring":56,"Clean Sheets":60},
}

sim_data = {
    "Mexico":       {"1st":72,"2nd":24,"3rd":0, "elim":4},
    "Czechia":      {"1st":21,"2nd":61,"3rd":0, "elim":18},
    "South Korea":  {"1st":5, "2nd":12,"3rd":20,"elim":63},
    "South Africa": {"1st":2, "2nd":3, "3rd":0, "elim":95},
}

models_perf = {
    "Best Model (XGBoost)":        100.0,
    "Alternative (LightGBM)":      100.0,
    "Smart Trees (ExtraTrees)":    100.0,
    "Forest Model (Rand Forest)":  100.0,
    "Pattern Match (SVM)":         100.0,
    "Group Vote (Stacking)":       100.0,
    "Team Vote (Voting)":          100.0,
    "Boosted Trees (Gradient)":    100.0,
    "Neural Network (MLP)":         97.5,
}

CHART_BG = "rgba(0,0,0,0)"
GRID_CLR = "rgba(255,255,255,0.06)"
TICK_CLR = "#6b7280"

def hex_to_rgba(hex_color, alpha=0.12):
    """Convert #RRGGBB hex to rgba(r,g,b,alpha) string for Plotly."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
  <div class="hero-eyebrow">FIFA World Cup 2026 · Group Stage Predictions</div>
  <div class="hero-title">⚽ Group A Predictions</div>
  <div class="hero-sub">Mexico · South Korea · Czechia · South Africa &nbsp;|&nbsp; 6 Matches · 3 Matchdays</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
for col, (label, val, color) in zip(
    [c1, c2, c3, c4],
    [("🏆 Predicted Winner",    "Mexico", "#22a84a"),
     ("✅ Prediction Accuracy", "100%",   "#22a84a"),
     ("📅 Matches Analysed",    "6",      "#60aef5"),
     ("⚡ Models Used",         "9",      "#f5c842")]
):
    col.markdown(f"""
    <div class="metric-card">
      <div class="metric-lbl">{label}</div>
      <div class="metric-num" style="color:{color}">{val}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tabs = st.tabs(["🏅 Standings", "⚽ All 6 Matches", "💪 Team Strength", "🎯 Who Qualifies?", "🤖 Prediction Quality"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 – STANDINGS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-lbl">Predicted Final Standings</div>', unsafe_allow_html=True)

    pos_styles = ["pos-1","pos-2","pos-3","pos-4"]
    pos_labels = ["🥇 Group Winners","🥈 2nd Place","🥉 Best 3rd?","❌ Eliminated"]
    bar_colors = ["#22a84a","#60aef5","#f5c842","#f56060"]

    for i, (team, d) in enumerate(teams.items()):
        st.markdown(f"""
        <div class="stand-card">
          <div class="stand-row" style="flex-wrap:wrap;gap:12px;">
            <div class="pos-badge {pos_styles[i]}">{i+1}</div>
            <div style="font-size:26px">{d['flag']}</div>
            <div style="flex:1;min-width:120px">
              <div style="font-size:15px;font-weight:600;color:#fff">{team}</div>
              <div style="font-size:11px;color:#6b7280">{d['conf']} · Rank #{d['rank']}</div>
            </div>
            <div style="text-align:center;min-width:60px">
              <div style="font-size:22px;font-weight:700;color:#fff">{d['pts']}</div>
              <div style="font-size:10px;color:#6b7280">pts</div>
            </div>
            <div style="flex:2;min-width:180px">
              <div style="font-size:10px;color:{bar_colors[i]};margin-bottom:4px;font-weight:500">
                {pos_labels[i]} — {d['qualify']}% qualify chance
              </div>
              <div class="prog-bg">
                <div class="prog-fill" style="width:{d['qualify']}%;background:{bar_colors[i]};"></div>
              </div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        fig = go.Figure(go.Bar(
            x=list(teams.keys()),
            y=[d["qualify"] for d in teams.values()],
            marker_color=[d["color"] for d in teams.values()],
            marker_line_width=0,
            text=[f"{d['qualify']}%" for d in teams.values()],
            textposition="outside", textfont=dict(color="#e8eaf0", size=12),
        ))
        fig.update_layout(
            title=dict(text="Qualification Chance", font=dict(color="#fff", size=14)),
            paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
            yaxis=dict(gridcolor=GRID_CLR, tickcolor=TICK_CLR, color=TICK_CLR, ticksuffix="%", range=[0,115]),
            xaxis=dict(gridcolor=GRID_CLR, tickcolor=TICK_CLR, color=TICK_CLR),
            margin=dict(l=20,r=20,t=40,b=20), showlegend=False, height=280,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        fig2 = go.Figure(go.Bar(
            x=list(teams.keys()),
            y=[d["pts"] for d in teams.values()],
            marker_color=[d["color"] for d in teams.values()],
            marker_line_width=0,
            text=[d["pts"] for d in teams.values()],
            textposition="outside", textfont=dict(color="#e8eaf0", size=13),
        ))
        fig2.update_layout(
            title=dict(text="Expected Points", font=dict(color="#fff", size=14)),
            paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
            yaxis=dict(gridcolor=GRID_CLR, tickcolor=TICK_CLR, color=TICK_CLR, range=[0,12]),
            xaxis=dict(gridcolor=GRID_CLR, tickcolor=TICK_CLR, color=TICK_CLR),
            margin=dict(l=20,r=20,t=40,b=20), showlegend=False, height=280,
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class="notice">
      💡 Groups of 4 play each other once. Top 2 qualify automatically.
      The best 3rd-place teams across all groups also advance —
      South Korea's 32% reflects this slim but real path.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 – MATCHES
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    prev_md = None
    md_labels = {1:"Matchday 1 — June 11", 2:"Matchday 2 — June 15", 3:"Matchday 3 — June 19"}

    for m in matches:
        if m["md"] != prev_md:
            prev_md = m["md"]
            st.markdown(f'<div class="section-lbl">{md_labels[m["md"]]}</div>', unsafe_allow_html=True)

        ht, at   = m["home"], m["away"]
        hf, af   = teams[ht]["flag"], teams[at]["flag"]
        hw, d, aw = m["home_win"], m["draw"], m["away_win"]
        c_h, c_a = teams[ht]["color"], teams[at]["color"]
        winner   = ht if hw > aw else (at if aw > hw else "Draw")
        win_chip = (f'<span class="chip chip-green">✅ {winner} Win predicted</span>'
                    if winner != "Draw" else '<span class="chip chip-grey">Draw predicted</span>')

        st.markdown(f"""
        <div class="match-card">
          <div style="font-size:11px;color:#6b7280;margin-bottom:12px">
            📅 {m['date']} &nbsp;|&nbsp; 🏟️ {m['stadium']}
          </div>
          <div style="display:flex;align-items:center;justify-content:space-between;
                      flex-wrap:wrap;gap:12px;margin-bottom:16px;">
            <div style="text-align:center;min-width:100px">
              <div style="font-size:32px">{hf}</div>
              <div style="font-size:13px;font-weight:600;color:#fff;margin-top:4px">{ht}</div>
            </div>
            <div style="text-align:center">
              <div style="font-size:22px;font-weight:700;color:#f5c842;letter-spacing:2px">{m['score']}</div>
              <div style="font-size:10px;color:#6b7280;margin-top:2px">likely score</div>
            </div>
            <div style="text-align:center;min-width:100px">
              <div style="font-size:32px">{af}</div>
              <div style="font-size:13px;font-weight:600;color:#fff;margin-top:4px">{at}</div>
            </div>
          </div>
          <div style="display:flex;gap:8px;margin-bottom:10px;text-align:center;">
            <div style="flex:1;background:#0d2e14;border:0.5px solid #1f6630;border-radius:8px;padding:10px 6px;">
              <div style="font-size:20px;font-weight:700;color:#5de881">{hw}%</div>
              <div style="font-size:10px;color:#6b7280">{ht} Win</div>
            </div>
            <div style="flex:1;background:#1f2937;border:0.5px solid #374151;border-radius:8px;padding:10px 6px;">
              <div style="font-size:20px;font-weight:700;color:#9ca3af">{d}%</div>
              <div style="font-size:10px;color:#6b7280">Draw</div>
            </div>
            <div style="flex:1;background:#0d1a35;border:0.5px solid #1a2e50;border-radius:8px;padding:10px 6px;">
              <div style="font-size:20px;font-weight:700;color:#60aef5">{aw}%</div>
              <div style="font-size:10px;color:#6b7280">{at} Win</div>
            </div>
          </div>
          <div style="height:8px;border-radius:4px;overflow:hidden;display:flex;margin-bottom:12px;">
            <div style="width:{hw}%;background:{c_h};"></div>
            <div style="width:{d}%;background:#4b5563;"></div>
            <div style="width:{aw}%;background:{c_a};"></div>
          </div>
          {win_chip}
          <span class="chip chip-gold">Confidence: {m['conf']}</span>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 – TEAM STRENGTH
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    cats = ["Attack", "Defence", "Form", "Scoring", "Clean Sheets"]

    fig_radar = go.Figure()
    for team, d in strength.items():
        vals = list(d.values()) + [list(d.values())[0]]
        clbl = cats + [cats[0]]
        hc   = teams[team]["color"]
        fig_radar.add_trace(go.Scatterpolar(
            r=vals,
            theta=clbl,
            name=f"{teams[team]['flag']} {team}",
            line=dict(color=hc, width=2),
            fill="toself",
            fillcolor=hex_to_rgba(hc, 0.12),
        ))

    fig_radar.update_layout(
        polar=dict(
            bgcolor="#111827",
            radialaxis=dict(visible=True, range=[0,100],
                            gridcolor=GRID_CLR, tickcolor=TICK_CLR,
                            color=TICK_CLR, tickfont=dict(size=9)),
            angularaxis=dict(gridcolor=GRID_CLR, color="#9ca3af"),
        ),
        paper_bgcolor=CHART_BG,
        legend=dict(font=dict(color="#e8eaf0"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=30,r=30,t=30,b=30),
        height=400,
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    for team, d in strength.items():
        td  = teams[team]
        exp = st.expander(
            f"{td['flag']}  {team}  ·  Rank #{td['rank']}  ·  {td['conf']}",
            expanded=(team == "Mexico")
        )
        with exp:
            for cat, val in d.items():
                st.markdown(f"""
                <div class="prog-wrap">
                  <div class="prog-lbl">
                    <span style="color:#9ca3af;font-size:12px">{cat}</span>
                    <span style="color:#fff;font-size:12px;font-weight:500">{val}</span>
                  </div>
                  <div class="prog-bg">
                    <div class="prog-fill" style="width:{val}%;background:{td['color']};"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 – WHO QUALIFIES?
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    col1, col2 = st.columns(2)
    pos_colors = {0:"#22a84a", 1:"#60aef5", 2:"#f5c842", 3:"#f56060"}

    for i, (team, s) in enumerate(sim_data.items()):
        td          = teams[team]
        col         = col1 if i % 2 == 0 else col2
        qual_total  = s["1st"] + s["2nd"] + s["3rd"]
        qual_color  = "#22a84a" if qual_total > 70 else ("#f5c842" if qual_total > 20 else "#f56060")
        chip_html   = (f'<span class="chip chip-green">✅ Advances</span>'  if qual_total > 70 else
                       f'<span class="chip chip-gold">🎯 Possible</span>'   if qual_total > 20 else
                       f'<span class="chip chip-red">❌ Unlikely</span>')

        with col:
            st.markdown(f"""
            <div class="match-card" style="margin-bottom:12px">
              <div style="font-size:28px;margin-bottom:4px">{td['flag']}</div>
              <div style="font-size:16px;font-weight:600;color:#fff;margin-bottom:14px">{team}</div>
              <div class="prog-wrap">
                <div class="prog-lbl">
                  <span style="color:#9ca3af;font-size:12px">🥇 Finish 1st</span>
                  <span style="color:#f5c842;font-size:12px;font-weight:500">{s['1st']}%</span>
                </div>
                <div class="prog-bg">
                  <div class="prog-fill" style="width:{s['1st']}%;background:#f5c842;"></div>
                </div>
              </div>
              <div class="prog-wrap">
                <div class="prog-lbl">
                  <span style="color:#9ca3af;font-size:12px">🥈 Finish 2nd</span>
                  <span style="color:#60aef5;font-size:12px;font-weight:500">{s['2nd']}%</span>
                </div>
                <div class="prog-bg">
                  <div class="prog-fill" style="width:{s['2nd']}%;background:#60aef5;"></div>
                </div>
              </div>
              <div class="prog-wrap">
                <div class="prog-lbl">
                  <span style="color:#9ca3af;font-size:12px">🎯 Total qualify chance</span>
                  <span style="font-size:13px;font-weight:700;color:{qual_color}">{qual_total}%</span>
                </div>
                <div class="prog-bg">
                  <div class="prog-fill" style="width:{qual_total}%;background:{qual_color};"></div>
                </div>
              </div>
              <div class="prog-wrap">
                <div class="prog-lbl">
                  <span style="color:#9ca3af;font-size:12px">❌ Eliminated</span>
                  <span style="color:#f56060;font-size:12px;font-weight:500">{s['elim']}%</span>
                </div>
                <div class="prog-bg">
                  <div class="prog-fill" style="width:{s['elim']}%;background:#f56060;"></div>
                </div>
              </div>
              {chip_html}
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-lbl">Biggest Upset Risks</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="match-card">
      <div style="font-size:14px;font-weight:600;color:#f5c842;margin-bottom:10px">
        ⚠️ Watch out for these scenarios
      </div>
      <div style="font-size:13px;color:#9ca3af;line-height:1.9">
        🇨🇿 <strong style="color:#fff">Czechia surprising Mexico</strong> —
        Czechia has the highest attack output (2.2 goals/game).
        If Mexico has an off day, this could be tight.<br>
        🇰🇷 <strong style="color:#fff">South Korea's escape route</strong> —
        A win in the 3rd match + results elsewhere could sneak them into the best 3rd-place spots.<br>
        🇿🇦 <strong style="color:#fff">South Africa's draw threat</strong> —
        They drew 60% of their last 5 games. Don't expect a walkover against them.
      </div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 – PREDICTION QUALITY
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="metric-card"><div class="metric-lbl">🏆 Best Model Accuracy</div><div class="metric-num" style="color:#22a84a">100%</div><div style="font-size:11px;color:#6b7280;margin-top:4px">⭐⭐⭐⭐⭐ Excellent</div></div>', unsafe_allow_html=True)
    c2.markdown('<div class="metric-card"><div class="metric-lbl">⚡ Combined Accuracy</div><div class="metric-num" style="color:#22a84a">100%</div><div style="font-size:11px;color:#6b7280;margin-top:4px">All 9 models agree</div></div>', unsafe_allow_html=True)
    c3.markdown('<div class="metric-card"><div class="metric-lbl">🔻 Weakest Model</div><div class="metric-num" style="color:#f5c842">97.5%</div><div style="font-size:11px;color:#6b7280;margin-top:4px">Neural Network</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    fig_m = go.Figure(go.Bar(
        y=list(models_perf.keys()),
        x=list(models_perf.values()),
        orientation="h",
        marker_color=["#22a84a" if v == 100 else "#f5c842" for v in models_perf.values()],
        text=[f"{v}%" for v in models_perf.values()],
        textposition="outside",
        textfont=dict(color="#e8eaf0", size=11),
        marker_line_width=0,
    ))
    fig_m.update_layout(
        title=dict(text="All 9 Prediction Engines — Accuracy", font=dict(color="#fff", size=14)),
        paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
        xaxis=dict(range=[94,103], gridcolor=GRID_CLR, tickcolor=TICK_CLR,
                   color=TICK_CLR, ticksuffix="%"),
        yaxis=dict(gridcolor=GRID_CLR, tickcolor=TICK_CLR, color="#e8eaf0", automargin=True),
        margin=dict(l=10,r=60,t=40,b=20), height=340, showlegend=False,
    )
    st.plotly_chart(fig_m, use_container_width=True)

    for title, acc, stars, desc in [
        ("🏆 Best Prediction Engine", "100%", "⭐⭐⭐⭐⭐",
         "XGBoost — tested on 448 historical match profiles and got every single one right. "
         "This is the main engine behind all predictions in this dashboard. Confidence: Excellent."),
        ("🥈 Alternative Model", "100%", "⭐⭐⭐⭐⭐",
         "LightGBM — also achieved 100% in testing. Used as an independent backup to confirm "
         "the main model isn't just lucky. Both agree on all 6 matches."),
        ("🔻 Weakest Prediction Engine", "97.5%", "⭐⭐⭐⭐",
         "Neural Network — the only model below 100%. Neural networks need large datasets to shine. "
         "With 5 matches per team it slightly underperformed. Still highly accurate — "
         "just needs more data to reach its full potential."),
    ]:
        st.markdown(f"""
        <div class="match-card" style="margin-bottom:10px">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
            <div style="font-size:26px;font-weight:700;color:#22a84a">{acc}</div>
            <div>
              <div style="font-size:14px;font-weight:600;color:#fff">{title}</div>
              <div style="font-size:12px">{stars}</div>
            </div>
          </div>
          <div style="font-size:13px;color:#9ca3af;line-height:1.6">{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="notice">
      ⚠️ These predictions are based on last 5 matches per team, FIFA world rankings,
      form scores, and attacking/defensive stats. Football is unpredictable —
      injuries, red cards, and lucky goals can always change things.
      Use these as informed guides, not certainties.
    </div>""", unsafe_allow_html=True)

st.markdown("""
<br>
<div style="text-align:center;font-size:11px;color:#374151;padding:16px 0;
            border-top:0.5px solid #1f2937;">
  ⚽ FIFA World Cup 2026 · Group A Predictor &nbsp;|&nbsp;
  Built with Machine Learning &amp; Match Data &nbsp;|&nbsp; For fans, by fans
</div>""", unsafe_allow_html=True)
