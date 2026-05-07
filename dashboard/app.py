import os
import sys

import pandas as pd
import streamlit as st


# Agregar raíz del proyecto
project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.append(project_root)


from models.poisson_model import PoissonModel
from predictions.value_betting import ValueBetting
from utils.data_loader import DataLoader


st.set_page_config(
    page_title="FIFA Quant System",
    layout="wide"
)

st.title("⚽ FIFA Quant Betting System")


matches = DataLoader.load_matches(
    "data/matches.csv"
)

results = []

for _, row in matches.iterrows():

    home_team = row['home_team']
    away_team = row['away_team']

    home_xg = row['home_xg']
    away_xg = row['away_xg']

    home_odds = row['home_odds']

    model = PoissonModel(
        home_xg,
        away_xg
    )

    probabilities = (
        model.calculate_probabilities()
    )

    score = model.most_likely_score()

    over_under = (
        model.over_under_probabilities()
    )

    btts = (
        model.both_teams_to_score()
    )

    value_analysis = (
        ValueBetting.analyze_bet(
            probabilities['home_win'] / 100,
            home_odds
        )
    )

    results.append({

        "Match":
        f"{home_team} vs {away_team}",

        "Home Win %":
        probabilities['home_win'],

        "Draw %":
        probabilities['draw'],

        "Away Win %":
        probabilities['away_win'],

        "Over 2.5 %":
        over_under['over_2_5'],

        "BTTS %":
        btts['yes'],

        "Score":
        f"{score['home_goals']}-"
        f"{score['away_goals']}",

        "Bookmaker Odds":
        home_odds,

        "Fair Odds":
        value_analysis['fair_odds'],

        "EV %":
        value_analysis['expected_value'],

        "Value Bet":
        value_analysis['is_value_bet']
    })


df = pd.DataFrame(results)

st.subheader("📊 Match Analysis")

st.dataframe(
    df,
    use_container_width=True
)

st.subheader("🔥 Value Bets")

value_bets = df[
    df['Value Bet'] == True
]

st.dataframe(
    value_bets,
    use_container_width=True
)