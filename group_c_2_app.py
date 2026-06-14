import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="⚽ Group C Predictions | FIFA World Cup 2026",
    page_icon="⚽", layout="wide", initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html,body,[class*="css"]{font-family:'Inter',sans-serif;}
  .stApp{background:#0a0f1a;color:#e8eaf0;}
  .block-container{padding:1.5rem 2rem !important;max-width:1200px;}
  h1,h2,h3{color:#ffffff !important;}
  .hero-box{background:linear-gradient(135deg,#1f0d00 0%,#3d1a00 50%,#0d1e35 100%);
    border-radius:16px;padding:28px 32px;border:0.5px solid #5a2800;margin-bottom:24px;}
  .hero-eyebrow{font-size:11px;letter-spacing:.1em;color:#fbbf24;text-transform:uppercase;margin-bottom:4px;}
  .hero-title{font-size:32px;font-weight:700;color:#fff;margin-bottom:6px;}
  .hero-sub{font-size:14px;color:#d4a87a;}
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
  .chip-grey{background:#1f2937;color:#9ca3af;} .chip-orange{background:#2a1500;color:#fb923c;}
  .stTabs [data-baseweb="tab-list"]{background:#111827;border-radius:10px;padding:4px;gap:2px;}
  .stTabs [data-baseweb="tab"]{background:transparent;color:#9ca3af;border-radius:8px;
    font-size:13px;padding:8px 18px;border:none;}
  .stTabs [aria-selected="true"]{background:#1f2937 !important;color:#fb923c !important;font-weight:600;}
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
    "Brazil":  {"flag":"🇧🇷","rank":5, "conf":"CONMEBOL","pts":7,"w":2,"d":1,"l":0,"color":"#16a34a","qualify":91,"elo":152,"form":78},
    "Morocco": {"flag":"🇲🇦","rank":13,"conf":"CAF",     "pts":7,"w":2,"d":1,"l":0,"color":"#dc2626","qualify":91,"elo":155,"form":80},
    "Scotland":{"flag":"🏴󠁧󠁢󠁳󠁣󠁴󠁿","rank":39,"conf":"UEFA",    "pts":3,"w":1,"d":0,"l":2,"color":"#1d4ed8","qualify":36,"elo":48, "form":60},
    "Haiti":   {"flag":"🇭🇹","rank":90,"conf":"CONCACAF","pts":0,"w":0,"d":0,"l":3,"color":"#7c3aed","qualify":3, "elo":-42,"form":50},
}
matches = [
    {"md":1,"date":"Jun 13","home":"Brazil", "away":"Morocco", "hw":0.3, "d":99.5,"aw":0.3,"score":"2–2","conf":"Very High","stadium":"MetLife Stadium, East Rutherford","h_elo":152,"a_elo":155,"h_form":78,"a_form":80},
    {"md":1,"date":"Jun 13","home":"Haiti",  "away":"Scotland","hw":0.2, "d":0.1, "aw":99.7,"score":"1–2","conf":"Very High","stadium":"Gillette Stadium, Foxborough",   "h_elo":-42,"a_elo":48, "h_form":50,"a_form":60},
    {"md":2,"date":"Jun 17","home":"Brazil", "away":"Haiti",   "hw":99.8,"d":0.1, "aw":0.1, "score":"2–1","conf":"Very High","stadium":"SoFi Stadium, Inglewood",       "h_elo":152,"a_elo":-42,"h_form":78,"a_form":50},
    {"md":2,"date":"Jun 18","home":"Morocco","away":"Scotland","hw":99.6,"d":0.3, "aw":0.1, "score":"2–2","conf":"Very High","stadium":"AT&T Stadium, Arlington",        "h_elo":155,"a_elo":48, "h_form":80,"a_form":60},
    {"md":3,"date":"Jun 22","home":"Brazil", "away":"Scotland","hw":99.5,"d":0.3, "aw":0.2, "score":"2–2","conf":"Very High","stadium":"Lumen Field, Seattle",           "h_elo":152,"a_elo":48, "h_form":78,"a_form":60},
    {"md":3,"date":"Jun 22","home":"Morocco","away":"Haiti",   "hw":99.8,"d":0.1, "aw":0.1, "score":"2–1","conf":"Very High","stadium":"BMO Field, Toronto",             "h_elo":155,"a_elo":-42,"h_form":80,"a_form":50},
]
strength = {
    "Brazil":  {"Attack":90,"Defence":80,"Form":78,"Elo Rating":85,"Goal Diff":68},
    "Morocco": {"Attack":85,"Defence":85,"Form":80,"Elo Rating":86,"Goal Diff":75},
    "Scotland":{"Attack":72,"Defence":68,"Form":60,"Elo Rating":55,"Goal Diff":65},
    "Haiti":   {"Attack":52,"Defence":48,"Form":50,"Elo Rating":32,"Goal Diff":40},
}
sim_data = {
    "Brazil":  {"1st":48,"2nd":43,"3rd":0,"elim":9},
    "Morocco": {"1st":47,"2nd":44,"3rd":0,"elim":9},
    "Scotland":{"1st":4, "2nd":10,"3rd":22,"elim":64},
    "Haiti":   {"1st":1, "2nd":3, "3rd":1, "elim":95},
}
models_perf = {
    "Best Model (XGBoost)":       100.0,
    "Alternative (LightGBM)":     100.0,
    "Smart Trees (ExtraTrees)":   100.0,
    "Forest Model (Rand Forest)": 100.0,
    "Pattern Match (SVM)":        100.0,
    "Neural Network (MLP)":        97.3,
}
weight_table = [
    ("⭐⭐⭐⭐⭐","Elo Difference",       "Brazil +152 vs Morocco +155 — virtually identical, confirming the draw"),
    ("⭐⭐⭐⭐⭐","Recent Form Score",    "Morocco 80/100 vs Brazil 78/100 — Morocco marginally better in form"),
    ("⭐⭐⭐⭐", "Goal Difference",      "Morocco avg +2.0/game vs Brazil +1.2 — Morocco's defence is actually stronger"),
    ("⭐⭐⭐⭐", "Competitive Match Flag","Scotland's WC qualifier win (4–2 vs Denmark) carries extra model weight"),
    ("⭐⭐⭐",  "Days Rest",            "Brazil avg 68 days between matches — fully rested going into tournament"),
    ("⭐⭐⭐⭐", "FIFA Ranking Diff",    "Brazil #5 vs Morocco #13 — tight. Model weights Morocco's form over ranking gap"),
    ("⭐⭐⭐⭐", "Avg Goals Scored L5",  "Brazil 2.6/game, Morocco 2.6/game — identical scoring output"),
    ("⭐⭐⭐⭐", "Avg Goals Conceded L5","Morocco 0.6 conceded vs Brazil 1.4 — Morocco's key defensive advantage"),
]

CHART_BG="rgba(0,0,0,0)"; GRID_CLR="rgba(255,255,255,0.06)"; TICK_CLR="#6b7280"

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
  <div class="hero-eyebrow">FIFA World Cup 2026 · Group Stage · Weighted ML Predictions</div>
  <div class="hero-title">⚽ Group C Predictions</div>
  <div class="hero-sub">Brazil · Morocco · Scotland · Haiti &nbsp;|&nbsp; 6 Matches · 3 Matchdays &nbsp;|&nbsp; Elo + Form weighted model</div>
</div>""", unsafe_allow_html=True)

c1,c2,c3,c4=st.columns(4)
for col,(label,val,color) in zip([c1,c2,c3,c4],[
    ("🏆 Predicted Winners","Brazil & Morocco","#fb923c"),
    ("✅ Best Accuracy","100%","#22a84a"),
    ("⚡ Elo Gap Brazil/Mor","+152 vs +155","#f5c842"),
    ("🔥 Most Contested","Group C","#60aef5")]):
    col.markdown(f'<div class="metric-card"><div class="metric-lbl">{label}</div>'
                 f'<div class="metric-num" style="color:{color};font-size:{"22px" if len(val)>8 else "36px"}">{val}</div></div>',unsafe_allow_html=True)

st.markdown("<br>",unsafe_allow_html=True)
tabs=st.tabs(["🏅 Standings","⚽ All 6 Matches","💪 Team Strength","🎯 Who Qualifies?","🤖 Prediction Quality"])

# ══════ TAB 1 ══════
with tabs[0]:
    st.markdown('<div class="section-lbl">Predicted Final Standings — Weighted Model</div>',unsafe_allow_html=True)
    pos_styles=["pos-1","pos-2","pos-3","pos-4"]
    pos_labels=["🥇 Group Winners (GD)","🥈 2nd Place (GD)","🥉 Best 3rd?","❌ Eliminated"]
    bar_colors=["#16a34a","#dc2626","#1d4ed8","#f56060"]
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
    🔥 <strong>Group C is statistically the tightest group in the tournament.</strong>
    Brazil and Morocco have virtually identical Elo (+152 vs +155), identical form (78 vs 80),
    and identical goals scored (2.6/game). The model is 99.5% confident they draw in MD1.
    1st vs 2nd place will be decided by goal difference in MD2 and MD3 — whoever wins by more goals finishes top.
    Brazil's rank (#5 vs #13) gives a very slight edge for 1st, but Morocco's better defensive record (+0.6 GA vs +1.4) could swing it.</div>""",unsafe_allow_html=True)

# ══════ TAB 2 ══════
with tabs[1]:
    prev_md=None
    md_labels={1:"Matchday 1 — June 13",2:"Matchday 2 — June 17/18",3:"Matchday 3 — June 22"}
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
        highlight=""
        if ht=="Brazil" and at=="Morocco":
            highlight='<span class="chip chip-orange">🔥 Closest match of tournament</span>'
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
            <div style="flex:1;background:#1a1010;border:0.5px solid #3a2010;border-radius:8px;padding:10px 6px;">
              <div style="font-size:20px;font-weight:700;color:#fb923c">{hw}%</div>
              <div style="font-size:10px;color:#6b7280">{ht} Win</div>
            </div>
            <div style="flex:1;background:#1f2937;border:0.5px solid #374151;border-radius:8px;padding:10px 6px;">
              <div style="font-size:20px;font-weight:700;color:#9ca3af">{d}%</div>
              <div style="font-size:10px;color:#6b7280">Draw</div>
            </div>
            <div style="flex:1;background:#1a1010;border:0.5px solid #3a2010;border-radius:8px;padding:10px 6px;">
              <div style="font-size:20px;font-weight:700;color:#fb923c">{aw}%</div>
              <div style="font-size:10px;color:#6b7280">{at} Win</div>
            </div>
          </div>
          <div style="height:8px;border-radius:4px;overflow:hidden;display:flex;margin-bottom:12px;">
            <div style="width:{hw}%;background:{c_h};"></div>
            <div style="width:{d}%;background:#4b5563;"></div>
            <div style="width:{aw}%;background:{c_a};"></div>
          </div>
          {win_chip} <span class="chip chip-gold">Confidence: {m['conf']}</span> {highlight}
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

    st.markdown('<div class="section-lbl">Elo vs Form — why the draw is the model\'s most confident prediction</div>',unsafe_allow_html=True)
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
        with st.expander(f"{td['flag']}  {team}  ·  Rank #{td['rank']}  ·  Elo {'+' if td['elo']>=0 else ''}{td['elo']}  ·  Form {td['form']}/100",expanded=(team=="Morocco")):
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
        qual_color="#fb923c" if qual_total>70 else("#f5c842" if qual_total>20 else "#f56060")
        chip_html=(f'<span class="chip chip-orange">✅ Advances</span>' if qual_total>70 else
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
      <div style="font-size:14px;font-weight:600;color:#f5c842;margin-bottom:10px">⚠️ What the weighted model tells us</div>
      <div style="font-size:13px;color:#9ca3af;line-height:1.9">
        🤝 <strong style="color:#fff">Brazil vs Morocco is the most evenly matched game in the tournament</strong> —
        Elo +152 vs +155, Form 78 vs 80, Goals Scored 2.6 vs 2.6. The model gives 99.5% confidence to a draw.
        No other match in this dataset is this statistically close.<br>
        🏴󠁧󠁢󠁳󠁣󠁴󠁿 <strong style="color:#fff">Scotland's competitive match flag is their secret weapon</strong> —
        Their 4–2 win over Denmark in World Cup qualifying carries 4× weight. It separates them clearly from Haiti
        and gives them a real shot at the best 3rd-place spots.<br>
        🇭🇹 <strong style="color:#fff">Haiti's Elo (-42) is the key barrier</strong> — They beat New Zealand 4–0,
        but NZ are ranked #104. Against Scotland (Elo +48) and Brazil/Morocco (Elo +150), the weighted gap is decisive.
      </div></div>""",unsafe_allow_html=True)

# ══════ TAB 5 ══════
with tabs[4]:
    c1,c2,c3=st.columns(3)
    c1.markdown('<div class="metric-card"><div class="metric-lbl">🏆 Best Model Accuracy</div><div class="metric-num" style="color:#fb923c">100%</div><div style="font-size:11px;color:#6b7280;margin-top:4px">⭐⭐⭐⭐⭐ Excellent</div></div>',unsafe_allow_html=True)
    c2.markdown('<div class="metric-card"><div class="metric-lbl">🔻 Weakest Model</div><div class="metric-num" style="color:#f5c842">97.3%</div><div style="font-size:11px;color:#6b7280;margin-top:4px">MLP — hardest group to model</div></div>',unsafe_allow_html=True)
    c3.markdown('<div class="metric-card"><div class="metric-lbl">🎯 Draw Confidence</div><div class="metric-num" style="color:#60aef5">99.5%</div><div style="font-size:11px;color:#6b7280;margin-top:4px">Brazil vs Morocco MD1</div></div>',unsafe_allow_html=True)

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
        marker_color=["#fb923c" if v==100 else"#f5c842" for v in models_perf.values()],
        text=[f"{v}%" for v in models_perf.values()],textposition="outside",
        textfont=dict(color="#e8eaf0",size=11),marker_line_width=0))
    fig_m.update_layout(title=dict(text="All 6 Prediction Engines — Accuracy",font=dict(color="#fff",size=14)),
        paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,
        xaxis=dict(range=[95,102],gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR,ticksuffix="%"),
        yaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color="#e8eaf0",automargin=True),
        margin=dict(l=10,r=60,t=40,b=20),height=280,showlegend=False)
    st.plotly_chart(fig_m,use_container_width=True)
    st.markdown("""<div class="notice">⚠️ This is the <strong>v2 weighted model</strong>. Elo Difference and Recent Form Score
    each carry 5× weight. Goal Difference, Competitive Match Flag, and FIFA Ranking Difference carry 4× weight.
    Lower-weight features (shots, possession, cards) carry 1–2× weight only.
    Group C is statistically the hardest group to model because Brazil and Morocco are almost perfectly matched —
    which is why the MLP neural network scores 97.3% here vs 100% in Group G.</div>""",unsafe_allow_html=True)

st.markdown("""<br>
<div style="text-align:center;font-size:11px;color:#374151;padding:16px 0;border-top:0.5px solid #1f2937;">
  ⚽ FIFA World Cup 2026 · Group C Predictor v2 (Weighted) &nbsp;|&nbsp; Machine Learning &amp; Match Data &nbsp;|&nbsp; For fans, by fans
</div>""",unsafe_allow_html=True)
