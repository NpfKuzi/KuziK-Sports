import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="KUZI Sports Analytics", page_icon="⚾", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; font-family: 'Segoe UI', sans-serif; }
    .banner-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #7f1d1d 100%);
        padding: 30px; border-radius: 12px; text-align: center; margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .banner-title { color: #ffffff !important; font-size: 2.5em !important; font-weight: 800 !important; margin: 0; }
    .banner-subtitle { color: #cbd5e1 !important; font-size: 1.1em !important; margin-top: 5px; }
    div[data-testid="stMetricValue"] { font-size: 2.2em !important; font-weight: 700 !important; color: #38bdf8 !important; }
    div[data-testid="stMetricLabel"] { font-size: 0.95em !important; color: #9ca3af !important; text-transform: uppercase; }
    .kuzi-badge-box { background: #111827; border-left: 5px solid #ef4444; padding: 20px; border-radius: 8px; margin-top: 15px; }
    .calc-container { background-color: #1f2937; padding: 20px; border-radius: 10px; border-top: 4px solid #38bdf8; }
    .sim-container { background-color: #111827; padding: 20px; border-radius: 10px; border: 1px solid #374151; margin-top: 10px;}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="banner-container">
        <h1 class="banner-title">⚾ KUZI SPORTS ANALYTICS ENGINE</h1>
        <div class="banner-subtitle">Proprietary Player Valuation & Performance Indexing</div>
    </div>
""", unsafe_allow_html=True)

LOCAL_MLB_DATABASE = {
    "aaron judge": {"id": "592450", "pos": "Outfielder", "games": 158, "avg": ".322", "ops": "1.159", "hr": 58, "rbi": 144},
    "shohei ohtani": {"id": "660271", "pos": "Designated Hitter", "games": 159, "avg": ".310", "ops": "1.036", "hr": 54, "rbi": 130},
    "juan soto": {"id": "665742", "pos": "Outfielder", "games": 157, "avg": ".288", "ops": ".989", "hr": 41, "rbi": 109},
    "bobby witt jr": {"id": "677951", "pos": "Shortstop", "games": 161, "avg": ".332", "ops": ".977", "hr": 32, "rbi": 109},
    "mookie betts": {"id": "605141", "pos": "Shortstop", "games": 116, "avg": ".289", "ops": ".863", "hr": 19, "rbi": 75},
    "bryce harper": {"id": "547180", "pos": "First Baseman", "games": 145, "avg": ".285", "ops": ".898", "hr": 30, "rbi": 87},
    "ronald acuna jr": {"id": "660670", "pos": "Outfielder", "games": 159, "avg": ".337", "ops": "1.012", "hr": 41, "rbi": 106},
    "freddie freeman": {"id": "518692", "pos": "First Baseman", "games": 147, "avg": ".282", "ops": ".854", "hr": 22, "rbi": 89},
    "kyle schwarber": {"id": "656941", "pos": "Designated Hitter", "games": 142, "avg": ".238", "ops": ".890", "hr": 44, "rbi": 92},
    "pete crow armstrong": {"id": "691718", "pos": "Center Fielder", "games": 149, "avg": ".279", "ops": ".875", "hr": 41, "rbi": 98},
    "yordan alvarez": {"id": "670541", "pos": "Outfielder", "games": 145, "avg": ".310", "ops": ".955", "hr": 38, "rbi": 96},
    "matt olson": {"id": "621566", "pos": "First Baseman", "games": 148, "avg": ".249", "ops": ".830", "hr": 38, "rbi": 82},
    "junior caminero": {"id": "691406", "pos": "Third Baseman", "games": 147, "avg": ".279", "ops": ".860", "hr": 40, "rbi": 95},
    "pete alonso": {"id": "624413", "pos": "First Baseman", "games": 149, "avg": ".266", "ops": ".850", "hr": 35, "rbi": 99},
    "rafael devers": {"id": "646240", "pos": "Third Baseman", "games": 148, "avg": ".258", "ops": ".870", "hr": 37, "rbi": 98},
    "james wood": {"id": "695578", "pos": "Right Fielder", "games": 123, "avg": ".266", "ops": ".845", "hr": 30, "rbi": 75},
    "vladimir guerrero jr": {"id": "665489", "pos": "First Baseman", "games": 159, "avg": ".323", "ops": ".940", "hr": 30, "rbi": 103},
    "gunnar henderson": {"id": "683002", "pos": "Shortstop", "games": 156, "avg": ".281", "ops": ".895", "hr": 37, "rbi": 92},
    "jose ramirez": {"id": "608070", "pos": "Third Baseman", "games": 158, "avg": ".279", "ops": ".865", "hr": 39, "rbi": 118},
    "marcell ozuna": {"id": "542303", "pos": "Designated Hitter", "games": 155, "avg": ".302", "ops": ".925", "hr": 39, "rbi": 104},
    "corey seager": {"id": "608369", "pos": "Shortstop", "games": 123, "avg": ".278", "ops": ".860", "hr": 30, "rbi": 74},
    "francisco lindor": {"id": "596019", "pos": "Shortstop", "games": 152, "avg": ".273", "ops": ".840", "hr": 31, "rbi": 86},
    "elly de la cruz": {"id": "682829", "pos": "Shortstop", "games": 160, "avg": ".259", "ops": ".805", "hr": 25, "rbi": 71},
    "will smith": {"id": "669221", "pos": "Catcher", "games": 128, "avg": ".248", "ops": ".770", "hr": 20, "rbi": 75},
    "corbin carroll": {"id": "672695", "pos": "Outfielder", "games": 155, "avg": ".231", "ops": ".750", "hr": 22, "rbi": 68},
    "trea turner": {"id": "607208", "pos": "Shortstop", "games": 115, "avg": ".295", "ops": ".815", "hr": 21, "rbi": 62},
    "manny machado": {"id": "592518", "pos": "Third Baseman", "games": 152, "avg": ".275", "ops": ".825", "hr": 29, "rbi": 105},
    "william contreras": {"id": "661388", "pos": "Catcher", "games": 155, "avg": ".281", "ops": ".820", "hr": 23, "rbi": 92},
    "adley rutschman": {"id": "668939", "pos": "Catcher", "games": 148, "avg": ".250", "ops": ".760", "hr": 19, "rbi": 79},
    "riley greene": {"id": "682985", "pos": "Outfielder", "games": 135, "avg": ".262", "ops": ".825", "hr": 24, "rbi": 74}
}

LOCAL_TEAM_DATABASE = {
    "New York Yankees": {"offense_rating": 8.8, "defense_rating": 7.9, "color": "#0C2340"},
    "Los Angeles Dodgers": {"offense_rating": 9.2, "defense_rating": 8.1, "color": "#005A9C"},
    "Houston Astros": {"offense_rating": 8.4, "defense_rating": 8.3, "color": "#EB6E1F"},
    "Atlanta Braves": {"offense_rating": 8.1, "defense_rating": 8.6, "color": "#CE1141"},
    "Baltimore Orioles": {"offense_rating": 8.6, "defense_rating": 7.8, "color": "#DF4601"},
    "Philadelphia Phillies": {"offense_rating": 8.5, "defense_rating": 8.4, "color": "#E81828"}
}

st.sidebar.header("🕹️ KUZI Matchup Simulator")
st.sidebar.write("Project outcomes between competing organizations.")
away_team_sel = st.sidebar.selectbox("Select Away Team:", options=list(LOCAL_TEAM_DATABASE.keys()), index=0)
home_team_sel = st.sidebar.selectbox("Select Home Team:", options=list(LOCAL_TEAM_DATABASE.keys()), index=1)
st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Custom Model Weighting")
defense_weight = st.sidebar.slider("Defense/Pitching Weight", min_value=10, max_value=90, value=40, step=5) / 100.0
home_field_edge = st.sidebar.slider("Home Field Advantage Run Edge", min_value=0.0, max_value=1.5, value=0.3, step=0.1)
offense_weight = 1.0 - defense_weight
st.sidebar.markdown("---")
sim_clicked = st.sidebar.button("⚡ Run Empirical Simulation")

leaderboard_rows = []
for name, data in LOCAL_MLB_DATABASE.items():
    ops_v = float(data["ops"])
    avg_v = float(data["avg"])
    calc_score = round((ops_v * 500) + (avg_v * 1000) + (int(data["hr"]) * 3) + (int(data["rbi"]) * 1.5), 1)
    leaderboard_rows.append({
        "Player Name": name.title(),
        "Position": data["pos"],
        "HR": int(data["hr"]),
        "RBI": int(data["rbi"]),
        "AVG": data["avg"],
        "OPS": data["ops"],
        "KUZI Rating": calc_score
    })

df_leaderboard = pd.DataFrame(leaderboard_rows).sort_values(by="KUZI Rating", ascending=False).reset_index(drop=True)
df_leaderboard.index += 1 

if sim_clicked:
    st.markdown(f"### 🏟️ Simulation Projection Report: {away_team_sel} vs. {home_team_sel}")
    t1 = LOCAL_TEAM_DATABASE[away_team_sel]
    t2 = LOCAL_TEAM_DATABASE[home_team_sel]
    random.seed(len(away_team_sel) + len(home_team_sel))
    away_base_runs = (t1["offense_rating"] * offense_weight) + ((10 - t2["defense_rating"]) * defense_weight)
    home_base_runs = (t2["offense_rating"] * offense_weight) + ((10 - t1["defense_rating"]) * defense_weight) + home_field_edge
    away_final_score = max(0, int(round(random.gauss(away_base_runs, 1.8))))
    home_final_score = max(0, int(round(random.gauss(home_base_runs, 1.8))))
    if away_final_score == home_final_score:
        home_final_score += 1 
    home_win_prob = round((home_base_runs / (away_base_runs + home_base_runs)) * 100, 1)
    away_win_prob = round(100 - home_win_prob, 1)
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric(f"🏃 {away_team_sel} (Away)", away_final_score, f"Win Prob: {away_win_prob}%")
    sc2.markdown("<h1 style='text-align: center; color: #9ca3af;'>FINAL SCORE</h1>", unsafe_allow_html=True)
    sc3.metric(f"🏠 {home_team_sel} (Home)", home_final_score, f"Win Prob: {home_win_prob}%")
    winner = home_team_sel if home_final_score > away_final_score else away_team_sel
    st.markdown(f"""
        <div class="sim-container" style="border-left: 5px solid #38bdf8;">
            🎉 <b>Simulation Verdict:</b> The KUZI Engine projects <b>{winner}</b> to win using custom model parameters (<b>{int(offense_weight*100)}% Offense / {int(defense_weight*100)}% Defense</b> weighting mix). 
            Expected total run value is <b>{away_final_score + home_final_score} runs</b>.
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

st.markdown("### 🏆 Global KUZI Index Leaderboard")
st.dataframe(df_leaderboard, use_container_width=True)
st.markdown("---")

st.markdown("### 🔍 Player Deep Analysis Profile")
sorted_names = sorted([n.title() for n in LOCAL_MLB_DATABASE.keys()])
selected_player = st.selectbox("Select Target Athlete Profile:", options=sorted_names, index=sorted_names.index("Aaron Judge"))

if selected_player:
    lookup_key = selected_player.lower()
    player_data = LOCAL_MLB_DATABASE[lookup_key]
    st.markdown(f"<div style='padding:12px; background-color:#1e3a8a; border-radius:8px; color:#f8fafc; font-weight:600; margin-bottom:20px;'>📊 Asset Analysis: {selected_player}</div>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
