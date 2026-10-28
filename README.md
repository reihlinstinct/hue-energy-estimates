# Hue energy estimates

Design-stage tooling for observation-based Hue lighting energy estimates. Not a power meter. No live collection or account connection is enabled.

Public files contain source and synthetic material only. Household data and credentials must never be committed.

## Validation

Run `python3 scripts/validate_docs.py` and
`python3 -m unittest discover -s tests -v` locally. These checks validate the
presence of design guardrails, not implementation correctness, privacy or a
working Hue integration. No collection runs in CI and no secrets are required.

## License status

No open-source license has been selected yet. Public visibility alone does not
grant reuse rights. License selection is a follow-up before code distribution.
