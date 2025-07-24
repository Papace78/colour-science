import pandas as pd
import pytest

from colour_science.formulation.ks_mix import PghKSCalculator


def test_init_ok(sample_models: pd.DataFrame, sample_base: pd.DataFrame):
    pkc = PghKSCalculator(sample_models, sample_base)
    pd.testing.assert_frame_equal(pkc.pigments_models, sample_models)
    pd.testing.assert_frame_equal(pkc.base_km, sample_base)


def test_init_ko(sample_models: pd.DataFrame, sample_base: pd.DataFrame):
    corrupted_models = sample_models.iloc[1:]
    with pytest.raises(
        ValueError,
        match=".*column must contain exactly one 'K', one 'S', and one 'KS' *.",
    ):
        PghKSCalculator(corrupted_models, sample_base)

    corrupted_models = sample_models.copy()
    corrupted_models['PIGMENT'] = corrupted_models['PIGMENT'].replace('RED', 'PURPLE')
    with pytest.raises(ValueError, match="Unexpected pigment found: {'PURPLE'}"):
        PghKSCalculator(corrupted_models, sample_base)

    corrupted_base = sample_base.drop(columns='VAR')
    with pytest.raises(ValueError, match='Missing "VAR" column with all KM *.'):
        PghKSCalculator(sample_models, corrupted_base)

    corrupted_base = sample_base[sample_base['VAR'] != 'S']
    with pytest.raises(ValueError, match='Missing a KM constant *.'):
        PghKSCalculator(sample_models, corrupted_base)

    corrupted_base = pd.concat([sample_base, sample_base], axis=0)
    with pytest.raises(ValueError, match='A KM constants is present two times *.'):
        PghKSCalculator(sample_models, corrupted_base)
