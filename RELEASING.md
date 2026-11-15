# Releasing Generapy

Publishing is manual through the
[Publish to PyPI workflow](https://github.com/HeskethGD/generapy/actions/workflows/release.yml).
Pushing a commit or tag does not publish a package. The version comes from Git
tags through setuptools-scm; do not edit the generated `_version.py` file.

## Prepare the release

1. Merge the intended changes into `main` and require its CI checks to pass.
   Confirm the final commit and review changes since the previous release tag.
2. Check existing remote tags and PyPI versions, then choose a fresh version.
   Never move a published tag or attempt to replace an existing PyPI version.
3. Finalize `CHANGELOG.md` with the version, release date, user-visible changes,
   issue/PR links, remaining limitations and any migration instructions.
   Start the entry with a concise AI-drafted summary, then review it against
   the actual release diff and resolved issues. Keep deferred proposals out
   of the list of shipped changes. The root changelog is included directly in
   the documentation; update that source rather than copying release entries.
4. Verify documentation and example links, including citations and public APIs.
   Ensure Read the Docs builds the intended release tag/version and displays
   the changelog entry in its navigation.

## Validate distributions locally

Use the development environment described in [CONTRIBUTING.md](CONTRIBUTING.md).
Run relevant tests during development; before a release, run full tests, Ruff,
coverage and the warnings-as-errors documentation build. CI also tests Python
3.11–3.14 and checks changed-line coverage against `origin/main`.

Build into a fresh output directory, for example `build/release-check` if it
does not already contain artifacts:

```sh
.venv/bin/python -m build --outdir build/release-check
.venv/bin/python -m twine check --strict build/release-check/*
```

Check the package name and expected version in both the wheel and source
distribution. A build before the final tag normally has a development version;
the publishing workflow validates the final tagged version. Install the wheel
in a separate clean environment with runtime dependencies only, and run smoke
checks from outside the source checkout so imports cannot accidentally use
the editable package. Include the public BA function in those checks.

## Trusted Publishing setup

The repository must have a GitHub environment named `pypi`, with a
[PyPI Trusted Publisher](https://docs.pypi.org/trusted-publishers/adding-a-publisher/)
registered for owner `HeskethGD`, repository `generapy`, workflow `release.yml`
and environment `pypi`. This uses OIDC and does not require a PyPI API token.
Verify the existing configuration before publishing.

## Publish and verify

1. Create and push a fresh tag on the intended commit, for example `v0.2.0`.
   The workflow accepts `vMAJOR.MINOR.PATCH` and `a`, `b` or `rc` prerelease
   suffixes. Confirm availability before selecting the version.
2. Open **Actions → Publish to PyPI → Run workflow**, select `main`, and enter
   that tag. The tagged commit must be an ancestor of `main`.
3. The workflow tests the tagged commit on supported Python versions, runs
   lint and documentation checks, builds and validates the wheel and sdist,
   checks metadata and an installed wheel, then publishes through Trusted
   Publishing. It uploads the validated distributions as workflow artifacts.
4. After publication, install the exact PyPI version in a clean environment,
   verify its version and public APIs, and check the versioned documentation.
5. Create GitHub release notes for the tag using the reviewed changelog summary
   and a link to its versioned documentation entry. Verify the README changelog
   link and the release's documentation page after publication.
   Close completed issues only when their acceptance checks are satisfied.

If a published version needs corrections, make a new release with a new tag
and version.
