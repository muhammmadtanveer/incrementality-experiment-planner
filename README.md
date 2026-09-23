# Incrementality Experiment Planner

A dependency-free Python tool for planning geo/holdout-style marketing experiments and interpreting conversion lift.

## Why it matters

Platform-reported ROAS can over-credit advertising. Incrementality testing estimates what changed *because of* an intervention by comparing a treatment group to a comparable holdout group.

## What it does

- Estimates minimum sample size per group from baseline conversion rate, minimum detectable effect, significance level, and power
- Calculates absolute lift, relative lift, and incremental conversions
- Uses a two-proportion test to flag statistically significant results
- Produces transparent JSON output for experiment records

## Run

```bash
python3 app.py --baseline 0.05 --mde 0.01 --power 0.8
python3 app.py --results data/holdout_results.json
```

## Assumptions

This is a planning and learning tool, not a replacement for experimental design review. Groups should be randomized or carefully matched; avoid changing major campaign variables during the test; and pre-register success metrics before launch.
