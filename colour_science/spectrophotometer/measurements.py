"""Import spectrophotometer's reflectances CSV to a dataframe."""

import numpy as np
import pandas as pd
import pandera as pa

from colour_science.spectrophotometer.spectro_file_schema import reflectance_schema

EXPECTED_WAVELENGTHS = np.arange(400, 710, 10)


class PghMeasures:
    """Handles reading, cleaning, and validating a spectrophotometer's CSV file.

    Attributes:
        measures (pd.DataFrame): Contains validated and processed reflectances.
    """

    def __init__(self, measures_path: str) -> None:
        """Initialize PghMeasures with the given file path and process the data."""
        self.measures: pd.DataFrame = self._process_file(measures_path)

    @classmethod
    def import_csv_as_dataframe(cls, measures_path: str) -> pd.DataFrame:
        """Convenience method to create a validated dataframe from a CSV file."""
        return cls(measures_path).measures

    @classmethod
    def _process_file(cls, measures_path: str) -> pd.DataFrame:
        """Reads, cleans, and processes the CSV file into a DataFrame."""
        return (
            cls._import_measures(measures_path)
            .pipe(cls._strip_strings)
            .pipe(cls._remove_duplicated_wavelengths)
            .pipe(cls._drop_date_column)
            .pipe(cls._average_measures_by_background)
            .pipe...
            .
            .
            .
