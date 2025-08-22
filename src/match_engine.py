# src/match_engine.py
import joblib
import numpy as np
from sklearn.ensemble import VotingClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
import os

MODEL_PATH = "match_model.pkl"

def train_model():
    np.random.seed(42)
    data = []
    for _ in range(20000):
        home_elo = np.random.randint(1500, 2000)
        away_elo = np.random.randint(1500, 2000)
        home_form = np.random.randint(0, 15)
        away_form = np.random.randint(0, 15)
        home_xg = np.random.uniform(1.0, 2.5)
        away_xg = np.random.uniform(1.0, 2.5)
        possession = np.random.uniform(0.4, 0.7)

        elo_diff = (home_elo - away_elo) / 100
        prob_home = 0.3 + elo_diff * 0.2 + (home_form - away_form) * 0.05
        prob_draw = 0.3
        prob_away = 1 - prob_home - prob_draw

        result = np.random.choice([2, 1, 0], p=[prob_home, prob_draw, max(prob_away, 0)])

        data.append([home_elo, away_elo, home_form, away_form, home_xg, away_xg, possession, result])

    import pandas as pd
    df = pd.DataFrame(data, columns=[
        'home_elo', 'away_elo', 'home_form', 'away_form',
        'home_xg', 'away_xg', 'possession', 'result'
    ])
    X = df.iloc[:, :-1]
    y = df['result']

    model = VotingClassifier([
        ('xgb', XGBClassifier(n_estimators=100)),
        ('rf', RandomForestClassifier(n_estimators=100))
    ], voting='soft')
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return model

def predict_match(home, away, home_elo, away_elo):
    if not os.path.exists(MODEL_PATH):
        print("🧠 Training AI match engine...")
        model = train_model()
    else:
        model = joblib.load(MODEL_PATH)

    home_form = np.random.randint(5, 12)
    away_form = np.random.randint(5, 12)
    home_xg = 1.2 + (home_elo - 1700) / 1000
    away_xg = 1.2 + (away_elo - 1700) / 1000
    possession = 0.5 + (home_elo - away_elo) / 2000

    pred = model.predict_proba([[
        home_elo, away_elo, home_form, away_form,
        home_xg, away_xg, possession
    ]])[0]

    rand = random.random()
    if rand < pred[2]:
        return 'home', 2, 0
    elif rand < pred[2] + pred[1]:
        return 'draw', 1, 1
    else:
        return 'away', 0, 2