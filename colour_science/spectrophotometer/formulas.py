"""Import R&D's formulation CSV to a dataframe."""

import pandas as pd
import pandera as pa

from colour_science.spectrophotometer.spectro_file_schema import composition_schema


class PghFormula:
    """Read and validate formulation CSV, importing it as a DataFrame.

    Attributes:
        compositions (pd.DataFrame): DataFrame containing validated and processed data.
    """

    def __init__(self, formula_path: str) -> None:
        """Initialize PghFormula with given file path and process the data."""
        self.compositions: pd.DataFrame = self._process_file(formula_path)

    @classmethod
    def import_csv_as_dataframe(cls, formula_path: str) -> pd.DataFrame:
        """Create a validated dataframe from a CSV file."""
        return cls(formula_path).compositions

    @classmethod
    def _process_file(cls, formula_path: str) -> pd.DataFrame:
        """Reads, cleans, and processes the CSV file into a DataFrame."""
        return (
            cls._import_formulas(formula_path)
            .pipe(cls._strip_strings)
            .pipe(cls._drop_batch_column)
            .pipe(cls._pivot_df)
            .pipe(cls._drop_nude_column)
            .pipe(cls._convert_weight_to_concentration)
        )

    @pa.check_output(composition_schema, lazy=True)
    @staticmethod
    def _import_formulas(formula_path: str) -> pd.DataFrame:
        """Import and validate the CSV file containing the formulas."""
        return pd.read_csv(formula_path, sep=',', header='infer')

    @staticmethod
    def _strip_strings(comp_df: pd.DataFrame) -> pd.DataFrame:
        """Remove leading and trailing spaces from string values and column headers."""
        comp_df...
        .
        .
        .
