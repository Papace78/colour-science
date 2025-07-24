from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

from colour_science.spectral_distribution.converters import (
    reflectances_to_lab,
    to_lab,
    to_spectral_distribution,
    to_xyz,
)


@pytest.mark.parametrize('interval_input', [1, 3])
@patch('pgh_colors.spectral_distribution.converters.SpectralShape')
def test_to_spectral_distribution(
    mock_shape: MagicMock,
    refl_input: pd.Series,
    mock_cs_api_spectral_distribution: tuple,
    interval_input: int,
):
    mock_sd, msd = mock_cs_api_spectral_distribution
    sd_returned = to_spectral_distribution(refl_input, interval=interval_input)
    mock_shape.assert_called_once_with(400, 700, interval_input)
    msd.assert_called_once_with(refl_input)
    mock_sd.align.assert_called_once_with(mock_shape.return_value)
    assert sd_returned == mock_sd


@patch('pgh_colors.spectral_distribution.converters.sd_to_XYZ')
@patch('pgh_colors.spectral_distribution.converters.MSDS_CMFS')
@patch('pgh_colors.spectral_distribution.converters.SDS_ILLUMINANTS')
def test_to_xyz(
    mock_sds_illuminants: MagicMock,
    mock_msds_cmfs: MagicMock,
    mock_sd_to_xyz: MagicMock,
    cmfs: str,
    illuminant: str,
):
    mock_sd = MagicMock()
    mock_sd_to_xyz.return_value = np.array([0.5, 0.5, 0.5])

    xyz_returned = to_xyz(mock_sd, cmfs=cmfs, illuminant=illuminant)

    mock_msds_cmfs.__getitem__.assert_called_once_with(cmfs)
    mock_sds_illuminants.__getitem__.assert_called_once_with(illuminant)
    mock_sd_to_xyz.assert_called_once_with(
        mock_sd,
        cmfs=mock_msds_cmfs[cmfs],
        illuminant=mock_sds_illuminants[illuminant],
    )
    np.testing.assert_array_equal(xyz_returned, np.array([0.5, 0.5, 0.5]))


@patch('pgh_colors.spectral_distribution.converters.XYZ_to_Lab')
@patch('pgh_colors.spectral_distribution.converters.to_xyz')
@patch('pgh_colors.spectral_distribution.converters.CCS_ILLUMINANTS')
def test_to_lab(
    mock_ccs_illuminants: MagicMock,
    mock_to_xyz: MagicMock,
    mock_xyz_to_lab: MagicMock,
    cmfs: str,
    illuminant: str,
):
    mock_sd = MagicMock()
    mock_to_xyz.return_value = np.array([50, 50, 50])
    scaled_xyz = np.array([0.5, 0.5, 0.5])
    mock_xyz_to_lab.r..
    .
    .
    .
