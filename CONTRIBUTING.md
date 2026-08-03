# Contributing to *nisystemlink-clients-python*

Contributions to *nisystemlink-clients-python* are welcome from all!

*nisystemlink-clients-python* is managed via [git](https://git-scm.com), with
the canonical upstream repository hosted on
[GitHub](https://github.com/ni/nisystemlink-clients-python/).

*nisystemlink-clients-python* follows a pull-request model for development.  If
you wish to contribute, you will need to create a GitHub account, fork this
project, push a branch with your changes to your project, and then submit a
pull request.

See [GitHub's official documentation](https://help.github.com/articles/using-pull-requests/)
for more details.

**Important:** Commit titles and messages should adhere to the
[Conventional Commits style](https://www.conventionalcommits.org/en/v1.0.0/#summary)
to ensure proper semantic versioning.

## Getting Started

To contribute to this project, it is recommended that you follow these steps:

1. Fork the repository on GitHub.
2. Run the unit tests on your system (see Testing section). At this point,
   if any tests fail, do not begin development. Try to investigate these
   failures. If you're unable to do so, report an issue through our
   [GitHub issues page](https://github.com/ni/nisystemlink-clients-python/issues).
3. Write new tests that demonstrate your bug or feature. Ensure that these
   new tests fail.
4. Make your change.
5. Run all the unit tests again (which include the tests you just added),
   and confirm that they all pass.
6. Send a GitHub Pull Request to the main repository's master branch. GitHub
   Pull Requests are the expected method of code collaboration on this project.

## Patching older versions
1. Contact the [repository owners](https://github.com/ni/nisystemlink-clients-python/blob/master/.github/CODEOWNERS) for approval and ask them to create a
   branch based on the commit that was used to generate the release to be patched.
   The naming for this branch should follow this guideline:
   - "1.x", if we want to create a new minor version for version 1
   - "1.3.x", if we want to create a new patch version for version 1.3

2. Fork the repository on GitHub.
3. Fetch and check out the maintenance branch created in step 1, then create and
   switch to a working branch from it.
4. Run the unit tests on your system (see Testing section). At this point,
   if any tests fail, do not begin development. Try to investigate these
   failures. If you're unable to do so, report an issue through our
   [GitHub issues page](https://github.com/ni/nisystemlink-clients-python/issues).
5. Write new tests that demonstrate your bug or feature. Ensure that these
   new tests fail.
6. Make your change.
7. Run all the unit tests again (which include the tests you just added),
   and confirm that they all pass.
8. Send a GitHub Pull Request to the main repository branch that was created as a result of step 1. GitHub
   Pull Requests are the expected method of code collaboration on this project.

## Testing

Before running any tests, you must have a supported version of Python (3.10+) and [Poetry](https://python-poetry.org/docs/) installed locally.

It is also helpful to install SystemLink Server and configure the NI Web Server
to run on localhost.

To install all development dependencies required:

```
poetry install
```

To run commands and scripts, spawn a shell within the virtual environment managed by Poetry:

```sh
poetry shell
# Alternatively, you can prefix commands with "poetry run"
poetry run pytest
```

There are a handful of helpful tasks in the `[tool.poe.tasks]` section of the `pyproject.toml` file. These can be run using [Poe](https://github.com/nat-n/poethepoet) like so:

```
poe types
```

To run all tests in place with your current python environment setup:

```
pytest
```

To only run the tests in one particular folder, run

```
pytest tests/myfolder
```

## Maintaining package exports

Package `__init__.py` files are part of the public API surface for this library.
When adding, renaming, or removing a public client or model type, update the
corresponding package exports in the same change.

- Keep `__all__` aligned with the intended public symbols exposed by the package.
- Do not include underscore-prefixed helper types in `__all__` unless they are
  intentionally part of the public API for compatibility reasons.
- If code is generated or assisted by AI, review the package exports explicitly;
  generated updates should preserve the same public/private distinction.
- Run the export contract tests locally after changing package exports:

```sh
pytest tests/test_service_package_exports.py tests/test_models_package_exports.py
```

To run the SystemLink Cloud tests,
[create an API key](https://www.ni.com/documentation/en/systemlink-cloud/latest/manual/creating-an-api-key/)
and then run

```
pytest -m cloud --cloud-api-key XXXXX
```

To run the SystemLink Enterprise tests, obtain a session API key from the
[main-test](https://test.lifecyclesolutions.ni.com/) cluster and then run

```
pytest -m enterprise --enterprise-uri "https://test-api.lifecyclesolutions.ni.com" --enterprise-api-key XXXXX
```

It is important to note that depending on the terminal you are using,
you may need to escape special characters in the API key.

## Security scanning

**Contributors within NI/Emerson**: See the [security scanning reference](https://dev.azure.com/ni/DevCentral/_wiki/wikis/Stratus/160265/Security-scanning-reference) for information on security scanning tools, workflows, and best practices.

**Contributors outside of NI/Emerson**: If you are having issues resolving a vulnerability identified on your PR, consult with a code owner to understand your options for resolution.

## Developer Certificate of Origin (DCO)

   Developer's Certificate of Origin 1.1

   By making a contribution to this project, I certify that:

   (a) The contribution was created in whole or in part by me and I
       have the right to submit it under the open source license
       indicated in the file; or

   (b) The contribution is based upon previous work that, to the best
       of my knowledge, is covered under an appropriate open source
       license and I have the right under that license to submit that
       work with modifications, whether created in whole or in part
       by me, under the same open source license (unless I am
       permitted to submit under a different license), as indicated
       in the file; or

   (c) The contribution was provided directly to me by some other
       person who certified (a), (b) or (c) and I have not modified
       it.

   (d) I understand and agree that this project and the contribution
       are public and that a record of the contribution (including all
       personal information I submit with it, including my sign-off) is
       maintained indefinitely and may be redistributed consistent with
       this project or the open source license(s) involved.

(taken from [developercertificate.org](https://developercertificate.org/))

See [LICENSE](https://github.com/ni/nisystemlink-clients-python/blob/master/LICENSE)
for details about how *nisystemlink-clients-python* is licensed.
