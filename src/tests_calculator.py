import os.path
from unittest import TestCase

import settings
from calculator import Calculator
from models import Portfolio
from utils import FileComparingMixin


class CalculatorTestCase(FileComparingMixin, TestCase):
    def test_that_equal_expectation_leads_to_equal_fractions(self):
        self._calculate_ideal_portfolio('equal_expectation_input.csv', 'equal_expectation_output.csv')

    def test_that_redistribution_occurs_iteratively(self):
        self._calculate_ideal_portfolio('redistribute_twice_input.csv', 'redistribute_twice_output.csv')

    def _calculate_ideal_portfolio(self, input_filename: str, reference_filename: str):
        input_file = os.path.join(settings.TEST_DIR, input_filename)
        reference_file = os.path.join(settings.TEST_DIR, reference_filename)
        generated_file = os.path.join(settings.TMP_DIR, reference_filename)
        portfolio = Portfolio.read_from_file(input_file)
        calculator = Calculator(portfolio)
        calculator.calculate_ideal_portfolio()
        portfolio.write_to_file(generated_file)
        self.compare_file_with_file(generated_file, reference_file, write_first=True)
        os.remove(generated_file)
