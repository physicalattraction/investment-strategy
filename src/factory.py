import os.path

from models import Portfolio, Position
from settings import PORTFOLIO_DIR


def generate_demo_csv():
    position_a = Position(quantity=2, ticker='AA', name='A & A', current_value=20, expected_value=30)
    position_b = Position(quantity=3, ticker='BB', name='B & B', current_value=30, expected_value=40)
    position_c = Position(quantity=4, ticker='CC', name='C & C', current_value=40, expected_value=50)
    position_d = Position(quantity=5, ticker='DD', name='D & D', current_value=50, expected_value=60)
    portfolio = Portfolio(position_a, position_b, position_c, position_d)
    portfolio.write_to_file(os.path.join(PORTFOLIO_DIR, 'demo.csv'))


if __name__ == '__main__':
    generate_demo_csv()
