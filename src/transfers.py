# src/transfers.py
import random

def simulate_transfer_window(teams, squad_value, elo_ratings):
    print("💸 January Transfer Window Open!")
    transfers = []

    for team in teams:
        if random.random() < 0.3:  # 30% chance to sign
            potential_signings = [t for t in teams if t != team]
            target = random.choice(potential_signings)
            fee = random.randint(30, 100)
            squad_value[team] += fee
            transfers.append(f"{team} signed from {target} for €{fee}M")

    print(f"✅ {len(transfers)} transfers completed.")
    return squad_value