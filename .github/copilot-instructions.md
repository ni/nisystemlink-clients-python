# Repository development

## Project conventions

- This is the NI SystemLink Python client library. Service clients and Pydantic
  models live in `nisystemlink/clients`; usage examples, tests, and Sphinx
  documentation live in `examples`, `tests`, and `docs`.
- Follow [CONTRIBUTING.md](../CONTRIBUTING.md) and the existing neighboring code.
  Consult the [decision index](../docs/decisions/README.md) for applicable ADRs
  before changing design or compatibility policy.
  Preserve public client/model contracts and keep package `__init__.py` exports
  and `__all__` consistent. Run the documented export contract tests when changing
  public exports.
- Use the Python floor and dependency constraints in
  [pyproject.toml](../pyproject.toml). Preserve type annotations, Google-style
  docstrings, and existing formatting/import conventions; do not suppress quality
  checks or make unrelated refactors.
- Keep `pyarrow` optional. Verify both base-install behavior and the extra when
  modifying Arrow support.
- Update relevant examples and documentation when behavior changes.

## Development and validation

- Use Poetry (`poetry install`, `poetry run ...`) and the existing Poe tasks.
  Never hand-edit `poetry.lock`; follow the contribution guide for dependency
  regeneration and auditing.
- Add a regression test for behavior changes and run the smallest relevant test
  selection during iteration. Established offline checks are:

  ```sh
  poetry run poe test
  poetry run poe check
  poetry run poe lint
  poetry run poe types
  poetry build
  ```

- Integration tests require SystemLink services and credentials. Prefer the
  existing PR workflow for the Python-version matrix and credentialed integration
  testing. Skipped tests are not proof that integration behavior works.
- Never retrieve, print, or hard-code API keys. Preserve the integration job's
  serialization to prevent shared-service collisions.
- Use Conventional Commits and the
  [pull request template](PULL_REQUEST_TEMPLATE.md). Report exact validation
  commands and outcomes, including checks not run.
