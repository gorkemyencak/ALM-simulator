import numpy as np

def discount_factor(
        rate: float, 
        t: int
):
    return 1 / (1+rate)**t

def rate_for_maturity(
        curve: dict,
        maturity: int
):
    """ Simple nearest interpolation for a given maturity """
    sorted_tenors = sorted(curve.keys(), key = lambda x: int(x.rstrip('Y')))
    closest_tenor = min(sorted_tenors, key = lambda x: abs(int(x.rstrip('Y')) - maturity))

    return curve[closest_tenor]

def price_bond(
        bond,
        yield_curve: dict
):
    """ Price bond using simple yield curve """

    cashflows = bond.generate_cashflow()
    pv = 0

    for t, cf in enumerate(cashflows, start = 1):
        rate = rate_for_maturity(yield_curve, t)
        pv += cf * discount_factor(rate, t)

    return pv

    
