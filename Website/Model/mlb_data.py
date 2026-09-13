import streamlit as st
import pandas as pd
import plotly.express as px

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
    </style>
""", unsafe_allow_html=True)

# 3. Render Top Banner
st.markdown("""
    <div class="banner-container">
        <h1 class="banner-title">⚾ KUZI SPORTS ANALYTICS ENGINE</h1>
        <div class="banner-subtitle">Proprietary Player Valuation & Performance Indexing</div>
    </div>
""", unsafe_allow_html=True)

# 4. Core Local Database Asset Registry
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

# Convert data and rank by rating from high to low
df_leaderboard = pd.DataFrame(leaderboard_rows).sort_values(by="KUZI Rating", ascending=False).reset_index(drop=True)
df_leaderboard.index += 1 # Set index rankings to start cleanly from 1

# Split visual layout into Leaderboard Table and Chart Matrix side-by-side
col_table, col_chart = st.columns([1, 1])

with col_table:
    st.markdown("### 🏆 Global KUZI Index Leaderboard")
    st.dataframe(df_leaderboard, use_container_width=True)

with col_chart:
    st.markdown("### 📊 Valuation Index Variance Comparison")
    # Build an interactive Plotly bar chart matrix matching the dashboard palette
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
        yaxis={"categoryorder": "total ascending"}
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 5. Interactive Deep Search Bar Input Field
player_query = st.text_input("🔍 Select or Enter MLB Player Name for Deep Analysis Profile:", value="Aaron Judge")

if player_query:
    lookup_key = player_query.strip().lower()
    
    if lookup_key in LOCAL_MLB_DATABASE:
        player_data = LOCAL_MLB_DATABASE[lookup_key]
        
        st.markdown(f"<div style='padding:12px; background-color:#1e3a8a; border-radius:8px; color:#f8fafc; font-weight:600; margin-bottom:20px;'>📊 Analysis Profile: {player_query.title()} (ID: {player_data['id']}) | Position: {player_data['pos']}</div>", unsafe_allow_html=True)
        
        # Render Metrics Grid
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Games Played", player_data["games"])
        m2.metric("Batting Average", player_data["avg"])
        m3.metric("On-Base Plus Slugging (OPS)", player_data["ops"])
        m4.metric("Production Output", f"{player_data['hr']} HR / {player_data['rbi']} RBI")
        
        # Recalculate deep score representation badge
        ops_val = float(player_data["ops"])
        avg_val = float(player_data["avg"])
        kuzi_score = round((ops_val * 500) + (avg_val * 1000) + (player_data["hr"] * 3) + (player_data["rbi"] * 1.5), 1)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🏆 Analytics Index Summary")
        
        status_tag = "<span style='color:#ef4444; font-weight:800;'>ELITE LEVEL PERFORMANCE</span>" if kuzi_score >= 750 else "<span style='color:#38bdf8; font-weight:800;'>STANDARD PRODUCTION COMPONENT</span>"
        badge_color = '#ef4444' if kuzi_score >= 750 else '#1e3a8a'
        
        st.markdown(f"""
            <div class="kuzi-badge-box" style="border-left-color: {badge_color};">
                <div style="font-size:0.9em; color:#9ca3af; text-transform:uppercase;">KUZI RATING SCORE</div>
                <div style="font-size:3.2em; font-weight:900; color:#ffffff; line-height:1em; margin-top:5px;">{kuzi_score}</div>
                <div style="font-size:1.2em; color:#ffffff; margin-top:10px;">System Classification: {status_tag}</div>
            </div>
        """, unsafe_allow_html=True)
        
        if kuzi_score >= 750:
            st.balloons()
    else:
        st.warning(f"⚠️ Profile '{player_query}' is currently unindexed in the sandbox core registry layer.")
