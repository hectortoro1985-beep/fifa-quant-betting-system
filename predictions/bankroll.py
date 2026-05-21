class BankrollManagement:

    def __init__(self, bankroll):

        self.bankroll = bankroll

    def kelly_criterion(
        self,
        probability,
        odds
    ):

        b = odds - 1

        q = 1 - probability

        kelly = (
            (b * probability) - q
        ) / b

        return max(
            round(kelly * 100, 2),
            0
        )

    def recommended_stake(
        self,
        probability,
        odds
    ):

        kelly_percent = (
            self.kelly_criterion(
                probability,
                odds
            )
        )

        stake = (
            self.bankroll *
            (kelly_percent / 100)
        )

        return round(stake, 2)