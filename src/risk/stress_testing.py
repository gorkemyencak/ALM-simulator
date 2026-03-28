import numpy as np 

class StressTesting:
    """ Interest rate stress testing engine, works with PCA ALM simulator outputs """

    def __init__(
            self,
            maturities
    ):
        
        self.maturities = np.asarray(maturities, dtype = float)
    

    def shock_parallel_up(
            self,
            curve,
            shock = 0.02
    ):

        return [r + shock for r in curve]
    

    def shock_parallel_down(
            self,
            curve,
            shock = 0.02
    ):
        
        return [r - shock for r in curve]
    
    
    def shock_steepener(
            self,
            curve,
            shock_bps = 0.02
    ):
        """ Long rates up, Short rates down """
        slope = (self.maturities - self.maturities.min()) / (self.maturities.max() - self.maturities.min()) # ranges between 0 and 1

        # - short on short end, +shock on long end
        shock_vector = (slope - 0.5) * 2 * shock_bps
         
        return curve + shock_vector
    

    def shock_flattener(
            self,
            curve,
            shock_bps = 0.02
    ):
                
        return self.shock_steepener(curve = curve, shock_bps = -shock_bps)
    

    def discount_factors(self, curve):
        """ Converts zero-curve into discount factors """
        curve = np.asarray(curve, dtype = float)
        return np.exp(-curve * self.maturities)
    

    def pv_cashflows(self, cashflows, disc_fact):

        pv = 0.0
        for item in cashflows:
            idx = np.argmin(np.abs(self.maturities - item['maturity']))
            pv += item['notional'] * disc_fact[idx]
        
        return pv


    def run_stress_test(
            self,
            base_curve,
            assets,
            liabilities
    ):
        
        scenarios = {
            'Base': lambda c: c,
            'Parallel Up +200bps': self.shock_parallel_up,
            'Parallel Down -200bps': self.shock_parallel_down,
            'Steepener': self.shock_steepener,
            'Flattener': self.shock_flattener
        }

        results = []

        for name, shock_fn in scenarios.items():

            shocked_curve = np.asarray(shock_fn(np.asarray(base_curve).copy()), dtype=float)
            dfs = self.discount_factors(curve = shocked_curve)

            # Assets
            asset_value = self.pv_cashflows(cashflows = assets, disc_fact = dfs)

            # Liabilities
            liability_value = self.pv_cashflows(cashflows = liabilities, disc_fact = dfs)

            equity = asset_value - liability_value
            funding_ratio = asset_value / liability_value

            results.append({
                'scenario': name,
                'assets': asset_value,
                'liabilities': liability_value,
                'equity': equity,
                'funding_ratio': funding_ratio,
                'curve': shocked_curve
            })
        
        return results