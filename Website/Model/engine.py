import streamlit as st
import sys
import os

# Dynamically force Python to see modules installed in the main Website directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import random

# --- PREMIUM DARK GRID UI THEME ENGINE ---
st.markdown("""
<style>
/* Main Background & Text Color */
.stApp {
background-color: #0d0e12 !important;
color: #f8fafc !important;
}

/* Header & Title Customization */
h1, h2, h3 {
color: #ffffff !important;
font-family: 'Inter', sans-serif;
font-weight: 800 !important;
letter-spacing: -0.5px;
}

/* Clean Cards for Profiles and Calculators */
div[data-testid="stVerticalBlock"] > div {
background-color: #161920;
border: 1px solid #242936;
border-radius: 12px;
padding: 20px;
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
}

/* Input Boxes & Dropdowns */
div[data-baseweb="select"], div[data-baseweb="input"] {
background-color: #1e2330 !important;
border: 1px solid #333b4f !important;
border-radius: 8px !important;
}

/* Interactive Metric Blocks */
div[data-testid="stMetricValue"] {
color: #10b981 !important; /* Premium Sportsbook Neon Green */
font-size: 32px !important;
font-weight: 700 !important;
}

div[data-testid="stMetricLabel"] {
color: #94a3b8 !important; /* Soft muted gray text */
font-size: 14px !important;
text-transform: uppercase;
letter-spacing: 0.5px;
}
</style>
""", unsafe_allow_html=True)

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

# # 4. Live MLB Automated Feed Engine with 24-Hour Cache Control
@st.cache_data(ttl=86400) # Automatically updates every 24 hours on autopilot
def load_automated_league_stats():
    import statsapi
    import random
leaderboard_rows = []

# Pulls the top 150 current active league players via live data stream
live_api_data = statsapi.league_leader_data('onBasePlusSlugging', season=2025, limit=150)

for row in live_api_data:
    player_name = row
    team_name = row
    ops_value = float(row) if row else 0.0

# Temporary dynamic metrics until we link the deeper API sub-arrays
hr_value = random.randint(15, 45)
rbi_value = random.randint(65, 110)
avg_value = round(random.uniform(0.240, 0.320), 3)
kuzi_calc = (ops_value * 1000) + (hr_value * 1.5)

leaderboard_rows.append({
"Player Name": player_name,
"Position": team_name,
"HR": hr_value,
"RBI": rbi_value,
"AVG": avg_value,
"OPS": ops_value,
"KUZI Rating": kuzi_calc
    })
return pd.DataFrame(leaderboard_rows)

# Execute the background automation system
df_leaderboard = load_automated_league_stats()
LOCAL_TEAM_DATABASE = {
"New York Yankees": {"offense_rating": 8.8, "defense_rating": 7.9},
"Los Angeles Dodgers": {"offense_rating": 9.2, "defense_rating": 8.1},
"Houston Astros": {"offense_rating": 8.4, "defense_rating": 8.3},
"Atlanta Braves": {"offense_rating": 8.1, "defense_rating": 8.6},
"Baltimore Orioles": {"offense_rating": 8.6, "defense_rating": 7.8},
"Philadelphia Phillies": {"offense_rating": 8.5, "defense_rating": 8.4}
}

# --- SECTION 1: MASTER CONTROLLER SELECT BOX ---
st.markdown("### 🎯 Global Profile Core Selector")
# Use the live database names once they are loaded below
sorted_names = ["Aaron Judge"] # Temporary placeholder until data loads
selected_player = st.selectbox("Choose a Player to Analyze and Lock Into the System Grid:", options=sorted_names)

# --- PROCESS AUTOMATIC LEADERBOARD RATING MATRICES (FLATTENED ONE-LINER BLOCK) ---
leaderboard_rows = []
# Pull the top 200 players across the league sorted by OPS metrics
import statsapi
live_api_data = statsapi.league_leader_data('onBasePlusSlugging', season=2025, limit=200)
for row in live_api_data:
    # The API returns data as a list: [rank, player_name, team_name, stat_value]
    player_name = row[1]
    team_name = row[2]
    ops_value = float(row[3])

    # Dynamically compute your KUZI Rating right here using live metrics!
    kuzi_calc = ops_value * 1000

    leaderboard_rows.append({
    "Player Name": player_name,
    "Position": team_name, # Temporary placeholder using team name text
    "HR": 0,
    "RBI": 0,
    "AVG": 0.000,
    "OPS": ops_value,
    "KUZI Rating": kuzi_calc
    })


df_leaderboard = pd.DataFrame(leaderboard_rows).sort_values(by="KUZI Rating", ascending=False).reset_index(drop=True)
df_leaderboard.index += 1

# --- SECTION 2: GLOBAL LEADERBOARD DISPLAY ---
st.markdown("### 🏆 Global KUZI Index Leaderboard")
st.dataframe(df_leaderboard, use_container_width=True)
st.markdown("---")

# --- SECTION 3: PLAYER DEEP ANALYSIS PROFILE ---
if   selected_player:
    # Look up the selected player's row inside your live data table
    player_match = df_leaderboard[df_leaderboard["Player Name"] == selected_player]
    player_data = player_match.iloc[0] if not player_match.empty else None

st.markdown(f"### 🔍 Deep Analysis Profile Card: {selected_player}")
m1, m2 = st.columns(2)
st.markdown(f"**Team / Assigned Position:*** {player_data['Position']}")
m2.metric("Batting Average (AVG)", f"{player_data['AVG']:.3f}" if isinstance(player_data['AVG'], float) else str(player_data['AVG']))
st.markdown("---")
m3, m4 = st.columns(2)
m3.metric("On-Base Plus Slugging (OPS)", f"{player_data['OPS']:.3f}" if isinstance(player_data['OPS'], float) else str(player_data['OPS']))
m4.metric("Production Output Volume", f"{player_data['HR']} HR / {player_data['RBI']} RBI")

ops_val = float(player_data["OPS"])
avg_val = float(player_data["AVG"])
kuzi_score = round(float(player_data["KUZI Rating"]), 1)
badge_color = '#ef4444' if kuzi_score >= 750 else '#1e3a8a'
status_tag = "ELITE LAYER" if kuzi_score >= 750 else "STANDARD LAYER"
st.markdown(f"""<div class="kuzi-badge-box" style="border-left-color: {badge_color};"><div style="font-size:0.9em; color:#9ca3af; text-transform:uppercase;">KUZI RATING SCORE</div><div style="font-size:2.8em; font-weight:900; color:#ffffff; line-height:1em; margin-top:5px;">{kuzi_score}</div><div style="font-size:1.1em; color:#ffffff; margin-top:10px;">Classification Status: {status_tag}</div></div>""", unsafe_allow_html=True)
if kuzi_score >= 750:
    st.balloons()

st.markdown("---")

# --- SECTION 4: PROBABILITY BETTING CALCULATOR PANEL ---
st.markdown("### 🧮 Implied Probability Valuation Calculator")
odds_input = st.number_input("Enter American Moneyline Odds lines for reference:", value=-110, step=5)
if odds_input < 0:
  implied_prob = (-odds_input) / (-odds_input + 100)
else:
  implied_prob = 100 / (odds_input + 100)
pct_format = round(implied_prob * 100, 1)

st.markdown(f"""<div class="calc-container"><div style="font-size:0.9em; color:#9ca3af; text-transform:uppercase;">Break-Even Win Probability Required</div><div style="font-size:3em; font-weight:900; color:#38bdf8; margin-top:5px;">{pct_format}%</div></div>""", unsafe_allow_html=True)
