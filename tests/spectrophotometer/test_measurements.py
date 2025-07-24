from unittest.mock import patch

import numpy as np
import pandas as pd
import pandera as pa
import pytest

from colour_science.spectrophotometer.measurements import PghMeasures
from colour_science.spectrophotometer.spectro_file_schema import reflectance_schema


def test_import_csv_as_dataframe(mono_red_path: str) -> None:
    with patch(
        'pgh_colors.spectrophotometer.measurements.PghMeasures._process_file',
    ) as mock_process_file:
        _ = PghMeasures.import_csv_as_dataframe(mono_red_path)
        mock_process_file.assert_called_once()


def test_process_file(mono_red_path: str) -> None:
    measures = PghMeasures._process_file(mono_red_path)
    assert isinstance(measures, pd.DataFrame)
    assert measures.shape == (18, 33)
    assert not measures.isna().any().any()
    assert (
        measures.groupby('FORMULA CODE')['BACKGROUND'].nunique() == len(['D', 'L'])
    ).all()
    np.array_equal(measures['BACKGROUND'].unique(), ['D', 'L'])
    np.array_equal(
        measures.columns,
        ['FORMULA CODE', 'BACKGROUND', *np.arange(400, 710, 10).astype(int)],
    )


def test_import_measures_ok(valid_measures_input: pd.DataFrame) -> None:
    reflectance_schema.validate(valid_measures_input)


def test_import_measures_ko(valid_measures_input: pd.DataFrame) -> None:
    errors = {
        '.*Missing reference to background in NAME.*': valid_measures_input.assign(
            NAME='MU000',
        ),
        r'.*less_than_or_equal_to\(100\).*': valid_measures_input.assign(
            **{'400': 150},
        ),
        r'.*greater_than_or_equal_to\(0\).*': valid_measures_input.assign(
            **{'400': -0.1},
        ),
        r'column .*\d+.* not in dataframe': valid_measures_input.drop('450', axis=1),
        r'column .*\d+.* not in DataFrameSchema': valid_measures_input.assign(
            **{'800': 50},
        ),
        '.*Must have three measures per background.*': valid_measures_input.iloc[
            [0, 1]
        ],
    }
    for error, corrupted_df in errors.items():
        with pytest.raises(pa.errors.SchemaError, match=error):
            reflectance_schema.validate(corrupted_df)


@pytest.mark.parametrize(
    'expected_df',
    [
        pd.DataFrame(
            {
                'NAME': ['MU043_D', 'MU043_D'],
                'DATE': ['2024-11-19', '2024-11-19'],
                '400': [50.23, 50.51],
                '400.1': [50.23, 50.51],
            },
        ),
    ],
)
def test_strip_strings(expected_df) -> None:
    corrupted_df = expected_df.copy()
    corrupted_df['NAME'] = ['   MU043_D', 'MU043_D ']
    corrupted_df.columns = ['    NAME', ' DATE ', '400    ', '400.1']
    returned_df = PghMeasures._strip_strings(corrupted_df)
    pd.testing.assert_frame_equal(returned_df, expected_df)


@pytest.mark.parametrize(
    ('input_df', 'expected_df'),
    [
        (
            pd.DataFrame(
                {
                    'NAME': ['MU043_D', 'MU043_D'],
                    'DATE': ['2024-11-19', '2024-11-19'],
                    '400': [50.23, 50.51],
                    '400.1': [50.23, 50.51],
                },
            ),
            pd.DataFrame(
                {
                    'NAME': ['MU043_D', 'MU043_D'],
                    'DATE': ['2024-11-19', '2024-11-19'],
                    '400': [50.23, 50.51],
                },
            ),
        ),
    ],
)
def test_remove_duplicated_wavelengths(input_df, expected_df) -> None:
    returned_df = PghMeasures._remove_duplicated_wavelengths(input_df)
    pd.testing.assert_frame_equal(returned_df, expected_df)


@pytest.mark.parametrize(
    ('input_df', 'expected_df'),
    [
        (
            pd.DataFrame(
                {
                    'NAME': ['MU043_D', 'MU043_D'],
                    'DATE': ['2024-11-19', '2024-11-19'],
                    '400': [50.23, 50.51],
                },
            ),
            pd.DataFrame(
                {
                    'NAME': ['MU043_D', 'MU043_D'],
                    '400': [50.23, 50.51],
                },
            ),
        ),
    ],
)
def test_drop_date_column(input_df, expected_df) -> None:
    returned_df = PghMeasures._drop_date_column(input_df)
    pd.testing.assert_frame_equal(returned_df, expected_df)


@pytest.mark.parametrize(
    ('input_df', 'expected_df'),
    [
        (
            pd.DataFrame(
                {
                    'NAME': ['MU043_D', 'MU043_D'],
                    '400': [100, 0],
                },
            ),
            pd.DataFrame(
                {
                    '400': [50.0],
                },
                index=pd.Index(['MU043_D'], name='NAME'),
            ),
        ),
    ],
)
def test_average_measures_by_background(input_df, expected_df) -> None:
    returned_df = PghMeasures._average_measures_by_background(input_df)
    pd.testing.assert_frame_equal(returned_df, expected_df)


@pytest.mark.parametrize(
    ('input_df', 'expected_df'),
    [
        (
            pd.DataFrame(
                {
                    '400': [50.0],
                },
                index=pd.Index(['MU043_D'], name='NAME'),
            ),
            pd.DataFrame(
                {
                    '400': [0.5],
                },
                index=pd.Index(['MU043_D'], name='NAME'),
            ),
        ),
    ],
)
def test_scale_reflectances_values(input_df, expected_df) -> None:
    returned_df = PghMeasures._scale_reflectances_values(input_df)
    pd.testing.assert_frame_equal(returned_df, expected_df)


@pytest.mark.parametrize(
    'input_df',
    [
        pd.DataFrame(
            [[0.5] * len(np.arange(400, 710, 10))],
            column...
            .
            .
            .
