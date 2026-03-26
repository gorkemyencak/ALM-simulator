import numpy as np

def rate_for_maturity(
        curve: dict,
        maturity: int
):
    """ Simple nearest interpolation for a given maturity """
    sorted_tenors = sorted(curve.keys())
    closest_tenor = min(sorted_tenors, key = lambda x: abs(x - maturity))

    return curve[closest_tenor]


def bond_duration(
        bond, 
        yield_curve
):
    """ Macaulay duration for a bond """

    cashflows = bond.generate_cashflow()
    pv_total = 0
    weighted_sum = 0

    for t, cf in enumerate(cashflows, start=1):
        rate = rate_for_maturity(
            curve = yield_curve,
            maturity = t
        )

        discount = 1 / (1 + rate)**t

        pv = cf * discount
        pv_total += pv

        weighted_sum += t * pv
    
    return weighted_sum / pv_total


def portfolio_duration(
        portfolio,
        yield_curve,
        pricing_function
):
    
    total_value = 0
    weighted_duration = 0

    for bond in portfolio.bonds:
        price = pricing_function(
            bond = bond,
            yield_curve = yield_curve
        )

        duration = bond_duration(
            bond = bond,
            yield_curve = yield_curve
        )

        total_value += price
        weighted_duration += price * duration
    
    return weighted_duration / total_value


def liability_duration(
        cashflows,
        yield_curve
):
    
    pv_total = 0
    weighted_sum = 0

    for t, cf in enumerate(cashflows, start=1):
        rate = rate_for_maturity(
            curve = yield_curve,
            maturity = t
        )

        discount = 1 / (1 + rate)**t

        pv = cf * discount
        pv_total += pv

        weighted_sum += t * pv
    
    return weighted_sum / pv_total


def duration_gap(
        asset_duration,
        liability_duration
):
    
    return asset_duration - liability_duration