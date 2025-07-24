"""Given set(s) of concentrations, get the predicted refl on both bacgrkounds."""

from typing import ClassVar

import numpy as np
import pandas as pd

from colour_science.formulation.ks_mix import PghKSCalculator


def coth(x: float) -> float:
    """No coth in numpy."""
    x = np.asarray(x)
    # Use element-wise conditions
    lower_bound = 1e-6
    small_x = np.abs(x) < lower_bound
    result = np.empty_like(x)
    result[small_x] = 1 / x[small_x]  # Approximation for small x
    result[~small_x] = np.cosh(x[~small_x]) / np.sinh(x[~small_x])  # General case
    return result
    x = np.clip(x, a_min=1e-8, a_max=None)
    return np.cosh(x) / np.sinh(x)


def kubelka_munk_two_constant_to_reflectance(
    rg: np.ndarray,
    k: np.ndarray,
    s: np.ndarray,
) -> np.ndarray:
    r"""General Kubelka-Munk two constant formula to get R from K and S.

    .. math::
        r = \frac{1 - r_g \cdot \left( a - b \cdot coth(b \cdot s) \right)}{
        a - r_g + b \cdot coth(b \cdot s) }
    """
    ks = np.divide(k, s)
    a = np.clip(ks + 1, a_min=1 + 1e-10, a_max=1e10)  # trick, best to raise error ?
    b = np.sqrt(np.square(a) - 1)  # if nan value, it means KS is negative < 1.
    coth_b_s = coth(b * s)
    r = (1 - rg * (a - b * coth_b_s)) / (a - rg + b * coth_b_s)
    return r.squeeze()


class PghFormulator:
    """Given set(s) of concentrations, calculate the ks_mix and convert it to refl.

    Attributes:
        rg (pd.DataFrame): Contains the measured reflectance for the contrast card
                            One row for 'D' background and one for 'L'.
                            Can be obtained calibration.auxiliaries.get_constant.
        km_models (PghKSCalculator): Encapsulated class that allows to predict K, S
                                    and KS for set(s) of concentrations. It is called
                                    once in self.calculate_reflectance as
                                    km_models.predict_km_constants.
                                    This returns a df containing the km coeffs per mix.
    """

    EXPECTED_PIGMENTS: ClassVar[list] = ['BLACK', 'RED', 'WHITE', 'YELLOW']

    def __init__(
        self,
        rg: pd.DataFrame,
        pigment_models: pd.DataFrame,
        base_km: pd.DataFrame,
    ) -> None:
        """Initialize with contrast card reflectances and models to calculate ks_mix.

        Args:
            rg (pd.DataFrame): Contains the measured reflectance for the contrast card
                            One row for 'D' background and one for 'L'.
                            Can be obtained calibration.auxiliaries.get_constant.
            pigment_models (pd.DataFrame): Contains the fitted models per pigment per
                                        Kubelka-Munk constant. The DF format allows to
                                        reference each model to the pigment/constant it
                                        predicts.
                                        Can be obtained calibration.linear_regressions.
            base_km (pd.DataFrame): Contains the calculated K, S and K/S for the base.
                                    Can be obtained by calibrating the base reflectance
                                    measurements calibration.intermediate_variables.
                                    Need to clear the 'X' in the VAR column though.
        """
        self.rg = rg
        self.km_models = PghKSCalculator(pigment_models, base_km)

    @property
    def wavelengths(self) -> np.ndarray:
        """Return expected wavelengths measured (400nm to 700nm, 1nm interval)."""
        return np.array([col for col in self.rg if isinstance(col, int)])

    @property
    def rgw(self) -> np.ndarray:
        """Return reflectances values of contrast card, white background."""
        return self.rg[self.rg['VAR'] == 'Rgw'][self.wavelengths].to_numpy().squeeze()

    @property
    def rgk(self) -> np.ndarray:
        """Return reflectances values of contrast card, white background."""
        return self.rg[self.rg['VAR'] == 'Rgk'][self.wavelengths].to_numpy().squeeze()

    def calculate_reflectance(
        self,
        mixtures_concentrations: pd.DataFrame,
    ) -> pd.DataFrame:
        r"""From concentrations to reflectances.

        Start by retrieving the sum of Kmix and Smix for each mixture of the input.
        Then plug in Kmix, Smix and reflectance values of a chosen background into the
        generalized form of Kubelka-Munk equation.

        Args:
            mixtures_concentrations (pd.DataFrame): Contains the concentrations per
                                                    pigment. One col per pigment, one
                                                    row per mixture.

        Returns:
            pd.DataFrame: Contains the predicted reflectance for the given
                        concentrations. Two rows per set of concentration, one for
                        reflectance on 'L' background and one for 'D' background.
        """
        k_s_mixtures = self.km_models.predict_km_constants(mixtures_concentrations)
        r_preds = pd.DataFrame()
        for _, k_s_mix in k_s_mixtures.groupby(self.km_models.EXPECTED_PIGMENTS):
            k, s = self._extract_k_and_s_mix(k_s_mix)
            r_pred...
            .
            .
            .
