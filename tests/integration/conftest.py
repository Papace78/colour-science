import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def mock_rg() -> pd.DataFrame:
    """Return constants dataframe."""
    data = {
        'PIGMENT': ['card', 'card'],
        'VAR': ['Rgk', 'Rgw'],
        'PAPER': ['n/a', 'n/a'],
        'FORMULA CODE': ['MU000', 'MU000'],
        'BLACK': [0.0, 0.0],
        'RED': [0.0, 0.0],
        'WHITE': [0.0, 0.0],
        'YELLOW': [0.0, 0.0],
        'BACKGROUND': ['D', 'L'],
        'LAB': [
            [10.473, -0.539, -0.91],
            [96.844, -0.503, 1.527],
        ],
    }

    for i in range(400, 701):
        data[i] = np.linspace(0.01, 0.9, 2)

    return pd.DataFrame(data)


@pytest.fixture
def mock_monochrome(lb: float = 0.00001, ub: float = 0.99) -> pd.DataFrame:
    """Return a monochrome dataframe."""
    data = {
        'FORMULA CODE': ['MU032', 'MU032', 'MU033', 'MU033', 'MU034', 'MU034'],
        'BLACK': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'RED': [0.005, 0.005, 0.1, 0.1, 0.5, 0.5],
        'WHITE': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'YELLOW': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'BACKGROUND': ['D', 'L', 'D', 'L', 'D', 'L'],
        'LAB': [
            [71.066, 14, 30],
            [94.066, 14, 30],
            [71.066, 15, 40],
            [94.066, 15, 40],
            [71.066, 15, 60],
            [94.066, 15, 60],
        ],
    }
    for i in range(400, 701):
        data[i] = [lb, lb, 0.0008 * i, 0.0012 * i, ub, ub]

    return pd.DataFrame(data)
