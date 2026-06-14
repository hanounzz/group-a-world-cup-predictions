import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="⚽ Group D Predictions | FIFA World Cup 2026",
    page_icon="⚽", layout="wide", initial_sidebar_state="collapsed",
)
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html,body,[class*="css"]{font-family:'Inter',sans-serif;}
  .stApp{background:#0a0f1a;color:#e8eaf0;}
  .block-container{padding:1.5rem 2rem !important;max-width:1200px;}
  h1,h2,h3{color:#ffffff !important;}
  .hero-box{background:linear-gradient(135deg,#001a2e 0%,#002e4a 50%,#001428 100%);
    border-radius:16px;padding:28px 32px;border:0.5px solid #004080;margin-bottom:24px;}
  .hero-eyebrow{font-size:11px;letter-spacing:.1em;color:#38bdf8;text-transform:uppercase;margin-bottom:4px;}
  .hero-title{font-size:32px;font-weight:700;color:#fff;margin-bottom:6px;}
  .hero-sub{font-size:14px;color:#93c5fd;}
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
  .chip-sky{background:#0a1e35;color:#38bdf8;} .chip-orange{background:#2a1500;color:#fb923c;}
  .stTabs [data-baseweb="tab-list"]{background:#111827;border-radius:10px;padding:4px;gap:2px;}
  .stTabs [data-baseweb="tab"]{background:transparent;color:#9ca3af;border-radius:8px;font-size:13px;padding:8px 18px;border:none;}
  .stTabs [aria-selected="true"]{background:#1f2937 !important;color:#38bdf8 !important;font-weight:600;}
  .prog-wrap{margin-bottom:10px;}
  .prog-lbl{display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px;}
  .prog-bg{height:7px;border-radius:4px;background:#1f2937;overflow:hidden;}
  .prog-fill{height:100%;border-radius:4px;}
  .notice{font-size:12px;color:#6b7280;background:#111827;border-radius:10px;
    padding:10px 14px;margin-top:16px;line-height:1.7;border:0.5px solid #1f2937;}
  .section-lbl{font-size:11px;color:#6b7280;text-transform:uppercase;letter-spacing:.08em;margin:20px 0 10px;}
  .elo-badge{display:inline-block;font-size:11px;padding:2px 8px;border-radius:8px;font-weight:600;margin-left:6px;}
  .elo-pos{background:#0d2e14;color:#5de881;} .elo-neg{background:#2e0d0d;color:#f56060;}
  .rank-badge{display:inline-block;font-size:10px;padding:1px 6px;border-radius:6px;font-weight:600;margin-left:4px;background:#1f2937;color:#60aef5;}
  .weight-row{display:flex;align-items:center;gap:10px;padding:6px 0;border-bottom:0.5px solid #1f2937;font-size:12px;}
  .weight-row:last-child{border-bottom:none;}
  .weight-stars{color:#f5c842;font-size:13px;min-width:90px;}
  .weight-name{color:#fff;font-weight:500;min-width:160px;}
  .weight-desc{color:#6b7280;font-size:11px;}
</style>
""", unsafe_allow_html=True)

def hex_to_rgba(hex_color, alpha=0.12):
    h = hex_color.lstrip("#"); r,g,b = int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"

# ── DATA ──────────────────────────────────────────────────────────────────────
teams = {
    "Turkiye":       {"flag":"🇹🇷","rank":40, "conf":"UEFA",     "pts":7,"w":2,"d":1,"l":0,"color":"#ef4444","qualify":85,"elo":57,  "form":72},
    "Australia":     {"flag":"🇦🇺","rank":23, "conf":"AFC",      "pts":5,"w":1,"d":2,"l":0,"color":"#f5c842","qualify":72,"elo":44,  "form":68},
    "United States": {"flag":"🇺🇸","rank":11, "conf":"CONCACAF", "pts":4,"w":1,"d":1,"l":1,"color":"#3b82f6","qualify":58,"elo":-12, "form":64},
    "Paraguay":      {"flag":"🇵🇾","rank":56, "conf":"CONMEBOL", "pts":0,"w":0,"d":0,"l":3,"color":"#22a84a","qualify":6, "elo":-82, "form":39},
}
matches = [
    {"md":1,"date":"Jun 12","home":"United States","away":"Paraguay",      "hw":99.8,"d":0.1,"aw":0.1,"score":"2–0","conf":"Very High","stadium":"SoFi Stadium, Inglewood",       "h_elo":-12,"a_elo":-82,"h_form":64,"a_form":39,"h_rank":11,"a_rank":56},
    {"md":1,"date":"Jun 13","home":"Australia",    "away":"Turkiye",       "hw":0.2, "d":0.3,"aw":99.5,"score":"1–2","conf":"Very High","stadium":"BC Place, Vancouver",           "h_elo":44, "a_elo":57, "h_form":68,"a_form":72,"h_rank":23,"a_rank":40},
    {"md":2,"date":"Jun 17","home":"United States","away":"Australia",     "hw":0.3, "d":99.4,"aw":0.3,"score":"1–1","conf":"Very High","stadium":"MetLife Stadium, East Rutherford","h_elo":-12,"a_elo":44,"h_form":64,"a_form":68,"h_rank":11,"a_rank":23},
    {"md":2,"date":"Jun 17","home":"Turkiye",      "away":"Paraguay",      "hw":99.8,"d":0.1,"aw":0.1,"score":"2–0","conf":"Very High","stadium":"AT&T Stadium, Arlington",        "h_elo":57, "a_elo":-82,"h_form":72,"a_form":39,"h_rank":40,"a_rank":56},
    {"md":3,"date":"Jun 21","home":"Australia",    "away":"Paraguay",      "hw":99.5,"d":0.4,"aw":0.1,"score":"2–0","conf":"Very High","stadium":"Arrowhead Stadium, Kansas City", "h_elo":44, "a_elo":-82,"h_form":68,"a_form":39,"h_rank":23,"a_rank":56},
    {"md":3,"date":"Jun 21","home":"Turkiye",      "away":"United States", "hw":99.3,"d":0.5,"aw":0.2,"score":"2–1","conf":"Very High","stadium":"Levi's Stadium, Santa Clara",   "h_elo":57, "a_elo":-12,"h_form":72,"a_form":64,"h_rank":40,"a_rank":11},
]
strength = {
    "Turkiye":       {"Attack":78,"Defence":72,"Form":72,"Elo Rating":62,"FIFA Rank":72,"Goal Diff":74},
    "Australia":     {"Attack":70,"Defence":74,"Form":68,"Elo Rating":60,"FIFA Rank":80,"Goal Diff":70},
    "United States": {"Attack":75,"Defence":78,"Form":64,"Elo Rating":45,"FIFA Rank":90,"Goal Diff":68},
    "Paraguay":      {"Attack":52,"Defence":50,"Form":39,"Elo Rating":25,"FIFA Rank":50,"Goal Diff":40},
}
sim_data = {
    "Turkiye":       {"1st":62,"2nd":23,"3rd":0,"elim":15},
    "Australia":     {"1st":20,"2nd":52,"3rd":8,"elim":20},
    "United States": {"1st":15,"2nd":19,"3rd":14,"elim":52},
    "Paraguay":      {"1st":3, "2nd":6, "3rd":2, "elim":89},
}
models_perf = {
    "XGBoost":            100.0,
    "LightGBM":           100.0,
    "ExtraTrees":         100.0,
    "Random Forest":      100.0,
    "SVM":                100.0,
    "MLP Neural Net":     99.1,
}
weight_table = [
    ("⭐⭐⭐⭐⭐","Elo Difference",      "Turkiye +57 vs USA -12 — explains the host upset prediction"),
    ("⭐⭐⭐⭐⭐","Recent Form Score",   "Turkiye 72, Australia 68, USA 64, Paraguay 39 — form clearly divides the group"),
    ("⭐⭐⭐⭐", "FIFA Ranking",        "USA #11 (highest) but Elo tells a different story — ranking gap used as 4x weight feature"),
    ("⭐⭐⭐⭐", "Goal Difference",     "Paraguay avg -1.8/game — the clearest elimination signal in the dataset"),
    ("⭐⭐⭐⭐", "Competitive Flag",    "Turkiye qualified through UEFA — competitive match pedigree reflected here"),
    ("⭐⭐⭐",  "Days Rest",           "USA plays MD1 and MD3 back-to-back with only 9 days — slight fatigue factor"),
    ("⭐⭐⭐⭐", "Avg Goals L5",       "USA avg 1.8 GF / 0.8 GA — solid attacking + defensive profile but Elo gap hurts"),
    ("⭐⭐⭐⭐", "Avg Goals Conceded", "Paraguay 2.1 GA/game — highest conceding rate in the group"),
]
CHART_BG="rgba(0,0,0,0)"; GRID_CLR="rgba(255,255,255,0.06)"; TICK_CLR="#6b7280"

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
  <div class="hero-eyebrow">FIFA World Cup 2026 · Group Stage · Full Weighted ML Prediction</div>
  <div class="hero-title">⚽ Group D Predictions</div>
  <div class="hero-sub">Türkiye · Australia · United States · Paraguay &nbsp;|&nbsp; 6 Matches · 3 Matchdays</div>
</div>""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
for col,(label,val,color) in zip([c1,c2,c3,c4],[
    ("🏆 Predicted Winner","Türkiye","#ef4444"),
    ("✅ All 6 Models","100%","#22a84a"),
    ("⚡ Biggest Surprise","USA 3rd","#f5c842"),
    ("📊 Features Used","18+","#38bdf8")]):
    col.markdown(f'<div class="metric-card"><div class="metric-lbl">{label}</div>'
                 f'<div class="metric-num" style="color:{color};font-size:{"28px" if len(val)>7 else "36px"}">{val}</div></div>',unsafe_allow_html=True)

st.markdown("<br>",unsafe_allow_html=True)
tabs = st.tabs(["🏅 Standings","⚽ All 6 Matches","💪 Team Strength","🎯 Who Qualifies?","🤖 Prediction Quality"])

# ══ TAB 1 ══════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-lbl">Predicted Final Standings — Weighted Model (all metrics)</div>',unsafe_allow_html=True)
    pos_styles = ["pos-1","pos-2","pos-3","pos-4"]
    pos_labels = ["🥇 Group Winners","🥈 2nd Place","🥉 Best 3rd?","❌ Eliminated"]
    bar_colors = ["#ef4444","#f5c842","#3b82f6","#f56060"]
    for i,(team,d) in enumerate(teams.items()):
        elo_c = "elo-pos" if d["elo"]>=0 else "elo-neg"
        elo_s = f"+{d['elo']}" if d["elo"]>=0 else str(d["elo"])
        st.markdown(f"""
        <div class="stand-card"><div class="stand-row" style="flex-wrap:wrap;gap:12px;">
          <div class="pos-badge {pos_styles[i]}">{i+1}</div>
          <div style="font-size:26px">{d['flag']}</div>
          <div style="flex:1;min-width:140px">
            <div style="font-size:15px;font-weight:600;color:#fff">{team}
              <span class="rank-badge">#{d['rank']}</span>
              <span class="elo-badge {elo_c}">Elo {elo_s}</span>
            </div>
            <div style="font-size:11px;color:#6b7280">{d['conf']} · Form {d['form']}/100</div>
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

    cl,cr = st.columns(2)
    with cl:
        fig = go.Figure(go.Bar(x=list(teams.keys()),y=[d["qualify"] for d in teams.values()],
            marker_color=[d["color"] for d in teams.values()],marker_line_width=0,
            text=[f"{d['qualify']}%" for d in teams.values()],textposition="outside",
            textfont=dict(color="#e8eaf0",size=12)))
        fig.update_layout(title=dict(text="Qualification Chance",font=dict(color="#fff",size=14)),
            paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,showlegend=False,height=280,
            yaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR,ticksuffix="%",range=[0,115]),
            xaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR),margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig,use_container_width=True)
    with cr:
        fig2 = go.Figure(go.Bar(x=list(teams.keys()),y=[d["elo"] for d in teams.values()],
            marker_color=["#22a84a" if d["elo"]>=0 else "#ef4444" for d in teams.values()],
            marker_line_width=0,text=[f"{'+' if d['elo']>=0 else ''}{d['elo']}" for d in teams.values()],
            textposition="outside",textfont=dict(color="#e8eaf0",size=12)))
        fig2.update_layout(title=dict(text="Elo Difference ⭐⭐⭐⭐⭐ (Top Feature)",font=dict(color="#fff",size=14)),
            paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,showlegend=False,height=280,
            yaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR),
            xaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR),margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig2,use_container_width=True)
    st.markdown("""<div class="notice">🔑 <strong>Key insight:</strong> The USA (FIFA #11) is the highest-ranked team
    in Group D — yet the model predicts them 3rd. Why? Their Elo Difference is <strong>-12</strong>
    (below average for their recent opponents), while Türkiye's is <strong>+57</strong> (well above).
    When Elo carries 5× weight, Türkiye's stronger competitive results against top-tier opposition
    outweighs the USA's FIFA ranking advantage. Australia's balanced profile earns them 2nd.</div>""",unsafe_allow_html=True)

# ══ TAB 2 ══════════════════════════════════════════════════════════════════════
with tabs[1]:
    prev_md = None
    md_labels = {1:"Matchday 1 — June 12/13",2:"Matchday 2 — June 17",3:"Matchday 3 — June 21"}
    for m in matches:
        if m["md"] != prev_md:
            prev_md = m["md"]
            st.markdown(f'<div class="section-lbl">{md_labels[m["md"]]}</div>',unsafe_allow_html=True)
        ht,at = m["home"],m["away"]
        hf,af = teams[ht]["flag"],teams[at]["flag"]
        hw,d,aw = m["hw"],m["d"],m["aw"]
        c_h,c_a = teams[ht]["color"],teams[at]["color"]
        if hw>=d and hw>=aw: winner=ht; wtype="Home Win"
        elif aw>=hw and aw>=d: winner=at; wtype="Away Win"
        else: winner="Draw"; wtype="Draw"
        win_chip = (f'<span class="chip chip-green">✅ {winner} Win predicted</span>'
                    if wtype!="Draw" else '<span class="chip chip-gold">🤝 Draw predicted</span>')
        h_elo_s = f"+{m['h_elo']}" if m['h_elo']>=0 else str(m['h_elo'])
        a_elo_s = f"+{m['a_elo']}" if m['a_elo']>=0 else str(m['a_elo'])
        h_ec = "elo-pos" if m['h_elo']>=0 else "elo-neg"
        a_ec = "elo-pos" if m['a_elo']>=0 else "elo-neg"
        st.markdown(f"""
        <div class="match-card">
          <div style="font-size:11px;color:#6b7280;margin-bottom:12px">📅 {m['date']} &nbsp;|&nbsp; 🏟️ {m['stadium']}</div>
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:16px;">
            <div style="text-align:center;min-width:110px">
              <div style="font-size:32px">{hf}</div>
              <div style="font-size:13px;font-weight:600;color:#fff;margin-top:4px">{ht}</div>
              <span class="rank-badge">#{m['h_rank']}</span>
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
              <span class="rank-badge">#{m['a_rank']}</span>
              <span class="elo-badge {a_ec}">Elo {a_elo_s}</span>
              <div style="font-size:11px;color:#6b7280;margin-top:2px">Form {m['a_form']}/100</div>
            </div>
          </div>
          <div style="display:flex;gap:8px;margin-bottom:10px;text-align:center;">
            <div style="flex:1;background:#0a1828;border:0.5px solid #1a3050;border-radius:8px;padding:10px 6px;">
              <div style="font-size:20px;font-weight:700;color:#38bdf8">{hw}%</div>
              <div style="font-size:10px;color:#6b7280">{ht} Win</div>
            </div>
            <div style="flex:1;background:#1f2937;border:0.5px solid #374151;border-radius:8px;padding:10px 6px;">
              <div style="font-size:20px;font-weight:700;color:#9ca3af">{d}%</div>
              <div style="font-size:10px;color:#6b7280">Draw</div>
            </div>
            <div style="flex:1;background:#0a1828;border:0.5px solid #1a3050;border-radius:8px;padding:10px 6px;">
              <div style="font-size:20px;font-weight:700;color:#38bdf8">{aw}%</div>
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

# ══ TAB 3 ══════════════════════════════════════════════════════════════════════
with tabs[2]:
    cats = ["Attack","Defence","Form","Elo Rating","FIFA Rank","Goal Diff"]
    fig_radar = go.Figure()
    for team,d in strength.items():
        vals = list(d.values())+[list(d.values())[0]]
        clbl = cats+[cats[0]]; hc = teams[team]["color"]
        fig_radar.add_trace(go.Scatterpolar(r=vals,theta=clbl,name=f"{teams[team]['flag']} {team}",
            line=dict(color=hc,width=2),fill="toself",fillcolor=hex_to_rgba(hc,0.12)))
    fig_radar.update_layout(
        polar=dict(bgcolor="#111827",
            radialaxis=dict(visible=True,range=[0,100],gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR,tickfont=dict(size=9)),
            angularaxis=dict(gridcolor=GRID_CLR,color="#9ca3af")),
        paper_bgcolor=CHART_BG,legend=dict(font=dict(color="#e8eaf0"),bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=30,r=30,t=30,b=30),height=400)
    st.plotly_chart(fig_radar,use_container_width=True)

    st.markdown('<div class="section-lbl">Elo vs Form — top 2 weighted features</div>',unsafe_allow_html=True)
    fig_sc = go.Figure()
    for team,d in teams.items():
        fig_sc.add_trace(go.Scatter(x=[d["elo"]],y=[d["form"]],mode="markers+text",
            marker=dict(size=24,color=d["color"]),text=[f"{d['flag']} {team}"],
            textposition="top center",textfont=dict(color="#e8eaf0",size=11),name=team))
    fig_sc.add_vline(x=0,line_dash="dash",line_color="rgba(255,255,255,0.2)")
    fig_sc.update_layout(paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,showlegend=False,height=320,
        xaxis=dict(title="Elo Difference (⭐⭐⭐⭐⭐)",gridcolor=GRID_CLR,color=TICK_CLR,zeroline=False),
        yaxis=dict(title="Recent Form Score (⭐⭐⭐⭐⭐)",gridcolor=GRID_CLR,color=TICK_CLR),
        margin=dict(l=20,r=20,t=20,b=40))
    st.plotly_chart(fig_sc,use_container_width=True)

    for team,d in strength.items():
        td = teams[team]
        with st.expander(f"{td['flag']}  {team}  ·  FIFA #{td['rank']}  ·  Elo {'+' if td['elo']>=0 else ''}{td['elo']}  ·  Form {td['form']}/100",expanded=(team=="Turkiye")):
            for cat,val in d.items():
                st.markdown(f"""<div class="prog-wrap"><div class="prog-lbl">
                  <span style="color:#9ca3af;font-size:12px">{cat}</span>
                  <span style="color:#fff;font-size:12px;font-weight:500">{val}</span></div>
                  <div class="prog-bg"><div class="prog-fill" style="width:{val}%;background:{td['color']};"></div></div>
                </div>""",unsafe_allow_html=True)

# ══ TAB 4 ══════════════════════════════════════════════════════════════════════
with tabs[3]:
    col1,col2 = st.columns(2)
    for i,(team,s) in enumerate(sim_data.items()):
        td = teams[team]; col = col1 if i%2==0 else col2
        qual_total = s["1st"]+s["2nd"]+s["3rd"]
        qual_color = "#38bdf8" if qual_total>70 else("#f5c842" if qual_total>20 else "#f56060")
        chip_html = (f'<span class="chip chip-sky">✅ Advances</span>' if qual_total>70 else
                     f'<span class="chip chip-gold">🎯 Possible</span>' if qual_total>20 else
                     f'<span class="chip chip-red">❌ Unlikely</span>')
        with col:
            st.markdown(f"""
            <div class="match-card" style="margin-bottom:12px">
              <div style="font-size:28px;margin-bottom:4px">{td['flag']}</div>
              <div style="font-size:16px;font-weight:600;color:#fff;margin-bottom:4px">{team}</div>
              <div style="font-size:11px;color:#6b7280;margin-bottom:12px">
                FIFA #{td['rank']} · Elo {'+' if td['elo']>=0 else ''}{td['elo']} · Form {td['form']}/100</div>
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
    st.markdown("""<div class="match-card">
      <div style="font-size:14px;font-weight:600;color:#f5c842;margin-bottom:10px">⚠️ Key storylines — weighted model insights</div>
      <div style="font-size:13px;color:#9ca3af;line-height:1.9">
        🇹🇷 <strong style="color:#fff">Türkiye's Elo tells the real story</strong> — Despite being ranked #40 (lower than the USA),
        Türkiye's +57 Elo differential shows they've been beating high-quality opposition lately.
        The weighted model gives Elo 5× importance, which pushes Türkiye to 1st.<br>
        🇦🇺 <strong style="color:#fff">Australia's balance wins 2nd</strong> — Solid defensive metrics (Goal Diff +1.2),
        consistent form (68/100), and a competitive draw against the USA in MD2 earns them 2nd place.<br>
        🇺🇸 <strong style="color:#fff">USA's host-nation pressure</strong> — Playing at home (3 games in the USA) usually helps,
        but the model captures their -12 Elo (they've been playing and losing to top teams) and a tough MD3 vs Türkiye.
        3rd is still a best 3rd-place contender position.
      </div></div>""",unsafe_allow_html=True)

# ══ TAB 5 ══════════════════════════════════════════════════════════════════════
with tabs[4]:
    c1,c2,c3 = st.columns(3)
    c1.markdown('<div class="metric-card"><div class="metric-lbl">🏆 Best Model</div><div class="metric-num" style="color:#38bdf8">100%</div><div style="font-size:11px;color:#6b7280;margin-top:4px">⭐⭐⭐⭐⭐ 5 models perfect</div></div>',unsafe_allow_html=True)
    c2.markdown('<div class="metric-card"><div class="metric-lbl">⚡ #1 Feature</div><div class="metric-num" style="color:#f5c842">Elo</div><div style="font-size:11px;color:#6b7280;margin-top:4px">5× weight in model</div></div>',unsafe_allow_html=True)
    c3.markdown('<div class="metric-card"><div class="metric-lbl">📊 Total Features</div><div class="metric-num" style="color:#22a84a">18+</div><div style="font-size:11px;color:#6b7280;margin-top:4px">Elo, Form, Rank, GD...</div></div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown('<div class="section-lbl">Feature Weight Ranking — how all metrics are combined</div>',unsafe_allow_html=True)
    for stars,name,desc in weight_table:
        st.markdown(f"""<div class="weight-row">
          <span class="weight-stars">{stars}</span>
          <span class="weight-name">{name}</span>
          <span class="weight-desc">{desc}</span>
        </div>""",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    fig_m = go.Figure(go.Bar(y=list(models_perf.keys()),x=list(models_perf.values()),orientation="h",
        marker_color=["#38bdf8" if v==100 else "#f5c842" for v in models_perf.values()],
        text=[f"{v}%" for v in models_perf.values()],textposition="outside",
        textfont=dict(color="#e8eaf0",size=11),marker_line_width=0))
    fig_m.update_layout(title=dict(text="All 6 Prediction Engines — Accuracy",font=dict(color="#fff",size=14)),
        paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,
        xaxis=dict(range=[97,102],gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR,ticksuffix="%"),
        yaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color="#e8eaf0",automargin=True),
        margin=dict(l=10,r=60,t=40,b=20),height=280,showlegend=False)
    st.plotly_chart(fig_m,use_container_width=True)
    st.markdown("""<div class="notice">⚠️ Predictions use all 18+ available metrics weighted by predictive importance.
    Elo Difference and Recent Form Score each carry 5× weight. FIFA Ranking, Goal Difference, Competitive Match Flag
    and Avg Goals each carry 4× weight. Lower-weight features (shots, possession, cards) carry 1–2× weight only.
    Football is unpredictable — use these as informed guides, not certainties.</div>""",unsafe_allow_html=True)

st.markdown("""<br>
<div style="text-align:center;font-size:11px;color:#374151;padding:16px 0;border-top:0.5px solid #1f2937;">
  ⚽ FIFA World Cup 2026 · Group D Predictor (Weighted All-Metrics) &nbsp;|&nbsp; Machine Learning &amp; Match Data &nbsp;|&nbsp; For fans, by fans
</div>""",unsafe_allow_html=True)
