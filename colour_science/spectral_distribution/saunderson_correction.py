"""Relate measured to internal reflectances through Saunderson correction."""

import numpy as np
import pandas as pd


def convert_to_internal_reflectance(
    r_meas: pd.Series,
    r1: float = 0.02,
    r2: float = 0.4,
) -> pd.Series:
    """Use Saunderson correction to return the internal reflectance R.

    Args:
        r_meas (pd.Series): The measured reflectances using spectrophotometry.
        r1 (float): The fraction of reflected light from the air-film interface.
        r2 (float): The fraction of diffuse light incident on the underside of the top
                    layer. Generally between 0.4 and 0.6.

    Returns:
        pd.Series: The internal reflectance R
    """
    r1, r2 = (np.clip(x, 0, 1) for x in (r1, r2))
    return np.clip(pd.Series(r_meas / ((1 - r1) * (1 - r2) + r2 * r_meas)), 0.0, 1.0)


def convert_to_measured_reflectance(
    refl: pd.Series,
    r1: float = 0.02,
    r2: float = 0.4,
    alpha: float = 0.0,
) -> pd.Series:
    """Use Saunderson correction to return the measured reflectance R.

    Args:
        refl (pd.Series): The internal reflectances.
        r1 (float): The fraction of reflected light from the air-film interface.
        r2 (float): The fraction of diffuse light incident on the underside of the top
                    layer. Generally between 0.4 and 0.6.
        alpha (float): Percentage of specular component included. Default to 0 on xrite.

    Returns:
        pd.Series: The measured reflectance R
    """
    r1, r2, alpha = (np.clip(x, 0, 1) for x in (r1, r2, alpha))
    return np.clip(
        pd.Series((r1 * alpha) + (((1 - r1) * (1 - r2) * refl) / (1 - (r2 * refl)))),
        0.0,
        1.0,
    )
