import numpy as np

def rate_for_maturity(
        curve: dict,
        maturity: int
):
    """ Simple nearest interpolation for a given maturity """
    sorted_tenors = sorted(curve.keys())
    closest_tenor = min(sorted_tenors, key = lambda x: abs(x - maturity))

    return curve[closest_tenor]


def present_value(
        cashflows, 
        yield_curve
):
    """ Present value of a given cashflow using simple yield curve """
    
    pv = 0
    for t, cf in enumerate(cashflows, start=1):
        rate = rate_for_maturity(yield_curve, t)
        pv += cf / (1 + rate)**t
    
    return pv
