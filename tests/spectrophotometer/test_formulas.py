from unittest.mock import patch

import numpy as np
import pandas as pd
import pandera as pa
import pytest

from colour_science.spectrophotometer.formulas import PghFormula
from colour_science.spectrophotometer.spectro_file_schema import composition_schema


def test_import_csv_as_dataframe(formulas_path: str) -> None:
    with patch(
        'pgh_colors.spectrophotometer.formulas.PghFormula._process_file',
    ) as mock_process_file:
        _ = PghFormula.import_csv_as_dataframe(formulas_path)
        mock_process_file.assert_called_once()


def test_process_file(formulas_path: str) -> None:
    compositions = PghFormula._process_file(formulas_path)
    assert isinstance(compositions, pd.DataFrame)
    assert compositions.shape == (59, 4)
    assert 'MU000' in compositions.index
    assert 'MU999' in compositions.index
    np.array_equal(compositions.columns, ['BLACK', 'RED', 'WHITE', 'YELLOW'])


@pytest.mark.parametrize(
    'input_df',
    [
        pd.DataFrame(
            {
                'FORMULA CODE': ['MU000', 'MU999', 'MU999', 'MU999', 'MU999'],
                'PIGMENT': ['NUDE', 'WHITE', 'BLACK', 'RED', 'YELLOW'],
                'BATCH': ['K-64602', 'K-64602', 'K-64602', 'K-64602', 'K-64602'],
                'ADDED WEIGHT': [0, 0, 0, 0, 0],
            },
        ),
    ],
)
def test_import_formulas_ok(input_df) -> None:
    composition_schema.validate(input_df)


@pytest.mark.parametrize(
    ('input_df', 'error'),
    [
        (
            pd.DataFrame(
                {
                    'FORMULA CODE': ['MU000'],
                    'PIGMENT': ['NUDE'],
                    'BATCH': ['K-64602'],
                    'ADDED WEIGHT': [0],
                },
            ),
            '.*Missing Base formulas \\(MU999\\) from CSV.*',
        ),
        (
            pd.DataFrame(
                {
                    'FORMULA CODE': ['MU000', 'MU999', 'MU999', 'MU999', 'MU999'],
                    'PIGMENT': ['NUDE', 'WHITE', 'BLACK', 'RED', 'YELLOW'],
                    'BATCH': ['K-64602', 'K-64602', 'K-64602', 'K-64602', 'K-64602'],
                    'ADDED WEIGHT': [5, 0, 0, 0, 0],
                },
            ),
            '.*Card Background MU000 added weight is not set to 0.*',
        ),
        (
            pd.DataFrame(
                {
                    'FORMULA CODE': ['MU000', 'MU999'],
                    'PIGMENT': ['NUDE', 'WHITE'],
                    'BATCH': ['K-64602', 'K-64602'],
                    'ADDED WEIGHT': [0, 0],
                },
            ),
            r'.*Pigment\(s\) missing from one of the formulas.*',
        ),
    ],
)
def test_import_formulas_ko(input_df, error) -> None:
    with pytest.raises(pa.errors.SchemaError, match=error):
        composition_schema.validate(input_df)


@pytest.mark.parametrize(
    'expected_df',
    [
        pd.DataFrame(
            {
                'FORMULA CODE': ['MU000', 'MU999'],
                'PIGMENT': ['WHITE', 'WHITE'],
                'BATCH': ['K-646402', 'K-646402'],
                'ADDED WEIGHT': [0, 0],
            },
        ),
    ],
)
def test_strip_strings(expected_df) -> None:
    corrupted_df = expected_df.copy(deep=True)
    corrupted_df['PIGMENT'] = [' WHITE', 'WHITE ']
    corrupted_df.columns = [
        ' FORMULA CODE',
        ' PIGMENT ',
        'BATCH ',
        'ADDED WEIGHT',
    ]
    returned_df = PghFormula._strip_strings(corrupted_df)
    pd.testing.assert_frame_equal(returned_df, expected_df)


@pytest.mark.parametrize(
    ('input_df', 'expected_df'),
    [
        (
            pd.DataFrame(
                {
                    'FORMULA CODE': ['MU043', 'MU043'],
                    'PIGMENT': ['WHITE', 'BLACK'],
                    'BATCH': ['K-64601', 'K-646402'],
                    'ADDED WEIGHT': [5.3, 0.0],
                },
            ),
            pd.DataFrame(
                {
                    'FORMULA CODE': ['MU043', 'MU043'],
                    'PIGMENT': ['WHITE', 'BLACK'],
                    'ADDED WEIGHT': [5.3, 0.0],
                },
            ),
        ),
    ],
)
def test_drop_batch_column(input_df, expected_df) -> None:
    returned_df = PghFormula._drop_batch_column(input_df)
    pd.testing.assert_frame_equal(returned_df, expected_df)


@pytest.mark.parametrize(
    ('input_df', 'expected_df'),
    [
        (
            pd.DataFrame(
                {
                    'FORMULA CODE': ['MU043', 'MU043'],
                    'PIGMENT': ['WHITE', 'BLACK'],
                    'ADDED WEIGHT': [6.3, 0.2],
                },
            ),
            pd.DataFrame(
                {
                    'BLACK': [0.2],
                    'WHITE': [6.3],
                },
                index=pd.Index(['MU043'], name='FORMULA CODE'),
            ).rename_axis(columns='PIGMENT'),
        ),
    ],
)
def test_pivot_df(input_df, expected_df) -> None:
    returned_df = PghFormula._pivot_df(input_df)
    pd.testing.assert_frame_equal(returned_df, expected_df)


@pytest.mark.parametrize(
    ('input_df', 'expected_df'),
    [
        (
            pd.DataFrame(
                {
                    'BLACK': [0.0],
                    'NUDE': [0.0],
                },
                index=pd.Index(['MU000'], name='FORMULA CODE'),
            ).rename_axis(columns='PIGMENT'),
            pd.DataFrame(
                {
                    'BLACK': [0.0],
                },
                index=pd.Index(['MU000'], name='FORMULA CODE'),
            ).rename_axis(columns='PIGMENT'),
        ),
    ],
)
def test_drop_nude_columns(input_df, expected_df) -> None:
    returned_df = PghFormula._drop_nude_column(input_df)
    pd.testing.assert_frame_equal(returned_df, expected_df)


@pytest.mark.parametrize(
    ('input_df', 'expected_df'),
    [
        (
            pd.DataFrame(
                {
                    'RED': [6.0],
                    'YELLOW': [4.0],
                },
                index=pd.Index(['MU000'], name='FORMULA CODE'),
            ).rename_axis(columns='PIGMENT'),
            pd.DataFrame(
                {
                    'RED': [0.06],
                    'YELLOW': [0.04],
                },
                index=pd.Index(['MU000'], name='FORMULA CODE'),
            ).rename_axis(columns='PIGMENT'),
        ),
    ],
)
def test_convert_weight_to_concentration(input_df, expected_df) -> None:
    returned_df = PghFormula._convert_weight_to_concentration(input_df)
    pd.testing.assert_frame_equal(returned_df, expected_df)
