class PerformanceTracker:

    def __init__(self, starting_bankroll):

        self.starting_bankroll = starting_bankroll

    def calculate_profit(
        self,
        stake,
        odds,
        result
    ):

        if result == "GANADA":
            return round(
                stake * (odds - 1),
                2
            )

        return round(
            -stake,
            2
        )

    def roi(
        self,
        total_profit
    ):

        roi = (
            total_profit /
            self.starting_bankroll
        ) * 100

        return round(
            roi,
            2
        )

    def yield_percentage(
        self,
        total_profit,
        total_staked
    ):

        if total_staked == 0:
            return 0

        yld = (
            total_profit /
            total_staked
        ) * 100

        return round(
            yld,
            2
        )

    def win_rate(
        self,
        wins,
        total_bets
    ):

        if total_bets == 0:
            return 0

        rate = (
            wins /
            total_bets
        ) * 100

        return round(
            rate,
            2
        )