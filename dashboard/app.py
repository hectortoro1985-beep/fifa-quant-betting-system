import os
import sys

import pandas as pd
import streamlit as st
import plotly.express as px


# ROOT PROJECT
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


# PAGE CONFIG
st.set_page_config(
    page_title="FIFA Quant System",
    layout="wide"
)

st.title("⚽ FIFA Quant Betting System")


# LOAD DATA
matches = DataLoader.load_matches(
    "data/matches.csv"
)

results = []


# ANALYSIS LOOP
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


# DATAFRAME
df = pd.DataFrame(results)


# KPIs
total_matches = len(df)

value_bets = len(
    df[df['Value Bet'] == True]
)

avg_ev = round(
    df['EV %'].mean(),
    2
)

best_ev = round(
    df['EV %'].max(),
    2
)


# KPI ROW
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Matches",
    total_matches
)

col2.metric(
    "Value Bets",
    value_bets
)

col3.metric(
    "Average EV %",
    avg_ev
)

col4.metric(
    "Best EV %",
    best_ev
)


st.divider()


# FULL TABLE
st.subheader("📊 Match Analysis")

st.dataframe(
    df,
    use_container_width=True
)


# FILTER VALUE BETS
st.subheader("🔥 Positive EV Bets")

positive_ev = df[
    df['Value Bet'] == True
]

st.dataframe(
    positive_ev,
    use_container_width=True
)


# BAR CHART
st.subheader("📈 Expected Value Ranking")

fig = px.bar(
    df.sort_values(
        by='EV %',
        ascending=False
    ),
    x='Match',
    y='EV %',
    text='EV %'
)

st.plotly_chart(
    fig,
    use_container_width=True
)