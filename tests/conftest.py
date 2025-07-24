from pathlib import Path

import pytest


@pytest.fixture
def formulas_path() -> str:
    return Path('tests') / 'spectrophotometer' / 'ressources' / 'formulas.csv'


@pytest.fixture
def mono_red_path() -> str:
    return Path('tests') / 'spectrophotometer' / 'ressources' / 'mono_red.csv'


@pytest.fixture
def mono_black_path() -> str:
    return Path('tests') / 'spectrophotometer' / 'ressources' / 'mono_black.csv'


@pytest.fixture
def mono_white_path() -> str:
    return Path('tests') / 'spectrophotometer' / 'ressources' / 'mono_white.csv'


@pytest.fixture
def mono_yellow_path() -> str:
    return Path('tests') / 'spectrophotometer' / 'ressources' / 'mono_yellow.csv'


@pytest.fixture
def else_path() -> str:
    return Path('tests') / 'spectrophotometer' / 'ressources' / 'else.csv'
