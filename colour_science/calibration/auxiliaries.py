"""Read measures_else.csv into a df.

Useful to output:
- Rg (Rgk and Rgw) used for calibration as well as reflectance calculations.
- Rb (Rbk and Rbw) used for base calibration.
- targets ()
"""

from typing import ClassVar

import pandas as pd


def get_constants(else_psd: pd.DataFrame, filter_by: str | None = None) -> pd.DataFrame:
    """Return (Rgk, Rgw, Rbk, Rbw) df, optionally filtered by prefix."""
    cst = PghCalibrationConstant.extract_constants(else_psd)
    if filter_by:
        cst = cst[cst['VAR'].str.startswith(filter_by)].reset_index(drop=True)
    return _validate_not_empty(cst)


def get_targets(else_psd: pd.DataFrame) -> pd.DataFrame:
    """Filter out Rb and Rg from measures_else and returns the dataframe."""
    targets = else_psd[~else_psd['FORMULA CODE'].isin(['MU000', 'MU999'])].reset_index(
        drop=True,
    )
    return _validate_not_empty(targets).sort_values(by='FORMULA CODE')


def _validate_not_empty(input_df: pd.DataFrame) -> pd.DataFrame:
    if input_df.empty:
        raise ValueError('No value matching criteria.')
    return input_df


class PghCalibrationConstant:
    """Extracts constants df based on the provided measured_formulas df."""

    CONSTANTS: ClassVar[dict] = {
        'Rgk': ('MU000', 'D', 'card'),
        'Rgw': ('MU000', 'L', 'card'),
        'Rbk': ('MU999', 'D', 'base'),
        'Rbw': ('MU999', 'L', 'base'),
    }

    COLUMNS_ORDER: ClassVar[list] = [
        'PIGMENT',
        'VAR',
        'PAPER',
        'FORMULA CODE',
        'BLACK',
        'RED',
        'WHITE',
        'YELLOW',
        'BACKGROUND',
        'LAB',
    ]

    @classmethod
    def extract_constants(cls, else_psd: pd.DataFrame) -> pd.DataFrame:
        """Extract constants (Rgk, Rgw, Rbk, Rbw) from the dataframe."""
        wavelengths = [col for col in else_psd.columns if isinstance(col, int)]
        constants_df = cls._filter_and_assign(else_psd)
        return constants_df[cls.COLUMNS_ORDER + wavelengths].reset_index(drop=True)

    @classmethod
    def _filter_and_assign(cls, else_psd: pd.DataFrame) -> pd.DataFrame:
        """Helper to filter the dataframe and assign additional columns."""
        constants = []
        for var, (code, bg, p) in cls.CONSTANTS.items():
            filtered_df = cls._filter_dataframe(else_psd, code, bg)
            constant_frame = cls._assign_a...
            .
            .
            .
