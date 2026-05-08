from models.poisson_model import PoissonModel
from predictions.value_betting import ValueBetting
from utils.data_loader import DataLoader


def main():

    # Cargar partidos desde CSV
    matches = DataLoader.load_matches(
        "data/matches.csv"
    )

    # Recorrer partidos
    for _, row in matches.iterrows():

        home_team = row['home_team']
        away_team = row['away_team']

        home_xg = row['home_xg']
        away_xg = row['away_xg']

        home_odds = row['home_odds']

        # Crear modelo
        model = PoissonModel(
            home_xg,
            away_xg
        )

        # Probabilidades
        probabilities = (
            model.calculate_probabilities()
        )

        # Marcador probable
        score = model.most_likely_score()

        # Over / Under
        over_under = (
            model.over_under_probabilities()
        )

        # Ambos marcan
        btts = (
            model.both_teams_to_score()
        )

        # Análisis EV+
        value_analysis = (
            ValueBetting.analyze_bet(
                probabilities['home_win'] / 100,
                home_odds
            )
        )

        # Mostrar resultados
        print("\n===================================")

        print(
            f"{home_team} vs {away_team}"
        )

        print("===================================")

        print(
            f"Probabilidad Local: "
            f"{probabilities['home_win']}%"
        )

        print(
            f"Probabilidad Empate: "
            f"{probabilities['draw']}%"
        )

        print(
            f"Probabilidad Visitante: "
            f"{probabilities['away_win']}%"
        )

        print(
            f"Over 2.5: "
            f"{over_under['over_2_5']}%"
        )

        print(
            f"BTTS Sí: "
            f"{btts['yes']}%"
        )

        print(
            f"Score probable: "
            f"{score['home_goals']}"
            f"-"
            f"{score['away_goals']}"
        )

        print(
            f"Cuota Bookmaker: "
            f"{home_odds}"
        )

        print(
            f"Cuota JUSTA: "
            f"{value_analysis['fair_odds']}"
        )

        print(
            f"Expected Value: "
            f"{value_analysis['expected_value']}%"
        )

        print(
            f"¿Value Bet?: "
            f"{value_analysis['is_value_bet']}"
        )


if __name__ == "__main__":
    main()
    