import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_models() -> pd.DataFrame:
    """Generate a DataFrame similar to the pigments_models structure."""
    data = {
        'PIGMENT': ['YELLOW', 'YELLOW', 'YELLOW', 'RED', 'RED', 'RED'],
        'PAPER': ['yon', 'yon', 'yon', 'yon', 'yon', 'yon'],
        'PREDICT': ['K', 'S', 'KS', 'K', 'S', 'KS'],
        'POLY_DEG': [3, 3, 1, 3, 3, 3],
        'Avg_RMSE': [-0.061084, -0.030828, -0.143427, -0.034868, -0.007056, -0.337608],
        'Std_RMSE': [0.078201, 0.031827, 0.118631, 0.062484, 0.010792, 0.479126],
        'MODELS': [
            '(PolynomialFeatures(degree=3), LinearRegression())',
            '(PolynomialFeatures(degree=3), LinearRegression())',
            '(PolynomialFeatures(degree=1), LinearRegression())',
            '(PolynomialFeatures(degree=3), LinearRegression())',
            '(PolynomialFeatures(degree=3), LinearRegression())',
            '(PolynomialFeatures(degree=3), LinearRegression())',
        ],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_base() -> pd.DataFrame:
    """Generate a DataFrame with base data."""
    pigments = ['card', 'card', 'base', 'base', 'base', 'base', 'base']
    intermediate_variables = ['Rgk', 'Rgw', 'a', 'b', 'S', 'K', 'KS']
    papers = ['n/a', 'n/a', 'yon', 'yon', 'yon', 'yon', 'yon']
    formula_codes = ['MU000', 'MU000', 'MU999', 'MU999', 'MU999', 'MU999', 'MU999']

    black = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    red = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    white = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    yellow = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    wavelengths = np.arange(400, 701, 1)

    pigment_values = {
        'PIGMENT': pigments,
        'VAR': intermediate_variables,
        'PAPER': papers,
        'FORMULA CODE': formula_codes,
        'BLACK': black,
        'RED': red,
        'WHITE': white,
        'YELLOW': yellow,
    }

    for wavelength in wavelengths:
        pigment_values[f'{wavelength}'] = np.linspace(0, 1, 7)

    return pd.DataFrame(pigment_values)
