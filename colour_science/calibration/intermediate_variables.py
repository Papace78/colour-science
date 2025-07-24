"""Calculates intermediate calibration variables required for linear regression.

This module computes the following intermediate variables for monochrome calibration:
- `acoth`: Inverse hyperbolic cotangent function used in variable calculations.
- `refl_w`: Monochromes reflectances for the light (L) background.
- `refl_k`: Monochromes reflectances for the dark (D) background.
- `a_yon`: Intermediate variable computed with "yon" paper.
- `a_cas`: Intermediate variable computed with "cas" paper.
- `b`: Another intermediate variable computed from 'a'.
- `sx_yon`: Scattering coefficient per concentration computed with "yon" paper.
- `sx_cas`: Scattering coefficient per concentration computed with "cas" paper.
- `kx`: Absorption coefficient per concentration computed based on 'a' and 'SX'.
- `kxsx`: The ratio of KX and SX.

The class `PghAbstractVariables` is designed to be extended for the formulas of the
papers 'PghMonochromeYon` for "yon" paper and `PghMonochromeCas` for "cas" paper.

Classes:
    - PghAbstractVariables (abstract class)
    - PghMonochromeYon (subclass for "yon" paper)
    - PghMonochromeCas (subclass for "cas" paper)
"""

from abc import ABC, abstractmethod
from typing import ClassVar

import numpy as np
import pandas as pd

from colour_science.calibration.auxiliaries import get_constants
from colour_science.spectral_distribution.spectral_distribution import (
    PghSpectralDistributions,
)


def acoth(x: np.ndarray) -> np.ndarray:
    """Return the inverse hyperbolic cotangent of x. Undefined in [-1,1]."""
    # https://www.wolframalpha.com/input?i=acoth%28x%29
    return np.arctanh(1 / x)


class PghAbstractVariables(ABC):
    """Framework for calculating intermediate variables."""

    AVAILABLE_PIGMENTS: ClassVar[list] = ['BLACK', 'RED', 'WHITE', 'YELLOW']
    PAPER = 'ABC'

    def __init__(
        self,
        refl_g: pd.DataFrame,
        c_indices_to_drop: list[int] | None = None,
    ) -> None:
        """Calculates all intermediate variables a, b, KX, SX and KXSX.

        Args:
            refl_g (pd.DataFrame): Reflectance of background. Contains both 'L' and 'D'.
            c_indices_to_drop (list[int]): List of concentration indices to drop.
                                            Default is empty, no c are dropped.
        """
        self.refl_g = refl_g
        self.c_indices_to_drop = c_indices_to_drop or []
        self.wavelengths = np.array([w for w in refl_g.columns if isinstance(w, int)])

    @property
    def refl_gk(self) -> np.ndarray:
        """Return the reflectance of the contrast card 'D'."""
        return (
            self.refl_g[self.refl_g['VAR'] == 'Rgk'][self.wavelengths]
            .to_numpy()
            .squeeze()
        )

    @property
    def refl_gw(self) -> np.ndarray:
        """Return the reflectance of the contrast card 'L'."""
        return (
            self.refl_g[self.refl_g['VAR'] == 'Rgw'][self.wavelengths]
            .to_numpy()
            .squeeze()
        )

    @classmethod
    def calibrate_from_files(
        cls,
        formula_path: str,
        measures_else_path: str,
        monochrome_path: str,
        c_indices_to_drop: list[int] | None = None,
    ) -> pd.DataFrame:
        """Return all intermediate calibration variables from CSVs.

        Args:
            formula_path (str): Path to the formula CSV.
            measures_else_path (str): Path to the Rg reflectances CSV.
            monochrome_path (str): Path to the monochrome reflectances CSV.
            c_indices_to_drop (list[int], optional): List of concentration indices to
                                                    drop.

        Returns:
            pd.DataFrame: Contains the calculated intermediate variables.
        """
        else_psd = PghSpectralDistributions.generate_from_files(
            formula_path,
            measures_else_path,
        )
        monochromes = PghSpectralDistributions.generate_from_files(
            formula_path,
            monochrome_path,
        )
        refl_g = get_constants(else_psd, 'Rg')
        c_indices_to_drop = c_indices_to_drop or []
        calibrator = cls(refl_g, c_indices_to_drop)
        return calibrator.calibrate(monochromes)

    def calibrate(self, monochrome: pd.DataFrame) -> pd.DataFrame:
        """Calculates the intermediate calibration variables: a, b, SX, KX, and KXSX."""
        pigment_name = self._get_pigment_name(monochrome, self.AVAILABLE_PIGMENTS)
        if self.c_indices_to_drop and pigment_name in self.AVAILABLE_PIGMENTS:
            monochrome = self.drop_concentrations(
                monochrome,
                pigment_name,
                self.c_indices_to_drop,
            )

        refl_k = self.get_reflectance_per_background(monochrome, 'D')
        refl_w = self.get_reflectance_per_background(monochrome, 'L')

        a, b, sx, kx, kxsx = self._get_intermediate_variables(refl_k, refl_w)

        return self.store_info_to_df(
            pigment_name,
            monochrome,
            self.refl_g,
            a,
            b,
            sx,
            kx,
            kxsx,
        )

    @staticmethod
    def _get_pigment_name(monochrome: pd.DataFrame, available_pigments: list) -> str:
        """Return pigment name from cls available pigments that has non-zero values."""
        pigment_name = [p for p in available_pigments if (monochrome[p] != 0).any()]
        return pigment_name[0] if pigment_name else 'base'

    @staticmethod
    def drop_concentrations(
        monochromes: pd.DataFrame,
        pigment_name: str,
        c_indices_to_drop: list[int],
    ) -> tuple[list, pd.DataFrame]:
        """Drops specific index of concentrations from the monochrome data.

        Args:
            monochromes (pd.DataFrame): Contains monochrome reflectances.
            pigment_name (str): Contains the name of the pigment to drop c from.
            c_indices_to_drop (list[int]): List of concentration indices to drop.

        Returns:
            tuple: The list of kept concentrations, and the filtered DataFrame.
        """
        c = sorted(monochromes[f'{pigment_name}'].unique())
        c_to_keep = set(np.delete(c, c_indices_to_drop))
        filtered_mono = monochromes[monochromes[f'{pigment_name}'].isin(c_to_keep)]
        if filtered_mono.empty:
            raise ValueError(f'No more monochromes, all dropped: {c_indices_to_drop}')
        return filtered_mono

    @staticmethod
    def get_reflectance_per_background(
        monochrome: pd.DataFrame,
        background: str,
    ) -> pd.DataFrame:
        """Separate reflectances of monochromes for a given background."""
        wavelengths = [w for w in monochrome.columns if isinstance(w, int)]
        return monochrome[monochrome['BACKGROUND'] == background][
            wavelengths
        ].reset_index(drop=True)

    def _get_intermediate_variables(
        self,
        refl_k: pd.DataFrame,
        refl_w: pd.DataFrame,
    ) -> tuple:
        """Crossroat to calculate the variables in accordance with a paper."""
        if self.PAPER == 'yon':
            return self.calculate_intermediate_variables(
                self.refl_gk,
                self.refl_gw,
                refl_k,
                refl_w,
            )
        if self.PAPER == 'cas':
            return self.calculate_intermediate_variables(refl_k, refl_w)
        raise ValueError('Paper reference missing. Instantiate within child class.')

    @classmethod
    @abstractmethod
    def calculate_intermediate_variables(
        cls,
        *args: pd.DataFrame,
        **kwargs: pd.DataFrame,
    ) -> tuple:
        """Define the process and arguments needed  for calculating the variables."""
        ...

    @staticmethod
    @abstractmethod
    def calculate_a(*args: pd.DataFrame, **kwargs: pd.DataFrame) -> pd.DataFrame:
        """Calculate an auxiliary."""
        ...

    @staticmethod
    def calculate_b(a: pd.DataFrame) -> pd.DataFrame:
        """Calculate an auxiliary."""
        return np.sqrt(np.square(a) - 1)

    @staticmethod
    @abstractmethod
    def calculate_sx(*args: pd.DataFrame, **kwargs: pd.DataFrame) -> pd.DataFrame:
        """Calculate the scattering coefficient."""
        ...

    @staticmethod
    def calculate_kx(a: pd.DataFrame, sx: pd.DataFrame) -> pd.DataFrame:
        """C...
        .
        .
        ."""


class PghMonochromeYon(PghAbstractVariables):
    """Handles calculations for the "yon" paper."""

    PAPER = 'yon'

    @classmethod
    def calculate_intermediate_variables(
        cls,
        refl_gk: np.ndarray,
        refl_gw: pd.DataFrame,
        refl_k: pd.DataFrame,
        refl_w: pd.DataFrame,
    ) -> tuple:
        """Process for calculating all intermediate variables."""
        a = cls.calculate_a(refl_gk, refl_gw, refl_k, refl_w)
        b = cls.calculate_b(a)
        sx = cls.calculate_sx(refl_gk, refl_k, a, b)
        kx = cls.calculate_kx(a, sx)
        kxsx = kx / sx
        return a, b, sx, kx, kxsx

    @staticmethod
    def calculate_a(
        refl_gk: np.ndarray,
        refl_gw: pd.DataFrame,
        refl_k: pd.DataFrame,
        refl_w: pd.DataFrame,
    ) -> pd.DataFrame:
        """Returned values must be > 1, otherwise b = 0."""
        return (
            ((refl_w - refl_k) * (1 + refl_gw * refl_gk))
            - ((refl_gw - refl_gk) * (1 + refl_w * refl_k))
        ) / (2 * (refl_w * refl_gk - refl_k * refl_gw))

    @staticmethod
    def calculate_sx(
        refl_gk: np.ndarray,
        refl_k: pd.DataFrame,
        a: pd.....
        .
        .
        .


class PghMonochromeCas(PghAbstractVariables):
    """Handles calculations for the "cas" paper."""

    PAPER = 'cas'

    @classmethod
    def calculate_intermediate_variables(
        cls,
        refl_k: pd.DataFrame,
        refl_w: pd.DataFrame,
    ) -> tuple:
        """Process for calculating all intermediate variables."""
        a = cls.calculate_a(refl_k, refl_w)
        b = cls.calculate_b(a)
        sx = cls.calculate_sx(refl_w, a, b)
        kx = cls.calculate_kx(a, sx)
        kxsx = kx / sx
        return a, b, sx, kx, kxsx

    @staticmethod
    def calculate_a(refl_k: pd.DataFrame, refl_w: pd.DataFrame) -> pd.DataFrame:
        """Retur...
        .
        .
        ."""
