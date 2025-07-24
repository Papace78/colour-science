"""Plot useful for comparing true vs pred."""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from colour_science.colour_matching.metrics import delta_E00_from_reflectances


def plot_compare_reflectance_prediction(r_preds: pd.DataFrame) -> pd.DataFrame:
    """Plot R_true vs R_pred separating one col for 'D' and col for 'L' background.

    Args:
        r_preds (pd.DataFrame): Output of MonochromeReflectance.predict_reflectances.
                        For each C, it contains both R_true and R_pred per background.
    """
    pigments_name = r_preds.columns[
        r_preds.columns.isin(['BLACK', 'RED', 'WHITE', 'YELLOW'])
    ]
    r_preds = r_preds.melt(
        id_vars=np.append(['FORMULA CODE', 'BACKGROUND', 'y'], pigments_name),
        value_vars=np.arange(400, 701, 1),
        var_name='Wavelength (nm)',
        value_name='R',
    )
    fig = px.line(
        r_preds,
        x='Wavelength (nm)',
        y='R',
        color='y',
        facet_col='BACKGROUND',
        facet_row='FORMULA CODE',
        title='Reflectance prediction',
        labels={'Value': 'R', 'Wavelength': 'Wavelength (nm)'},
        hover_data={
            'BLACK': True,
            'RED': True,
            'WHITE': True,
            'YELLOW': True,
            'FORMULA CODE': True,
            'BACKGROUND': False,
        },
    )

    fig.update_layout(
        legend_title='R',
        template='plotly_white',
        height=700,
    )

    fig.show()


def quick_plot(
    true_rk: np.ndarray,
    true_rw: np.ndarray,
    pred_rk: np.ndarray,
    pred_rw: np.ndarray,
    title: str = 'Reflectance',
    subplot_title_1: str= 'D',
    subplot_title_2: str= 'L'
) -> None:
    """Quick plot of two couples of np.ndarray (true vs pred). One col per bg."""
    wavelengths = np.arange(400, 701, 1)
    delta_rk = np.round(delta_E00_from_reflectances(true_rk, pred_rk), 2)
    delta_rw = np.round(delta_E00_from_reflectances(true_rw, pred_rw), 2)
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            f'{subplot_title_1} / d...
            ..
            ..
            ..'
