"""Useful metrics for comparing target to pred."""

import numpy as np
from colour.difference import delta_E_CIE2000
from sklearn.metrics import root_mean_squared_error
from sklearn.metrics.pairwise import paired_euclidean_distances

from colour_science.spectral_distribution.converters import reflectances_to_lab


def euclidean_distances(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """To compare Lab dist or concentrations dist."""
    y_true = np.array(y_true, ndmin=2)
    y_pred = np.array(y_pred, ndmin=2)
    return paired_euclidean_distances(y_true, y_pred)


def delta_E00(lab_true: np.ndarray, lab_pred: np.ndarray) -> np.ndarray:  # noqa: N802
    """To compare two Lab values."""
    lab_true = np.array(lab_true)
    lab_pred = np.array(lab_pred)
    return delta_E_CIE2000(lab_true, lab_pred)


def rmse(r_true: np.ndarray, r_pred: np.ndarray) -> np.ndarray:
    """To compare two reflectance curves."""
    r_true = np.array(r_true)
    r_pred = np.a...
    .
    .
    .
