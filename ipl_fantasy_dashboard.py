import streamlit as st
import pandas as pd

st.set_page_config(page_title="IPL 2026 Fantasy League", layout="wide", page_icon="🏏")
st.title("🏏 IPL 2026 Private Fantasy League Dashboard")
st.caption("Points system: Batting (Runs +1, Boundary +1, Six +2, 30-run bonus +4, 50 +8, 100 +16) | Bowling (Wicket +25, LBW/Bowled +8, Maiden +12, 3W +4, 4W +8, 5W +12) | Fielding (Catch +8, Stumping +12, Run-out +6)")

# ====================== TEAM DATA ======================
teams = {
    "Abhinay": {
        "players": ["Kishan", "Sooryavanshi", "Sundar", "Will Jacks", "Arshdeep", "Jansen", "Gill", "Bethell", "Butler", "Khaleel", "Angrish Raghuvanshi"],
        "prices": [11.25, 1.1, 3.2, 5.25, 18.0, 7.0, 16.5, 2.6, 15.75, 4.8, 3.0],
        "total_spend": 88.45,
        "remaining": 1.55,
        "total_points": 0
    },
    "Ritu": {
        "players": ["Kohli", "Rahul", "Bishnoi", "Miller", "Anshul Kambhoj", "Priyansh Arya", "Deepak Chahar", "Mohsin Khan", "Hetmyer", "Sunil Narine", "Sai Kishore"],
        "prices": [21.0, 14.0, 7.2, 2.0, 3.4, 3.8, 9.25, 4.0, 11.0, 12.0, 2.0],
        "total_spend": 89.65,
        "remaining": 0.35,
        "total_points": 0
    },
    "Prayas": {
        "players": ["Tilak Varma", "Hardik", "Allen", "Brevis", "Bhuvi", "Abhishek", "Varun", "Ayush Mhatre", "Mitchell Marsh", "Jitesh Sharma", "Zeeshan Ansari"],
        "prices": [8.0, 16.35, 2.0, 2.2, 10.75, 14.0, 12.0, 0.3, 3.4, 11.0, 0.4],
        "total_spend": 80.4,
        "remaining": 9.6,
        "total_points": 0
    },
    "Akshay": {
        "players": ["Sanju Samson", "Green", "Dube", "qdk", "Digvesh", "shardul", "Padikkal", "Stubbs", "Rahul Tripathi", "Dhoni", "Seifert"],
        "prices": [18.0, 25.2, 12.0, 1.0, 0.3, 2.0, 6.5, 10.0, 3.4, 4.0, 1.5],
        "total_spend": 83.9,
        "remaining": 6.1,
        "total_points": 0
    },
    "Aayush": {
        "players": ["Sai Sudarshan", "Yashaswi Jaiswal", "Markram", "Noor Ahmad", "ngidi", "Krunal", "Ruturaj", "Head", "Rahane", "David", "Nitish Rana"],
        "prices": [8.5, 18.0, 2.0, 10.0, 2.0, 5.75, 18.0, 14.0, 1.5, 3.0, 4.2],
        "total_spend": 86.95,
        "remaining": 3.05,
        "total_points": 0
    },
    "Kaushal": {
        "players": ["Bumrah", "Iyer", "Rachin Ravindra", "prabhsimran", "NKR", "Suyash", "Ramandeep", "Patidar", "Sandeep Sharma", "Shashank Singh", "Tewatia"],
        "prices": [18.0, 26.75, 4.0, 4.0, 6.0, 2.0, 4.0, 11.0, 4.0, 5.5, 4.0],
        "total_spend": 89.25,
        "remaining": 0.75,
        "total_points": 0
    }
}

# ====================== LEAGUE STANDINGS ======================
standings_data = []
for name, data in teams.items():
    standings_data.append({
        "Team": name,
        "Total Fantasy Points": data["total_points"],
        "Spent (cr)": data["total_spend"],
        "Purse Left (cr)": data["remaining"],
        "Players": len(data["players"])
    })

standings_df = pd.DataFrame(standings_data).sort_values("Total Fantasy Points", ascending=False).reset_index(drop=True)

# ====================== UI ======================
tab1, tab2 = st.tabs(["📊 League Standings", "👥 All Teams"])

with tab1:
    st.dataframe(standings_df.style.background_gradient(cmap="RdYlGn", subset=["Total Fantasy Points"]), use_container_width=True, hide_index=True)

with tab2:
    cols = st.columns(3)
    for i, (name, data) in enumerate(teams.items()):
        with cols[i % 3]:
            with st.container(border=True):
                st.subheader(f"**{name}**")
                st.caption(f"Spent: **₹{data['total_spend']} cr** | Left: **₹{data['remaining']} cr** | Points: **{data['total_points']}**")
                
                df = pd.DataFrame({
                    "Player": data["players"],
                    "Price (cr)": data["prices"],
                    "Points": [0] * len(data["players"])
                })
                st.dataframe(df, hide_index=True, use_container_width=True)

st.info("💡 **Real-time updates managed by Grok** — After any match just reply here “Update points after MI vs KKR” (or Match 2 etc.) and I’ll calculate everything using your exact points system and give you the numbers to paste.")
st.success("Dashboard ready! Deploy it and share the link 🎉")
