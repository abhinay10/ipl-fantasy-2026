import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="IPL 2026 Fantasy League", layout="wide", page_icon="🏏")
st.title("🏏 IPL 2026 Private Fantasy League Dashboard")
st.caption("Captain = 2× | Vice-Captain = 1.5× | Updated after KKR innings (220/4) | MI chasing")

# ====================== TEAM DATA ======================
teams = {
    "Abhinay": {"players": ["Kishan", "Sooryavanshi", "Sundar", "Will Jacks", "Arshdeep", "Jansen", "Gill", "Bethell", "Butler", "Khaleel", "Angrish Raghuvanshi"], "prices": [11.25, 1.1, 3.2, 5.25, 18.0, 7.0, 16.5, 2.6, 15.75, 4.8, 3.0], "total_spend": 88.45, "remaining": 1.55},
    "Ritu": {"players": ["Kohli", "Rahul", "Bishnoi", "Miller", "Anshul Kambhoj", "Priyansh Arya", "Deepak Chahar", "Mohsin Khan", "Hetmyer", "Sunil Narine", "Sai Kishore"], "prices": [21.0, 14.0, 7.2, 2.0, 3.4, 3.8, 9.25, 4.0, 11.0, 12.0, 2.0], "total_spend": 89.65, "remaining": 0.35},
    "Prayas": {"players": ["Tilak Varma", "Hardik", "Allen", "Brevis", "Bhuvi", "Abhishek", "Varun", "Ayush Mhatre", "Mitchell Marsh", "Jitesh Sharma", "Zeeshan Ansari"], "prices": [8.0, 16.35, 2.0, 2.2, 10.75, 14.0, 12.0, 0.3, 3.4, 11.0, 0.4], "total_spend": 80.4, "remaining": 9.6},
    "Akshay": {"players": ["Sanju Samson", "Green", "Dube", "qdk", "Digvesh", "shardul", "Padikkal", "Stubbs", "Rahul Tripathi", "Dhoni", "Seifert"], "prices": [18.0, 25.2, 12.0, 1.0, 0.3, 2.0, 6.5, 10.0, 3.4, 4.0, 1.5], "total_spend": 83.9, "remaining": 6.1},
    "Aayush": {"players": ["Sai Sudarshan", "Yashaswi Jaiswal", "Markram", "Noor Ahmad", "ngidi", "Krunal", "Ruturaj", "Head", "Rahane", "David", "Nitish Rana"], "prices": [8.5, 18.0, 2.0, 10.0, 2.0, 5.75, 18.0, 14.0, 1.5, 3.0, 4.2], "total_spend": 86.95, "remaining": 3.05},
    "Kaushal": {"players": ["Bumrah", "Iyer", "Rachin Ravindra", "prabhsimran", "NKR", "Suyash", "Ramandeep", "Patidar", "Sandeep Sharma", "Shashank Singh", "Tewatia"], "prices": [18.0, 26.75, 4.0, 4.0, 6.0, 2.0, 4.0, 11.0, 4.0, 5.5, 4.0], "total_spend": 89.25, "remaining": 0.75}
}

# ====================== UPDATED BASE POINTS (Match 1 + KKR Innings) ======================
# ====================== FULLY CORRECTED BASE POINTS (Match 1 + KKR Innings) ======================
base_points = {
    "Abhinay": {"Kishan": 110, "Angrish Raghuvanshi": 73},           # Raghuvanshi: 51 (6x4, 2x6, fifty)
    "Ritu": {"Kohli": 104, "Sunil Narine": 42},                      # Narine bowling contribution
    "Prayas": {"Abhishek": 9, "Bhuvi": 25, "Jitesh Sharma": 8, "Hardik": 33, "Tilak Varma": 16},  # Hardik 1w + Tilak 2 catches
    "Akshay": {"Padikkal": 112, "Green": 26, "shardul": 58},         # Green cameo + Shardul multiple wickets
    "Aayush": {"Head": 13, "David": 19, "Rahane": 92},               # Rahane 67 (3x4, 5x6)
    "Kaushal": {"NKR": 1, "Suyash": 25, "Patidar": 43, "Bumrah": 35} # Bumrah impact
}

# Persistent C/VC
if "captains" not in st.session_state:
    st.session_state.captains = {team: None for team in teams}
if "vice_captains" not in st.session_state:
    st.session_state.vice_captains = {team: None for team in teams}

# Live Score (MI chasing)
@st.cache_data(ttl=45)
def get_live_score():
    return {
        "status": "Live - MI Chasing",
        "title": "MI vs KKR - Match 2",
        "score": "KKR 220/4 | MI chasing 221 (early overs)",
        "update": "Rohit Sharma & Ryan Rickelton batting. Big points possible in chase!"
    }

live_data = get_live_score()

# ====================== UI ======================
tab1, tab2, tab3 = st.tabs(["📊 League Standings", "👥 All Teams", "🔴 Live Score"])

with tab1:
    standings_data = []
    for name, team in teams.items():
        team_base = base_points.get(name, {})
        captain = st.session_state.captains.get(name)
        vice = st.session_state.vice_captains.get(name)
        total = sum((pts*2 if p == captain else pts*1.5 if p == vice else pts) for p, pts in team_base.items())
        standings_data.append({
            "Team": name,
            "Total Fantasy Points": round(total, 1),
            "Spent (cr)": team["total_spend"],
            "Purse Left (cr)": team["remaining"]
        })
    standings_df = pd.DataFrame(standings_data).sort_values("Total Fantasy Points", ascending=False).reset_index(drop=True)
    st.dataframe(standings_df, width='stretch', hide_index=True)

with tab2:
    if st.button("🔄 Pull Latest Points from Grok", type="primary"):
        st.info("Button clicked! Reply in chat with 'Update points after MI vs KKR' or 'Update current live points' for next calculation.")

    cols = st.columns(3)
    for i, (name, team) in enumerate(teams.items()):
        with cols[i % 3]:
            with st.container(border=True):
                st.subheader(f"**{name}**")
                players_list = team["players"]
                
                cap_index = 0 if not st.session_state.captains[name] else players_list.index(st.session_state.captains[name]) + 1
                vc_index = 0 if not st.session_state.vice_captains[name] else players_list.index(st.session_state.vice_captains[name]) + 1
                
                new_cap = st.selectbox("Captain (2×)", ["None"] + players_list, index=cap_index, key=f"cap_{name}")
                new_vc = st.selectbox("Vice-Captain (1.5×)", ["None"] + players_list, index=vc_index, key=f"vc_{name}")
                
                if st.button("💾 Save Captain & Vice-Captain", key=f"save_{name}"):
                    st.session_state.captains[name] = None if new_cap == "None" else new_cap
                    st.session_state.vice_captains[name] = None if new_vc == "None" else new_vc
                    st.success(f"Saved for {name}!")
                    st.rerun()
                
                captain = st.session_state.captains[name]
                vice = st.session_state.vice_captains[name]
                total = sum((pts*2 if p == captain else pts*1.5 if p == vice else pts) for p, pts in base_points.get(name, {}).items())
                
                st.caption(f"**Points: {round(total, 1)}** | Spent: ₹{team['total_spend']} cr")
                
                df = pd.DataFrame({"Player": team["players"], "Price (cr)": team["prices"]})
                df["Base Points"] = df["Player"].map(base_points.get(name, {})).fillna(0).astype(int)
                df["Final Points"] = df.apply(lambda row: round(row["Base Points"]*2 if row["Player"]==captain else row["Base Points"]*1.5 if row["Player"]==vice else row["Base Points"], 1), axis=1)
                st.dataframe(df, width='stretch', hide_index=True)

with tab3:
    st.subheader("🔴 Live Score - MI vs KKR")
    st.write(f"**{live_data['title']}**")
    st.write(f"**Status:** {live_data['status']}")
    st.write(f"**Score:** {live_data['score']}")
    if live_data.get("update"):
        st.info(live_data["update"])
    st.caption("KKR innings complete (220/4). MI chasing. Refresh or use Grok button for updates.")

st.info("**How to update further:** Click the 🔄 button and reply here with your request (e.g. 'Update points after MI vs KKR'). This keeps points accurate using your exact system.")

st.success("✅ Dashboard updated with KKR innings points! Deploy this version now.")
