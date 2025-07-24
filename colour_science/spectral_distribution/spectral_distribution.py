"""Builds a dataframe containing formulas, reflectances, and colour information.

This is the basic object on which later calculation can be made, either for colour
matching or for calibrating.
"""

from typing import ClassVar

import numpy as np
import pandas as pd

from colour_science.spectral_distribution.converters import (
    to_lab,
    to_spectral_distribution,
)
from colour_science.spectral_distribution.saunderson_correction import (
    convert_to_internal_reflectance,
)
from colour_science.spectrophotometer.reader import return_measured_formulas


class PghSpectralDistributions:
    """Handles spectral distribution generation and processing."""

    AVAILABLE_PIGMENTS: ClassVar[list] = ['BLACK', 'RED', 'WHITE', 'YELLOW']

    def __init__(
        self,
        saunderson_r1: float = 0.02,
        saunderson_r2: float = 0.4,
        spectral_interval: int = 1,
    ) -> None:
        """Parameters for reflectance correction and spectral distrib interpolation."""
        self.saunderson_r1 = saunderson_r1
        self.saunderson_r2 = saunderson_r2
        self.spectral_interval = spectral_interval

    def process_measurements(self, measurements: pd.DataFrame) -> pd.DataFrame:
        """Processes raw measurements using instance hyperparameters."""
        return self.process_measurements_with_params(
            measurements,
            self.saunderson_r1,
            self.saunderson_r2,
            self.spectral_interval,
        )

    @classmethod
    def process_measurements_with_params(
        cls,
        measurements: pd.DataFrame,
        saunderson_r1: float = 0.02,
        saunderson_r2: float = 0.4,
        spectral_interval: int = 1,
    ) -> pd.DataFrame:
        """Override instance hyperparameter to processes raw measurements."""
        formulas, reflectances = cls._split(measurements)
        pigment_name = cls._extract_pigment_name(formulas)
        saunderson_reflectances = cls._correct(
            reflectances,
            saunderson_r1,
            saunderson_r2,
        )
        sd = cls._get_interpolated_spectral_distribution(
            saunderson_reflectances,
            spectral_interval,
        )
        lab_df = cls._get_lab(sd)
        sd_df = cls._sd_to_df(sd, spectral_interval)
        return cls._build_df(pigment_name, formulas, lab_df, sd_df)

    @classmethod
    def generate_from_files(
        cls,
        path_to_composition: str,
        path_to_measures: str,
        saunderson_r1: float = 0.02,
        saunderson_r2: float = 0.4,
        spectral_interval: int = 1,
    ) -> pd.DataFrame:
        """Process CSV into a df with formulas, Lab, and spectral data."""
        measurements = return_measured_formulas(path_to_composition, path_to_measures)
        return cls.process_measurements_with_params(
            measurements,
            saunderson_r1,
            saunderson_r2,
            spectral_interval,
        )

    @staticmethod
    def _split(measurements: pd.DataFrame) -> tuple:
        """Separate df into the formulas compositions and the reflectances values."""
        wavelengths = [col for col in measurements.columns if isinstance(col, int)]
        formulas = measurements.drop(columns=wavelengths)
        reflect...
        .
        .
        .
