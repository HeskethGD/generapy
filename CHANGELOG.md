# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Summary

Generapy now exposes Baker–Akhiezer values and ordinary directional derivatives
with hyperelliptic spectral and reference normalizations, with worked numerical
examples. Directional theta and sigma jets avoid constructing full derivative
tensors, and theta reduction selection accounts for derivative work.
Resolved differential bases support integration along chosen finite paths.
First- and second-kind Abel maps use consistent branch choices,
chart continuation preserves sheets more reliably, and repeated integrations reuse numerical
setup. Developer and release instructions have moved into dedicated guides,
and this changelog is displayed in the documentation.

### Added

- `Curve.resolved_differentials_kind_1()` and
  `Curve.resolved_differentials_kind_2()` return callable bases with a
  `CurveDifferentials` metadata record for explicit path integration.
  Automatic forms include numerical polynomial descriptions in original
  curve coordinates, including completed-square shifts; supplied callables
  remain distinguishable and the existing supplied-basis properties retain
  their meaning.
- `rtheta_directional_jet` and `kleinian_sigma_directional_jet` evaluate
  ordinary derivatives along a supplied real or complex direction, including
  through theta period reduction.
- Public `baker_akhiezer` evaluator with hyperelliptic spectral normalization
  and reference normalization. Accepts a `Curve` or sparse polynomial mapping
  with a spectral `point`, or compatible explicit `shift`, second-kind and
  period data. Reference normalization also accepts supplied custom-basis
  curve data. Includes a genus-two sheet-product example.
- `baker_akhiezer_jet` returns zero-safe ordinary directional derivatives for
  both BA normalizations, including dense Abel directions. A reference example
  checks finite derivatives at a numerator zero.

### Changed

- Refocus the README on installation, usage and feedback, with separate
  contributor and release guides. Document AI-first development and welcome
  issue, discussion and citation feedback.
- Display the repository changelog in the documentation, with release summaries
  and links from the README.

### Performance

- Reuse common continued square-root products across hyperelliptic Abel
  differential components at shared quadrature nodes, with evaluation-local,
  precision-aware reuse and unchanged componentwise quadrature.
- Share chart coordinate conversion and ambient-curve validation across
  differential components at each quadrature node, reusing polynomial terms
  for the residual and scale checks.
- Refine theta derivative reduction selection using derivative truncation
  radii, argument shifts, tensor composition and transformed-direction costs.
  Preserve fast decisions for well-conditioned and strongly unreduced cases.
- BA directional jets use direct theta/sigma directional evaluation without
  constructing the full mixed-derivative tensor. The BA interface is unchanged.
- Reuse evaluated theta values and derivative jets for identical requests in
  bounded, context- and precision-aware caches. Large jets bypass retention.
- Reuse immutable Gauss rules across repeated path and chart integrations,
  with bounded caches separated by numerical context and precision; construct
  cold rules using symmetric Legendre root iteration.
- Reuse invariant hyperelliptic Abel data across moving targets and finite
  bases, while retaining target validation and fresh returned matrices.
  Cancel shared branch references in finite-base first-kind Abel maps before
  integration, preserving the marked branch-to-point paths.
- Use the existing fibre-polynomial Newton corrector for chart quadrature
  nodes while retaining branch-consistency checks.

### Fixed

- First- and second-kind hyperelliptic Abel maps now choose branch anchors at
  a shared routing precision, with deterministic distance ties. This prevents
  incompatible cycle lifts at equidistant conjugate branches
  ([#11](https://github.com/HeskethGD/generapy/issues/11)),
  including in the Baker–Akhiezer curve route.
- Chart continuation now checks local sheet separation and full-step/half-step
  consistency, preventing the silent branch switch reported in
  [#4](https://github.com/HeskethGD/generapy/issues/4).
  Ambiguous quadrature nodes are refined and checked against endpoint branch
  labels. Unresolved continuation raises `NoConvergence`.

## [0.1.0] - 2026-10-04

### Initial Release

This is an experimental research release providing arbitrary-precision computation with algebraic curves and Abelian functions.

**What's supported:**
- Algebraic curve representation with automatic period matrix computation
- Abel maps for integration on algebraic curves
- Kleinian sigma and P functions for Abelian function theory
- Abelian function evaluation at arbitrary precision using mpmath
- Arbitrary-precision arithmetic throughout

**Known limitations:**
- API may change in minor releases during the 0.x series
- Numerical stability edge cases under investigation
- Windows testing not yet comprehensive

**API stability promise:**
- 0.x releases are experimental
- Breaking changes may occur in 0.x minor versions with notice in changelog
- Will follow strict semantic versioning from 1.0.0 onwards
- Public API changes will be documented in this changelog

**Features:**
- Algebraic curve representation and period matrix computation
- Kleinian sigma functions with canonical hyperelliptic normalization
- Kleinian P functions (derivatives of log sigma)
- Abelian function evaluation at arbitrary argument vectors
- Integration with mpmath for arbitrary-precision numerics

[0.1.0]: https://github.com/HeskethGD/generapy/releases/tag/v0.1.0
