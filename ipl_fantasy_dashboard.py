import streamlit as st
import pandas as pd
import matplotlib

st.set_page_config(page_title="IPL 2026 Fantasy League", layout="wide", page_icon="🏏")
st.title("🏏 IPL 2026 Private Fantasy League Dashboard")
st.caption("Captain = 2× points | Vice-Captain = 1.5× points | Base: Runs +1, Boundary +1, Six +2, 30-run bonus +4, 50 +8, 100 +16 | Wicket +25, LBW/Bowled +8, Maiden +12, 3W +4, 4W +8, 5W +12 | Catch +8, Stumping +12, Run-out +6")

# ====================== TEAM DATA ======================
teams = {
    "Abhinay": {
        "players": ["Kishan", "Sooryavanshi", "Sundar", "Will Jacks", "Arshdeep", "Jansen", "Gill", "Bethell", "Butler", "Khaleel", "Angrish Raghuvanshi"],
        "prices": [11.25, 1.1, 3.2, 5.25, 18.0, 7.0, 16.5, 2.6, 15.75, 4.8, 3.0],
        "total_spend": 88.45, "remaining": 1.55
    },
    "Ritu": {
        "players": ["Kohli", "Rahul", "Bishnoi", "Miller", "Anshul Kambhoj", "Priyansh Arya", "Deepak Chahar", "Mohsin Khan", "Hetmyer", "Sunil Narine", "Sai Kishore"],
        "prices": [21.0, 14.0, 7.2, 2.0, 3.4, 3.8, 9.25, 4.0, 11.0, 12.0, 2.0],
        "total_spend": 89.65, "remaining": 0.35
    },
    "Prayas": {
        "players": ["Tilak Varma", "Hardik", "Allen", "Brevis", "Bhuvi", "Abhishek", "Varun", "Ayush Mhatre", "Mitchell Marsh", "Jitesh Sharma", "Zeeshan Ansari"],
        "prices": [8.0, 16.35, 2.0, 2.2, 10.75, 14.0, 12.0, 0.3, 3.4, 11.0, 0.4],
        "total_spend": 80.4, "remaining": 9.6
    },
    "Akshay": {
        "players": ["Sanju Samson", "Green", "Dube", "qdk", "Digvesh", "shardul", "Padikkal", "Stubbs", "Rahul Tripathi", "Dhoni", "Seifert"],
        "prices": [18.0, 25.2, 12.0, 1.0, 0.3, 2.0, 6.5, 10.0, 3.4, 4.0, 1.5],
        "total_spend": 83.9, "remaining": 6.1
    },
    "Aayush": {
        "players": ["Sai Sudarshan", "Yashaswi Jaiswal", "Markram", "Noor Ahmad", "ngidi", "Krunal", "Ruturaj", "Head", "Rahane", "David", "Nitish Rana"],
        "prices": [8.5, 18.0, 2.0, 10.0, 2.0, 5.75, 18.0, 14.0, 1.5, 3.0, 4.2],
        "total_spend": 86.95, "remaining": 3.05
    },
    "Kaushal": {
        "players": ["Bumrah", "Iyer", "Rachin Ravindra", "prabhsimran", "NKR", "Suyash", "Ramandeep", "Patidar", "Sandeep Sharma", "Shashank Singh", "Tewatia"],
        "prices": [18.0, 26.75, 4.0, 4.0, 6.0, 2.0, 4.0, 11.0, 4.0, 5.5, 4.0],
        "total_spend": 89.25, "remaining": 0.75
    }
}

# ====================== BASE POINTS (after Match 1 - RCB vs SRH) ======================
base_points = {
    "Abhinay": {"Kishan": 110},
    "Ritu": {"Kohli": 104},
    "Prayas": {"Abhishek": 9, "Bhuvi": 25, "Jitesh Sharma": 8},
    "Akshay": {"Padikkal": 112},
    "Aayush": {"Head": 13, "David": 19},
    "Kaushal": {"NKR": 1, "Suyash": 25, "Patidar": 43}
}

# Initialize session state for C/VC
if "captains" not in st.session_state:
    st.session_state.captains = {team: None for team in teams}
if "vice_captains" not in st.session_state:
    st.session_state.vice_captains = {team: None for team in teams}

# ====================== UI ======================
tab1, tab2 = st.tabs(["📊 League Standings", "👥 All Teams"])

with tab1:
    standings_data = []
    for name, team in teams.items():
        team_base = base_points.get(name, {})
        captain = st.session_state.captains.get(name)
        vice = st.session_state.vice_captains.get(name)
        total = 0.0
        for player, pts in team_base.items():
            if player == captain:
                total += pts * 2
            elif player == vice:
                total += pts * 1.5
            else:
                total += pts
        standings_data.append({
            "Team": name,
            "Total Fantasy Points": round(total, 1),
            "Spent (cr)": team["total_spend"],
            "Purse Left (cr)": team["remaining"],
            "Captain": captain or "Not set",
            "Vice-Captain": vice or "Not set"
        })

    standings_df = pd.DataFrame(standings_data).sort_values("Total Fantasy Points", ascending=False).reset_index(drop=True)
    st.dataframe(
        standings_df.style.background_gradient(cmap="RdYlGn", subset=["Total Fantasy Points"]),
        use_container_width=True,
        hide_index=True
    )

with tab2:
    cols = st.columns(3)
    for i, (name, team) in enumerate(teams.items()):
        with cols[i % 3]:
            with st.container(border=True):
                st.subheader(f"**{name}**")
                
                # Dropdowns for C/VC
                players_list = team["players"]
                current_cap = st.session_state.captains[name]
                current_vc = st.session_state.vice_captains[name]
                
                new_cap = st.selectbox(
                    "Captain (2×)", 
                    options=["None"] + players_list, 
                    index=0 if current_cap is None else players_list.index(current_cap) + 1,
                    key=f"cap_{name}"
                )
                new_vc = st.selectbox(
                    "Vice-Captain (1.5×)", 
                    options=["None"] + players_list, 
                    index=0 if current_vc is None else players_list.index(current_vc) + 1,
                    key=f"vc_{name}"
                )
                
                # Update session state
                st.session_state.captains[name] = None if new_cap == "None" else new_cap
                st.session_state.vice_captains[name] = None if new_vc == "None" else new_vc
                
                # Calculate and show total
                team_base = base_points.get(name, {})
                captain = st.session_state.captains[name]
                vice = st.session_state.vice_captains[name]
                total = 0.0
                for player, pts in team_base.items():
                    if player == captain:
                        total += pts * 2
                    elif player == vice:
                        total += pts * 1.5
                    else:
                        total += pts
                
                st.caption(f"**Points: {round(total, 1)}** | Spent: ₹{team['total_spend']} cr | Left: ₹{team['remaining']} cr")
                
                # Player table with final points
                df = pd.DataFrame({
                    "Player": team["players"],
                    "Price (cr)": team["prices"]
                })
                df["Base Points"] = df["Player"].map(team_base).fillna(0).astype(int)
                df["Final Points"] = df.apply(
                    lambda row: round(row["Base Points"] * 2 if row["Player"] == captain else
                                    row["Base Points"] * 1.5 if row["Player"] == vice else
                                    row["Base Points"], 1), axis=1)
                st.dataframe(df, hide_index=True, use_container_width=True)

st.info("**How it works:** Select Captain and Vice-Captain using the dropdowns. Changes update instantly. You can change them anytime. Points after Match 1 (RCB vs SRH) are loaded. Tonight’s MI vs KKR match starts at 7:30 PM IST — reply “Update points after MI vs KKR” when it ends and I’ll give you the next base points update.")
st.success("✅ Captain & Vice-Captain dropdowns added! Select them now and watch the totals update live.")
