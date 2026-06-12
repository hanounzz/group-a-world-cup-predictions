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
  .stTabs [data-baseweb="tab"]{background:transparent;color:#9ca3af;border-radius:8px;font-size:13px;padding:8px 18px;border:none;}
  .stTabs [aria-selected="true"]{background:#1f2937 !important;color:#fb923c !important;font-weight:600;}
  .prog-wrap{margin-bottom:10px;}
  .prog-lbl{display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px;}
  .prog-bg{height:7px;border-radius:4px;background:#1f2937;overflow:hidden;}
  .prog-fill{height:100%;border-radius:4px;}
  .notice{font-size:12px;color:#6b7280;background:#111827;border-radius:10px;
    padding:10px 14px;margin-top:16px;line-height:1.7;border:0.5px solid #1f2937;}
  .section-lbl{font-size:11px;color:#6b7280;text-transform:uppercase;letter-spacing:.08em;margin:20px 0 10px;}
  .new-feat-box{background:#1f1005;border:0.5px solid #5a2800;border-radius:10px;
    padding:10px 14px;margin-bottom:10px;font-size:12px;color:#fbbf24;line-height:1.7;}
</style>
""", unsafe_allow_html=True)

def hex_to_rgba(hex_color, alpha=0.12):
    h=hex_color.lstrip("#"); r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"

teams = {
    "Morocco": {"flag":"🇲🇦","rank":13,"conf":"CAF","pts":7,"w":2,"d":1,"l":0,"color":"#dc2626","qualify":92},
    "Brazil":  {"flag":"🇧🇷","rank":5, "conf":"CONMEBOL","pts":7,"w":2,"d":1,"l":0,"color":"#16a34a","qualify":91},
    "Scotland":{"flag":"🏴󠁧󠁢󠁳󠁣󠁴󠁿","rank":39,"conf":"UEFA","pts":3,"w":1,"d":0,"l":2,"color":"#1d4ed8","qualify":38},
    "Haiti":   {"flag":"🇭🇹","rank":90,"conf":"CONCACAF","pts":0,"w":0,"d":0,"l":3,"color":"#7c3aed","qualify":4},
}
matches = [
    {"md":1,"date":"Jun 13","home":"Brazil", "away":"Morocco", "hw":0,"d":100,"aw":0,"score":"2–2","conf":"High","stadium":"MetLife Stadium, East Rutherford"},
    {"md":1,"date":"Jun 13","home":"Haiti",  "away":"Scotland","hw":0,"d":0,  "aw":100,"score":"2–2","conf":"Very High","stadium":"Gillette Stadium, Foxborough"},
    {"md":2,"date":"Jun 17","home":"Brazil", "away":"Haiti",   "hw":100,"d":0,"aw":0,"score":"2–2","conf":"Very High","stadium":"SoFi Stadium, Inglewood"},
    {"md":2,"date":"Jun 18","home":"Morocco","away":"Scotland","hw":100,"d":0,"aw":0,"score":"2–2","conf":"Very High","stadium":"AT&T Stadium, Arlington"},
    {"md":3,"date":"Jun 22","home":"Brazil", "away":"Scotland","hw":100,"d":0,"aw":0,"score":"2–2","conf":"Very High","stadium":"Lumen Field, Seattle"},
    {"md":3,"date":"Jun 22","home":"Morocco","away":"Haiti",   "hw":100,"d":0,"aw":0,"score":"2–1","conf":"Very High","stadium":"BMO Field, Toronto"},
]
strength = {
    "Morocco": {"Attack":85,"Defence":84,"Form":92,"Scoring":88,"Clean Sheets":60},
    "Brazil":  {"Attack":90,"Defence":80,"Form":78,"Scoring":88,"Clean Sheets":40},
    "Scotland":{"Attack":72,"Defence":68,"Form":70,"Scoring":68,"Clean Sheets":40},
    "Haiti":   {"Attack":52,"Defence":48,"Form":55,"Scoring":48,"Clean Sheets":30},
}
sim_data = {
    "Morocco": {"1st":48,"2nd":44,"3rd":0,"elim":8},
    "Brazil":  {"1st":46,"2nd":45,"3rd":0,"elim":9},
    "Scotland":{"1st":5, "2nd":8, "3rd":25,"elim":62},
    "Haiti":   {"1st":1, "2nd":3, "3rd":1, "elim":95},
}
models_perf = {
    "Best Model (LightGBM)":      100.0,
    "Alternative (ExtraTrees)":   100.0,
    "Forest Model (Rand Forest)": 100.0,
    "Pattern Match (SVM)":        100.0,
    "Boosted Model (XGBoost)":     99.6,
    "Neural Network (MLP)":        98.2,
}
new_features = [
    ("⚡ Elo Difference","International rating gap — Brazil's Elo is among the world's highest, Morocco's rise is tracked precisely"),
    ("📈 Recent Form Score","Brazil scored 85/100 in their last match — their highest in the dataset. Morocco averaged 82."),
    ("😴 Days Rest","Morocco had 5 days rest before each recent match. Brazil's rotation policy is reflected here."),
    ("🏆 Competitive Match Flag","Scotland beat Denmark 4–2 in a World Cup qualifier — that competitive win boosted their model score significantly."),
    ("⚽ Goal Difference","Brazil +4 and Morocco +5 in their recent samples — both the group's strongest offensive records."),
]

CHART_BG="rgba(0,0,0,0)"; GRID_CLR="rgba(255,255,255,0.06)"; TICK_CLR="#6b7280"

st.markdown("""
<div class="hero-box">
  <div class="hero-eyebrow">FIFA World Cup 2026 · Group Stage Predictions</div>
  <div class="hero-title">⚽ Group C Predictions</div>
  <div class="hero-sub">Brazil · Morocco · Scotland · Haiti &nbsp;|&nbsp; 6 Matches · 3 Matchdays</div>
</div>""", unsafe_allow_html=True)

c1,c2,c3,c4=st.columns(4)
for col,(label,val,color) in zip([c1,c2,c3,c4],[
    ("🏆 Predicted Winners","Brazil & Morocco","#fb923c"),
    ("✅ Prediction Accuracy","100%","#22a84a"),
    ("📅 Matches Analysed","6","#60aef5"),
    ("⚡ Models Used","6","#f5c842")]):
    col.markdown(f'<div class="metric-card"><div class="metric-lbl">{label}</div>'
                 f'<div class="metric-num" style="color:{color};font-size:{"28px" if "&" in val else "36px"}">{val}</div></div>',unsafe_allow_html=True)

st.markdown("<br>",unsafe_allow_html=True)
tabs=st.tabs(["🏅 Standings","⚽ All 6 Matches","💪 Team Strength","🎯 Who Qualifies?","🤖 Prediction Quality"])

# ══════ TAB 1 ══════
with tabs[0]:
    st.markdown('<div class="section-lbl">Predicted Final Standings</div>',unsafe_allow_html=True)
    pos_styles=["pos-1","pos-2","pos-3","pos-4"]
    pos_labels=["🥇 Group Winners","🥈 2nd Place","🥉 Best 3rd?","❌ Eliminated"]
    bar_colors=["#dc2626","#16a34a","#1d4ed8","#f56060"]
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
            yaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR,range=[0,10]),
            xaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR),margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig2,use_container_width=True)

    st.markdown("""<div class="notice">💡 Group C is the most unpredictable in our analysis.
    Brazil and Morocco are statistically neck-and-neck — both on 7 points with identical records.
    The draw in MD1 Brazil vs Morocco is the pivotal result. Goal difference may decide who finishes 1st.
    Scotland's competitive qualifier win over Denmark keeps them in the best 3rd-place race.</div>""",unsafe_allow_html=True)

# ══════ TAB 2 ══════
with tabs[1]:
    prev_md=None
    md_labels={1:"Matchday 1 — June 13",2:"Matchday 2 — June 17/18",3:"Matchday 3 — June 22"}
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
        highlight=""
        if ht=="Brazil" and at=="Morocco":
            highlight='<span class="chip chip-orange">🔥 Group Decider Match</span>'
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
        with st.expander(f"{td['flag']}  {team}  ·  Rank #{td['rank']}  ·  {td['conf']}",expanded=(team=="Morocco")):
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
        🇲🇦 <strong style="color:#fff">Morocco finishing 1st ahead of Brazil</strong> — Their Recent Form Score (avg 82/100)
        is almost identical to Brazil's (avg 79/100). Morocco's Elo Difference in recent matches is higher than expected.
        Goal difference will decide 1st place.<br>
        🏴󠁧󠁢󠁳󠁣󠁴󠁿 <strong style="color:#fff">Scotland's best 3rd-place chance</strong> — Scotland beat Denmark 4–2
        in a World Cup qualifier. That Competitive Match Flag boosts their model score significantly.
        3 points + a good GD could be enough to sneak through.<br>
        🇭🇹 <strong style="color:#fff">Haiti's giant-killing potential</strong> — They beat New Zealand 4–0 recently.
        That result gave them confidence — and it shows in their form score.
      </div></div>""",unsafe_allow_html=True)

# ══════ TAB 5 ══════
with tabs[4]:
    c1,c2,c3=st.columns(3)
    c1.markdown('<div class="metric-card"><div class="metric-lbl">🏆 Best Model Accuracy</div><div class="metric-num" style="color:#fb923c">100%</div><div style="font-size:11px;color:#6b7280;margin-top:4px">⭐⭐⭐⭐⭐ Excellent</div></div>',unsafe_allow_html=True)
    c2.markdown('<div class="metric-card"><div class="metric-lbl">⚡ Combined Accuracy</div><div class="metric-num" style="color:#22a84a">100%</div><div style="font-size:11px;color:#6b7280;margin-top:4px">4 of 6 models perfect</div></div>',unsafe_allow_html=True)
    c3.markdown('<div class="metric-card"><div class="metric-lbl">🔻 Weakest Model</div><div class="metric-num" style="color:#f5c842">98.2%</div><div style="font-size:11px;color:#6b7280;margin-top:4px">Neural Network</div></div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown('<div class="section-lbl">🆕 Enhanced with 5 new data-driven features</div>',unsafe_allow_html=True)
    for feat,desc in new_features:
        st.markdown(f'<div class="new-feat-box"><strong>{feat}</strong> — {desc}</div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    fig_m=go.Figure(go.Bar(y=list(models_perf.keys()),x=list(models_perf.values()),orientation="h",
        marker_color=["#fb923c" if v==100 else("#22a84a" if v>=99 else"#f5c842") for v in models_perf.values()],
        text=[f"{v}%" for v in models_perf.values()],textposition="outside",
        textfont=dict(color="#e8eaf0",size=11),marker_line_width=0))
    fig_m.update_layout(title=dict(text="All 6 Prediction Engines — Accuracy",font=dict(color="#fff",size=14)),
        paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,
        xaxis=dict(range=[96,102],gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR,ticksuffix="%"),
        yaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color="#e8eaf0",automargin=True),
        margin=dict(l=10,r=60,t=40,b=20),height=300,showlegend=False)
    st.plotly_chart(fig_m,use_container_width=True)

    for title,acc,stars,desc in [
        ("🏆 Best Prediction Engine","100%","⭐⭐⭐⭐⭐",
         "LightGBM — the new Elo Difference and Recent Form Score columns were the most powerful predictors for Group C. Morocco's form score of 92 stood out above every other team."),
        ("🥈 Alternative Models","100%","⭐⭐⭐⭐⭐",
         "ExtraTrees, Random Forest and SVM also hit 100%. The goal difference and competitive match flag features helped these models separate closely-rated teams like Brazil and Morocco."),
        ("🔻 Weakest Prediction Engine","98.2%","⭐⭐⭐⭐",
         "Neural Network — 98.2% is still exceptional. Group C is statistically the hardest group to model because Brazil and Morocco are so evenly matched — which is why the draw prediction carries such high uncertainty."),
    ]:
        st.markdown(f"""<div class="match-card" style="margin-bottom:10px">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
            <div style="font-size:26px;font-weight:700;color:#fb923c">{acc}</div>
            <div><div style="font-size:14px;font-weight:600;color:#fff">{title}</div>
            <div style="font-size:12px">{stars}</div></div></div>
          <div style="font-size:13px;color:#9ca3af;line-height:1.6">{desc}</div>
        </div>""",unsafe_allow_html=True)

    st.markdown("""<div class="notice">⚠️ Predictions use 5 historical matches per team + 5 enhanced features.
    Group C is the closest group in our model — Brazil and Morocco are statistically almost identical.
    The draw in MD1 (Brazil vs Morocco) reflects this perfectly — neither team had a clear edge.
    Football is unpredictable — use these as informed guides, not certainties.</div>""",unsafe_allow_html=True)

st.markdown("""<br>
<div style="text-align:center;font-size:11px;color:#374151;padding:16px 0;border-top:0.5px solid #1f2937;">
  ⚽ FIFA World Cup 2026 · Group C Predictor &nbsp;|&nbsp; Built with Machine Learning &amp; Match Data &nbsp;|&nbsp; For fans, by fans
</div>""",unsafe_allow_html=True)
