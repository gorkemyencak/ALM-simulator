import numpy as np
import pandas as pd

def fit_ar1(series: pd.Series):
    """ Fit AR(1): X_t = mu + phi*(X_{t-1} - mu) + eps_t """

    x = series.values
    x_lag = x[:-1]
    x_next = x[1:]

    # estimate phi
    phi = np.corrcoef(x_lag, x_next)[0, 1]

    # long-run mean
    mu = np.mean(x)

    # residuals
    residuals = x_next - (mu + phi * (x_lag - mu))
    sigma = np.std(residuals)

    return {
        'mu': mu, 'phi': phi, 'sigma': sigma
    }


def calibrate_factor_models(pca_factors: pd.DataFrame):
    """ Fit AR(1) to each PCA factor column """
    models = {}

    for col in pca_factors.columns:
        models[col] = fit_ar1(pca_factors[col])
    
    return models


def simulate_factor_paths(
        models,
        n_steps = 120,
        n_sims = 1000,
        seed = 7
):
    """
    Simulate AR(1) paths for each PCA factor

    Returns:
        dict of arrays [n_sims, n_steps] per factor
    """

    np.random.seed(seed)
    simulations = {}

    for factor, params in models.items():

        mu = params['mu']
        phi = params['phi']
        sigma = params['sigma']

        paths = np.zeros((n_sims, n_steps))
        paths[:, 0] = mu # start at long-run mean

        for t in range(1, n_steps):
            shocks = np.random.normal(0, 1, n_sims)
            paths[:, t] = (
                mu
                + phi * (paths[:, t-1] - mu)
                + sigma * shocks
            )
        
        simulations[factor] = paths
    
    return simulations


def rebuild_yield_curves(
        factor_paths,
        eigenvectors,
        mean_curve
):
    """ 
    Convert factor simulations into full yield curves

    Returns:
        yield_curves -> shape: [n_sims, n_steps, n_maturities] 
    """
    factors = list(factor_paths.keys())
    n_sims, n_steps = next(iter(factor_paths.values())).shape
    n_maturities = eigenvectors.shape[1]

    yield_curves = np.zeros((n_sims, n_steps, n_maturities))

    for s in range(n_sims):
        for t in range(n_steps):

            curve = mean_curve.copy()

            for i, factor in enumerate(factors):
                curve += factor_paths[factor][s, t] * eigenvectors[i]
            
            yield_curves[s, t] = curve
    
    return yield_curves


def yield_to_discount(yield_curves, maturities):
    """ Convert zero-rates to discount factors """
    maturities = np.array(maturities)
    discount_factors = np.exp(-yield_curves * maturities)

    return discount_factors


# pipeline function
def generate_yield_curve_scenarios(
        pca_factors,
        eigenvectors,
        mean_curve,
        maturities,
        n_steps = 120,
        n_sims = 1000
):
    """
    Full pipeline:
    PCA factors -> simulate -> rebuild curves -> discount factors
    """

    # 1. Calibrate AR(1) models
    models = calibrate_factor_models(
        pca_factors = pca_factors
    )

    # 2. Simulate factor paths
    factor_paths = simulate_factor_paths(
        models = models,
        n_steps = n_steps,
        n_sims = n_sims
    )

    # 3. Rebuild yield curves
    yield_curves = rebuild_yield_curves(
        factor_paths = factor_paths,
        eigenvectors = eigenvectors,
        mean_curve = mean_curve
    )

    # 4. Discount factors
    discount_factors = yield_to_discount(
        yield_curves = yield_curves,
        maturities = maturities
    )

    return yield_curves, discount_factors

