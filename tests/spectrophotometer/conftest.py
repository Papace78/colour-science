from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def valid_measures_input() -> pd.DataFrame:
    """Returns a valid DataFrame matching the reflectance schema."""
    return pd.DataFrame(
        {
            'NAME': ['MU000_D', 'MU000_D', 'MU000_D'],  # schema enforces three measures
            'DATE': ['2024-11-19', '2024-11-19', '2024-11-19'],
            '400': [50.23, 50.51, 50.12],
            '400.1': [50.23, 50.51, 50.12],
            '400.2': [50.23, 50.51, 50.12],
            '400.3': [50.23, 50.51, 50.12],
            '400.4': [50.23, 50.51, 50.12],
            '410': [50.32, 50.67, 50.15],
            '420': [60.15, 60.99, 60.22],
            '430': [70.98, 70.56, 70.23],
            '440': [80.24, 80.62, 80.49],
            '450': [90.10, 90.33, 90.56],
            '460': [50.22, 50.59, 50.48],
            '470': [60.76, 60.11, 60.87],
            '480': [70.31, 70.99, 70.65],
            '490': [80.55, 80.88, 80.25],
            '500': [90.65, 90.21, 90.75],
            '510': [50.11, 50.45, 50.89],
            '520': [60.37, 60.83, 60.22],
            '530': [70.77, 70.44, 70.56],
            '540': [80.90, 80.34, 80.65],
            '550': [90.12, 90.50, 90.72],
            '560': [50.92, 50.55, 50.28],
            '570': [60.43, 60.56, 60.77],
            '580': [70.22, 70.11, 70.33],
            '590': [80.11, 80.25, 80.62],
            '600': [90.54, 90.23, 90.99],
            '610': [50.99, 50.21, 50.66],
            '620': [60.78, 60.10, 60.34],
            '630': [70.99, 70.87, 70.55],
            '640': [80.78, 80.21, 80.56],
            '650': [90.54, 90.32, 90.21],
            '660': [50.77, 50.33, 50.99],
            '670': [60.88, 60.99, 60.23],
            '680': [70.77, 70.55, 70.44],
            '690': [80.88, 80.99, 80.76],
            '700': [90.11, 90.55, 90.33],
            '700.1': [90.11, 90.55, 90.33],
            '700.2': [90.11, 90.55, 90.33],
            '700.3': [90.11, 90.55, 90.33],
            '700.4': [90.11, 90.55, 90.33],
            '700.5': [90.11, 90.55, 90.33],
        },
    )


@pytest.fixture
def mock_formulas_import_csv_as_dataframe():
    with patch(
        'pgh_colors.spectrophotometer.formulas.'
        'PghFormula.import_csv_as_dataframe',
    ) as mock_formulas_df:
        mock_formulas_df.return_value = pd.DataFrame(
            [[0.1, 0.0, 0.0, 0.0], [0.1, 0.2, 0.3, 0.4]],
            columns=pd.Index(['BLACK', 'RED', 'WHITE', 'YELLOW'], name='PIGMENT'),
            index=pd.Index(['MU003', 'MU043'], name='FORMULA CODE'),
        )
        yield mock_formulas_df


@pytest.fixture
def mock_measures_import_csv_as_dataframe():
    with patch(
        'pgh_colors.spectrophotometer.measurements.'
        'PghMeasures.import_csv_as_dataframe',
    ) as mock_measures_df:
        mock_measures_df.return_value = pd.DataFrame(
            [['MU043', 'D', 0.9, 0.8, 0.7]],
            columns=['FORMULA CODE', 'BACKGROUND', 400, 410, 420],
        )
        yield mock_measures_df


@pytest.fixture
def expected_merged_df() -> pd.DataFrame:
    """Merged of both abovementionned example df."""
    return pd.DataFrame(
        [
            ['MU003', 0.1, 0.0, 0.0, 0.0, np.nan, np.nan, np.nan, np.nan],
            ['MU043', 0.1, 0.2, 0.3, 0.4, 'D', 0.9, 0.8, 0.7],
        ],
        columns=[
            'FORMULA CODE',
            'BLACK',
            'RED',
            'WHITE',
            'YELLOW',
            'BACKGROUND',
            400,
            410,
            420,
        ],
    )


@pytest.fixture
def expected_filtered_for_measured_df() -> pd.DataFrame:
    """return only the formulas that have been measured in expected_merged_df."""
    return pd.DataFrame(
        [['MU043', 0.1, 0.2, 0.3, 0.4, 'D', 0.9, 0.8, 0.7]],
        columns=[
            'FORMULA CODE',
            'BLACK',
            'RED',
            'WHITE',
            'YELLOW',
            'BACKGROUND',
            400,
            410,
            420,
        ],
    )


@pytest.fixture
def expected_filtered_for_not_measured_df() -> pd.DataFrame:
    """return only the formulas that have not been measured in expected_merged_df."""
    return pd.DataFrame(
        [['MU003', 0.1, 0.0, 0.0, 0.0]],
        columns=['FORMULA CODE', 'BLACK', 'RED', 'WHITE', 'YELLOW'],
    )
