from src.data_loader.fred_loader import FredDataLoader
from src.data_loader.market_data import save_raw_data

FRED_API_KEY = "41504b53ebf306bcd89ceb69bbd6eba8"

def main():
    loader = FredDataLoader(
        api_key = FRED_API_KEY
    )

    yield_curve = loader.load_yield_curve(
        start_date = '2000-01-01'
    )

    print(yield_curve.head())
    
    save_raw_data(yield_curve, 'yield_curve_fred.csv')

if __name__ == "__main__":
    main()

