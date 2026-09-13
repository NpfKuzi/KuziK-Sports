import streamlit as st
import pandas as pd
import plotly.express as px
import random

# 1. Page Configuration Setup
st.set_page_config(page_title="KUZI Sports Analytics", page_icon="⚾", layout="wide")

# 2. Premium Professional UI Theme CSS Styling
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

# 3. Render Top Banner
st.markdown("""
    <div class="banner-container">
        <h1 class="banner-title">⚾ KUZI SPORTS ANALYTICS ENGINE</h1>
        <div class="banner-subtitle">Proprietary Player Valuation & Performance Indexing</div>
    </div>
""", unsafe_allow_html=True)

# 4. Master Local Databases (Players & Teams Matrices)
LOCAL_MLB_DATABASE = {
    "aaron judge": {"id": "592450", "pos": "Outfielder", "games": 158, "avg": ".322", "ops": "1.159", "hr": 58, "rbi": 144},
    "shohei ohtani": {"id": "660271", "pos": "Designated Hitter", "games": 159, "avg": ".310", "ops": "1.036", "hr": 54, "rbi": 130},
    "mookie betts": {"id": "605141", "pos": "Shortstop/Outfield", "games": 116, "avg": ".289", "ops": ".863", "hr": 19, "rbi": 75},
    "juan soto": {"id": "665742", "pos": "Outfielder", "games": 157, "avg": ".288", "ops": ".989", "hr": 41, "rbi": 109},
    "bryce harper": {"id": "547180", "pos": "First Baseman", "games": 145, "avg": ".285", "ops": ".898", "hr": 30, "rbi": 87},
    "bobby witt jr.": {"id": "677951", "pos": "Shortstop", "games": 161, "avg": ".332", "ops": ".977", "hr": 32, "rbi": 109},
    "ronald acuna jr.": {"id": "660670", "pos": "Outfielder", "games": 159, "avg": ".337", "ops": "1.012", "hr": 41, "rbi": 106},
    "freddie freeman": {"id": "518692", "pos": "First Baseman", "games": 147, "avg": ".282", "ops": ".854", "hr": 22, "rbi": 89}
}

LOCAL_TEAM_DATABASE = {
    "New York Yankees": {"offense_rating": 8.8, "defense_rating": 7.9, "color": "#0C2340"},
    "Los Angeles Dodgers": {"offense_rating": 9.2, "defense_rating": 8.1, "color": "#005A9C"},
    "Houston Astros": {"offense_rating": 8.4, "defense_rating": 8.3, "color": "#EB6E1F"},
    "Atlanta Braves": {"offense_rating": 8.1, "defense_rating": 8.6, "color": "#CE1141"},
    "Baltimore Orioles": {"offense_rating": 8.6, "defense_rating": 7.8, "color": "#DF4601"},
    "Philadelphia Phillies": {"offense_rating": 8.5, "defense_rating": 8.4, "color": "#E81828"}
}

# --- SIDEBAR INTERACTIVE MODULES ---
st.sidebar.header("🕹️ KUZI Matchup Simulator")
st.sidebar.write("Project outcomes between competing organizations.")

away_team_sel = st.sidebar.selectbox("Select Away Team:", options=list(LOCAL_TEAM_DATABASE.keys()), index=0)
home_team_sel = st.sidebar.selectbox("Select Home Team:", options=list(LOCAL_TEAM_DATABASE.keys()), index=1)

st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Custom Model Weighting")
st.sidebar.write("Adjust parameters to shift simulation weight distribution.")

defense_weight = st.sidebar.slider("Defense/Pitching Weight", min_value=10, max_value=90, value=40, step=5) / 100.0
home_field_edge = st.sidebar.slider("Home Field Advantage Run Edge", min_value=0.0, max_value=1.5, value=0.3, step=0.1)

offense_weight = 1.0 - defense_weight

st.sidebar.markdown("---")
sim_clicked = st.sidebar.button("⚡ Run Empirical Simulation")

# --- PROCESS AUTOMATIC LEADERBOARD RATING MATRICES ---
leaderboard_rows = []
for name, data in LOCAL_MLB_DATABASE.items():
    ops_v = float(data["ops"])
    avg_v = float(data["avg"])
    calc_score = round((ops_v * 500) + (avg_v * 1000) + (data["hr"] * 3) + (data["rbi"] * 1.5), 1)
    leaderboard_rows.append({
        "Player Name": name.title(),
        "Position": data["pos"],
        "HR": data["hr"],
        "RBI": data["rbi"],
        "AVG": data["avg"],
        "OPS": data["ops"],
        "KUZI Rating": calc_score
    })

df_leaderboard = pd.DataFrame(leaderboard_rows).sort_values(by="KUZI Rating", ascending=False).reset_index(drop=True)
df_leaderboard.index += 1 

# --- CONDITIONAL LAYOUT SWITCH IF SIMULATOR RUNS ---
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

# Split visual layout into Leaderboard Table and Chart Matrix side-by-side
col_table, col_chart = st.columns(2)

with col_table:
    st.markdown("### 🏆 Global KUZI Index Leaderboard")
    st.dataframe(df_leaderboard, use_container_width=True)

with col_chart:
    st.markdown("### 📊 Valuation Index Variance Comparison")
    fig = px.bar(
        df_leaderboard, 
        x="KUZI Rating", 
        y="Player Name", 
        orientation="h",
        color="KUZI Rating",
        color_continuous_scale=["#1e3a8a", "#7f1d1d"]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ffffff",
        yaxis={"categoryorder": "total ascending"},
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Interactive Deep Search Bar Input Field & Betting Analytics Engine Splits
c_left, c_right = st.columns(2)

with c_left:
    st.markdown("### 🔍 Player Deep Analysis Profile")
    player_query = st.text_input("Select or Enter MLB Player Name:", value="Aaron Judge")

    if player_query:
        lookup_key = player_query.strip().lower()
        
        if lookup_key in LOCAL_MLB_DATABASE:
            player_data = LOCAL_MLB_DATABASE[lookup_key]
            
            st.markdown(f"<div style='padding:12px; background-color:#1e3a8a; border-radius:8px; color:#f8fafc; font-weight:600; margin-bottom:20px;'>📊 Asset Analysis: {player_query.title()}</div>", unsafe_allow_html=True)
            
            m1, m2 = st.columns(2)
            m1.metric("Games / Position", f"{player_data['games']} G | {player_data['pos']}")
            m2.metric("Batting Average", player_data["avg"])
            
            m3, m4 = st.columns(2)
            m3.metric("On-Base Plus Slugging (OPS)", player_data["ops"])
            m4.metric("Production Output", f"{player_data['hr']} HR / {player_data['rbi']} RBI")
            
            ops_val = float(player_data["ops"])
            avg_val = float(player_data["avg"])
            kuzi_score = round((ops_val * 500) + (avg_val * 1000) + (player_data["hr"] * 3) + (player_data["rbi"] * 1.5), 1)
            
            status_tag = "<span style='color:#ef4444; font-weight:800;'>ELITE LAYER</span>" if kuzi_score >= 750 else "<span style='color:#38bdf8; font-weight:800;'>STANDARD PRODUCTION</span>"
            badge_color = '#ef4444' if kuzi_score >= 750 else '#1e3a8a'
            
            st.markdown(f"""
                <div class="kuzi-badge-box" style="border-left-color: {badge_color};">
                    <div style="font-size:0.9em; color:#9ca3af; text-transform:uppercase;">KUZI RATING SCORE</div>
                    <div style="font-size:2.8em; font-weight:900; color:#ffffff; line-height:1em; margin-top:5px;">{kuzi_score}</div>
                    <div style="font-size:1.1em; color:#ffffff; margin-top:10px;">Classification: {status_tag}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ Profile '{player_query}' is currently unindexed.")
