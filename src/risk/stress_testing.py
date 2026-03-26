
class StressTesting:

    def __init__(
            self,
            curve
    ):
        
        self.curve = curve
    

    def shock_parallel_up(
            self,
            shock = 0.02
    ):
        
        return {m: r + shock for m, r in self.curve.items()}
    

    def shock_parallel_down(
            self,
            shock = 0.02
    ):
        
        return {m: r - shock for m, r in self.curve.items()}
    
    def shock_steepener(
            self,
            short_shock = 0.005,
            long_shock = 0.02
    ):
        
        shocked_curve = {}

        for m, r in self.curve.items():

            if m <= 2:
                shocked_curve[m] = r + short_shock
            elif m >= 10:
                shocked_curve[m] = r + long_shock
            else:
                shocked_curve[m] = r + (short_shock + long_shock) / 2
        
        return shocked_curve
    

    def shock_flattener(
            self,
            short_shock = 0.02,
            long_shock = 0.005
    ):
        
        shocked_curve = {}

        for m, r in self.curve.items():

            if m <= 2:
                shocked_curve[m] = r + short_shock
            elif m >= 10:
                shocked_curve[m] = r + long_shock
            else:
                shocked_curve[m] = r + (short_shock + long_shock) / 2
        
        return shocked_curve


    def run_stress_test(
            self,
            portfolio,
            deposit_model,
            pricing_function,
            liability_pv_function
    ):
        
        scenarios = {
            'Base': self.curve,
            'Parallel Up +200bps': self.shock_parallel_up(),
            'Parallel Down -200bps': self.shock_parallel_down(),
            'Steepener': self.shock_steepener(),
            'Flattener': self.shock_flattener()
        }

        results = []

        for name, shocked_curve in scenarios.items():

            # Assets
            asset_value = portfolio.total_value(
                yield_curve = shocked_curve,
                pricing_function = pricing_function
            )

            # Liabilities
            cashflows = deposit_model.generate_cashflows(
                years = 10
            )
            liability_value = liability_pv_function(
                cashflows = cashflows,
                yield_curve = shocked_curve
            )

            equity = asset_value - liability_value
            funding_ratio = asset_value / liability_value

            results.append({
                'scenario': name,
                'assets': asset_value,
                'liabilities': liability_value,
                'equity': equity,
                'funding_ratio': funding_ratio
            })
        
        return results