# src/simulate.py
import random
import numpy as np
from .elo import update_elo
from .injuries import apply_injuries
from .match_engine import predict_match
from .transfers import simulate_transfer_window

def simulate_season(teams, initial_elo, initial_squad_value, season_half=1):
    points = {t: 0 for t in teams}
    gd = {t: 0 for t in teams}
    current_elo = initial_elo.copy()
    squad_value = initial_squad_value.copy()

    # Simulate January transfer window
    if season_half == 1:
        squad_value = simulate_transfer_window(teams, squad_value, current_elo)

    fixtures = [(h, a) for h in teams for a in teams if h != a]

    for home, away in fixtures:
        # Apply injuries/suspensions
        home_injured = apply_injuries(home, squad_value[home])
        away_injured = apply_injuries(away, squad_value[away])

        # Adjust ELO based on squad strength drop
        home_elo_adj = current_elo[home] - home_injured * 20
        away_elo_adj = current_elo[away] - away_injured * 20

        # Predict match
        result, goals_h, goals_a = predict_match(home, away, home_elo_adj, away_elo_adj)

        # Update points
        if result == 'home': points[home] += 3
        elif result == 'draw':
            points[home] += 1
            points[away] += 1
        else: points[away] += 3

        gd[home] += goals_h - goals_a
        gd[away] += goals_a - goals_h

        # Update ELO
        if result != 'draw':
            winner = home if result == 'home' else away
            loser = away if result == 'home' else home
            winner_elo = current_elo[winner]
            loser_elo = current_elo[loser]
            w_elo, l_elo = update_elo(winner_elo, loser_elo, home_advantage=80)
            current_elo[winner] = w_elo
            current_elo[loser] = l_elo

    standings = sorted(points.items(), key=lambda x: (x[1], gd[x[0]]), reverse=True)
    champion = standings[0][0]
    top_4 = [t[0] for t in standings[:4]]
    relegated = [t[0] for t in standings[-3:]]

    return {
        'champion': champion,
        'top_4': top_4,
        'relegated': relegated,
        'standings': standings,
        'final_elo': current_elo,
        'squad_value': squad_value
    }