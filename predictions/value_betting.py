class ValueBetting:

    @staticmethod
    def implied_probability(odds):

        return 1 / odds

    @staticmethod
    def fair_odds(real_probability):

        return 1 / real_probability

    @staticmethod
    def expected_value(real_probability, odds):

        return (
            (real_probability * odds) - 1
        )

    @staticmethod
    def analyze_bet(real_probability, odds):

        implied_prob = (
            ValueBetting.implied_probability(odds)
        )

        fair_odds = (
            ValueBetting.fair_odds(real_probability)
        )

        ev = ValueBetting.expected_value(
            real_probability,
            odds
        )

        return {

            "real_probability": round(
                real_probability * 100,
                2
            ),

            "implied_probability": round(
                implied_prob * 100,
                2
            ),

            "fair_odds": round(
                fair_odds,
                2
            ),

            "expected_value": round(
                ev * 100,
                2
            ),

            "is_value_bet": ev > 0
        }