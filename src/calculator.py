from decimal import Decimal

from models import Portfolio


class Calculator:
    max_position = Decimal(0.3)
    portfolio: Portfolio

    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def calculate_ideal_portfolio(self):
        # Calculate ideal ideal_fraction
        for position in self.portfolio.positions:
            position.ideal_fraction = position.stock.expected_earnings / self.portfolio.total_expected_earnings
        self._redistribute_over_max()

        # Reset the current value to the ideal value
        total_value = self.portfolio.total_value
        for position in self.portfolio.positions:
            position.quantity = round(position.ideal_fraction * total_value / position.stock.current_value)

        self.portfolio.calculate_fractions()

    def _redistribute_over_max(self):
        # Check if the max position can be reached with the number of positions
        nr_positions = len(self.portfolio.positions)
        if nr_positions * self.max_position < 1:
            raise ValueError(f'Cannot have a max position of {self.max_position} with only {nr_positions} positions')

        # When all positions are under the maximum, there is nothing to redistribute anymore
        # The condition above guarantees that we do not end up in an endless loop
        if all([position.ideal_fraction <= self.max_position for position in self.portfolio.positions]):
            return

        # Determine the ideal_fractions that should be capped
        positions_over_max = [position for position in self.portfolio.positions
                              if position.ideal_fraction > self.max_position]
        total_ideal_fraction_to_redistribute = sum([position.ideal_fraction - self.max_position
                                                    for position in positions_over_max])
        for position in positions_over_max:
            position.ideal_fraction = self.max_position

        # Determine the ideal_fractions that should receive additional ideal_fraction
        positions_under_max = [position for position in self.portfolio.positions
                               if position.ideal_fraction < self.max_position]
        total_ideal_fraction_under_max = sum([position.ideal_fraction for position in positions_under_max])

        # Make the redistribution
        for position in positions_under_max:
            position.ideal_fraction += position.ideal_fraction / total_ideal_fraction_under_max * total_ideal_fraction_to_redistribute

        # Repeat the procedure until no position is above the maximum position
        self._redistribute_over_max()


if __name__ == '__main__':
    _portfolio = Portfolio.read_from_file('demo.csv')
    calculator = Calculator(_portfolio)
    calculator.calculate_ideal_portfolio()
    _portfolio.write_to_file('ideal.csv')
