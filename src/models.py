import csv
import os.path
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional, Union

from settings import PORTFOLIO_DIR

Number = Union[Decimal, float, int]
Numeric = Union[Number, str]


@dataclass
class Stock:
    ticker: str
    name: str
    current_value: Decimal
    expected_value: Decimal

    def __init__(self, ticker: str, name: str, current_value: Numeric, expected_value: Numeric, **kwargs):
        self.ticker = ticker
        self.name = name
        self.current_value = Decimal(current_value).quantize(Decimal('.01'))
        self.expected_value = Decimal(expected_value).quantize(Decimal('.01'))

    @property
    def expected_earnings(self) -> Decimal:
        """
        Calculate the expected earnings as a fraction of the current value

        Example:
        stock = Stock('AA', 'Alexandra & Amelia', 20, 30)
        stock.expected_earnings
        > 0.5
        """

        return (self.expected_value - self.current_value) / self.current_value

    def as_dict(self) -> Dict[str, Any]:
        return {
            'ticker': self.ticker,
            'name': self.name,
            'current_value': self.current_value.quantize(Decimal('0.01')),
            'expected_value': self.expected_value.quantize(Decimal('0.01')),
        }


@dataclass
class Position:
    stock: Stock
    quantity: int
    fraction: Decimal

    def __init__(self, quantity: Numeric, *, stock: Optional[Stock] = None,
                 ticker: Optional[str] = None, name: Optional[str] = None,
                 current_value: Optional[Numeric] = None, expected_value: Optional[Numeric] = None):
        self.quantity = int(quantity)
        if stock:
            self.stock = stock
        else:
            self.stock = Stock(ticker, name, current_value, expected_value)

    @property
    def value(self) -> Decimal:
        return self.quantity * self.stock.current_value

    def as_dict(self) -> Dict[str, Any]:
        result = self.stock.as_dict()
        result['quantity'] = self.quantity
        result['value'] = self.value.quantize(Decimal('0.01'))
        result['fraction'] = self.fraction.quantize(Decimal('0.0001'))
        return result


@dataclass
class Portfolio:
    positions: List[Position]

    def __init__(self, *positions: Position):
        self.positions = list(positions)
        self.calculate_fractions()

    def calculate_fractions(self):
        """
        We can only fill the fractions after we have set all positions
        """

        for position in self.positions:
            position.fraction = position.value / self.total_value

    @property
    def total_value(self) -> Decimal:
        return sum([position.value for position in self.positions])

    @property
    def total_quantity(self) -> int:
        return sum([position.quantity for position in self.positions])

    @property
    def total_fraction(self) -> Decimal:
        return sum([position.fraction for position in self.positions])

    @property
    def total_expected_earnings(self) -> Decimal:
        return sum([position.stock.expected_earnings for position in self.positions])

    @staticmethod
    def read_from_file(filename: str) -> 'Portfolio':
        """
        :param filename: Either name of the file in PORTFOLIO DIR, or full path to portfolio csv file
        """

        if not os.path.dirname(filename):
            filename = os.path.join(PORTFOLIO_DIR, filename)
        result = Portfolio()
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    expected_input = ['quantity', 'ticker', 'name', 'current_value', 'expected_value']
                    input_data = {k: v for k, v in row.items() if k in expected_input}
                    result.positions.append(Position(**input_data))
                except (TypeError, InvalidOperation):
                    # We ignore rows that cannot be interpreted as a Position, e.g. total row
                    continue
        result.calculate_fractions()
        return result

    def write_to_file(self, filename: str):
        """
        :param filename: Either name of the file in PORTFOLIO DIR, or full path to portfolio csv file
        """

        if not os.path.dirname(filename):
            filename = os.path.join(PORTFOLIO_DIR, filename)

        # Write the table of positions
        fieldnames = ['ticker', 'name', 'current_value', 'expected_value', 'quantity', 'value', 'fraction']
        with open(filename, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            writer.writerows([position.as_dict() for position in self.positions])
            writer.writerow({'ticker': 'Total', 'name': None, 'current_value': None, 'expected_value': None,
                             'quantity': self.total_quantity, 'value': self.total_value.quantize(Decimal('0.01')),
                             'fraction': self.total_fraction.quantize(Decimal('0.0001'))})
