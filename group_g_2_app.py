import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="⚽ Group G Predictions | FIFA World Cup 2026",
    page_icon="⚽", layout="wide", initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html,body,[class*="css"]{font-family:'Inter',sans-serif;}
  .stApp{background:#0a0f1a;color:#e8eaf0;}
  .block-container{padding:1.5rem 2rem !important;max-width:1200px;}
  h1,h2,h3{color:#ffffff !important;}
  .hero-box{background:linear-gradient(135deg,#1a0a3d 0%,#0d1e35 100%);
    border-radius:16px;padding:28px 32px;border:0.5px solid #2f1f50;margin-bottom:24px;}
  .hero-eyebrow{font-size:11px;letter-spacing:.1em;color:#b07ef5;text-transform:uppercase;margin-bottom:4px;}
  .hero-title{font-size:32px;font-weight:700;color:#fff;margin-bottom:6px;}
  .hero-sub{font-size:14px;color:#c0aad8;}
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
  .chip-grey{background:#1f2937;color:#9ca3af;} .chip-purple{background:#1a0d35;color:#c080f0;}
  .chip-orange{background:#2a1500;color:#fb923c;}
  .stTabs [data-baseweb="tab-list"]{background:#111827;border-radius:10px;padding:4px;gap:2px;}
  .stTabs [data-baseweb="tab"]{background:transparent;color:#9ca3af;border-radius:8px;
    font-size:13px;padding:8px 18px;border:none;}
  .stTabs [aria-selected="true"]{background:#1f2937 !important;color:#a855f7 !important;font-weight:600;}
  .prog-wrap{margin-bottom:10px;}
  .prog-lbl{display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px;}
  .prog-bg{height:7px;border-radius:4px;background:#1f2937;overflow:hidden;}
  .prog-fill{height:100%;border-radius:4px;}
  .notice{font-size:12px;color:#6b7280;background:#111827;border-radius:10px;
    padding:10px 14px;margin-top:16px;line-height:1.7;border:0.5px solid #1f2937;}
  .section-lbl{font-size:11px;color:#6b7280;text-transform:uppercase;
    letter-spacing:.08em;margin:20px 0 10px;}
  .elo-badge{display:inline-block;font-size:11px;padding:2px 8px;border-radius:8px;
    font-weight:600;margin-left:6px;}
  .elo-pos{background:#0d2e14;color:#5de881;} .elo-neg{background:#2e0d0d;color:#f56060;}
  .weight-row{display:flex;align-items:center;gap:10px;padding:6px 0;
    border-bottom:0.5px solid #1f2937;font-size:12px;}
  .weight-row:last-child{border-bottom:none;}
  .weight-stars{color:#f5c842;font-size:13px;min-width:90px;}
  .weight-name{color:#fff;font-weight:500;min-width:160px;}
  .weight-desc{color:#6b7280;font-size:11px;}
</style>
""", unsafe_allow_html=True)

def hex_to_rgba(hex_color, alpha=0.12):
    h=hex_color.lstrip("#"); r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"

# ── Data ── (results from weighted ML pipeline)
teams = {
    "Belgium":     {"flag":"🇧🇪","rank":3,  "conf":"UEFA",     "pts":9,"w":3,"d":0,"l":0,"color":"#a855f7","qualify":96,"elo":364,"form":75},
    "Iran":        {"flag":"🇮🇷","rank":20, "conf":"AFC",      "pts":6,"w":2,"d":0,"l":1,"color":"#22a84a","qualify":74,"elo":120,"form":75},
    "New Zealand": {"flag":"🇳🇿","rank":104,"conf":"OFC",      "pts":3,"w":1,"d":0,"l":2,"color":"#4a7fc1","qualify":18,"elo":62,"form":38},
    "Egypt":       {"flag":"🇪🇬","rank":37, "conf":"CAF",      "pts":0,"w":0,"d":0,"l":3,"color":"#e0903a","qualify":3, "elo":-44,"form":49},
}
matches = [
    {"md":1,"date":"Jun 15","home":"Belgium","away":"Egypt",      "hw":99.9,"d":0.0,"aw":0.1,"score":"3–1","conf":"Very High","stadium":"Lumen Field, Seattle",        "h_elo":364,"a_elo":-44,"h_form":75,"a_form":49},
    {"md":1,"date":"Jun 15","home":"Iran",   "away":"New Zealand","hw":99.8,"d":0.1,"aw":0.1,"score":"2–1","conf":"Very High","stadium":"SoFi Stadium, Inglewood",     "h_elo":120,"a_elo":62, "h_form":75,"a_form":38},
    {"md":2,"date":"Jun 19","home":"Belgium","away":"Iran",        "hw":99.3,"d":0.3,"aw":0.5,"score":"3–2","conf":"Very High","stadium":"AT&T Stadium, Arlington",    "h_elo":364,"a_elo":120,"h_form":75,"a_form":75},
    {"md":2,"date":"Jun 19","home":"Egypt",  "away":"New Zealand","hw":0.4, "d":0.1,"aw":99.6,"score":"1–0","conf":"Very High","stadium":"Levi's Stadium, Santa Clara","h_elo":-44,"a_elo":62, "h_form":49,"a_form":38},
    {"md":3,"date":"Jun 23","home":"Belgium","away":"New Zealand","hw":99.9,"d":0.1,"aw":0.1,"score":"3–1","conf":"Very High","stadium":"Gillette Stadium, Boston",    "h_elo":364,"a_elo":62, "h_form":75,"a_form":38},
    {"md":3,"date":"Jun 23","home":"Egypt",  "away":"Iran",       "hw":0.1, "d":0.1,"aw":99.9,"score":"1–2","conf":"Very High","stadium":"Hard Rock Stadium, Miami",  "h_elo":-44,"a_elo":120,"h_form":49,"a_form":75},
]
strength = {
    "Belgium":     {"Attack":95,"Defence":85,"Form":75,"Elo Rating":98,"Goal Diff":92},
    "Iran":        {"Attack":72,"Defence":75,"Form":75,"Elo Rating":65,"Goal Diff":72},
    "New Zealand": {"Attack":42,"Defence":48,"Form":38,"Elo Rating":40,"Goal Diff":30},
    "Egypt":       {"Attack":60,"Defence":68,"Form":49,"Elo Rating":35,"Goal Diff":55},
}
sim_data = {
    "Belgium":     {"1st":90,"2nd":6, "3rd":0,"elim":4},
    "Iran":        {"1st":8, "2nd":62,"3rd":18,"elim":12},
    "New Zealand": {"1st":1, "2nd":28,"3rd":25,"elim":46},
    "Egypt":       {"1st":1, "2nd":4, "3rd":2, "elim":93},
}
models_perf = {
    "Best Model (XGBoost)":       100.0,
    "Alternative (LightGBM)":     100.0,
    "Smart Trees (ExtraTrees)":   100.0,
    "Forest Model (Rand Forest)": 100.0,
    "Pattern Match (SVM)":        100.0,
    "Neural Network (MLP)":       100.0,
}
weight_table = [
    ("⭐⭐⭐⭐⭐","Elo Difference",       "Belgium +364 vs Egypt -44 — the biggest gap in the group"),
    ("⭐⭐⭐⭐⭐","Recent Form Score",    "Belgium 75, Iran 75 (tied) — why MD2 is the key match"),
    ("⭐⭐⭐⭐", "Goal Difference",      "Belgium avg +3.4 per match — exceptional finishing"),
    ("⭐⭐⭐⭐", "Competitive Match Flag","Belgium 1 competitive flag — their UEFA Nations League result counted"),
    ("⭐⭐⭐",  "Days Rest",            "Iran only 6 days between all matches — fatigue factor"),
    ("⭐⭐⭐⭐", "FIFA Ranking Diff",    "Belgium #3 vs Egypt #37 — 34-place gap drives the model hard"),
    ("⭐⭐⭐⭐", "Avg Goals Scored L5",  "Belgium 4.0/game, Iran 2.2/game — both strong attackers"),
    ("⭐⭐⭐⭐", "Avg Goals Conceded L5","NZ 2.0 conceded/game — explains 3 consecutive losses"),
]

CHART_BG="rgba(0,0,0,0)"; GRID_CLR="rgba(255,255,255,0.06)"; TICK_CLR="#6b7280"

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
  <div class="hero-eyebrow">FIFA World Cup 2026 · Group Stage · Weighted ML Predictions</div>
  <div class="hero-title">⚽ Group G Predictions</div>
  <div class="hero-sub">Belgium · Iran · New Zealand · Egypt &nbsp;|&nbsp; 6 Matches · 3 Matchdays &nbsp;|&nbsp; Elo + Form weighted model</div>
</div>""", unsafe_allow_html=True)

c1,c2,c3,c4=st.columns(4)
for col,(label,val,color) in zip([c1,c2,c3,c4],[
    ("🏆 Predicted Winner","Belgium","#a855f7"),
    ("✅ All 6 Models","100%","#22a84a"),
    ("⚡ Elo — Top Feature","+364","#f5c842"),
    ("📊 Key Shift vs v1","NZ 3rd","#60aef5")]):
    col.markdown(f'<div class="metric-card"><div class="metric-lbl">{label}</div>'
                 f'<div class="metric-num" style="color:{color}">{val}</div></div>',unsafe_allow_html=True)

st.markdown("<br>",unsafe_allow_html=True)
tabs=st.tabs(["🏅 Standings","⚽ All 6 Matches","💪 Team Strength","🎯 Who Qualifies?","🤖 Prediction Quality"])

# ══════ TAB 1 ══════
with tabs[0]:
    st.markdown('<div class="section-lbl">Predicted Final Standings — Weighted Model</div>',unsafe_allow_html=True)
    pos_styles=["pos-1","pos-2","pos-3","pos-4"]
    pos_labels=["🥇 Group Winners","🥈 2nd Place","🥉 Best 3rd?","❌ Eliminated"]
    bar_colors=["#a855f7","#22a84a","#4a7fc1","#f56060"]

    for i,(team,d) in enumerate(teams.items()):
        elo_class="elo-pos" if d["elo"]>=0 else "elo-neg"
        elo_sign="+" if d["elo"]>=0 else ""
        st.markdown(f"""
        <div class="stand-card"><div class="stand-row" style="flex-wrap:wrap;gap:12px;">
          <div class="pos-badge {pos_styles[i]}">{i+1}</div>
          <div style="font-size:26px">{d['flag']}</div>
          <div style="flex:1;min-width:140px">
            <div style="font-size:15px;font-weight:600;color:#fff">{team}
              <span class="elo-badge {elo_class}">Elo {elo_sign}{d['elo']}</span>
            </div>
            <div style="font-size:11px;color:#6b7280">{d['conf']} · Rank #{d['rank']} · Form {d['form']}/100</div>
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
        fig_elo=go.Figure(go.Bar(
            x=list(teams.keys()),y=[d["elo"] for d in teams.values()],
            marker_color=["#22a84a" if d["elo"]>=0 else "#f56060" for d in teams.values()],
            marker_line_width=0,text=[f"{'+' if d['elo']>=0 else ''}{d['elo']}" for d in teams.values()],
            textposition="outside",textfont=dict(color="#e8eaf0",size=12)))
        fig_elo.update_layout(title=dict(text="Elo Difference (⭐⭐⭐⭐⭐ Top Feature)",font=dict(color="#fff",size=14)),
            paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,showlegend=False,height=280,
            yaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR),
            xaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR),margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig_elo,use_container_width=True)

    st.markdown("""<div class="notice">
    🔄 <strong>Key change from v1:</strong> In the previous model Egypt finished 3rd and New Zealand last.
    With weighted features, <strong>New Zealand's Elo (+62 average) is actually higher than Egypt's (-44)</strong>.
    When Elo gets 5x weight, this flips the 3rd/4th positions. Iran's consistent form score (75/100)
    also confirmed their 2nd place over the original draw prediction.</div>""",unsafe_allow_html=True)

# ══════ TAB 2 ══════
with tabs[1]:
    prev_md=None
    md_labels={1:"Matchday 1 — June 15",2:"Matchday 2 — June 19",3:"Matchday 3 — June 23"}
    for m in matches:
        if m["md"]!=prev_md:
            prev_md=m["md"]; st.markdown(f'<div class="section-lbl">{md_labels[m["md"]]}</div>',unsafe_allow_html=True)
        ht,at=m["home"],m["away"]
        hf,af=teams[ht]["flag"],teams[at]["flag"]
        hw,d,aw=m["hw"],m["d"],m["aw"]; c_h,c_a=teams[ht]["color"],teams[at]["color"]
        if hw>=d and hw>=aw: winner=ht; wtype="Home Win"
        elif aw>=hw and aw>=d: winner=at; wtype="Away Win"
        else: winner="Draw"; wtype="Draw"
        win_chip=(f'<span class="chip chip-green">✅ {winner} Win predicted</span>'
                  if wtype!="Draw" else '<span class="chip chip-gold">🤝 Draw predicted</span>')
        h_elo_s=f"+{m['h_elo']}" if m['h_elo']>=0 else str(m['h_elo'])
        a_elo_s=f"+{m['a_elo']}" if m['a_elo']>=0 else str(m['a_elo'])
        h_ec="elo-pos" if m['h_elo']>=0 else "elo-neg"
        a_ec="elo-pos" if m['a_elo']>=0 else "elo-neg"
        st.markdown(f"""
        <div class="match-card">
          <div style="font-size:11px;color:#6b7280;margin-bottom:12px">📅 {m['date']} &nbsp;|&nbsp; 🏟️ {m['stadium']}</div>
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:16px;">
            <div style="text-align:center;min-width:110px">
              <div style="font-size:32px">{hf}</div>
              <div style="font-size:13px;font-weight:600;color:#fff;margin-top:4px">{ht}</div>
              <span class="elo-badge {h_ec}">Elo {h_elo_s}</span>
              <div style="font-size:11px;color:#6b7280;margin-top:2px">Form {m['h_form']}/100</div>
            </div>
            <div style="text-align:center">
              <div style="font-size:22px;font-weight:700;color:#f5c842;letter-spacing:2px">{m['score']}</div>
              <div style="font-size:10px;color:#6b7280;margin-top:2px">likely score</div>
            </div>
            <div style="text-align:center;min-width:110px">
              <div style="font-size:32px">{af}</div>
              <div style="font-size:13px;font-weight:600;color:#fff;margin-top:4px">{at}</div>
              <span class="elo-badge {a_ec}">Elo {a_elo_s}</span>
              <div style="font-size:11px;color:#6b7280;margin-top:2px">Form {m['a_form']}/100</div>
            </div>
          </div>
          <div style="display:flex;gap:8px;margin-bottom:10px;text-align:center;">
            <div style="flex:1;background:#1a0d2e;border:0.5px solid #3a1a60;border-radius:8px;padding:10px 6px;">
              <div style="font-size:20px;font-weight:700;color:#c080f0">{hw}%</div>
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
          {win_chip} <span class="chip chip-gold">Confidence: {m['conf']}</span>
        </div>""",unsafe_allow_html=True)

# ══════ TAB 3 ══════
with tabs[2]:
    cats=["Attack","Defence","Form","Elo Rating","Goal Diff"]
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

    st.markdown('<div class="section-lbl">Elo vs Form — The two top-weighted features</div>',unsafe_allow_html=True)
    fig_scatter=go.Figure()
    for team,d in teams.items():
        fig_scatter.add_trace(go.Scatter(x=[d["elo"]],y=[d["form"]],mode="markers+text",
            marker=dict(size=24,color=d["color"]),text=[f"{d['flag']} {team}"],
            textposition="top center",textfont=dict(color="#e8eaf0",size=11),name=team))
    fig_scatter.add_vline(x=0,line_dash="dash",line_color="rgba(255,255,255,0.2)")
    fig_scatter.update_layout(paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,showlegend=False,height=320,
        xaxis=dict(title="Elo Difference (⭐⭐⭐⭐⭐)",gridcolor=GRID_CLR,color=TICK_CLR,zeroline=False),
        yaxis=dict(title="Recent Form Score (⭐⭐⭐⭐⭐)",gridcolor=GRID_CLR,color=TICK_CLR),
        margin=dict(l=20,r=20,t=20,b=40))
    st.plotly_chart(fig_scatter,use_container_width=True)

    for team,d in strength.items():
        td=teams[team]
        with st.expander(f"{td['flag']}  {team}  ·  Rank #{td['rank']}  ·  Elo {'+' if td['elo']>=0 else ''}{td['elo']}  ·  Form {td['form']}/100",expanded=(team=="Belgium")):
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
        qual_color="#a855f7" if qual_total>70 else("#f5c842" if qual_total>20 else "#f56060")
        chip_html=(f'<span class="chip chip-purple">✅ Advances</span>' if qual_total>70 else
                   f'<span class="chip chip-gold">🎯 Possible</span>' if qual_total>20 else
                   f'<span class="chip chip-red">❌ Unlikely</span>')
        with col:
            st.markdown(f"""
            <div class="match-card" style="margin-bottom:12px">
              <div style="font-size:28px;margin-bottom:4px">{td['flag']}</div>
              <div style="font-size:16px;font-weight:600;color:#fff;margin-bottom:4px">{team}</div>
              <div style="font-size:11px;color:#6b7280;margin-bottom:12px">
                Elo: {'+' if td['elo']>=0 else ''}{td['elo']} · Form: {td['form']}/100 · Rank #{td['rank']}</div>
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

    st.markdown('<div class="section-lbl">Key storylines — Weighted model insights</div>',unsafe_allow_html=True)
    st.markdown("""<div class="match-card">
      <div style="font-size:14px;font-weight:600;color:#f5c842;margin-bottom:10px">⚠️ What changed and why</div>
      <div style="font-size:13px;color:#9ca3af;line-height:1.9">
        🔄 <strong style="color:#fff">Egypt dropped to 4th (was 3rd in v1)</strong> — Their average Elo Difference is -44.
        When Elo carries 5x weight, a negative Elo team cannot finish above a positive one.
        Egypt's recent form (49/100) is also the weakest in the group.<br>
        🇳🇿 <strong style="color:#fff">New Zealand rises to 3rd</strong> — Despite being ranked #104,
        their Elo Difference avg (+62) is actually above Egypt's. They beat a stronger schedule.
        One win predicted in MD2 vs Egypt.<br>
        🇮🇷 <strong style="color:#fff">Iran solidly 2nd</strong> — Form score 75/100 (identical to Belgium!),
        positive Elo, and a consistent record. The weighted model is much more confident about Iran than v1.
      </div></div>""",unsafe_allow_html=True)

# ══════ TAB 5 ══════
with tabs[4]:
    c1,c2,c3=st.columns(3)
    c1.markdown('<div class="metric-card"><div class="metric-lbl">🏆 Best Model Accuracy</div><div class="metric-num" style="color:#a855f7">100%</div><div style="font-size:11px;color:#6b7280;margin-top:4px">⭐⭐⭐⭐⭐ All 6 perfect</div></div>',unsafe_allow_html=True)
    c2.markdown('<div class="metric-card"><div class="metric-lbl">⚡ #1 Feature</div><div class="metric-num" style="color:#f5c842">Elo</div><div style="font-size:11px;color:#6b7280;margin-top:4px">5× weight in model</div></div>',unsafe_allow_html=True)
    c3.markdown('<div class="metric-card"><div class="metric-lbl">🔄 Results Changed</div><div class="metric-num" style="color:#60aef5">2</div><div style="font-size:11px;color:#6b7280;margin-top:4px">MD2 Egy/NZ + MD3 Egy/Iran</div></div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown('<div class="section-lbl">Feature Weight Ranking — how the model prioritises each signal</div>',unsafe_allow_html=True)
    for stars,name,desc in weight_table:
        st.markdown(f"""<div class="weight-row">
          <span class="weight-stars">{stars}</span>
          <span class="weight-name">{name}</span>
          <span class="weight-desc">{desc}</span>
        </div>""",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    fig_m=go.Figure(go.Bar(y=list(models_perf.keys()),x=list(models_perf.values()),orientation="h",
        marker_color=["#a855f7"]*len(models_perf),
        text=[f"{v}%" for v in models_perf.values()],textposition="outside",
        textfont=dict(color="#e8eaf0",size=11),marker_line_width=0))
    fig_m.update_layout(title=dict(text="All 6 Prediction Engines — 100% Accuracy",font=dict(color="#fff",size=14)),
        paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,
        xaxis=dict(range=[98,102],gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR,ticksuffix="%"),
        yaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color="#e8eaf0",automargin=True),
        margin=dict(l=10,r=60,t=40,b=20),height=280,showlegend=False)
    st.plotly_chart(fig_m,use_container_width=True)
    st.markdown("""<div class="notice">⚠️ This is the <strong>v2 weighted model</strong>. Features are weighted by predictive importance:
    Elo Difference and Recent Form Score carry 5× weight each, Goal Difference and Competitive Match Flag 4×,
    Days Rest and Venue 3×. Lower-weight features (shots, possession, cards) are still included but carry 1–2× weight.
    Two results changed vs v1: Egypt vs New Zealand and Egypt vs Iran in MD3.</div>""",unsafe_allow_html=True)

st.markdown("""<br>
<div style="text-align:center;font-size:11px;color:#374151;padding:16px 0;border-top:0.5px solid #1f2937;">
  ⚽ FIFA World Cup 2026 · Group G Predictor v2 (Weighted) &nbsp;|&nbsp; Machine Learning &amp; Match Data &nbsp;|&nbsp; For fans, by fans
</div>""",unsafe_allow_html=True)
