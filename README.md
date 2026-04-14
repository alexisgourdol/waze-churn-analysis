# Waze User Churn — Exploratory Data Analysis

[![nbviewer](https://img.shields.io/badge/render-nbviewer-orange?logo=jupyter)](https://nbviewer.org/github/alexisgourdol/waze-churn-analysis/blob/main/notebooks/eda.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alexisgourdol/waze-churn-analysis/blob/main/notebooks/eda.ipynb)

Exploratory analysis of one month of Waze app activity to identify behavioural differences between users who churn and those who are retained.

## Business question

Which activity patterns distinguish churned users from retained users, and which features are most likely to be predictive in a churn model?

## Dataset

`data/waze_dataset.csv` — 14,999 users, 13 columns.

| Column | Description |
|---|---|
| `label` | Target: `churned` / `retained` (700 missing) |
| `sessions` | App opens during the month |
| `drives` | Trips of ≥ 1 km during the month |
| `activity_days` | Days the app was opened |
| `driving_days` | Days at least one trip was taken |
| `driven_km_drives` | Total km driven during the month |
| `duration_minutes_drives` | Total drive time (minutes) during the month |
| `total_sessions` | Model estimate of sessions since onboarding |
| `n_days_after_onboarding` | Days since sign-up |
| `total_navigations_fav1/2` | Navigations to saved favourites since onboarding |
| `device` | `iPhone` or `Android` |

Source: Google Advanced Data Analytics Professional Certificate (Coursera).
Note: Data and names used are fictional and are not representative of Waze.

## Preview

![Churn rate drops monotonically as activity days increase](docs/churn_by_activity_days.png)

## Key findings

- **~18% monthly churn** in the labeled population (82/18 class split).
- Churned users drove **~92% more km per driving day** and took **~2× more drives per driving day** — high-intensity, low-frequency use.
- Retained users opened the app on **twice as many days** per month — habitual, low-intensity use.
- **Device type is not a predictor**: iPhone 17.8% vs Android 17.6% churn.

## Repo structure

```
data/               # source dataset
notebooks/
├── eda.ipynb       # exploratory analysis
└── utils.py        # shared helper functions
.devcontainer/      # VS Code dev container (Python 3.12, uv, Claude Code)
Makefile            # lint and clean targets
```

## How to run

```bash
uv run --group dev jupyter lab
```

Then open `notebooks/eda.ipynb`.

## Development

```bash
make lint    # run ruff (isort + format) on notebooks/
make clean   # remove .venv and __pycache__
```
