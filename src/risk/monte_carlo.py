import numpy as np

from src.risk.duration_gap import portfolio_duration, liability_duration, duration_gap

from src.curve_model.factor_simulator import generate_yield_curve_scenarios

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

            # -- DURATIONS --
            duration_asset = portfolio_duration(
                portfolio = self.portfolio,
                yield_curve = curve,
                pricing_function = self.pricing_function
            )

            duration_liability = liability_duration(
                cashflows = cashflows,
                yield_curve = curve
            )

            gap = duration_gap(
                asset_duration = duration_asset,
                liability_duration = duration_liability
            )

            # -- METRICS --
            equity = asset_value - liability_value
            funding_ratio = asset_value / liability_value if liability_value != 0 else np.nan

            results.append({
                'assets': asset_value,
                'liabilities': liability_value,
                'equity': equity,
                'funding_ratio': funding_ratio,
                'asset_duration': duration_asset,
                'liability_duration': duration_liability,
                'duration_gap': gap
            })
            
        return results
    

    def run_simulation_pca(
            self,
            assets,
            liabilities,
            pca_factors,
            eigenvectors,
            mean_curve,
            maturities,
            n_sims = 1000,
            n_steps = 120 # valuation horizon (10Y)           
    ):
        """ ALM Monte Carlo using PCA yield curve scenarios """
        # 1. Generate yield curve scenarios
        yield_curve, discount_factors = generate_yield_curve_scenarios(
            pca_factors = pca_factors,
            eigenvectors = eigenvectors,
            mean_curve = mean_curve,
            maturities = maturities,
            n_steps = n_steps,
            n_sims = n_sims
        )

        # use last time step for valuation horizon (10Y)
        dfs_T = discount_factors[:, -1, :] # disc_fact shape -> [n_sims, n_steps, n_maturities]

        # 2. Value assets under scenarios
        asset_values = []

        for sim in range(n_sims):
            df_curve = dfs_T[sim]

            pv_assets = 0.0
            for asset in assets:
                maturity_idx = np.argmin(
                    np.abs(np.array(maturities) - asset['maturity'])
                )

                df = df_curve[maturity_idx]
                pv_assets += asset['notional'] * df
            
            asset_values.append(pv_assets)
        
        asset_values = np.array(asset_values)

        # 3. Value liabilities under scenarios
        liability_values = []

        for sim in range(n_sims):
            df_curve = dfs_T[sim]

            pv_liabilities = 0.0
            for liability in liabilities:
                maturity_idx = np.argmin(
                    np.abs(np.array(maturities) - liability['maturity'])
                )

                df = df_curve[maturity_idx]
                pv_liabilities += liability['notional'] * df
            
            liability_values.append(pv_liabilities)
        
        liability_values = np.array(liability_values)

        # 4. Compute ALM Metrics
        equity = asset_values - liability_values
        funding_ratio = asset_values / liability_values
        underfunding_probability = np.mean(funding_ratio < 1)

        results = {
            'asset_values': asset_values,
            'liability_values': liability_values,
            'equity': equity,
            'funding_ratio': funding_ratio,
            'underfunding_probability': underfunding_probability,
            'yield_curves': yield_curve,
            'discount_factors': discount_factors,
            'maturities': maturities
        }

        return results

        


