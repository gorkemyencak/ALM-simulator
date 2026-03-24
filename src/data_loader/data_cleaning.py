import pandas as pd

def clean_yield_curve(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # ensuring datetime index
    df = df.reset_index()
    df['date_datetime'] = pd.to_datetime(df['date'])
    df = (
        df
        .drop(columns=['date'])
        .set_index('date_datetime')
    )
    df.index.name = 'date'

    # ensuring sorted index
    df = df.sort_index()

    # forward fill missing values
    df = df.ffill()

    # dropping NaNs at the start of the series if any 
    df = df.dropna()

    # Converting yield curves in percentages to decimals
    df = df / 100.0

    return df