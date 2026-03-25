import numpy as np

class MonteCarlo:

    def __init__(
            self,
            portfolio,
            deposit_model,
            pricing_function,
            liability_pv_function
    ):
        
        self.portfolio = portfolio
        self.deposit_model = deposit_model
        self.pricing_function = pricing_function
        self.liability_pv_function = liability_pv_function

    
    def run_simulation(
            self,
            rate_paths,
            dt = 1.0
    ):
        """ Assumption: we will use short rate as flat discount curve approximation """
        # rate_paths: (n_paths, n_steps)
        n_paths, n_steps = rate_paths.shape

        results = []

        for i in range(n_paths):
            path = rate_paths[i]

            # use average rate as proxy for discounting
            avg_rate = np.mean(path)

            # build simple flat curve
            curve = {
                1: avg_rate,
                2: avg_rate,
                5: avg_rate,
                10: avg_rate,
                30: avg_rate
            }

            # -- ASSETS --
            asset_value = self.portfolio.total_value(
                yield_curve = curve,
                pricing_function = self.pricing_function
            )

            # -- LIABILITIES --
            cashflows = self.deposit_model.generate_cashflows(
                years = 10
            )

            liability_value = self.liability_pv_function(
                cashflows = cashflows,
                yield_curve = curve
            )

            # -- METRICS --
            equity = asset_value - liability_value
            funding_ratio = asset_value / liability_value if liability_value != 0 else np.nan

            results.append({
                'assets': asset_value,
                'liabilities': liability_value,
                'equity': equity,
                'funding_ratio': funding_ratio
            })
            
        return results


