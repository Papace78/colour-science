"""DataFrame Schema for both composition and reflectance files from R&D.

Composition file contains Formula code, concentrations, batch number, and added weight.
Reflectance file contains the measurements done by the spectrophotometer.
"""

import numpy as np
from pandera import Check, Column, DataFrameSchema, Index

composition_schema = DataFrameSchema(
    columns={
        'FORMULA CODE': Column(
            dtype='str',
            checks=[Check.str_startswith('MU'), Check.str_length(5, 5)],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        'PIGMENT': Column(
            dtype='str',
            checks=[Check.isin(['NUDE', 'WHITE', 'BLACK', 'RED', 'YELLOW'])],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        'BATCH': Column(
            dtype='str',
            checks=[Check.str_startswith('K-'), Check.str_length(7, 7)],
            nullable=True,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        'ADDED WEIGHT': Column(
            dtype='float64',
            checks=[
                Check.greater_than_or_equal_to(min_value=0),
                Check.less_than_or_equal_to(max_value=30),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
    },
    checks=[
        Check(
            lambda df: ('MU000' in df['FORMULA CODE'].to_numpy()),
            error='Missing Card Background formulas (MU000) from CSV.',
        ),
        Check(
            lambda df: ('MU999' in df['FORMULA CODE'].to_numpy()),
            error='...
            .
            .
            .
            ''
