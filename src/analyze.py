# src/analyze.py
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

def plot_champion_probs(results, league):
    df = pd.DataFrame([
        {'Team': team, 'Wins': wins} for team, wins in results['champions'].items()
    ])
    df['Probability'] = 100 * df['Wins'] / df['Wins'].sum()
    df = df.sort_values('Probability', ascending=False).head(10)

    fig = px.bar(df, x='Team', y='Probability', title=f"{league} Champion Probability")
    fig.update_layout(yaxis_title="Win Probability (%)")
    return fig