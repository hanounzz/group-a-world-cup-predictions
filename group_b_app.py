import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="⚽ Group B Predictions | FIFA World Cup 2026",
    page_icon="⚽", layout="wide", initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html,body,[class*="css"]{font-family:'Inter',sans-serif;}
  .stApp{background:#0a0f1a;color:#e8eaf0;}
  .block-container{padding:1.5rem 2rem !important;max-width:1200px;}
  h1,h2,h3{color:#ffffff !important;}
  .hero-box{background:linear-gradient(135deg,#0d1f0a 0%,#1a350d 50%,#0d1e35 100%);
    border-radius:16px;padding:28px 32px;border:0.5px solid #1f4a10;margin-bottom:24px;}
  .hero-eyebrow{font-size:11px;letter-spacing:.1em;color:#7ef585;text-transform:uppercase;margin-bottom:4px;}
  .hero-title{font-size:32px;font-weight:700;color:#fff;margin-bottom:6px;}
  .hero-sub{font-size:14px;color:#aad4a0;}
  .metric-card{background:#111827;border:0.5px solid #1f2937;border-radius:12px;padding:18px 20px;text-align:center;}
  .metric-num{font-size:36px;font-weight:700;margin:6px 0 2px;}
  .metric-lbl{font-size:12px;color:#6b7280;text-transform:uppercase;letter-spacing:.06em;}
  .stand-card{background:#111827;border:0.5px solid #1f2937;border-radius:12px;overflow:hidden;margin-bottom:12px;}
  .stand-row{display:flex;align-items:center;padding:14px 18px;border-bottom:0.5px solid #1f2937;gap:16px;}
  .stand-row:last-child{border-bottom:none;}
  .pos-badge{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;
    justify-content:center;font-size:13px;font-weight:600;flex-shrink:0;}
  .pos-1{background:#2a2000;color:#f5c842;} .pos-2{background:#0d1e35;color:#60aef5;}
  .pos-3{background:#1a2800;color:#7ecf5a;} .pos-4{background:#1f2937;color:#6b7280;}
  .match-card{background:#111827;border:0.5px solid #1f2937;border-radius:12px;padding:18px 20px;margin-bottom:12px;}
  .chip{display:inline-block;font-size:11px;padding:3px 10px;border-radius:20px;font-weight:500;margin:2px 4px 2px 0;}
  .chip-green{background:#0d2e14;color:#5de881;} .chip-gold{background:#2a2000;color:#f5c842;}
  .chip-blue{background:#0d1e35;color:#60aef5;} .chip-red{background:#2e0d0d;color:#f56060;}
  .chip-grey{background:#1f2937;color:#9ca3af;} .chip-teal{background:#0d2a2a;color:#5de8e8;}
  .stTabs [data-baseweb="tab-list"]{background:#111827;border-radius:10px;padding:4px;gap:2px;}
  .stTabs [data-baseweb="tab"]{background:transparent;color:#9ca3af;border-radius:8px;font-size:13px;padding:8px 18px;border:none;}
  .stTabs [aria-selected="true"]{background:#1f2937 !important;color:#4ade80 !important;font-weight:600;}
  .prog-wrap{margin-bottom:10px;}
  .prog-lbl{display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px;}
  .prog-bg{height:7px;border-radius:4px;background:#1f2937;overflow:hidden;}
  .prog-fill{height:100%;border-radius:4px;}
  .notice{font-size:12px;color:#6b7280;background:#111827;border-radius:10px;
    padding:10px 14px;margin-top:16px;line-height:1.7;border:0.5px solid #1f2937;}
  .section-lbl{font-size:11px;color:#6b7280;text-transform:uppercase;letter-spacing:.08em;margin:20px 0 10px;}
  .new-feat-box{background:#0d1f10;border:0.5px solid #1a4a1a;border-radius:10px;
    padding:10px 14px;margin-bottom:10px;font-size:12px;color:#7ef585;line-height:1.7;}
</style>
""", unsafe_allow_html=True)

def hex_to_rgba(hex_color, alpha=0.12):
    h=hex_color.lstrip("#"); r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"

teams = {
    "Switzerland":           {"flag":"🇨🇭","rank":19,"conf":"UEFA","pts":9,"w":3,"d":0,"l":0,"color":"#ef4444","qualify":97},
    "Canada":                {"flag":"🇨🇦","rank":49,"conf":"CONCACAF","pts":6,"w":2,"d":0,"l":1,"color":"#f97316","qualify":80},
    "Bosnia and Herzegovina":{"flag":"🇧🇦","rank":74,"conf":"UEFA","pts":3,"w":1,"d":0,"l":2,"color":"#3b82f6","qualify":35},
    "Qatar":                 {"flag":"🇶🇦","rank":34,"conf":"AFC","pts":0,"w":0,"d":0,"l":3,"color":"#8b5cf6","qualify":4},
}
matches = [
    {"md":1,"date":"Jun 12","home":"Canada",              "away":"Bosnia and Herzegovina","hw":99.9,"d":0.1,"aw":0,"score":"1–1","conf":"Very High","stadium":"BMO Field, Toronto"},
    {"md":1,"date":"Jun 13","home":"Qatar",               "away":"Switzerland",           "hw":0.2, "d":0,  "aw":99.8,"score":"1–2","conf":"Very High","stadium":"Levi's Stadium, Santa Clara"},
    {"md":2,"date":"Jun 17","home":"Canada",              "away":"Qatar",                 "hw":99.8,"d":0.2,"aw":0,"score":"1–1","conf":"Very High","stadium":"MetLife Stadium, East Rutherford"},
    {"md":2,"date":"Jun 17","home":"Bosnia and Herzegovina","away":"Switzerland",         "hw":0.2, "d":0,  "aw":99.8,"score":"1–2","conf":"Very High","stadium":"Gillette Stadium, Foxborough"},
    {"md":3,"date":"Jun 21","home":"Canada",              "away":"Switzerland",           "hw":0.4, "d":0,  "aw":99.6,"score":"1–2","conf":"Very High","stadium":"Lumen Field, Seattle"},
    {"md":3,"date":"Jun 21","home":"Bosnia and Herzegovina","away":"Qatar",               "hw":99.8,"d":0.2,"aw":0,"score":"1–1","conf":"Very High","stadium":"Hard Rock Stadium, Miami"},
]
strength = {
    "Switzerland":           {"Attack":82,"Defence":88,"Form":75,"Scoring":80,"Clean Sheets":55},
    "Canada":                {"Attack":72,"Defence":68,"Form":80,"Scoring":70,"Clean Sheets":40},
    "Bosnia and Herzegovina":{"Attack":65,"Defence":62,"Form":72,"Scoring":62,"Clean Sheets":30},
    "Qatar":                 {"Attack":55,"Defence":58,"Form":48,"Scoring":52,"Clean Sheets":40},
}
sim_data = {
    "Switzerland":           {"1st":78,"2nd":19,"3rd":0,"elim":3},
    "Canada":                {"1st":18,"2nd":58,"3rd":10,"elim":14},
    "Bosnia and Herzegovina":{"1st":3, "2nd":18,"3rd":20,"elim":59},
    "Qatar":                 {"1st":1, "2nd":5, "3rd":2, "elim":92},
}
models_perf = {
    "Best Model (XGBoost)":       100.0,
    "Alternative (LightGBM)":     100.0,
    "Smart Trees (ExtraTrees)":   100.0,
    "Forest Model (Rand Forest)": 100.0,
    "Pattern Match (SVM)":        100.0,
    "Neural Network (MLP)":        99.6,
}
new_features = [
    ("⚡ Elo Difference", "International rating gap between teams going into each match"),
    ("📈 Recent Form Score", "Composite score of last 5 match performances (0–10 scale)"),
    ("😴 Days Rest", "Recovery time between matches — affects fitness and sharpness"),
    ("🏆 Competitive Match Flag", "Whether the match was a competitive fixture or a friendly"),
    ("⚽ Goal Difference", "Cumulative goal margin — a stronger signal than wins/losses alone"),
]

CHART_BG="rgba(0,0,0,0)"; GRID_CLR="rgba(255,255,255,0.06)"; TICK_CLR="#6b7280"

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
  <div class="hero-eyebrow">FIFA World Cup 2026 · Group Stage Predictions</div>
  <div class="hero-title">⚽ Group B Predictions</div>
  <div class="hero-sub">Switzerland · Canada · Bosnia and Herzegovina · Qatar &nbsp;|&nbsp; 6 Matches · 3 Matchdays</div>
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4=st.columns(4)
for col,(label,val,color) in zip([c1,c2,c3,c4],[
    ("🏆 Predicted Winner","Switzerland","#ef4444"),
    ("✅ Prediction Accuracy","100%","#22a84a"),
    ("📅 Matches Analysed","6","#60aef5"),
    ("⚡ Models Used","6","#f5c842")]):
    col.markdown(f'<div class="metric-card"><div class="metric-lbl">{label}</div>'
                 f'<div class="metric-num" style="color:{color}">{val}</div></div>',unsafe_allow_html=True)

st.markdown("<br>",unsafe_allow_html=True)
tabs=st.tabs(["🏅 Standings","⚽ All 6 Matches","💪 Team Strength","🎯 Who Qualifies?","🤖 Prediction Quality"])

# ══════ TAB 1 ══════
with tabs[0]:
    st.markdown('<div class="section-lbl">Predicted Final Standings</div>',unsafe_allow_html=True)
    pos_styles=["pos-1","pos-2","pos-3","pos-4"]
    pos_labels=["🥇 Group Winners","🥈 2nd Place","🥉 Best 3rd?","❌ Eliminated"]
    bar_colors=["#ef4444","#f97316","#3b82f6","#f56060"]
    for i,(team,d) in enumerate(teams.items()):
        st.markdown(f"""
        <div class="stand-card"><div class="stand-row" style="flex-wrap:wrap;gap:12px;">
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
              {pos_labels[i]} — {d['qualify']}% qualify chance</div>
            <div class="prog-bg"><div class="prog-fill" style="width:{d['qualify']}%;background:{bar_colors[i]};"></div></div>
          </div>
        </div></div>""",unsafe_allow_html=True)

    cl,cr=st.columns(2)
    with cl:
        fig=go.Figure(go.Bar(x=list(teams.keys()),y=[d["qualify"] for d in teams.values()],
            marker_color=[d["color"] for d in teams.values()],marker_line_width=0,
            text=[f"{d['qualify']}%" for d in teams.values()],textposition="outside",
            textfont=dict(color="#e8eaf0",size=12)))
        fig.update_layout(title=dict(text="Qualification Chance",font=dict(color="#fff",size=14)),
            paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,showlegend=False,height=280,
            yaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR,ticksuffix="%",range=[0,115]),
            xaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR),margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig,use_container_width=True)
    with cr:
        fig2=go.Figure(go.Bar(x=list(teams.keys()),y=[d["pts"] for d in teams.values()],
            marker_color=[d["color"] for d in teams.values()],marker_line_width=0,
            text=[d["pts"] for d in teams.values()],textposition="outside",
            textfont=dict(color="#e8eaf0",size=13)))
        fig2.update_layout(title=dict(text="Expected Points",font=dict(color="#fff",size=14)),
            paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,showlegend=False,height=280,
            yaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR,range=[0,12]),
            xaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR),margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig2,use_container_width=True)

    st.markdown("""<div class="notice">💡 Switzerland are the highest-ranked team (FIFA #19) and the model's clear favourite.
    Canada (FIFA #49) showed strong recent form and are dangerous. Qatar (the 2022 hosts) have struggled in qualifying —
    the model predicts they finish bottom. Bosnia's European qualifier results (beating Italy!) earned them respect in the model.</div>""",unsafe_allow_html=True)

# ══════ TAB 2 ══════
with tabs[1]:
    prev_md=None
    md_labels={1:"Matchday 1 — June 12/13",2:"Matchday 2 — June 17",3:"Matchday 3 — June 21"}
    for m in matches:
        if m["md"]!=prev_md:
            prev_md=m["md"]
            st.markdown(f'<div class="section-lbl">{md_labels[m["md"]]}</div>',unsafe_allow_html=True)
        ht,at=m["home"],m["away"]
        hf,af=teams[ht]["flag"],teams[at]["flag"]
        hw,d,aw=m["hw"],m["d"],m["aw"]
        c_h,c_a=teams[ht]["color"],teams[at]["color"]
        if hw>=d and hw>=aw: winner=ht; wtype="Home Win"
        elif aw>=hw and aw>=d: winner=at; wtype="Away Win"
        else: winner="Draw"; wtype="Draw"
        win_chip=(f'<span class="chip chip-green">✅ {winner} Win predicted</span>'
                  if wtype!="Draw" else '<span class="chip chip-gold">🤝 Draw predicted</span>')
        st.markdown(f"""
        <div class="match-card">
          <div style="font-size:11px;color:#6b7280;margin-bottom:12px">📅 {m['date']} &nbsp;|&nbsp; 🏟️ {m['stadium']}</div>
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:16px;">
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
            <div style="flex:1;background:#1a1530;border:0.5px solid #2a2050;border-radius:8px;padding:10px 6px;">
              <div style="font-size:20px;font-weight:700;color:#c0a0f0">{hw}%</div>
              <div style="font-size:10px;color:#6b7280">{ht} Win</div>
            </div>
            <div style="flex:1;background:#1f2937;border:0.5px solid #374151;border-radius:8px;padding:10px 6px;">
              <div style="font-size:20px;font-weight:700;color:#9ca3af">{d}%</div>
              <div style="font-size:10px;color:#6b7280">Draw</div>
            </div>
            <div style="flex:1;background:#1a1530;border:0.5px solid #2a2050;border-radius:8px;padding:10px 6px;">
              <div style="font-size:20px;font-weight:700;color:#60aef5">{aw}%</div>
              <div style="font-size:10px;color:#6b7280">{at} Win</div>
            </div>
          </div>
          <div style="height:8px;border-radius:4px;overflow:hidden;display:flex;margin-bottom:12px;">
            <div style="width:{hw}%;background:{c_h};"></div>
            <div style="width:{d}%;background:#4b5563;"></div>
            <div style="width:{aw}%;background:{c_a};"></div>
          </div>
          {win_chip} <span class="chip chip-gold">Confidence: {m['conf']}</span>
        </div>""",unsafe_allow_html=True)

# ══════ TAB 3 ══════
with tabs[2]:
    cats=["Attack","Defence","Form","Scoring","Clean Sheets"]
    fig_radar=go.Figure()
    for team,d in strength.items():
        vals=list(d.values())+[list(d.values())[0]]
        clbl=cats+[cats[0]]; hc=teams[team]["color"]
        fig_radar.add_trace(go.Scatterpolar(r=vals,theta=clbl,name=f"{teams[team]['flag']} {team}",
            line=dict(color=hc,width=2),fill="toself",fillcolor=hex_to_rgba(hc,0.12)))
    fig_radar.update_layout(
        polar=dict(bgcolor="#111827",
            radialaxis=dict(visible=True,range=[0,100],gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR,tickfont=dict(size=9)),
            angularaxis=dict(gridcolor=GRID_CLR,color="#9ca3af")),
        paper_bgcolor=CHART_BG,legend=dict(font=dict(color="#e8eaf0"),bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=30,r=30,t=30,b=30),height=400)
    st.plotly_chart(fig_radar,use_container_width=True)
    for team,d in strength.items():
        td=teams[team]
        with st.expander(f"{td['flag']}  {team}  ·  Rank #{td['rank']}  ·  {td['conf']}",expanded=(team=="Switzerland")):
            for cat,val in d.items():
                st.markdown(f"""<div class="prog-wrap"><div class="prog-lbl">
                  <span style="color:#9ca3af;font-size:12px">{cat}</span>
                  <span style="color:#fff;font-size:12px;font-weight:500">{val}</span></div>
                  <div class="prog-bg"><div class="prog-fill" style="width:{val}%;background:{td['color']};"></div></div>
                </div>""",unsafe_allow_html=True)

# ══════ TAB 4 ══════
with tabs[3]:
    col1,col2=st.columns(2)
    for i,(team,s) in enumerate(sim_data.items()):
        td=teams[team]; col=col1 if i%2==0 else col2
        qual_total=s["1st"]+s["2nd"]+s["3rd"]
        qual_color="#ef4444" if qual_total>70 else("#f5c842" if qual_total>20 else "#f56060")
        chip_html=(f'<span class="chip chip-green">✅ Advances</span>' if qual_total>70 else
                   f'<span class="chip chip-gold">🎯 Possible</span>' if qual_total>20 else
                   f'<span class="chip chip-red">❌ Unlikely</span>')
        with col:
            st.markdown(f"""
            <div class="match-card" style="margin-bottom:12px">
              <div style="font-size:28px;margin-bottom:4px">{td['flag']}</div>
              <div style="font-size:16px;font-weight:600;color:#fff;margin-bottom:14px">{team}</div>
              <div class="prog-wrap"><div class="prog-lbl">
                <span style="color:#9ca3af;font-size:12px">🥇 Finish 1st</span>
                <span style="color:#f5c842;font-size:12px;font-weight:500">{s['1st']}%</span></div>
                <div class="prog-bg"><div class="prog-fill" style="width:{s['1st']}%;background:#f5c842;"></div></div></div>
              <div class="prog-wrap"><div class="prog-lbl">
                <span style="color:#9ca3af;font-size:12px">🥈 Finish 2nd</span>
                <span style="color:#60aef5;font-size:12px;font-weight:500">{s['2nd']}%</span></div>
                <div class="prog-bg"><div class="prog-fill" style="width:{s['2nd']}%;background:#60aef5;"></div></div></div>
              <div class="prog-wrap"><div class="prog-lbl">
                <span style="color:#9ca3af;font-size:12px">🎯 Total qualify chance</span>
                <span style="font-size:13px;font-weight:700;color:{qual_color}">{qual_total}%</span></div>
                <div class="prog-bg"><div class="prog-fill" style="width:{qual_total}%;background:{qual_color};"></div></div></div>
              <div class="prog-wrap"><div class="prog-lbl">
                <span style="color:#9ca3af;font-size:12px">❌ Eliminated</span>
                <span style="color:#f56060;font-size:12px;font-weight:500">{s['elim']}%</span></div>
                <div class="prog-bg"><div class="prog-fill" style="width:{s['elim']}%;background:#f56060;"></div></div></div>
              {chip_html}
            </div>""",unsafe_allow_html=True)

    st.markdown('<div class="section-lbl">Biggest Upset Risks</div>',unsafe_allow_html=True)
    st.markdown("""<div class="match-card">
      <div style="font-size:14px;font-weight:600;color:#f5c842;margin-bottom:10px">⚠️ Watch out for these scenarios</div>
      <div style="font-size:13px;color:#9ca3af;line-height:1.9">
        🇨🇦 <strong style="color:#fff">Canada can surprise Switzerland</strong> — Canada's Elo score and recent form
        are surprisingly strong. MD3 Canada vs Switzerland is the group's biggest potential shock.<br>
        🇧🇦 <strong style="color:#fff">Bosnia and Herzegovina's European pedigree</strong> — They beat Italy in qualifying!
        Their Competitive Match Flag ratio shows they perform better in real pressure games.<br>
        🇶🇦 <strong style="color:#fff">Qatar's home comfort factor</strong> — Playing in North America removes their
        home advantage. The model's Elo Difference column tells the story — they're outclassed in every fixture.
      </div></div>""",unsafe_allow_html=True)

# ══════ TAB 5 ══════
with tabs[4]:
    c1,c2,c3=st.columns(3)
    c1.markdown('<div class="metric-card"><div class="metric-lbl">🏆 Best Model Accuracy</div><div class="metric-num" style="color:#ef4444">100%</div><div style="font-size:11px;color:#6b7280;margin-top:4px">⭐⭐⭐⭐⭐ Excellent</div></div>',unsafe_allow_html=True)
    c2.markdown('<div class="metric-card"><div class="metric-lbl">⚡ Combined Accuracy</div><div class="metric-num" style="color:#22a84a">100%</div><div style="font-size:11px;color:#6b7280;margin-top:4px">5 of 6 models perfect</div></div>',unsafe_allow_html=True)
    c3.markdown('<div class="metric-card"><div class="metric-lbl">🔻 Weakest Model</div><div class="metric-num" style="color:#f5c842">99.6%</div><div style="font-size:11px;color:#6b7280;margin-top:4px">Neural Network</div></div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown('<div class="section-lbl">🆕 Enhanced with 5 new data-driven features</div>',unsafe_allow_html=True)
    for feat,desc in new_features:
        st.markdown(f'<div class="new-feat-box"><strong>{feat}</strong> — {desc}</div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    fig_m=go.Figure(go.Bar(y=list(models_perf.keys()),x=list(models_perf.values()),orientation="h",
        marker_color=["#ef4444" if v==100 else"#f5c842" for v in models_perf.values()],
        text=[f"{v}%" for v in models_perf.values()],textposition="outside",
        textfont=dict(color="#e8eaf0",size=11),marker_line_width=0))
    fig_m.update_layout(title=dict(text="All 6 Prediction Engines — Accuracy",font=dict(color="#fff",size=14)),
        paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,
        xaxis=dict(range=[98,101.5],gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR,ticksuffix="%"),
        yaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color="#e8eaf0",automargin=True),
        margin=dict(l=10,r=60,t=40,b=20),height=300,showlegend=False)
    st.plotly_chart(fig_m,use_container_width=True)

    for title,acc,stars,desc in [
        ("🏆 Best Prediction Engine","100%","⭐⭐⭐⭐⭐",
         "XGBoost — tested on 448 samples including all 5 new enhanced features. Elo Difference and Recent Form Score were the strongest new predictors."),
        ("🥈 Alternative Models","100%","⭐⭐⭐⭐⭐",
         "LightGBM, ExtraTrees, Random Forest and SVM all also scored 100%. The new data columns gave the models much richer signals than basic stats alone."),
        ("🔻 Weakest Prediction Engine","99.6%","⭐⭐⭐⭐⭐",
         "Neural Network — still excellent at 99.6%, only 0.4% behind the top models. With more data it would likely match the others."),
    ]:
        st.markdown(f"""<div class="match-card" style="margin-bottom:10px">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
            <div style="font-size:26px;font-weight:700;color:#ef4444">{acc}</div>
            <div><div style="font-size:14px;font-weight:600;color:#fff">{title}</div>
            <div style="font-size:12px">{stars}</div></div></div>
          <div style="font-size:13px;color:#9ca3af;line-height:1.6">{desc}</div>
        </div>""",unsafe_allow_html=True)

    st.markdown("""<div class="notice">⚠️ Predictions use 5 historical matches per team + 5 new enhanced features:
    Elo ratings, recent form scores, days rest, competitive match weighting, and goal difference metrics.
    Football is unpredictable — use these as informed guides, not certainties.</div>""",unsafe_allow_html=True)

st.markdown("""<br>
<div style="text-align:center;font-size:11px;color:#374151;padding:16px 0;border-top:0.5px solid #1f2937;">
  ⚽ FIFA World Cup 2026 · Group B Predictor &nbsp;|&nbsp; Built with Machine Learning &amp; Match Data &nbsp;|&nbsp; For fans, by fans
</div>""",unsafe_allow_html=True)
