from unittest.mock import ANY, MagicMock, patch

import numpy as np
import pandas as pd
import pytest

from colour_science.calibration.linear_regressions import PghLinearRegressions


@pytest.mark.parametrize(
    ('poly_degree', 'sample_weights'),
    [(1, None), (1, []), (1, [0.0, 1.0]), (5, np.arange(1.0, 100.0))],
)
def test_init_ok(poly_degree: int, sample_weights: list[float] | None) -> None:
    with patch(
        'pgh_colors.calibration.linear_regressions.'
        'PghLinearRegressions._create_model',
    ) as mock_model:
        plr = PghLinearRegressions(poly_degree, sample_weights)
        assert plr.poly_degree == poly_degree
        assert np.equal(plr.sample_weights, np.array(sample_weights)).all()
        mock_model.assert_called_once()


@pytest.mark.parametrize(
    ('poly_degree', 'expected_poly', 'sample_weights', 'expected_weights'),
    [(-1, 1, [], []), (1000, 10, [], []), (1, 1, [np.nan, 10.0], [1.0, 10.0])],
)
def test_init_clipped(
    poly_degree: int,
    expected_poly: int,
    sample_weights: list[float],
    expected_weights: list[float],
) -> None:
    with patch(
        'pgh_colors.calibration.linear_regressions.'
        'PghLinearRegressions._create_model',
    ) as mock_model:
        plr = PghLinearRegressions(poly_degree, sample_weights)
        assert plr.poly_degree == expected_poly
        assert np.equal(plr.sample_weights, np.array(expected_weights)).all()
        mock_model.assert_called_once()


@pytest.mark.parametrize(
    ('poly_degree', 'sample_weights', 'error'),
    [
        (-1, [-10], '.*All weights must be >=0*.'),
        (100, [[1, 10]], '.*Weights must be 1D*.'),
    ],
)
def test_init_ko(poly_degree: int, sample_weights: list[float], error: str) -> None:
    with pytest.raises(ValueError, match=error):
        PghLinearRegressions(poly_degree, sample_weights)


def test_create_model() -> None:
    poly_degree = 2
    with (
        patch(
            'pgh_colors.calibration.linear_regressions.PolynomialFeatures',
        ) as mock_poly,
        patch(
            'pgh_colors.calibration.linear_regressions.make_pipeline',
        ) as mock_make_pipeline,
    ):
        PghLinearRegressions(poly_degree=poly_degree)
        mock_make_pipeline.assert_called_once()
        mock_poly.assert_called_once_with(degree=poly_degree)


def test_fit_to_calibration_variables() -> None:
    plr = PghLinearRegressions()
    with (
        patch.object(plr, 'fit_to', return_value=pd.DataFrame({'model': ['X_model']})),
        patch.object(
            plr,
            'retrieve_best_models',
            return_value=pd.DataFrame({'best_model': ['K', 'S', 'KS']}),
        ),
    ):
        result = plr.fit_to_calibration_variables(MagicMock())

        plr.fit_to.assert_any_call(ANY)
        assert plr.fit_to.call_count == 3  # noqa: PLR2004
        plr.retrieve_best_models.assert_called_once()
        assert 'best_model' in result.columns
        assert len(result) == plr.retrieve_best_models.return_value.shape[0]
        assert result['best_model'].iloc[0] == 'K'
        assert result['best_model'].iloc[1] == 'S'
        assert result['best_model'].iloc[2] == 'KS'


def test_fit_to() -> None:
    plr = PghLinearRegressions(poly_degree=4, sample_weights=[1, 2])
    with patch.object(plr, 'fit_with_params', return_value='finish.'):
        var = MagicMock()
        plr.fit_to(var)
        plr.fit_with_params.assert_called_once_with(
            var,
            plr.model,
            plr.poly_degree,
            plr.sample_weights,
        )


def test_fit_with_params() -> None:
    mock_var = MagicMock(name='mock_var')
    mock_model = MagicMock(name='mock_model')
    mock_poly_degree = MagicMock(name='mock_deg')
    mock_sample_weights = MagicMock(name='mock_w')
    with patch.multiple(
        'pgh_colors.calibration.linear_regressions.PghLinearRegressions',
        _extract_metadata=MagicMock(return_value=('yon', 'RED', 'K')),
        _extract_x_y=MagicMock(return_value=('X', 'y')),
        _create_param_grid=MagicMock(return_value={'deg': [2]}),
        _align_sample_weights=MagicMock(return_value='aligned_weights'),
        _loo_cross_validate=MagicMock(return_value={'score': -0.85}),
        _store_info_to_df=MagicMock(
            return_value=pd.DataFrame({'pigment': ['RED'], 'score': [-0.85]}),
        ),
    ):
        result = PghLinearRegressions.fit_with_params(
            mock_var,
            mock_model,
            mock_poly_degree,
            mock_sample_weights,
        )
        PghLinearRegressions._extract_metadata.assert_called_once_with(mock_var)
        PghLinearRegressions._extract_x_y.assert_called_once_with('RED', mock_var)
        PghLinearRe...
        .
        .
        .
