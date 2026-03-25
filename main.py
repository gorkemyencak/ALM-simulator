from src.data_loader.fred_loader import FredDataLoader
from src.data_loader.market_data import save_raw_data, save_processed_data
from src.data_loader.data_cleaning import clean_yield_curve

from src.utils.rate_utils import GetRates

from src.assets.bond import Bond
from src.assets.portfolio import BondPortfolio
from src.assets.pricing import price_bond

from src.liabilities.deposit_model import DepositModel
from src.liabilities.cashflow_generator import present_value

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


if __name__ == "__main__":
    main()

