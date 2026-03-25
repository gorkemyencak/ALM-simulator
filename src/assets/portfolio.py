class BondPortfolio:

    def __init__(
            self, 
            bonds: list
    ):
        
        self.bonds = bonds


    def total_value(
            self, 
            yield_curve,
            pricing_function
    ):
        
        portfolio_value = sum(pricing_function(bond, yield_curve) for bond in self.bonds) 
        return portfolio_value
