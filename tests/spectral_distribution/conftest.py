from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def saunderson_default_params() -> tuple:
    r1 = 0.02
    r2 = 0.4
    alpha = 0.0
    return r1, r2, alpha


@pytest.fixture
def refl_input() -> pd.Series:
    return pd.Series(np.linspace(0, 1, 31), index=np.linspace(400, 700, 31))


@pytest.fixture
def sample_measurements():
    return pd.DataFrame(
        {
            'BLACK': [0, 0],
            'RED': [1, 0],
            'WHITE': [0, 0],
            'YELLOW': [0, 0],
            'BACKGROUND': ['D', 'L'],
            400: [0.5, 0.1],
            500: [0.6, 0.2],
            600: [0.7, 0.3],
            700: [0.8, 0.4],
        },
    )


@pytest.fixture
def sample_formulas():
    return pd.DataFrame(
        {
            'BLACK': [0, 0],
            'RED': [1, 0],
            'WHITE': [0, 0],
            'YELLOW': [0, 0],
            'BACKGROUND': ['D', 'L'],
        },
    )


@pytest.fixture
def sample_measures():
    return pd.DataFrame(
        {
            400: [0.5, 0.1],
            500: [0.6, 0.2],
            600: [0.7, 0.3],
            700: [0.8, 0.4],
        },
    )


@pytest.fixture
def cmfs() -> str:
    return ('CIE 1964 10 Degree Standard Observer',)


@pytest.fixture
def illuminant() -> str:
    return 'illuminant'


@pytest.fixture
def mock_cs_api_spectral_distribution():
    with patch(
        'pgh_colors.spectral_distribution.converters.SpectralDistribution',
    ) as msd:
        mock_sd = MagicMock()
        msd.return_value = mock_sd
        mock_sd.align.return_value = mock_sd
        yield mock_sd, msd
