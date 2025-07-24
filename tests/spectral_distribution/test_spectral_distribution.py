from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

from colour_science.spectral_distribution.spectral_distribution import (
    PghSpectralDistributions,
)

MOCK_PATH = (
    'pgh_colors.spectral_distribution.spectral_distribution.'
    'PghSpectralDistributions'
)


@pytest.mark.parametrize(
    ('r1', 'r2', 'spectral_interval'),
    [(0.2, 0.4, 1), (0.5, 0.3, 2)],
)
def test_initialization_with_params(
    r1: float,
    r2: float,
    spectral_interval: int,
) -> None:
    psd = PghSpectralDistributions(r1, r2, spectral_interval)
    assert psd.saunderson_r1 == r1
    assert psd.saunderson_r2 == r2
    assert psd.spectral_interval == spectral_interval


@pytest.mark.parametrize(
    ('r1', 'r2', 'spectral_interval'),
    [(0.02, 0.4, 1), (0.03, 0.5, 3)],
)
@patch(f'{MOCK_PATH}.process_measurements_with_params')
def test_process_measurements(
    mock_process_measurements_with_params: MagicMock,
    r1: float,
    r2: float,
    spectral_interval: int,
) -> None:
    psd = PghSpectralDistributions(r1, r2, spectral_interval)
    measurements = MagicMock(name='mock_measurements')
    returned_df = psd.process_measurements(measurements)
    mock_process_measurements_with_params.assert_called_once_with(
        measurements,
        r1,
        r2,
        spectral_interval,
    )
    assert returned_df == mock_process_measurements_with_params.return_value


@pytest.mark.parametrize(
    ('r1', 'r2', 'spectral_interval'),
    [(0.02, 0.4, 1), (0.03, 0.5, 3)],
)
@patch(
    'pgh_colors.spectral_distribution.spectral_distribution.'
    'return_measured_formulas',
)
@patch(f'{MOCK_PATH}.process_measurements_with_params')
def test_generate_from_files(
    mock_process_measurements_with_params: MagicMock,
    mock_return_measured_formulas: MagicMock,
    r1: float,
    r2: float,
    spectral_interval: int,
):
    returned_df = PghSpectralDistributions.generate_from_files(
        'path/to/formulas',
        'path/to/measures',
        r1,
        r2,
        spectral_interval,
    )
    mock_return_measured_formulas.assert_called_once_with(
        'path/to/formulas',
        'path/to/measures',
    )
    mock_process_measurements_with_params.assert_called_once_with(
        mock_return_measured_formulas.return_value,
        r1,
        r2,
        spectral_interval,
    )
    assert returned_df == mock_process_measurements_with_params.return_value


@pytest.mark.parametrize(
    ('r1', 'r2', 'spectral_interval'),
    [(0.02, 0.4, 1), (0.03, 0.5, 3)],
)
@patch(f'{MOCK_PATH}._build_df')
@patch(f'{MOCK_PATH}._sd_to_df')
@patch(f'{MOCK_PATH}._get_lab')
@patch(f'{MOCK_PATH}._get...
    .
    .
    .
