import numpy as np

def load_assets():
    """ Create synthetic bank asset portfolio """
    assets = [
        # Mortgages
        {'type': 'mortgage', 'maturity': 30, 'notional': 400},
        {'type': 'mortgage', 'maturity': 20, 'notional': 250},
        {'type': 'mortgage', 'maturity': 10, 'notional': 150},

        # Corporate loans
        {'type': 'corporate_loan', 'maturity': 7, 'notional': 200},
        {'type': 'corporate_loan', 'maturity': 5, 'notional': 150},

        # Government bonds
        {'type': 'gov_bond', 'maturity': 10, 'notional': 120},
        {'type': 'gov_bond', 'maturity': 5, 'notional': 80},
        {'type': 'gov_bond', 'maturity': 2, 'notional': 70}
    ]

    return assets


def load_liabilities():
    """ Create synthetic bank liabilities """
    liabilities = [
        # Retail deposits
        {'type': 'retail_deposit', 'maturity': 3, 'notional': 500},
        {'type': 'retail_deposit', 'maturity': 2, 'notional': 300},

        # Corporate deposits
        {'type': 'corporate_deposit', 'maturity': 1, 'notional': 250},
        {'type': 'corporate_deposit', 'maturity': 0.5, 'notional': 150},

        # Wholesale funding
        {'type': 'wholesale', 'maturity': 5, 'notional': 200}
    ]

    return liabilities
