import argparse
import os.path
import random
from decimal import Decimal

import settings
from calculator import Calculator
from models import Portfolio


class Simulator:
    SCENARIO_UP_AND_DOWN = 'up_and_down'
    SCENARIOS = {SCENARIO_UP_AND_DOWN}

    def __init__(self, scenario: str):
        if scenario not in self.SCENARIOS:
            raise NotImplementedError(f'Unknown scenario {scenario}. Choose from: {sorted(self.SCENARIOS)}')

        self.scenario = scenario
        self.data_dir = os.path.join(settings.SIMULATION_DIR, scenario)
        self.portfolio = Portfolio.read_from_file(os.path.join(self.data_dir, 'start.csv'))
        self.reference_portfolio = Portfolio.read_from_file(os.path.join(self.data_dir, 'start.csv'))

    def start_simulation(self, nr_steps: int = 10):
        self.portfolio.write_to_file(os.path.join(self.data_dir, f'step_00.csv'))
        for step in range(1, nr_steps + 1):
            self._rebalance()
            self.portfolio.write_to_file(os.path.join(self.data_dir, f'step_{step:02}_rebalance.csv'))
            self._update_reality(step)
            self.portfolio.write_to_file(os.path.join(self.data_dir, f'step_{step:02}_update_reality_portfolio.csv'))
            self.reference_portfolio.write_to_file(
                os.path.join(self.data_dir, f'step_{step:02}_update_reality_reference.csv'))

    def _rebalance(self):
        calculator = Calculator(self.portfolio)
        calculator.calculate_ideal_portfolio()

    def _update_reality(self, step: int):
        if self.scenario == self.SCENARIO_UP_AND_DOWN:
            # In odd steps, the price goes down. In even steps, the price goes up.
            # The stocks with the highest expected earnings will fluctuate the most.
            # One out of four steps we expect a loss 20%-40%, the other steps we expect a gain 10-30%
            if step % 4 == 0:
                fluctuation = - random.uniform(0.2, 0.4)
            else:
                fluctuation = random.uniform(0.1, 0.3)
            fluctuation = Decimal(fluctuation)

            for position in self.portfolio.positions + self.reference_portfolio.positions:
                position.stock.current_value += fluctuation * position.stock.expected_earnings * position.stock.current_value


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculator')
    parser.add_argument('--scenario', type=str, default=Simulator.SCENARIO_UP_AND_DOWN,
                        help=f'Name of scenario. Choose from: {sorted(Simulator.SCENARIOS)}. Defaults to up_and_down')
    parser.add_argument('--steps', type=int, default=10,
                        help='Number of steps in the simulation. Defaults to 10')
    args = parser.parse_args()

    simulator = Simulator(args.scenario)
    simulator.start_simulation(args.steps)
