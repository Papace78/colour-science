from unittest.mock import MagicMock, call, patch

import pandas as pd
import pytest

from colour_science.calibration.auxiliaries import (
    PghCalibrationConstant,
    _validate_not_empty,
    get_constants,
    get_targets,
)

@patch(
    'pgh_colors.calibration.auxiliaries.'
    'PghCalibrationConstant._filter_dataframe',
)
@patch(
    'pgh_colors.calibration.auxiliaries.'
    'PghCalibrationConstant._assign_additional_columns',
)
def test_filter_and_assign(
    mock_assign: MagicMock,
    mock_filter: MagicMock,
    sample_constants: pd.DataFrame,
) -> None:
    input_df = MagicMock()
    mock_filter.return_value = MagicMock(name='filtered_df')
    mock_assign.return_value = sample_constants

    expected_filter_calls = [
        call(input_df, 'MU000', 'D'),
        call(input_df, 'MU000', 'L'),
        call(input_df, 'MU999', 'D'),
        call(input_df, 'MU999', 'L'),
    ]

    expected_assign_calls = [
        call(mock_filter.return_value, 'Rgk', 'card'),
        call(mock_filter.return_value, 'Rgw', 'card'),
        call(mock_filter.return_value, 'Rbk', 'base'),
        call(mock_filter.return_value, 'Rbw', 'base'),
    ]

    returned_df = PghCalibrationConstant._filter_and_assign(input_df)

    mock_filter.assert_has_calls(expected_filter_calls, any_order=True)
    mock_assign.assert_has_calls(expected_assign_calls, any_order=True)
    pd.testing.assert_frame_equal(returned_df, pd.concat([sample_constants] * 4))


@pytest.mark.parametrize(
    ('formula_code', 'background'),
    [('MU000', 'D'), ('MU000', 'L'), ('MU999', 'D'), ('MU999', 'L')],
)
def test_filter_dataframe(
    formula_code: str,
    background: str,
    sample_measures_else: pd.DataFrame,
) -> None:
    returned_df = PghCalibrationConstant._filter_dataframe(
        sample_measures_else,
        formu...
        .
        .
        .
