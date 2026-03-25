import numpy as np

class DepositModel:

    def __init__(
            self,
            initial_amount: float,
            decay_rate: float
    ):
        
        self.initial_amount = initial_amount
        self.decay_rate = decay_rate
    

    def generate_cashflows(
            self,
            years: int
    ):
        """ Simulating yearly withdrawals and returning the list of withdrawals per each year """
        balances = []
        current = self.initial_amount

        for t in range(years):
            withdrawal = current * (1 - self.decay_rate)
            balances.append(withdrawal)
            current -= withdrawal
        
        return np.array(balances)
