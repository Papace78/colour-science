import numpy as np
import pandas as pd
import pytest

from colour_science.spectral_distribution.saunderson_correction import (
    convert_to_internal_reflectance,
    convert_to_measured_reflectance,
)



@pytest.mark.parametrize('r_input', [pd.Series([0.5, 0.9])])
def test_internal_reflectance_standard(r_input, saunderson_default_params) -> None:
    r1, r2, _ = saunderson_default_params
    r_returned = convert_to_internal_reflectance(r_input, r1, r2)
    assert isinstance(r_returned, pd.Series)
    assert len(r_returned) == len(r_input)
    r_expected = r_input / ((1 - r1) * (1 - r2) + r2 * r_input)
    pd.testing.assert_series_equal(r_returned, r_expected)


@pytest.mark.parametrize('r_input', [pd.Series([])])
def test_internal_reflectance_empty(r_input, saunderson_default_params) -> None:
    r1, r2, _ = saunderson_default_params
    r_returned = convert_to_internal_reflectance(r_input, r1, r2)
    pd.testing.assert_series_equal(r_returned, pd.Series([]))


@pytest.mark.parametrize('r_input', [pd.Series([0.0, 0.0])])
def test_internal_reflectance_zero(r_input, saunderson_default_params) -> None:
    r1, r2, _ = saunderson_default_params
    r_returned = convert_to_internal_reflectance(r_input, r1, r2)
    pd.testing.assert_series_equal(r_returned, pd.Series([0.0, 0.0]))


@pytest.mark.parametrize(
    'r_input',
    [pd.Series([1.0, 1.0]), pd.Series([0, 1]), pd.Series([1.0, 0.0])],
)
def test_internal_reflectance_edge_r(r_input, saunderson_default_params) -> None:
    r1, r2, _ = saunderson_default_params
    r_returned = convert_to_internal_reflectance(r_input, r1, r2)
    assert np.all((r_returned >= 0) & (r_returned <= 1))


@pytest.mark.parametrize(
    ('r1', 'r2', 'r_input', 'r_expected'),
    [
        (-1e-7, -100, pd.Series([0.8, 0.5]), pd.Series([0.8, 0.5])),
        (1 + 1e-7, 100, pd.Series([0.8, 0.5]), pd.Series([1.0, 1.0])),
        (-100, -1e-7, pd.Series([0.8, 0.5]), pd.Series([0.8, 0.5])),
        (100, 1 + 1e-7, pd.Series([0.8, 0.5]), pd.Series([1.0, 1.0])),
        (0, 0, pd.Series([...
                          .
                          .
                          .
