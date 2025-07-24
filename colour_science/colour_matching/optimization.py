"""Given pigments estimators for K and S, estimate C to colour match a target R."""

import numpy as np
import pandas as pd
from scipy.optimize import Bounds, OptimizeResult, minimize

from colour_science.calibration.auxiliaries import get_constants, get_targets
from colour_science.calibration.intermediate_variables import PghMonochromeYon
from colour_science.calibration.linear_regressions import PghLinearRegressions
from colour_science.colour_matching.metrics import (
    delta_E00,
    euclidean_distances,
    rmse,
)
from colour_science.formulation.formulate import PghFormulator
from colour_science.spectral_distribution.converters import reflectances_to_lab
from colour_science.spectral_distribution.spectral_distribution import (
    PghSpectralDistributions,
)

# Below upperbounds stay within the linear part of each pigment.
# Replace with commented bounds to match the whole expected range of pigments
# concentrations instead.
BOUNDS = {
    'BLACK': Bounds(lb=0, ub=0.0021),  # Bounds(lb=0, ub=0.006)
    'RED': Bounds(lb=0, ub=0.0053),  # Bounds(lb=0, ub=0.1)
    'WHITE': Bounds(lb=0, ub=0.063),  # Bounds(lb=0, ub=0.035)
    'YELLOW': Bounds(lb=0, ub=0.03),  # Bounds(lb=0, ub=0.08)
}
# The sum of all concentrations cannot go above 0.1 (10% of the mixture).
CONSTRAINTS = {'type': 'ineq', 'fun': lambda x: 0.1 - np.sum(x)}


class PghMinimizer:
    """Estimate pigment concentrations that color match a target reflectance.

    Utilizes fitted estimators for K and S pigments to estimate the concentrations
    needed to achieve a target reflectance (R). The estimation is done through
    optimization techniques that minimize the difference between target and predicted
    reflectance values.

    Attributes:
        r_estimator (PghFormulator): An instance that handles the calculation
                                        of reflectance based on pigments concentrations.
        pigments_name (list): List of names of the pigments. Derived from given models.
        R_pred (pd.DataFrame): Holds the last predicted reflectance values.
        R_preds (pd.DataFrame): Holds all predicted reflectance values.
        target (pd.DataFrame): Holds the last targeted reflectance.
        targets (pd.DataFrame): Holds all targeted reflectance values.
        result (pd.DataFrame): Holds the last result of optimization.
        results (pd.DataFrame): Holds all optimization results.
    """

    def __init__(self, r_estimator: PghFormulator) -> None:
        """Initializes the PghMinimizer with a reflectance calculator.

        Args:
            r_estimator (PghFormulator): An estimator to calculate reflectance
                                                on given pigment concentrations.
        """
        self.r_estimator = r_estimator
        self.pigments_name = r_estimator.EXPECTED_PIGMENTS
        self.reset()

    def reset(self) -> None:
        """Reboot all stored predictions."""
        self.r_pred = pd.DataFrame()
        self.r_preds = pd.DataFrame()
        self.target = pd.DataFrame()
        self.targets = pd.DataFrame()
        self.result = pd.DataFrame()
        self.results = pd.DataFrame()

    @classmethod
    def instantiate_from_file(
        cls,
        formula_path: str,
        measures_else_path: str,
        monochromes_pathes: list[str],
        c_indices_to_drop: list[int] | None = None,
        poly_degree: int = 5,
    ) -> 'PghMinimizer':
        """Instantiates a PghMinimizer from the provided file paths.

        Args:
            formula_path (str): Path to the CSV containing pigment formulas.
            measures_else_path (str): Path to the CSV containing Rg and targets R.
            monochromes_pathes (list[str]): List of path to the monochromes CSV.
            c_indices_to_drop (list[int], optional): Indices of concentrations to
                                                    ignore during fitting.
            poly_degree (int, optional): The degree of polynomial to use in fitting.

        Returns:
            PghMinimizer: An instance of PghMinimizer with loaded models,
                            targets, and predictions.
        """
        c_indices_to_drop = c_indices_to_drop or []
        else_psd = PghSpectralDistributions().generate_from_files(
            formula_path,
            measures_else_path,
        )
        rg = get_constants(else_psd, 'Rg')
        rb = get_constants(else_psd, 'Rb')
        targets = get_targets(else_psd)
        regressions = [
            PghLinearRegressions.fit_to_file(
                formula_path,
                measures_else_path,
                monochromes_path,
                c_indices_to_drop,
                poly_degree,
            )
            for monochromes_path in monochromes_pathes
        ]
        models = pd.concat(regressions).reset_index(drop=True)
        base = PghMonochromeYon(rg).calibrate(rb)
        r_estimator = PghFormulator(rg, models, base)
        pm = cls(r_estimator)
        pm.estimate_c(targets)
        return pm

    @property
    def wavelengths(self) -> np.ndarray:
        """Returns the wavelengths measured in the target."""
        return np.array([w for w in self.target.columns if isinstance(w, int)])

    @property
    def target_r(self) -> np.ndarray:
        """Used to compute rmse with R_pred array during minimizing."""
        return self.target[self.wavelengths].to_numpy().squeeze()

    @property
    def target_c(self) -> pd.DataFrame:
        """Used for scoring purposes in metrics."""
        return self.target[self.pigments_name]

    @property
    def reflectances(self) -> pd.DataFrame:
        """Combine df of targets and predicted reflectance values."""
        r = (
            pd.concat([self.targets, self.r_preds], axis=0)
            .sort_values(by=['FORMULA CODE', 'BACKGROUND'])
            .reset_index(drop=True)
        )
        return r[['y'] + [col for col in r.columns if col != 'y']]

    def estimate_c(self, targets: pd.DataFrame, max_retries: int = 10) -> pd.DataFrame:
        """Estimate pigment concentrations to match the target reflectance values.

        Args:
            targets (pd.DataFrame): Contains the targets as read by
                                    PghSpectralDistributions. It contains the target
                                    formula code, concentrations, Lab, and reflectance.
            max_retries (int, optional): Maximum number of optimization retries in case
                                        of failure.

        Returns:
            pd.DataFrame: Contains the targeted and their corresponding predicted
                        reflectance values.
        """
        for _, row in targets.iterrows():
            self.target = row.to_frame().T.assign(y='R_true')
            res = self._optimize_with_retries(max_retries)
            self.r_pred['LAB'] = self.r_pred[self.wavelengths].apply(
                reflectances_to_lab,
                axis=1,
            )
            self.result = self._extract_metrics(res)
            self.results = self._update_results()
            self.targets = self._update_targets()
            self.r_preds = self._update_r_preds()
        return self.reflectances

    def _optimize_with_retries(self, max_retries: int) -> OptimizeResult:
        """Attempt to minimize the objective function with a set number of retries."""
        for attempt in range(max_retries):
            try:
                return minimize(
                    fun=self._objective,
                    x0=self._initialize_concentrations(),
                    bounds=[
                        (BOUNDS[name].lb, BOUNDS[name].ub)
                        for name in self.pigments_name
                    ],
                    constraints=CONSTRAINTS,
                    method='SLSQP',
                    options={'maxiter': 1000},
                )
            except Exception as e:  # noqa: BLE001
                print(  # noqa: T201
                    f'{self.target["FORMULA CODE"].values[0]}\
                        {self.target["BACKGROUND"].values[0]} '  # noqa: PD011
                    f'attempt {attempt + 1} failed with error: {e}',
                )
                if attempt == max_retries - 1:
                    raise ValueError('Max retries reached.') from None

        return OptimizeResult(success=False, message='Optimization failed.')

    def _objective(self, concentrations: np.ndarray) -> np.ndarray:
        """Objective function to minimize during optimization.

        Uses the reflectance calculator to predict reflectances values given a set of
        concentrations. Then calculates and returns the root mean square error (RMSE)
        between the target and predicted reflectance.

        Args:...
        .
        .
        ."""
