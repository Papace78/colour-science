import numpy as np
import pandas as pd
import pytest

from colour_science.calibration.auxiliaries import get_constants
from colour_science.calibration.intermediate_variables import PghMonochromeYon
from colour_science.formulation.formulate import (
    kubelka_munk_two_constant_to_reflectance,
)
from colour_science.spectral_distribution.spectral_distribution import (
    PghSpectralDistributions,
)
from colour_science.spectrophotometer.reader import return_measured_formulas


@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_calibration_integration_yon(
    mock_monochrome: pd.DataFrame,
    mock_rg: pd.DataFrame,
):
    """Integration test with mock values for each monochrome sample.

    Assert that:
        1. All intermediate variables are present within the output df.
        2. Each variable rows is appropriately placed against its concentrations. This
        is done by intentionally triggering extreme values:
            MU032 : extremely low reflectances.
            MU033 : regular reflectances.
            MU034 : extremely high reflectances.
    """
    wavelengths = np.arange(400, 701, 1)
    variables = ['a', 'b', 'SX', 'KX', 'KXSX']

    pmy = PghMonochromeYon(mock_rg)
    result_df = pmy.calibrate(mock_monochrome)

    assert not result_df.empty
    assert result_df['VAR'].value_counts().get('Rgk') == 1
    assert result_df['VAR'].value_counts().get('Rgw') == 1
    for var in variables:
        assert result_df['VAR'].value_counts().get(var) == 3  # noqa: PLR2004

    stupidly_high_nbr = 1000
    low_r = result_df[result_df['FORMULA CODE'] == 'MU032']
    assert (low_r[low_r['VAR'] == 'a'][wavelengths] > stupidly_high_nbr).all().all()
    assert (low_r[low_r['VAR'] == 'b'][wavelengths] > stupidly_high_nbr).all().all()
    assert (low_r[low_r['VAR'] == 'SX'][wavelengths].isna()).all().all()
    assert (low_r[low_r['VAR'] == 'KX'][wavelengths].isna()).all().all()
    assert (low_r[low_r['VAR'] == 'KXSX'][wavelengths].isna()).all().all()

    std_r = result_df[result_df['FORMULA CODE'] == 'MU033']
    assert (std_r[wavelengths].to_numpy() > 0).all()

    high_r = result_df[result_df['FORMULA CODE'] == 'MU034']
    assert np.allclose(high_r[high_r['VAR'] == 'a'][wavelengths], 1, atol=0.0001)
    assert np.allclose(high_r[high_r['VAR'] == 'b'][wavelengths], 0, atol=0.011)
    assert (high_r[high_r['VAR'] == 'SX'][wavelengths] > stupidly_high_nbr).all().all()
    assert np.allclose(high_r[high_r['VAR'] == 'KX'][wavelengths], 0, atol=0.0777)
    assert np.allclose(high_r[high_r['VAR'] == 'KXSX'][wavelengths], 0, atol=0.0001)


@pytest.mark.filterwarnings('ignore')
def test_calibration_from_file_integration_yon(
    formulas_path: str,
    else_path: str,
    mono_red_path: str,
) -> None:
    """Assert full path from csv file to output df."""
    variables = ['a', 'b', 'SX', 'KX', 'KXSX']

    result_df = PghMonochromeYon.calibrate_from_files(
        formulas_path,
        else_path,
        mono_red_path,
        c_indices_to_drop=[],
    )
    assert not result_df.empty
    assert result_df['VAR'].value_counts().get('Rgk') == 1
    assert result_df['VAR'].value_counts().get('Rgw') == 1
    for var in variables:
        assert result_df['VAR'].value_counts().get(var) == 9  # noqa: PLR2004

    filtered_result_df = PghMonochromeYon.calibrate_from_files(
        formulas_path,
        else_path,
        mono_red_path,
        c_indic...
        .
        .
