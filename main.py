from src.data_loader.fred_loader import FredDataLoader
from src.data_loader.market_data import save_raw_data, save_processed_data
from src.data_loader.data_cleaning import clean_yield_curve

FRED_API_KEY = "41504b53ebf306bcd89ceb69bbd6eba8"

def main():
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


if __name__ == "__main__":
    main()

