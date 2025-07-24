import warnings
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def mock_pcc_extract_constants(sample_constants: pd.DataFrame):
    with patch(
        'pgh_colors.calibration.auxiliaries.'
        'PghCalibrationConstant.extract_constants',
    ) as mock_pcc_extract:
        mock_pcc_extract.return_value = sample_constants
        yield mock_pcc_extract


@pytest.fixture
def mock_validate_not_empty():
    with patch('pgh_colors.calibration.auxiliaries._validate_not_empty') as mock_empt:
        mock_empt.side_effect = lambda x: x
        yield mock_empt


@pytest.fixture
def sample_measures_else() -> pd.DataFrame:
    """Return the measures_else df obtained from PghSpectralDistribution."""
    # using frame.insert causes poor performance and generate warning message.
    # decide to ignore them as the df are very small.
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        data = {
            'FORMULA CODE': ['MU000', 'MU000', 'MU999', 'MU999', 'MU043', 'MU043'],
            'BLACK': [0.0, 0.0, 0.0, 0.0, 0.002, 0.002],
            'RED': [0.0, 0.0, 0.0, 0.0, 0.005, 0.005],
            'WHITE': [0.0, 0.0, 0.0, 0.0, 0.063, 0.063],
            'YELLOW': [0.0, 0.0, 0.0, 0.0, 0.03, 0.03],
            'BACKGROUND': ['D', 'L', 'D', 'L', 'D', 'L'],
            'LAB': [
                [10.473, -0.539, -0.91],
                [96.844, -0.503, 1.527],
                [15.62, 0.032, -1.007],
                [94.066, -0.998, 2.751],
                [71.066, 14, 30],
                [94.066, 14, 30],
            ],
        }
        for i in range(400, 701):
            data[i] = np.linspace(0, 1, 6)

        return pd.DataFrame(data)


@pytest.fixture
def sample_constants() -> pd.DataFrame:
    """Return constants dataframe."""
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        data = {
            'PIGMENT': ['card', 'card', 'base', 'base'],
            'VAR': ['Rgk', 'Rgw', 'Rbk', 'Rbw'],
            'PAPER': ['n/a', 'n/a', 'n/a', 'n/a'],
            'FORMULA CODE': ['MU000', 'MU000', 'MU999', 'MU999'],
            'BLACK': [0.0, 0.0, 0.0, 0.0],
            'RED': [0.0, 0.0, 0.0, 0.0],
            'WHITE': [0.0, 0.0, 0.0, 0.0],
            'YELLOW': [0.0, 0.0, 0.0, 0.0],
            'BACKGROUND': ['D', 'L', 'D', 'L'],
            'LAB': [
                [10.473, -0.539, -0.91],
                [96.844, -0.503, 1.527],
                [15.62, 0.032, -1.007],
                [94.066, -0.998, 2.751],
            ],
        }

        for i in range(400, 701):
            data[i] = np.linspace(0, 0.6, 4)

        return pd.DataFrame(data)


@pytest.fixture
def sample_targets() -> pd.DataFrame:
    """Return a targets dataframe."""
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        data = {
            'FORMULA CODE': ['MU043', 'MU043'],
            'BLACK': [0.002, 0.002],
            'RED': [0.005, 0.005],
            'WHITE': [0.063, 0.063],
            'YELLOW': [0.03, 0.03],
            'BACKGROUND': ['D', 'L'],
            'LAB': [
                [71.066, 14, 30],
                [94.066, 14, 30],
            ],
        }
        for i in range(400, 701):
            data[i] = np.linspace(0.8, 1, 2)

        return pd.DataFrame(data)


@pytest.fixture
def sample_monochrome() -> pd.DataFrame:
    """Return a targets dataframe."""
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
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
            data[i] = np.linspace(0, 1, 6)

        return pd.DataFrame(data)


@pytest.fixture
def sample_calibration_df() -> pd.DataFrame:
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        data = {
            'PIGMENT': [
                'card',
                'card',
                'RED',
                'RED',
                'RED',
                'RED',
                'RED',
                'RED',
                'RED',
                'RED',
                'RED',
                'RED',
            ],
            'VAR': [
                'Rgk',
                'Rgw',
                'a',
                'a',
                'b',
                'b',
                'SX',
                'SX',
                'KX',
                'KX',
                'KXSX',
                'KXSX',
            ],
            'PAPER': [
                'n/a',
                'n/a',
                'yon',
                'yon',
                'yon',
                'yon',
                'yon',
                'yon',
                'yon',
                'yon',
                'yon',
                'yon',
            ],
            'FORMULA CODE': [
                'MU000',
                'MU000',
                'MU032',
                'MU031',
                'MU029',
                'MU028',
                'MU030',
                'MU006',
                'MU027',
                'MU032',
                'MU031',
                'MU029',
            ],
            'BLACK': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            'RED': [
                0.0,
                0.0,
                0.0020,
                0.03,
                0.0020,
                0.03,
                0.0020,
                0.03,
                0.0020,
                0.03,
                0.0020,
                0.03,
            ],
            'WHITE': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            'YELLOW': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        }

        columns = list(range(400, 701))
        rng = np.random.default_rng()
        values = rng.uniform(20.0, 25.0, (12, len(columns)))
        simplified_values = np.round(values, 1)

        calib_df = pd.DataFrame(data)
        for i, column in enumerate(columns):
            calib_df[column] = simplified_values[:, i]

        return calib_df


@pytest.fixture
def sample_kx() -> pd.DataFrame:
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        data = {
            'PIGMENT': ['RED', 'RED', 'RED', 'RED'],
            'VAR': ['KX', 'KX', 'KX', 'KX'],
            'PAPER': ['yon', 'yon', 'yon', 'yon'],
            'FORMULA CODE': ['MU032', 'MU031', 'MU029', 'MU028'],
            'BLACK': [0.0, 0.0, 0.0, 0.0],
            'RED': [0.02, 0.03, 0.2, 0.3],
            'WHITE': [0.0, 0.0, 0.0, 0.0],
            'YELLOW': [0.0, 0.0, 0.0, 0.0],
        }

        columns = list(range(400, 701))
        values = np.ones((4, len(columns))) * 1.5

        kx = pd.DataFrame(data)
        for i, column in enumerate(columns):
            kx[column] = values[:, i]

        return kx
