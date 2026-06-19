import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="⚽ Group L Predictions | FIFA World Cup 2026",
    page_icon="⚽", layout="wide", initial_sidebar_state="collapsed",
)
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html,body,[class*="css"]{font-family:'Inter',sans-serif;}
  .stApp{background:#0a0f1a;color:#e8eaf0;}
  .block-container{padding:1.5rem 2rem !important;max-width:1200px;}
  h1,h2,h3{color:#ffffff !important;}
  .hero-box{background:linear-gradient(135deg,#001428 0%,#002244 50%,#001a0a 100%);
    border-radius:16px;padding:28px 32px;border:0.5px solid #003060;margin-bottom:24px;}
  .hero-eyebrow{font-size:11px;letter-spacing:.1em;color:#34d399;text-transform:uppercase;margin-bottom:4px;}
  .hero-title{font-size:32px;font-weight:700;color:#fff;margin-bottom:6px;}
  .hero-sub{font-size:14px;color:#6ee7b7;}
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
  .chip-teal{background:#0a2420;color:#34d399;} .chip-red{background:#2e0d0d;color:#f56060;}
  .stTabs [data-baseweb="tab-list"]{background:#111827;border-radius:10px;padding:4px;gap:2px;}
  .stTabs [data-baseweb="tab"]{background:transparent;color:#9ca3af;border-radius:8px;font-size:13px;padding:8px 18px;border:none;}
  .stTabs [aria-selected="true"]{background:#1f2937 !important;color:#34d399 !important;font-weight:600;}
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
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

teams = {
    "England": {"flag":"🏴󠁧󠁢󠁥󠁮󠁧󠁿","rank":4, "conf":"UEFA",    "pts":9,"w":3,"d":0,"l":0,"color":"#60aef5","qualify":97,"elo":336,"form":69},
    "Ghana":   {"flag":"🇬🇭","rank":68,"conf":"CAF",     "pts":4,"w":1,"d":1,"l":1,"color":"#22a84a","qualify":52,"elo":54, "form":69},
    "Croatia": {"flag":"🇭🇷","rank":10,"conf":"UEFA",    "pts":4,"w":1,"d":1,"l":1,"color":"#ef4444","qualify":48,"elo":64, "form":63},
    "Panama":  {"flag":"🇵🇦","rank":45,"conf":"CONCACAF","pts":0,"w":0,"d":0,"l":3,"color":"#f5c842","qualify":4, "elo":-30,"form":62},
}
matches = [
    {"md":1,"date":"Jun 17","home":"England", "away":"Croatia","hw":74.3,"d":23.1,"aw":2.6,"score":"2-1","conf":"High",    "stadium":"AT&T Stadium, Arlington",         "h_elo":336,"a_elo":64, "h_form":69,"a_form":63,"h_rank":4, "a_rank":10},
    {"md":1,"date":"Jun 17","home":"Ghana",   "away":"Panama", "hw":63.4,"d":32.9,"aw":3.7,"score":"2-2","conf":"Medium",  "stadium":"BMO Field, Toronto",              "h_elo":54, "a_elo":-30,"h_form":69,"a_form":62,"h_rank":68,"a_rank":45},
    {"md":2,"date":"Jun 21","home":"England", "away":"Ghana",  "hw":76.2,"d":21.4,"aw":2.4,"score":"1-2","conf":"High",    "stadium":"MetLife Stadium, East Rutherford","h_elo":336,"a_elo":54, "h_form":69,"a_form":69,"h_rank":4, "a_rank":68},
    {"md":2,"date":"Jun 21","home":"Croatia", "away":"Panama", "hw":65.2,"d":31.3,"aw":3.5,"score":"2-2","conf":"Medium",  "stadium":"Arrowhead Stadium, Kansas City",  "h_elo":64, "a_elo":-30,"h_form":63,"a_form":62,"h_rank":10,"a_rank":45},
    {"md":3,"date":"Jun 25","home":"England", "away":"Panama", "hw":89.6,"d":9.4, "aw":1.0,"score":"2-2","conf":"Very High","stadium":"Lumen Field, Seattle",            "h_elo":336,"a_elo":-30,"h_form":69,"a_form":62,"h_rank":4, "a_rank":45},
    {"md":3,"date":"Jun 25","home":"Croatia", "away":"Ghana",  "hw":0.3, "d":99.4,"aw":0.3,"score":"1-2","conf":"Medium",  "stadium":"Estadio BBVA, Monterrey",         "h_elo":64, "a_elo":54, "h_form":63,"a_form":69,"h_rank":10,"a_rank":68},
]
strength = {
    "England": {"Attack":82,"Defence":90,"Form":69,"Elo Rating":98,"FIFA Rank":97,"Goal Diff":84},
    "Ghana":   {"Attack":72,"Defence":80,"Form":69,"Elo Rating":62,"FIFA Rank":42,"Goal Diff":76},
    "Croatia": {"Attack":70,"Defence":65,"Form":63,"Elo Rating":64,"FIFA Rank":92,"Goal Diff":62},
    "Panama":  {"Attack":65,"Defence":55,"Form":62,"Elo Rating":38,"FIFA Rank":58,"Goal Diff":52},
}
sim_data = {
    "England": {"1st":88,"2nd":11,"3rd":0,"elim":1},
    "Ghana":   {"1st":6, "2nd":42,"3rd":10,"elim":42},
    "Croatia": {"1st":6, "2nd":42,"3rd":10,"elim":42},
    "Panama":  {"1st":0, "2nd":1, "3rd":0, "elim":99},
}
models_perf = {"XGBoost":100.0,"LightGBM":100.0,"ExtraTrees":100.0,"Random Forest":100.0,"SVM":100.0,"MLP":97.2}
weight_table = [
    ("⭐⭐⭐⭐⭐","Elo Difference",     "England +336 — 4th highest Elo in tournament. Ghana +54 edges Croatia +64 for 2nd"),
    ("⭐⭐⭐⭐⭐","Recent Form Score",  "England 69 = Ghana 69 — identical form; Croatia 63 drives England win prediction"),
    ("⭐⭐⭐⭐", "FIFA Ranking",       "England #4, Croatia #10 — but Ghana #68 despite matching England's form score"),
    ("⭐⭐⭐⭐", "Goal Difference",    "GD computed from Goals Scored minus Goals Conceded — source file had NaN"),
    ("⭐⭐⭐⭐", "Avg Goals Scored",   "Panama 2.0 GF/game — most in group! But 2.2 GA/game is too costly"),
    ("⭐⭐⭐",  "Days Rest",          "Croatia vs Ghana MD3 with near-equal rest — reflected in the draw prediction"),
    ("⭐⭐⭐⭐", "Competitive Flag",   "England Nations League, Euro 2024 — full competitive record available"),
    ("⭐⭐⭐⭐", "Possession %",      "England 67% — highest in group. Tactical dominance captured in model"),
]
ACCENT = "#34d399"
CHART_BG = "rgba(0,0,0,0)"; GRID_CLR = "rgba(255,255,255,0.06)"; TICK_CLR = "#6b7280"

st.markdown("""
<div class="hero-box">
  <div class="hero-eyebrow">FIFA World Cup 2026 · Group Stage · Full Weighted ML Prediction</div>
  <div class="hero-title">⚽ Group L Predictions</div>
  <div class="hero-sub">England · Croatia · Ghana · Panama &nbsp;|&nbsp; 6 Matches · 3 Matchdays</div>
</div>""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
c1.markdown(f'<div class="metric-card"><div class="metric-lbl">🏆 Predicted Winner</div><div class="metric-num" style="color:#60aef5">England</div></div>',unsafe_allow_html=True)
c2.markdown('<div class="metric-card"><div class="metric-lbl">✅ Best Accuracy</div><div class="metric-num" style="color:#22a84a">100%</div></div>',unsafe_allow_html=True)
c3.markdown(f'<div class="metric-card"><div class="metric-lbl">🔥 Surprise Result</div><div class="metric-num" style="color:{ACCENT};font-size:26px">Ghana 2nd</div></div>',unsafe_allow_html=True)
c4.markdown('<div class="metric-card"><div class="metric-lbl">⚡ MD3 Draw</div><div class="metric-num" style="color:#f5c842">Cro/Ghana</div></div>',unsafe_allow_html=True)

st.markdown("<br>",unsafe_allow_html=True)
tabs = st.tabs(["🏅 Standings","⚽ All 6 Matches","💪 Team Strength","🎯 Who Qualifies?","🤖 Prediction Quality"])

with tabs[0]:
    st.markdown('<div class="section-lbl">Predicted Final Standings — Weighted Model (all metrics)</div>',unsafe_allow_html=True)
    pos_styles = ["pos-1","pos-2","pos-3","pos-4"]
    pos_labels = ["🥇 Group Winners","🥈 2nd Place","🥉 Best 3rd?","❌ Eliminated"]
    bar_colors = [d["color"] for d in teams.values()]
    for i,(team,d) in enumerate(teams.items()):
        elo_c = "elo-pos" if d["elo"] >= 0 else "elo-neg"
        elo_s = f"+{d['elo']}" if d["elo"] >= 0 else str(d["elo"])
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
        </div></div>""", unsafe_allow_html=True)
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
        elo_vals = [d["elo"] for d in teams.values()]
        elo_colors = ["#22a84a" if v >= 0 else "#ef4444" for v in elo_vals]
        elo_text = [f"+{v}" if v >= 0 else str(v) for v in elo_vals]
        fig2 = go.Figure(go.Bar(x=list(teams.keys()),y=elo_vals,
            marker_color=elo_colors,marker_line_width=0,
            text=elo_text,textposition="outside",textfont=dict(color="#e8eaf0",size=12)))
        fig2.update_layout(title=dict(text="Elo Difference (5x weight — top feature)",font=dict(color="#fff",size=14)),
            paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,showlegend=False,height=280,
            yaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR),
            xaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR),margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig2,use_container_width=True)
    st.markdown("""<div class="notice">🔑 <strong>The big surprise in Group L: Ghana edges Croatia for 2nd place.</strong>
    Ghana ranks #68 but their form score (69/100) exactly matches England's and beats Croatia's (63/100).
    Their Elo +54 is only 10 points below Croatia's +64 — in a 5x weighted feature, that 10-point gap
    is what the model uses to resolve their near-identical profile in MD3, giving a draw and placing
    Ghana ahead on goal difference.</div>""",unsafe_allow_html=True)

with tabs[1]:
    prev_md = None
    md_labels = {1:"Matchday 1 — June 17",2:"Matchday 2 — June 21",3:"Matchday 3 — June 25"}
    for m in matches:
        if m["md"] != prev_md:
            prev_md = m["md"]
            st.markdown(f'<div class="section-lbl">{md_labels[m["md"]]}</div>',unsafe_allow_html=True)
        ht,at = m["home"],m["away"]
        hf,af = teams[ht]["flag"],teams[at]["flag"]
        hw,d,aw = m["hw"],m["d"],m["aw"]
        c_h,c_a = teams[ht]["color"],teams[at]["color"]
        if hw >= d and hw >= aw: winner = ht; wtype = "Home Win"
        elif aw >= hw and aw >= d: winner = at; wtype = "Away Win"
        else: winner = "Draw"; wtype = "Draw"
        win_chip = (f'<span class="chip chip-green">✅ {winner} Win predicted</span>'
                    if wtype != "Draw" else '<span class="chip chip-gold">🤝 Draw predicted</span>')
        h_elo_s = f"+{m['h_elo']}" if m['h_elo'] >= 0 else str(m['h_elo'])
        a_elo_s = f"+{m['a_elo']}" if m['a_elo'] >= 0 else str(m['a_elo'])
        h_ec = "elo-pos" if m['h_elo'] >= 0 else "elo-neg"
        a_ec = "elo-pos" if m['a_elo'] >= 0 else "elo-neg"
        surprise = '<span class="chip chip-teal">🔥 Surprise: Ghana away win</span>' if ht=="England" and at=="Ghana" else ""
        final_draw = '<span class="chip chip-teal">🏆 Group decider for 2nd</span>' if ht=="Croatia" and at=="Ghana" else ""
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
            <div style="flex:1;background:#0a2420;border:0.5px solid #1a5040;border-radius:8px;padding:10px 6px;">
              <div style="font-size:20px;font-weight:700;color:#34d399">{hw}%</div>
              <div style="font-size:10px;color:#6b7280">{ht} Win</div>
            </div>
            <div style="flex:1;background:#1f2937;border:0.5px solid #374151;border-radius:8px;padding:10px 6px;">
              <div style="font-size:20px;font-weight:700;color:#9ca3af">{d}%</div>
              <div style="font-size:10px;color:#6b7280">Draw</div>
            </div>
            <div style="flex:1;background:#0a2420;border:0.5px solid #1a5040;border-radius:8px;padding:10px 6px;">
              <div style="font-size:20px;font-weight:700;color:#34d399">{aw}%</div>
              <div style="font-size:10px;color:#6b7280">{at} Win</div>
            </div>
          </div>
          <div style="height:8px;border-radius:4px;overflow:hidden;display:flex;margin-bottom:12px;">
            <div style="width:{hw}%;background:{c_h};"></div>
            <div style="width:{d}%;background:#4b5563;"></div>
            <div style="width:{aw}%;background:{c_a};"></div>
          </div>
          {win_chip} <span class="chip chip-gold">Confidence: {m['conf']}</span> {surprise}{final_draw}
        </div>""", unsafe_allow_html=True)

with tabs[2]:
    cats = ["Attack","Defence","Form","Elo Rating","FIFA Rank","Goal Diff"]
    fig_r = go.Figure()
    for team,d in strength.items():
        vals = list(d.values()) + [list(d.values())[0]]
        clbl = cats + [cats[0]]
        hc = teams[team]["color"]
        fig_r.add_trace(go.Scatterpolar(r=vals,theta=clbl,name=f"{teams[team]['flag']} {team}",
            line=dict(color=hc,width=2),fill="toself",fillcolor=hex_to_rgba(hc,0.12)))
    fig_r.update_layout(
        polar=dict(bgcolor="#111827",
            radialaxis=dict(visible=True,range=[0,100],gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR,tickfont=dict(size=9)),
            angularaxis=dict(gridcolor=GRID_CLR,color="#9ca3af")),
        paper_bgcolor=CHART_BG,legend=dict(font=dict(color="#e8eaf0"),bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=30,r=30,t=30,b=30),height=400)
    st.plotly_chart(fig_r,use_container_width=True)
    for team,d in strength.items():
        td = teams[team]
        elo_sign = "+" if td["elo"] >= 0 else ""
        with st.expander(f"{td['flag']}  {team}  ·  FIFA #{td['rank']}  ·  Elo {elo_sign}{td['elo']}  ·  Form {td['form']}/100",expanded=(team=="England")):
            for cat,val in d.items():
                st.markdown(f"""<div class="prog-wrap"><div class="prog-lbl">
                  <span style="color:#9ca3af;font-size:12px">{cat}</span>
                  <span style="color:#fff;font-size:12px;font-weight:500">{val}</span></div>
                  <div class="prog-bg"><div class="prog-fill" style="width:{val}%;background:{td['color']};"></div></div>
                </div>""",unsafe_allow_html=True)

with tabs[3]:
    col1,col2 = st.columns(2)
    for i,(team,s) in enumerate(sim_data.items()):
        td = teams[team]; col = col1 if i % 2 == 0 else col2
        qual_total = s["1st"] + s["2nd"] + s["3rd"]
        qual_color = "#60aef5" if team=="England" else (ACCENT if qual_total > 70 else ("#f5c842" if qual_total > 20 else "#f56060"))
        chip_html = (f'<span class="chip chip-teal">✅ Advances</span>' if qual_total > 70 else
                     f'<span class="chip chip-gold">🎯 Possible</span>' if qual_total > 20 else
                     f'<span class="chip chip-red">❌ Unlikely</span>')
        elo_sign = "+" if td["elo"] >= 0 else ""
        with col:
            st.markdown(f"""
            <div class="match-card" style="margin-bottom:12px">
              <div style="font-size:28px;margin-bottom:4px">{td['flag']}</div>
              <div style="font-size:16px;font-weight:600;color:#fff;margin-bottom:4px">{team}</div>
              <div style="font-size:11px;color:#6b7280;margin-bottom:12px">
                FIFA #{td['rank']} · Elo {elo_sign}{td['elo']} · Form {td['form']}/100</div>
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
      <div style="font-size:14px;font-weight:600;color:#f5c842;margin-bottom:10px">⚠️ Key insights — weighted model</div>
      <div style="font-size:13px;color:#9ca3af;line-height:1.9">
        🏴󠁧󠁢󠁥󠁮󠁧󠁿 <strong style="color:#fff">England are clear group winners</strong> — Elo +336 (4th in tournament),
        67% possession average and consistent form. Perfect 9-point sweep predicted.<br>
        🇬🇭 <strong style="color:#fff">Ghana's shock 2nd place</strong> — Despite being ranked #68, Ghana's form score
        of 69/100 exactly equals England's and beats Croatia's 63/100. Their Elo +54 is only 10 points
        below Croatia's +64 — these near-identical numbers force the MD3 draw and give Ghana 2nd on goal difference.<br>
        🇭🇷 <strong style="color:#fff">Croatia miss out</strong> — Despite being ranked #10 (higher than Ghana), their
        63/100 form score and slightly lower Elo are what the model sees. Data beats reputation.
      </div></div>""",unsafe_allow_html=True)

with tabs[4]:
    c1,c2,c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card"><div class="metric-lbl">🏆 Best Models</div><div class="metric-num" style="color:{ACCENT}">100%</div><div style="font-size:11px;color:#6b7280;margin-top:4px">5 models perfect</div></div>',unsafe_allow_html=True)
    c2.markdown('<div class="metric-card"><div class="metric-lbl">⚡ Top Feature</div><div class="metric-num" style="color:#f5c842">Elo</div><div style="font-size:11px;color:#6b7280;margin-top:4px">5x weight</div></div>',unsafe_allow_html=True)
    c3.markdown('<div class="metric-card"><div class="metric-lbl">📝 Form Scale</div><div class="metric-num" style="color:#22a84a">0-10</div><div style="font-size:11px;color:#6b7280;margin-top:4px">Normalized to 0-100</div></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown('<div class="section-lbl">Feature Weight Ranking — how all metrics are combined</div>',unsafe_allow_html=True)
    for stars,name,desc in weight_table:
        st.markdown(f"""<div class="weight-row">
          <span class="weight-stars">{stars}</span>
          <span class="weight-name">{name}</span>
          <span class="weight-desc">{desc}</span>
        </div>""",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    best_acc = max(models_perf.values())
    fig_m = go.Figure(go.Bar(y=list(models_perf.keys()),x=list(models_perf.values()),orientation="h",
        marker_color=[ACCENT if v >= best_acc else "#f5c842" for v in models_perf.values()],
        text=[f"{v}%" for v in models_perf.values()],textposition="outside",
        textfont=dict(color="#e8eaf0",size=11),marker_line_width=0))
    fig_m.update_layout(title=dict(text="All 6 Prediction Engines — Accuracy",font=dict(color="#fff",size=14)),
        paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,
        xaxis=dict(range=[95,102],gridcolor=GRID_CLR,tickcolor=TICK_CLR,color=TICK_CLR,ticksuffix="%"),
        yaxis=dict(gridcolor=GRID_CLR,tickcolor=TICK_CLR,color="#e8eaf0",automargin=True),
        margin=dict(l=10,r=60,t=40,b=20),height=280,showlegend=False)
    st.plotly_chart(fig_m,use_container_width=True)
    st.markdown("""<div class="notice">⚠️ Group L Goal Difference column was NaN in source file — pipeline computed it
    from Goals Scored minus Goals Conceded automatically. Form is on 0-10 scale — normalized to 0-100.
    Predictions derived from actual match data in group_l_matches_history.xlsx.</div>""",unsafe_allow_html=True)

st.markdown("""<br>
<div style="text-align:center;font-size:11px;color:#374151;padding:16px 0;border-top:0.5px solid #1f2937;">
  ⚽ FIFA World Cup 2026 · Group L Predictor · Data from group_l_matches_history.xlsx &nbsp;|&nbsp; For fans, by fans
</div>""",unsafe_allow_html=True)
