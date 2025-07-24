"""Perform linear regression on KX, or SX, or KX/SX."""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV, LeaveOneOut
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import PolynomialFeatures

from colour_science.calibration.intermediate_variables import (
    PghMonochromeCas,
    PghMonochromeYon,
)


class PghLinearRegressions:
    """Perform Poly+linear regression on KX, SX, or KX/SX.

    The polynomial degree can be specified via the poly_degree parameter.

    The two class methods return a DataFrame containing:
        - PIGMENT: 'RED', 'WHITE',...
        - PAPER: 'cas' or 'yon'
        - PREDICT: 'K', 'S', or 'K/S'
        - POLY_DEG: poly_degree of the fitted model.
        - Avg_RMSE: Average of RMSE values.
        - RMSE: List of RMSE values from Leave-One-Out cross-validation.
        - MODELS: Fitted model.
    """

    def __init__(
        self,
        poly_degree: int = 1,
        sample_weights: list[float] | None = None,
    ) -> None:
        """Initialize with optional sample weights.

        Args:
            poly_degree (int, optional): The degree of the polynomial features.
                                        Defaults to 1.
            sample_weights (list[float], optional): Sample weights to be applied during
                                                    model fitting.
                                                    Defaults to an empty list.
        """
        self.poly_degree = np.clip(poly_degree, 1, 10)
        self.sample_weights = self.validate_sample_weights(np.array(sample_weights))
        self.model = self._create_model()

    def _create_model(self) -> Pipeline:
        """Return a pipeline with polynomial features and linear regression."""
        return make_pipeline(
            PolynomialFeatures(degree=self.poly_degree),
            LinearRegression(),
        )

    def validate_sample_weights(self, sample_weights: np.ndarray) -> np.ndarray:
        """Validate and process sample weights.

        Args:
            sample_weights (np.ndarray | None): Sample weights to be validated.

        Returns:
            np.ndarray: Processed sample weights as a NumPy array.

        Raises:
            ValueError: If sample_weights is multi-dimensional or contains non-positive
                        values.
        """
        if sample_weights.ndim == 0 or sample_weights.size == 0:
            return np.array([])
        if sample_weights.ndim != 1:
            raise ValueError(f'Weights must be 1D, found {sample_weights}.')
        if np.any(sample_weights < 0):
            raise ValueError(f'All weights must be >= 0, found: {sample_weights}')
        return np.nan_to_num(sample_weights, nan=1)

    def fit_to_calibration_variables(
        self,
        calibration_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Fit K, S, and K/S models from calibration_df.

        Args:
            calibration_df (pd.DataFrame): Contains all intermediate variables.

        Returns:
            pd.DataFrame: Containing cv_results and best_estimator for three models
                        fitted to K, to S, and to K/S.
        """
        kx = calibration_df[calibration_df['VAR'] == 'KX']
        sx = calibration_df[calibration_df['VAR'] == 'SX']
        kxsx = calibration_df[calibration_df['VAR'] == 'KXSX']
        models = pd.concat(
            [
                self.fit_to(kx),
                self.fit_to(sx),
                self.fit_to(kxsx),
            ],
            axis=0,
        )
        return self.retrieve_best_models(models)

    def fit_to(self, var: pd.DataFrame) -> pd.DataFrame:
        """Fit a model to one of a specific variable (KX, SX, or KXSX)."""
        return self.fit_with_params(
            var,
            self.model,
            self.poly_degree,
            self.sample_weights,
        )

    @classmethod
    def fit_with_params(
        cls,
        var: pd.DataFrame,
        model: Pipeline,
        poly_degree: int,
        sample_weights: np.ndarray,
    ) -> pd.DataFrame:
        """Fit a gridsearchCV and save results into a df.

        Args:
            var (pd.DataFrame): KX, SX, or KXSX.
            model (Pipeline): The   model pipeline to be used for fitting.
            poly_degree (int): The degree of polynomial features.
            sample_weights (list[float]): The sample weights for the regression.

        Returns:
            pd.DataFrame: A DataFrame containing the fitted model, RMSE values,
                        and other model metadata.
        """
        paper, pigment_name, predict = cls._extract_metadata(var)
        x, y = cls._extract_x_y(pigment_name, var)
        param_grid = cls._create_param_grid(poly_degree)
        sample_weights = cls._align_sample_weights(sample_weights, x)
        grid_cv = cls._loo_cross_validate(
            model,
            x,
            y,
            param_grid,
            sample_weights,
        )
        return cls._store_info_to_df(pigment_name, paper, predict, grid_cv)

    @staticmethod
    def retrieve_best_models(models: pd.DataFrame) -> pd.DataFrame:
        """Retrieve the models with the lowest average RMSE per variable.

        Args:
            models (pd.DataFrame): A DataFrame containing model results.

        Returns:
            pd.DataFrame: The best models based on the lowest average RMSE.
        """
        models = models.dropna(subset=['MODELS']).reset_index(drop=True)
        best_models = models.loc[
            models.groupby('PREDICT')['Avg_RMSE'].idxmax()
        ].reset_index(drop=True)

        best_models['PREDICT'] = pd.Categorical(
            best_models['PREDICT'],
            categories=['K', 'S', 'KS'],
            ordered=True,
        )
        return (
            best_models.sort_values(by='PREDICT')
            .drop(columns=['RANK'], errors='ignore')
            .reset_index(drop=True)
        )


    @staticmethod
    def _loo_cross_validate(
        model: Pipeline,
        x: np.ndarray,
        y: np.ndarray,
        param_grid: dict,
        sample_weights: list[float],
    ) -> GridSearchCV:
        """Perform Leave-One-Out Cross Validation with GridSearchCV.

        Arg...
        .
        .
        ."""
