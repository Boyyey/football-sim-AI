# app.py
import streamlit as st
import pickle
import os
from src.simulate import simulate_season

# Title
st.title("🔮 EuroLeague Oracle 2026 – Pro Edition")
st.subheader("AI-Powered Football Season Simulator")

# Sidebar
st.sidebar.header("Simulation Settings")
n_sims = st.sidebar.slider("Number of Simulations", 100, 5000, 1000)
leagues = ["Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]
selected_league = st.sidebar.selectbox("Select League", leagues)
run = st.sidebar.button("🚀 Run Simulation")

# Team data (same as before)
TEAM_ELO = { /* ... paste from previous script ... */ }
SQUAD_VALUE = {l: {t: 100 + abs(hash(t)) % 400 for t in teams} for l, teams in TEAM_ELO.items()}

if run:
    with st.spinner(f"Simulating {n_sims} seasons of {selected_league}..."):
        teams = list(TEAM_ELO[selected_league].keys())
        initial_elo = TEAM_ELO[selected_league]
        initial_squad = SQUAD_VALUE[selected_league]

        results = {'champions': {}, 'top_4': {}, 'relegated': {}}

        for _ in range(n_sims):
            sim = simulate_season(teams, initial_elo, initial_squad)
            champ = sim['champion']
            top4 = sim['top_4']
            relegates = sim['relegated']

            results['champions'][champ] = results['champions'].get(champ, 0) + 1
            for t in top4: results['top_4'][t] = results['top_4'].get(t, 0) + 1
            for r in relegates: results['relegated'][r] = results['relegated'].get(r, 0) + 1

        # Save results
        with open("data/simulations.pkl", "wb") as f:
            pickle.dump(results, f)

    st.success("✅ Simulation Complete!")

    # Display Results
    from src.analyze import plot_champion_probs
    fig = plot_champion_probs(results, selected_league)
    st.plotly_chart(fig)

    st.subheader("🏆 Champion Wins")
    champ_df = pd.DataFrame([
        {"Team": t, "Wins": w, "Win %": f"{100*w/n_sims:.1f}"} 
        for t, w in sorted(results['champions'].items(), key=lambda x: -x[1])
    ])
    st.dataframe(champ_df)

    st.subheader("🔝 Top 4 Chances")
    top4_df = pd.DataFrame([
        {"Team": t, "Top 4 Apps": w, "Chance %": f"{100*w/n_sims:.1f}"} 
        for t, w in sorted(results['top_4'].items(), key=lambda x: -x[1])
    ])
    st.dataframe(top4_df)

    # UCL Qualification
    st.subheader("🎯 Champions League Projection")
    top4 = champ_df.head(4)['Team'].tolist()
    st.info(f"Projected UCL: {', '.join(top4)}")

    # Add live odds comparison (mock)
    st.subheader("📊 AI vs Bookmakers (Mock)")
    st.write({
        "Manchester City": {"AI": "48%", "Odds": "2.10 (47.6%)"},
        "Real Madrid": {"AI": "51%", "Odds": "1.90 (52.6%)"},
        "Bayer Leverkusen": {"AI": "38%", "Odds": "2.50 (40.0%)"}
    })