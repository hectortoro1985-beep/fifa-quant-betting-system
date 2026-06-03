import os
import sys

import pandas as pd
import streamlit as st
import plotly.express as px

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.append(project_root)

from models.poisson_model import PoissonModel
from predictions.value_betting import ValueBetting
from predictions.bankroll import BankrollManagement
from predictions.performance_tracker import PerformanceTracker
from utils.data_loader import DataLoader

st.set_page_config(
    page_title="Sistema Cuantitativo FIFA",
    layout="wide"
)

st.title("⚽ Sistema Cuantitativo de Apuestas FIFA")

matches = DataLoader.load_matches(
    "data/matches.csv"
)

results_data = DataLoader.load_matches(
    "data/results.csv"
)

bankroll_system = BankrollManagement(
    bankroll=1000
)

tracker = PerformanceTracker(
    starting_bankroll=1000
)

results = []

current_bankroll_tracker = 1000

for _, row in matches.iterrows():

    home_team = row["home_team"]
    away_team = row["away_team"]

    home_xg = row["home_xg"]
    away_xg = row["away_xg"]

    home_odds = row["home_odds"]

    match_name = (
        f"{home_team} vs {away_team}"
    )

    result_row = results_data[
        results_data["match"] == match_name
    ]

    final_result = (
        result_row.iloc[0]["result"]
        if not result_row.empty
        else "PERDIDA"
    )

    model = PoissonModel(
        home_xg,
        away_xg
    )

    probabilities = (
        model.calculate_probabilities()
    )

    score = (
        model.most_likely_score()
    )

    over_under = (
        model.over_under_probabilities()
    )

    btts = (
        model.both_teams_to_score()
    )

    value_analysis = (
        ValueBetting.analyze_bet(
            probabilities["home_win"] / 100,
            home_odds
        )
    )

    kelly_percent = (
        bankroll_system.kelly_criterion(
            probabilities["home_win"] / 100,
            home_odds
        )
    )

    stake = (
        bankroll_system.recommended_stake(
            probabilities["home_win"] / 100,
            home_odds
        )
    )

    profit = (
        tracker.calculate_profit(
            stake,
            home_odds,
            final_result
        )
    )

    current_bankroll_tracker += profit

    results.append({

        "Partido": match_name,

        "Resultado": final_result,

        "Prob. Local %":
        probabilities["home_win"],

        "Prob. Empate %":
        probabilities["draw"],

        "Prob. Visitante %":
        probabilities["away_win"],

        "Over 2.5 %":
        over_under["over_2_5"],

        "BTTS %":
        btts["yes"],

        "Marcador":
        f"{score['home_goals']}-{score['away_goals']}",

        "Cuota":
        home_odds,

        "Cuota Justa":
        value_analysis["fair_odds"],

        "EV %":
        value_analysis["expected_value"],

        "Value Bet":
        value_analysis["is_value_bet"],

        "Kelly %":
        kelly_percent,

        "Stake":
        stake,

        "Ganancia":
        profit,

        "Bankroll":
        round(
            current_bankroll_tracker,
            2
        )
    })

df = pd.DataFrame(results)

total_profit = round(
    df["Ganancia"].sum(),
    2
)

total_staked = round(
    df["Stake"].sum(),
    2
)

wins = len(
    df[df["Resultado"] == "GANADA"]
)

total_bets = len(df)

roi = tracker.roi(
    total_profit
)

yield_pct = (
    tracker.yield_percentage(
        total_profit,
        total_staked
    )
)

win_rate = (
    tracker.win_rate(
        wins,
        total_bets
    )
)

current_bankroll = round(
    1000 + total_profit,
    2
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Bankroll Actual",
    f"${current_bankroll}"
)

col2.metric(
    "Ganancia",
    f"${total_profit}"
)

col3.metric(
    "ROI %",
    roi
)

col4.metric(
    "Rendimiento %",
    yield_pct
)

col5.metric(
    "Acierto %",
    win_rate
)

st.divider()

st.subheader(
    "📊 Seguimiento de Rendimiento"
)

st.dataframe(
    df,
    use_container_width=True
)

st.subheader(
    "📈 Ganancia por Partido"
)

fig_profit = px.bar(
    df,
    x="Partido",
    y="Ganancia",
    text="Ganancia"
)

st.plotly_chart(
    fig_profit,
    use_container_width=True
)

st.subheader(
    "💰 Evolución del Bankroll"
)

fig_bankroll = px.line(
    df,
    x="Partido",
    y="Bankroll",
    markers=True
)

st.plotly_chart(
    fig_bankroll,
    use_container_width=True
)