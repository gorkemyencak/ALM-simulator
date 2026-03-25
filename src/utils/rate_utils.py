import pandas as pd

class GetRates:

    @staticmethod
    def get_latest_curve(
            df: pd.DataFrame
    ) -> dict:
        """
        Extracting latest yield curve as dictionary

        These rates will be used for:
            - discounting bond cashflows
            - computing PV of liabilities
        """
        df = df.copy()
        #df = df.set_index('date')
        # most recent yield curve
        curve = df.iloc[-1] 

        curve_dict = {
            1: round(float(curve['1Y']), 6),
            2: round(float(curve['2Y']), 6),
            5: round(float(curve['5Y']), 6),
            10: round(float(curve['10Y']), 6),
            30: round(float(curve['30Y']), 6)
        }

        return curve_dict
    

    @staticmethod
    def get_short_rate(
        curve: dict
    ):
        """ Use 1Y as proxy for short rate """
        return curve[1]
