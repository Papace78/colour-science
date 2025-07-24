import pandas as pd
import pytest

from colour_science.spectrophotometer.reader import (
    build_formulas_with_measures_df,
    return_measured_formulas,
    return_missing_measurements,
)


@pytest.mark.usefixtures(
    'mock_formulas_import_csv_as_dataframe',
    'mock_measures_import_csv_as_dataframe',
)
def test_build_formulas_with_measures_df(expected_merged_df) -> None:
    returned_df = build_formulas_with_measures_df('mock_path_form', 'mock_path_meas')
    pd.testing.assert_frame_equal(returned_df, expected_merged_df)


@pytest.mark.usefixtures(
    'mock_formulas_import_csv_as_dataframe',
    'mock_measures_import_csv_as_dataframe',
)
def test_return_measured_formulas(expected_filtered_for_measured_df) -> None:
    returned_df = return_measured_formulas('mock_path_form', 'mock_path_meas')
    pd.testing.assert_frame_equal(returned_df, expected_filtered_for_measured_df)


@pytest.mark.usefixtures(
    'mock_formulas_import_csv_as_dataframe',
    'mock_measures_import_csv_as_dataframe',
)
def test_return_missing_measurements(expected_filtered_for_not_measured_df) -> None:
    returned_df = return_missing_measurements('mock_path_form', 'mock_path_meas')
    pd.testing.assert_frame_equal(returned_df, expected_filtered_for_not_measured_df)
