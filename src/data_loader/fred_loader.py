import pandas as pd
from fredapi import Fred

class FredDataLoader:

    def __init__(self, api_key: str):
        self.fred = Fred(api_key = api_key)
    

    def load_yield_curve(
            self,
            start_date = '2000-01-01'
    ) -> pd.DataFrame:
        """ Loading Treasury yields from FRED """

        series_ids = {
            'DGS1': '1Y',
            'DGS2': '2Y',
            'DGS5': '5Y',
            'DGS10': '10Y',
            'DGS30': '30Y'
        }

        data = {}

        for fred_id, label in series_ids.items():
            series = self.fred.get_series(
                fred_id, 
                observation_start = start_date
            )

            data[label] = series
        
        df = pd.DataFrame(data)
        df.index.name = 'date'

        return df
    
    
