from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

from colour_science.calibration.intermediate_variables import (
    PghMonochromeCas,
    PghMonochromeYon,
    acoth,
)


@pytest.mark.parametrize(
    'c_indices_to_drop',
    [[], [0, 1, 2], [-2, -1], [50, 100], [0, 1, -3]],
)
def test_init(c_indices_to_drop: list[int], sample_constants: pd.DataFrame) -> None:
    pmc = PghMonochromeCas(sample_constants, c_indices_to_drop)
    pmy = PghMonochromeYon(sample_constants, c_indices_to_drop)

    pd.testing.assert_frame_equal(pmc.refl_g, pmy.refl_g)
    assert np.array_equal(pmc.c_indices_to_drop, pmy.c_indices_to_drop)
    assert np.array_equal(pmc.wavelengths, np.arange(400, 701, 1))
    assert np.array_equal(pmc.wavelengths, pmy.wavelengths)
    assert pmc.PAPER == 'cas'
    assert pmy.PAPER == 'yon'
    assert np.array_equal(pmc.refl_gk, np.zeros(301))
    assert np.allclose(pmc.refl_gw, np.multiply(np.ones(301), 0.2), atol=1e-6)


@patch(
    'pgh_colors.spectral_distribution.spectral_distribution.'
    'PghSpectralDistributions.generate_from_files',
)
@patch('pgh_colors.calibration.intermediate_variables.get_constants')
@patch('pgh_colors.calibration.intermediate_variables.PghMonochromeYon.calibrate')
def test_calibrate_from_files(
    mock_calibrate: MagicMock,
    mock_get_cst: MagicMock,
    mock_generate_from_files: MagicMock,
) -> None:
    PghMonochromeYon.calibrate_from_files(
        'path/to/formulas',
        'path/to/else',
        'path/to/monochrome',
        c_indices_to_drop=[],
    )
    mock_generate_from_files.assert_called_with(
        'path/to/formulas',
        'path/to/monochrome',
    )
    mock_get_cst.assert_called_with(mock_generate_from_files.return_value, 'Rg')
    mock_calibrate.assert_called_once_with(mock_generate_from_files.return_value)


@patch(
    'pgh_colors.calibration.intermediate_variables.'
    'PghMonochromeYon._get_pigment_name',
)
@patch(
    'pgh_colors.calibration.intermediate_variables.'
    'PghMonochromeYon.drop_concentrations',
)
@patch(
    'pgh_colors.calibration.intermediate_variables.'
    'PghMonochromeYon.get_reflectance_per_background',
)
@patch(
    'pgh_colors.calibration.intermediate_variables.'
    'PghMonochromeYon._get_intermediate_variables',
)
@patch(
    'pgh_colors.calibration.intermediate_variables.'
    'PghMonochromeYon.store_info_to_df',
)
def test_calibrate(
    mock_store_df: MagicMock,
    mock_get_variables: MagicMock,
    mock_get_refl_bg: MagicMock,
    mock_drop_c: MagicMock,
    mock_get_pigment: MagicMock,
    sample_monochrome: pd.DataFrame,
    sample_constants: pd.DataFrame,
) -> None:
    pigments = ['BLACK', 'RED', 'WHITE', 'YELLOW']
    sample_rg = sample_constants[sample_constants['VAR'].isin(['Rgk', 'Rgw'])]
    mock_get_variables.return_value = (
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    )

    PghMonochromeYon(sample_rg).calibrate(sample_monochrome)

    mock_get_pigment.assert_called_once_with(sample_monochrome, pigments)
    mock_drop_c.assert_not_called()
    mock_get_refl_bg.assert_called_with(sample_monochrome, 'L')
    mock_get_variables.assert_called_once()
    mock_store_df.assert_called_once()


def test_get_pigment_name(sample_monochrome: pd.DataFrame) -> None:
    expected_pigment = 'RED'
    returned_pigment = PghMonochromeYon._get_pigment_name(
        sample_monochrome,
        ['RED', 'BLACK', 'YELLOW', 'WHITE'],
    )
    assert returned_pigment == expected_pigment


def test_drop_concentrations_ok(sample_monochrome: pd.DataFrame) -> None:
    c_indices_to_drop = [[], [0], [-2, -1], [0, -1]]
    expected_df_list = [
        sample_monochrome,
        sample_monochrome[sample_monochrome['RED'] != 0.005],  # noqa: PLR2004
        sample_monochrome[sample_monochrome['RED'] == 0.005],  # noqa: PLR2004
        sample_monochrome[sample_monochrome['RED'] == 0.1],  # noqa: PLR2004
    ]

    for indices, expected_df in zip(c_indices_to_drop, expected_df_list, strict=True):
        returned_df = PghMonochromeYon.drop_concentrations(
            sample_monochrome,
            'RED',
            indices,
        )
        pd.testing.assert_frame_equal(returned_df, expected_df)


def test_drop_concentrations_ko(sample_monochrome: pd.DataFrame) -> None:
    c_indices_to_drop = [0, 1, 2]
    with pytest.raises(
        ValueError,
        match='.*No more monochromes*.',
    ):
        PghMonochromeYon.drop_concentrations(
            sample_monochrome,
            'RED',
            c_indices_to_drop,
        )

    c_indices_to_drop = [1000]
    with pytest.raises(IndexError):
        PghMonochromeYon.drop_concentrations(
            sample_monochrome,
            'RED',
            c_indices_to_drop,
        )


@pytest.mark.parametrize('background', ['D', 'L'])
def test_get_reflectance_per_background(
    background: str,
    sample_monochrome: pd.DataFrame,
) -> None:
    expected_wavelengths = np.arange(400, 701, 1)
    expected_df = sample_monochrome[sample_monochrome['BACKGROUND'] == background][
        expected_wavelengths
    ].reset_index(drop=True)

    returned_df = PghMonochromeYon.get_reflectance_per_background(
        sample_monochrome,
        background,
    )
    pd.testing.assert_frame_equal(returned_df, expected_df)


def test_get_intermediate_variable() -> None:
    with patch(
        'pgh_colors.calibration.intermediate_variables.'
        'PghMonochromeYon.calculate_intermediate_variables',
    ):
        pmy = PghMonochromeYon(MagicMock())
        rk = MagicMock(name='rk')
        rw = MagicMock(name='rw')

        pmy._get_intermediate_variables(rk, rw)

        pmy.calculate_intermediate_variables.assert_called_once_with(
            pmy.refl_gk,
            pmy.refl_gw,
            rk,
            rw,
        )


@patch('pgh_colors.calibration.intermediate_variables.PghMonochromeYon.calculate_a')
@patch('pgh_colors.calibration.intermediate_variables.PghMonochromeYon.calculate_b')
@patch(
    'pgh_colors.calibration.intermediate_variables.'
    'PghMonochromeYon.calculate_sx',
)
@patch(
    'pgh_colors.calibration.intermediate_variables.'
    'PghMonochromeYon.calculate_kx',
)
def test_calculate_intermediate_variables(
    mock_kx: MagicMock,
    mock_sx: MagicMock,
    mock_b: MagicMock,
    mock_a: MagicMock,
) -> None:
    mock_a.return_value = 0.0
    mock_b.return_value = 1.0
    mock_sx.return_value = 2.0
    mock_kx.return_value = 3.0
    expected_tuple = (0.0, 1.0, 2.0, 3.0, 3.0 / 2.0)
    returned_tuple = PghMonochromeYon.calculate_intermediate_variables(
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    )
    assert expected_tuple == returned_tuple
    mock_a.assert_called_once()
    mock_b.assert_called_once()
    mock_sx.assert_called_once()
    mock_kx.assert_called_once()


@pytest.mark.parametrize(
    ('x', 'expected_result'),
    [
        # calculated with excel
        # https://www.wolframalpha.com/input?i=acoth%28x%29
        (0.5, np.nan),
        (1, np.inf),
        (-1, -np.inf),
        (1.001, 3.8),
        (10, 0.1),
        (-10, -0.1),
        (20, 0.05),
        (100, 0.01),
        (
            np.array([0.5, 1, -1, 10, -10, 20, 100]),
            np.array([np.nan, np.inf, -np.inf, 0.1, -0.1, 0.05, 0.01]),
        ),
    ],
)
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_acoth(x, expected_result) -> None:
    returned_result = acoth(x)
    assert np.allclose(returned_result, expected_result, atol=0.01, equal_nan=True)


def test_calculate_a_yon() -> None:
    pmy = PghMonochromeYon(MagicMock())
    rk = pd.DataFrame([[0.3, 0.2], [0.4, 0.5]])
    rw = pd.DataFrame([[0.6, 0.7], [0.8, 0.9]])

    rgk = np.array([1, 1])
    rgw = np.array([1, 1])
    expected_result = pd.DataFrame([[1.0, 1.0], [1.0, 1.0]])
    returned_result = pmy.calculate_a(rgk, rgw, rk, rw)
    pd.testing.assert_frame_equal(returned_result, expected_result)

    rgk = np.array([0, 0])
    rgw = np.array([1, 1])
    expected_result = ((rw - rk) - (1 + rw * rk)) / (2 * (-rk))
    returned_result = pmy.calculate_a(rgk, rgw, rk, rw)
    pd.testing.assert_frame_equal(returned_result, expected_result)

    rgk = np.array([1, 1])
    rgw = np.array([0, 0])
    expected_result = ((rw - rk) - (-1 * (1 + rw * rk))) / (2 * rw)
    returned_result = pmy.calculate_a(rgk, rgw, rk, rw)
    pd.testing.assert_frame_equal(returned_result, expected_result)

    rgk = np.array([0, 0])
    rgw = np.array([0, 0])
    expected_result = pd.DataFrame([[np.inf, np.inf], [np.inf, np.inf]])
    returned_result = pmy.calculate_a(rgk, rgw, rk, rw)
    pd.testing.assert_frame_equal(returned_result, expected_result)

    rgw = np.array([0.9, 0.8])
    rgk = np.array([0.1, 0.2])
    rk = pd.DataFrame([[1, 1], [1, 1]])
    rw = pd.DataFrame([[1, 1], [1, 1]])
    expected_result = pd.DataFrame([[1.0, 1.0], [1.0, 1.0]])
    returned_result = pmy.calculate_a(rgk, rgw, rk, rw)
    pd.testing.assert_frame_equal(returned_result, expected_result)

    rk = pd.DataFrame([[0, 0], [0, 0]])
    rw = pd.DataFrame([[0, 0], [0, 0]])
    expected_result = pd.DataFrame([[-np.inf, -np.inf], [-np.inf, -np.inf]])
    returned_result = pmy.calculate_a(rgk, rgw, rk, rw)
    pd.testing.assert_frame_equal(returned_result, expected_result)

    rk = pd.DataFrame([[0, 0.5], [0.1, 0]])
    rw = pd.DataFrame([[0.2, 0.1], [0, 0.3]])
    expected_result = ((rw - rk) * (1 + rgw * rgk) - (rgw - rgk) * (1 + rw * rk)) / (
        2 * (rw * rgk - rk * rgw)
    )
    returned_result = pmy.calculate_a(rgk, rgw, rk, rw)
    pd.testing.assert_frame_equal(returned_result, expected_result)


@pytest.mark.parametrize(
    ('a', 'expected_result'),
    [
        (pd.DataFrame([[1, 1], [1, 1]]), pd.DataFrame([[0.0, 0.0], [0.0, 0.0]])),
        (
            pd.DataFrame([[2, 3], [4, 5]]),
            pd.DataFrame([[np.sqrt(3), np.sqrt(8)], [np.sqrt(15), np.sqrt(24)]]),
        ),
        (
            pd.DataFrame([[-2, -3], [-4, -5]]),
            pd.DataFrame([[np.sqrt(3), np.sqrt(8)], [np.sqrt(15), np.sqrt(24)]]),
        ),
        (
            pd.DataFrame([[0, 0], [0.5, 0.8]]),
            pd.DataFrame([[np.nan, np.nan], [np.nan, np.nan]]),
        ),
        (
            pd.DataFrame([[-0.1, -0.5], [-0.9, -0.99]]),
            pd.DataFrame([[np.nan, np.nan], [np.nan, np.nan]]),
        ),
        (
            pd.DataFrame([[np.nan, 3], [4, np.nan]]),
            pd.DataFrame([[np.nan, np.sqrt(8)], [np.sqrt(15), np.nan]]),
        ),
    ],
)
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_calculate_b(a, expected_result) -> None:
    returned_result = PghMonochromeYon.calculate_b(a)
    pd.testing.assert_frame_equal(returned_result, expected_result)


@pytest.mark.parametrize(
    ('rgk', 'rk', 'a', 'b'),
    [
        (
            np.array([0.008, 0.01, 0.012]),
            pd.DataFrame(
                {
                    400: [0.01, 0.01, 0.01],
                    555: [0.05, 0.05, 0.05],
                    700: [0.1, 0.1, 0.1],
                },
            ),
            pd.DataFrame(
                {
                    400: [10.0, 20.0, 40.0],
                    555: [5.0, 6.0, 7.0],
                    700: [1.2, 1.4, 1.6],
                },
            ),
            pd.DataFrame(
                {
                    400: [9.9, 19.9, 39.9],
                    555: [4.5, 5.5, 6.5],
                    700: [1.0, 1.2, 1.4],
                },
            ),
        ),
        (
            np.array([0.008, 0.01, 0.012]),
            pd.DataFrame(
                {
                    400: [0.01, 0.01, 0.01],
                    555: [0.05, 0.05, 0.05],
                    700: [0.1, 0.1, 0.1],
                },
            ),
            pd.DataFrame(
                {
                    400: [10.0, 20.0, 40.0],
                    555: [5.0, 6.0, np.inf],
                    700: [np.nan, 1.4, 1.6],
                },
            ),
            pd.DataFrame(
                {
                    400: [9.9, 19.9, 39.9],
                    555: [4.5, 5.5, 1000],
                    700: [1.0, 1.2, 1.4],
                },
            ),
        ),
    ],
)
@patch('pgh_colors.calibration.intermediate_variables.acoth')
def test_calculate_sx_yon(
    mock_acoth: MagicMock,
    rgk: np.ndarray,
    rk: pd....
    .
    .
    .
