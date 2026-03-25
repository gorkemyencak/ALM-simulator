import numpy as np

class Bond:

    def __init__(
            self,
            face_value: float,
            coupon_rate: float,
            maturity: int
    ):
        self.face_value = face_value
        self.coupon_rate = coupon_rate
        self.maturity = maturity

    
    def generate_cashflow(self):
        """ Generating annual cashflows """
        coupon = self.face_value * self.coupon_rate

        cashflows = [coupon] * self.maturity
        cashflows[-1] += self.face_value # adding principal at maturity

        return np.array(cashflows)
