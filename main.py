import numpy as np
import pandas as pd

from src.data_loader.fred_loader import FredDataLoader
from src.data_loader.market_data import save_raw_data, save_processed_data
from src.data_loader.data_cleaning import clean_yield_curve

from src.utils.rate_utils import GetRates

from src.assets.bond import Bond
from src.assets.portfolio import BondPortfolio
from src.assets.pricing import price_bond

from src.liabilities.deposit_model import DepositModel
from src.liabilities.cashflow_generator import present_value

from src.rates.hull_white import HullWhite

from src.risk.monte_carlo import MonteCarlo

FRED_API_KEY = "41504b53ebf306bcd89ceb69bbd6eba8"

def main():

    ### --- LOAD DATA ---
    loader = FredDataLoader(
        api_key = FRED_API_KEY
    )

    # loading raw data
    yield_curve = loader.load_yield_curve(
        start_date = '2000-01-01'
    )
    save_raw_data(yield_curve, 'yield_curve_fred.csv')

    print(yield_curve.head())

    # cleaning raw data 
    yield_curve_clean = clean_yield_curve(yield_curve)
    save_processed_data(yield_curve_clean, 'cleaned_yield_curve_fred.csv')

    print(yield_curve_clean.head())

    # latest yield curve
    curve = GetRates().get_latest_curve(yield_curve_clean)
    print(f"Latest yield curve: {curve}")

    ### --- ASSETS ---
    # sample bond portfolio
    bonds = [
        Bond(face_value=1000, coupon_rate=0.02, maturity=3),
        Bond(face_value=1000, coupon_rate=0.03, maturity=5),
        Bond(face_value=1000, coupon_rate=0.04, maturity=10)
    ]

    bond_portfolio = BondPortfolio(bonds)
    print(f'Curve: {curve}')
    asset_value = bond_portfolio.total_value(curve, price_bond)

    ### --- LIABILITIES ---
    # a sample deposit
    deposit_model = DepositModel(initial_amount=10000, decay_rate=0.98)
    liability_cashflows = deposit_model.generate_cashflows(years=10)
    liability_value = present_value(
        cashflows=liability_cashflows,
        yield_curve=curve
    )

    ### --- BALANCE SHEET ---
    print("\n--- BALANCE SHEET ---")
    print(f"Assets Value: {asset_value:.2f}")
    print(f"Liabilities Value: {liability_value:.2f}")
    print(f"Equity Gap: {(asset_value - liability_value):.2f}")

    ### --- INT RATE SIMULATION MODEL ---
    r0 = GetRates().get_short_rate(curve)
    theta = np.mean(list(curve.values()))

    int_rate_model = HullWhite(
        a = 0.1,            # mean-reversion
        sigma = 0.01,       # volatility
        initial_rate = r0,
        theta = theta
    )

    # generating simulated interest rate paths
    int_rate_paths = int_rate_model.simulate_paths(
        n_paths = 1000,
        n_steps = 60,
        dt = 1.0 # yearly
    )

    print(f"Simulated rates shape: {int_rate_paths.shape}")
    print(f"First 5 steps in the first simulated path: {int_rate_paths[0, :5 ]}")

    # --- MONTE CARLO ---
    alm_mc = MonteCarlo(
        portfolio = bond_portfolio,
        deposit_model = deposit_model,
        pricing_function = price_bond,
        liability_pv_function = present_value
    )

    results = alm_mc.run_simulation(
        rate_paths = int_rate_paths,
        dt = 1.0 # yearly
    )

    df_results = pd.DataFrame(results)
    print(df_results.head())


if __name__ == "__main__":
    main()

