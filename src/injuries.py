# src/injuries.py
import random

def apply_injuries(team, squad_value):
    # Higher value = more games played = higher injury risk
    base_injury_rate = 0.15
    risk = base_injury_rate * (squad_value / 500)  # 500M = max
    return 1 if random.random() < risk else 0  # 1 injured player