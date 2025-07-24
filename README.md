# Colour-Science

An example of my code structure and documentation style from a now-defunct internal project. Code is truncated for confidentiality.

## Overview

This project aimed to calculate pigment concentrations needed to achieve a target color. The process involves measuring color reflectance using a spectrophotometer and using Kubelka-Munk theory to determine pigment concentration.

_This code was authored solely by me during a previous role. The project is no longer in use, and logic has been truncated to preserve confidentiality. This repository is intended as a portfolio artifact only._

## What This Demonstrates

- Modular algorithm design
- Data preprocessing and validation
- Scientific modeling and regression workflows
- Structured documentation and pipeline clarity

## Algorithm Overview

The algorithm is structured as a sequential pipeline, where each module processes and passes its output to the next. Below is a high-level overview of the flow:

1. **spectrophotometer**: Reads, validates, and preprocesses the measurement CSVs.
2. **spectral_distribution**: Applies Saunderson correction and interpolates reflectance data. Calculates Lab color values for comparison with predicted reflectances.
3. **calibration**: Builds predictive models for pigment properties (K, S, K/S). Processes monochromes of individual pigments to calculate key variables (KX, SX, KX/SX) per concentration, and fits polynomial regression models for...

...
