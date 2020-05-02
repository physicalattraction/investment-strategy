from decimal import Decimal
from unittest import TestCase

from models import Portfolio, Position, Stock


class StocktestCase(TestCase):
    def test_expected_earnings(self):
        stock = Stock('ticker', 'name', 20, 30)
        self.assertEqual(Decimal('0.5'), stock.expected_earnings)


class PortfolioTestCase(TestCase):
    def test_total_expected_earnings(self):
        position_1 = Position(stock=Stock('ticker', 'name', 20, 30), quantity=2)
        position_2 = Position(stock=Stock('ticker', 'name', 20, 40), quantity=2)
        portfolio = Portfolio(position_1, position_2)
        self.assertEqual(Decimal('1.5'), portfolio.total_expected_earnings)
