"""Given a set of pigments concentration, predict K, S and KS of the mix.

example concentrations format:
pd.DataFrame([
    {
        'BLACK':0.0,
        'RED':0.03,
        'WHITE':0.0,
        'YELLOW':0.4,
    }
]).
"""

from typing import ClassVar

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline


class PghKSCalculator:
    """Calculate Kubelka Munk (km) constants for a given set of concentrations."""

    EXPECTED_PIGMENTS: ClassVar[list] = ['BLACK', 'RED', 'WHITE', 'YELLOW']
    KM_CONSTANTS: ClassVar[list] = ['K', 'S', 'KS']

    def __init__(self, pigments_models: pd.DataFrame, base_km: pd.DataFrame) -> None:
        """Initialize with pigments models and base KM data.

        Args:
            pigments_models (pd.DataFrame): Contains the fitted models per pigment per
                                        Kubelka-Munk constant. The DF format allows to
                                        reference each model to the pigment/constant it
                                        predicts.
                                        Can be obtained calibration.linear_regressions.
            base_km (pd.DataFrame): Contains the calculated K, S and K/S for the base.
                                    Can be obtained by calibrating the base reflectance
                                    measurements calibration.intermediate_variables.
                                    Need to clear the 'X' in the VAR column though.
        """
        self._validate_pigments_models(pigments_models)
        self._validate_base(base_km)
        self.pigments_models = pigments_models
        self.base_km = base_km

    def predict_km_constants(
        self,
        mixtures_concentrations: pd.DataFrame,
    ) -> pd.DataFrame:
        """Return km constants (K, S, K/S) for a given set of concentrations.

        Works in two steps:

            1. Creates a DataFrame.
            Associating each pigment with its concentration and fitted model.
            It generates one row for each constant in cls.KM_CONSTANTS and columns for
            each pigment in cls.EXPECTED_PIGMENTS
            If no concentration is provided for a pigment, it defaults to 0.
            If no model is provided, it defaults to `None`.
            These defaults won't be considered the calculations.

            2. Predict Kmix, Smix, KSmix.
            By iterating over each row of the above dataframe.
            Store the predicted arrays into a new dataframe.

        The above method allows for a consistent calculation process, whatever the input
        and whatever the fitted models (as long as both respect the input format).
        The above method also allows for easier testing as most of the logic is
        performed inside staticmethod.

        Args:
            mixtures_concentrations (pd.DataFrame): Contains the pigments concentrations
                                                    to make preditions on. The columns
                                                    must be pigments name, and one row
                                                    per sample.
                                                    Any pigment not in
                                                    cls.EXPECTED_PIGMENTS is ignored.

        Returns:
            pd.DataFrame: Three rows per sample, one for each constant in
                        cls.KM_CONSTANTS.
                        Columns starts by pigments concentrations, and are followed by
                        the km constants values from 400 to 700nm wavelengths.
        """
        return mixtures_concentrations.pipe(
            self._create_input_dataframe,
            pigments_models=self.pigments_models,
        ).pipe(self._predict, base_km=self.base_km)

    @classmethod
    def _validate_pigments_models(cls, pigments_models: pd.DataFrame) -> pd.DataFrame:
        """Validate pigments_models contains expected pigments and km_constants."""
        cls._validate_pre...
        .
        .
        .
