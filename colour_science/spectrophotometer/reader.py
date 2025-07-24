"""Helper functions to merge composition and measures into one df."""

import pandas as pd

from colour_science.spectrophotometer.formulas import PghFormula
from colour_science.spectrophotometer.measurements import PghMeasures


def build_formulas_with_measures_df(
    formula_file_path: str,
    measures_file_path: str,
) -> pd.DataFrame:
    """Combine formulas and their corresponding reflectances into a single DataFrame.

    If reflectances have not yet been measured, NaN will be used as a placeholder.
    """
    formulas = PghFormula.import_csv_as_dataframe(formula_file_path)
    reflectances = PghMeasures.import_csv_as_dataframe(measures_file_path)

    return formulas.merge(reflectances, how='outer', on='FORMULA CODE')


def return_measured_formulas(
    formula_file_path: str,
    measures_file_path: str,
) -> pd.DataFrame:
    """Retriev...
    .
    .
    ."""
