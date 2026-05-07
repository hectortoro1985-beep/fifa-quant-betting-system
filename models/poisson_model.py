import numpy as np
import pandas as pd
from scipy.stats import poisson


class PoissonModel:

    def __init__(self, home_xg, away_xg):
        self.home_xg = home_xg
        self.away_xg = away_xg

    def calculate_score_matrix(self, max_goals=5):

        matrix = np.zeros((max_goals + 1, max_goals + 1))

        for home_goals in range(max_goals + 1):
            for away_goals in range(max_goals + 1):

                home_prob = poisson.pmf(
                    home_goals,
                    self.home_xg
                )

                away_prob = poisson.pmf(
                    away_goals,
                    self.away_xg
                )

                matrix[home_goals][away_goals] = (
                    home_prob * away_prob
                )

        return matrix

    def calculate_probabilities(self):

        matrix = self.calculate_score_matrix()

        home_win = 0
        draw = 0
        away_win = 0

        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):

                if i > j:
                    home_win += matrix[i][j]

                elif i == j:
                    draw += matrix[i][j]

                else:
                    away_win += matrix[i][j]

        return {
            "home_win": round(home_win * 100, 2),
            "draw": round(draw * 100, 2),
            "away_win": round(away_win * 100, 2)
        }

    def most_likely_score(self):

        matrix = self.calculate_score_matrix()

        index = np.unravel_index(
            np.argmax(matrix),
            matrix.shape
        )

        return {
            "home_goals": index[0],
            "away_goals": index[1],
            "probability": round(
                matrix[index] * 100,
                2
            )
        }

    def over_under_probabilities(self):

        matrix = self.calculate_score_matrix()

        over_25 = 0
        under_25 = 0

        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):

                total_goals = i + j

                if total_goals > 2:
                    over_25 += matrix[i][j]
                else:
                    under_25 += matrix[i][j]

        return {
            "over_2_5": round(over_25 * 100, 2),
            "under_2_5": round(under_25 * 100, 2)
        }

    def both_teams_to_score(self):

        matrix = self.calculate_score_matrix()

        yes = 0
        no = 0

        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):

                if i > 0 and j > 0:
                    yes += matrix[i][j]
                else:
                    no += matrix[i][j]

        return {
            "yes": round(yes * 100, 2),
            "no": round(no * 100, 2)
        }
    def score_matrix_dataframe(self):

        matrix = self.calculate_score_matrix()

        df = pd.DataFrame(matrix)

        return round(df * 100, 2)