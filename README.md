# Hue energy estimates

[![docs](https://github.com/reihlinstinct/hue-energy-estimates/actions/workflows/docs.yml/badge.svg)](https://github.com/reihlinstinct/hue-energy-estimates/actions/workflows/docs.yml)

Design-stage tooling for observation-based Hue lighting energy estimates. Not a power meter. No live collection or account connection is enabled.

Public files contain source and synthetic material only. Household data and credentials must never be committed.

## Validation

Run `python3 scripts/validate_docs.py` and
`python3 -m unittest discover -s tests -v` locally. These checks validate the
presence of design guardrails, not implementation correctness, privacy or a
working Hue integration. No collection runs in CI and no secrets are required.

Every workflow ends with a `Run summary` job that writes a summary to the top of the run page: which jobs ran, their result and duration, what was skipped and why, the commits and files the run changed, and which checks cover those changes (`.github/ci-coverage-map.json` declares the coverage; files matching no mapping are flagged). The script is `scripts/ci/run_summary.py`.

## License status

No open-source license has been selected yet. Public visibility alone does not
grant reuse rights. License selection is a follow-up before code distribution.
