import numpy as np
import pandas as pd

from sklearn.decomposition import PCA

class PCAYieldCurveModel:
    """ PCA-based yield curve factor model """
    def __init__(self, n_components: int = 3):
        self.n_components = n_components
        self.pca = PCA (n_components = self.n_components)

        self.maturities = None
        self.mean_curve = None
        self.loadings = None
        self.factor_history = None

    
    def prepare_matrix(
            self,
            df_rates: pd.DataFrame
    ):
        
        # keep maturities order
        self.maturities = list(df_rates.columns)

        # converting to numpy matrix
        yield_matrix = df_rates.values

        return yield_matrix
    

    def compute_yield_changes(
            self,
            yield_matrix
    ):
        """ Compute daily changes in yield curve """
        dy = np.diff(yield_matrix, axis = 0)

        return dy
    

    def fit(
            self,
            df_rates
    ):
        """ Fit PCA on yield changes """
        Y = self.prepare_matrix(df_rates)
        dy = self.compute_yield_changes(Y)

        # fit PCA
        self.pca.fit(dy)

        # store results
        self.loadings = self.pca.components_
        self.factor_history = self.pca.transform(dy)
        self.mean_curve = Y[-1] # last observed curve

        return self.factor_history
    

    def explained_variance(self):

        return self.pca.explained_variance_ratio_
    

    def transform(
            self,
            yield_changes
    ):
        
        return self.pca.transform(yield_changes)
    

    def inverse_transform(
            self,
            factors
    ):
        """ Converts factors into yield changes """
        return self.pca.inverse_transform(factors)
    

    def reconstruct_curve(
            self,
            simulated_dy
    ):
        """ Build yield curve path from simulated changes """
        curves = [self.mean_curve]

        for dy in simulated_dy:
            new_curve = curves[-1] + dy
            curves.append(new_curve)
        
        return np.array(curves)
    

    def curve_vector_to_dict(
            self,
            curve_vector
    ):
        """ Convert curve vector into dictionary format """
        return {
            maturity: rate for maturity, rate in zip(self.maturities, curve_vector)
        }


