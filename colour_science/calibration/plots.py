"""Plot to be used on single pigment at a time."""

import numpy as np
import pandas as pd
import plotly.colors
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def _get_pigment_name(df: pd.DataFrame) -> str:
    """Returns the only pigment where concentrations is not equal to 0."""
    return next(p for p in ['BLACK', 'RED', 'WHITE', 'YELLOW'] if (df[p] != 0).any())


def plot_monochromes_wavelength_distribution(monochromes: pd.DataFrame) -> None:
    """Plot monochromes R vs wavelengths."""
    pigment_name = _get_pigment_name(monochromes)
    monochromes = monochromes.melt(
        id_vars=['FORMULA CODE', f'{pigment_name}', 'BACKGROUND'],
        value_vars=list(range(400, 701)),
        var_name='Wavelength (nm)',
        value_name='Rcorr',
    )
    fig = px.line(
        monochromes,
        x='Wavelength (nm)',
        y='Rcorr',
        color=f'{pigment_name}',
        facet_col='BACKGROUND',
        title=f'{pigment_name} monochrome wavelengths',
        labels={'Wavelength': 'Wavelength', 'Value': 'Value'},
    )

    fig.show()


def plot_monochromes_concentration_distribution(
    monochromes: pd.DataFrame,
    wavelengths_to_plot: list[int] | None = None,
) -> None:
    """Plot monochromes R vs concentrations."""
    if not isinstance(wavelengths_to_plot,np.ndarray):
        wavelengths_to_plot = np.arange(400, 750, 50)
    pigment_name = _get_pigment_name(monochromes)
    monochromes = monochromes.melt(
        id_vars=['FORMULA CODE', f'{pigment_name}', 'BACKGROUND'],
        value_vars=list(range(400, 701)),
        var_name='Wavelength (nm)',
        value_name='Rcorr',
    )
    monochromes = monochromes[
        monochromes['Wavelength (nm)'].isin(np.array(wavelengths_to_plot))
    ]
    fig = px.line(
        monochromes,
        x=f'{pigment_name}',
        y='Rcorr',
        color='Wavelength (nm)',
        facet_col='BACKGROUND',
        title=f'{pigment_name} monochrome concentrations',
        labels={'Wavelength': 'Wavelength', 'Value': 'Value'},
    )

    fig.show()


def plot_intermediate_variables_wavelength_distrubtion(
    calibration_variable: pd.DataFrame,
) -> None:
    """Given calibration df, plot the variables spectrum."""
    plot_df = calibration_variable[calibration_variable['PAPER'] != 'n/a']
    pigment_name = plot_df['PIGMENT'].unique()[0]
    plot_df = plot_df.reset_index().melt(
        id_vars=['PIGMENT', 'PAPER', 'VAR', 'FORMULA CODE', f'{pigment_name}'],
        value_vars=list(range(400, 701)),
        var_name='Wavelength (nm)',
        value_name='value',
    )
    fig = px.line(
        plot_df,
        x='Wavelength (nm)',
        y='value',
        color=f'{pigment_name}',
        facet_col='VAR',
        facet_row='PAPER',
        title='Pigment monochrome wavelength distributions',
        labels={'Wavelength': 'Wavelength', 'Value': 'Value'},
        hover_data={'VAR': False, 'PAPER': False, 'FORMULA CODE': True},
        height=600,
    )

    fig.show()


def plot_intermediate_variables_concentration_distrubtion(
    calibration_variable: pd.DataFrame,
    wavelengths_to_plot: list[int] | None = None,
) -> None:
    """Given a calibration df, plot each variables within it on its own graph."""
    if not isinstance(wavelengths_to_plot,np.ndarray):
        wavelengths_to_plot = np.arange(400, 750, 50)
    plot_df = calibration_variable[calibration_variable['PAPER'] != 'n/a']
    pigment_name = plot_df['PIGMENT'].unique()[0]
    plot_df = plot_df.reset_index().melt(
        id_vars=['PIGMENT', 'PAPER', 'VAR', 'FORMU...
                 ..
                 ..
                 ..
