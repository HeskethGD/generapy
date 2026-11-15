# Contributing to Generapy

Generapy welcomes improvements to numerical algorithms, mathematical examples,
documentation and references. For substantial API or mathematical changes,
open an [issue](https://github.com/HeskethGD/generapy/issues) or
[discussion](https://github.com/HeskethGD/generapy/discussions) to explain the
use case and proposed conventions before implementing them.

## Developer setup

From a source checkout, create an isolated environment and install the
development dependencies:

```sh
python -m venv .venv
.venv/bin/python -m pip install -e '.[develop]'
```

The numerical package lives in `src/generapy/`, tests in `tests/`, runnable
literature examples in `examples/`, and Sphinx documentation in `docs/`.
Read any `AGENTS.md` instructions in the directories you change.

## Checking a change

Run the checks relevant to your change while developing. For example:

```sh
.venv/bin/ruff check .
.venv/bin/pytest tests/unit/test_kleinian.py
.venv/bin/pytest docs/examples/baker_akhiezer.rst
.venv/bin/sphinx-build -W --keep-going -b html docs build/sphinx/html
```

For numerical changes, compare against independent identities, quadrature or
trusted reference values at appropriate working precisions. Agreement between
two wrappers around the same implementation is not an independent check.
Preserve numerical context, basis, normalization and path/lift conventions.
Report accuracy alongside performance measurements; do not assert portable
timing guarantees from one machine.

Documentation examples should reuse tracked runnable code and include
meaningful executable assertions. Check the corresponding example smoke tests
when changing them, and inspect any new or changed plots. The documentation
guide in `docs/AGENTS.md` describes these checks in detail.

The full test and coverage commands used for broader validation are:

```sh
.venv/bin/pytest
.venv/bin/pytest --cov=generapy --cov-report=term-missing --cov-report=xml
```

CI checks supported Python versions, lint, coverage, documentation and package
builds. Changed source lines must meet the workflow's 100% coverage requirement.
See [RELEASING.md](RELEASING.md) for distribution checks and publishing.

## Pull requests

Keep each commit focused on one change. Explain the user-visible behavior,
mathematical conventions and validation in the PR description, and link the
relevant issues. Add an entry under `Unreleased` in `CHANGELOG.md` for
user-visible changes. Include compatibility or migration guidance when an API
changes, and preserve attribution for formulas and reference implementations.
