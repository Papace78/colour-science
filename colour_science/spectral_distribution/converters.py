"""Performs conversion between reflectance, sd, xyz and lab."""

import numpy as np
import pandas as pd
from colour import (
    CCS_ILLUMINANTS,
    MSDS_CMFS,
    SDS_ILLUMINANTS,
    SpectralDistribution,
    SpectralShape,
    XYZ_to_Lab,
    sd_to_XYZ,
)


def to_spectral_distribution(
    sd: pd.Series,
    interval: int = 1,
) -> SpectralDistribution:
    """Convert the spectro measured reflectances array to a colour-science object.

    Args:
        sd (pd.Series): Contains wavelengths as column name,
                            and reflectance as column values.
        interval (int): The above sd will get interpolated to have all reflectances
                        between range(400,700,interval).

    Returns:
        SpectralDistribution: Colour-science object allowing for colour conversion.
                            In its form, similar to a dict with wavelengths as keys and
                            reflectances as values.
    """
    return SpectralDistribution(sd).align(SpectralShape(400, 700, interval))


def to_xyz(
    sd: SpectralDistribution,
    cmfs: str = 'CIE 1964 10 Degree Standard Observer',
    illuminant: str = 'D65',
) -> np.ndarray:
    """Converts reflectances SD to XYZ using specified CMFS and illuminant."""
    return sd_to_XYZ(
        sd,
        cmfs=MSDS_CMFS[cmfs],
        illuminant=SDS_ILLUMINANTS[illuminant],
    )


def to_lab(
    sd: SpectralDistribution,
    cmfs: str = 'CIE 1964 10 Degree Standard Observer',
    illuminant: str = 'D65',
) -> np.ndarray:
    """Converts reflectance SD to Lab using specified CMFS and illuminant."""
    scaled_xyz = to_xyz(sd, cmfs, illuminant) / 100
    return np.round(
        XYZ_to_Lab(scaled_xyz, illuminant=CCS_ILLUMINANTS[cmfs][illuminant]),
        3,
    )


def reflectances_to_lab(
    refl: pd.Series,
    cmfs: str = 'CIE 1964 10 Degree Standard Observer',
    illuminant: str = 'D65',
) -> np.ndarray:
    """Converts reflectance series to Lab using specified CMFS and illuminant."""
    if isinstance(refl, np.ndarray):
        refl = pd.Series(refl, index=np.arange(400, 701, 1))
    sd = to_spectral_distribution(refl)
    return to_lab(sd, cmfs, illuminant)
