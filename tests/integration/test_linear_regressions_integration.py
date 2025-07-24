import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from colour_science.calibration.linear_regressions import PghLinearRegressions


@pytest.mark.parametrize(
    ('c_indices_to_drop', 'poly_degree', 'sample_weights'),
    [
        ([], 1, []),
        ([0, 1], 1, []),
        ([-1, -2], 1, []),
        ([], 5, []),
        ([], 15, []),
        ([], -5, []),
        ([-1], 5, []),
        ([], 2, [1, 10]),
        ([], 5, [1, 10, 100, 100, 1000, 0.5, 0.01, 0.001, 0.00001, 2, 2, 2, 2, 2, 2]),
    ],
)
@pytest.mark.filterwarnings('ignore')
def test_fit_to_file_ok(
    formulas_path: str,
    else_path: str,
    mono_red_path: str,
    c_indices_to_drop: list,
    poly_degree: int,
    sample_weights: list,
):
    returned_df = PghLinearRegressions.fit_to_file(
        formulas_path,
        else_path,
        mono_red_path,
        c_indices_to_drop=c_indices_to_drop,
        poly_degree=poly_degree,
        sample_weights=sample_weights,
    )

    assert isinstance(returned_df, pd.DataFrame)
    assert np.array_equal(
        np.array(
            [
                'PIGMENT',
                'PAPER',
                'PREDICT',
                'POLY_DEG',
                'Avg_RM...
                .
                .
                .
