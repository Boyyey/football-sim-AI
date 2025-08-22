# src/elo.py
def update_elo(winner_elo, loser_elo, home_advantage=80, k=30):
    winner_exp = 1 / (1 + 10**((loser_elo - winner_elo - home_advantage)/400))
    new_winner = winner_elo + k * (1 - winner_exp)
    new_loser = loser_elo + k * (0 - (1 - winner_exp))
    return new_winner, new_loser