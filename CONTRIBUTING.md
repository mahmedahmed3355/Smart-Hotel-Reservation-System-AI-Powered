# Contributing

Thanks for contributing to Smart Hotel Reservation System.

## Development Setup

The project targets Python 3.12.

Install the locked development dependencies:

    make install-dev

Alternatively:

    python -m pip install --upgrade pip
    python -m pip install pip-tools==7.6.1
    python -m piptools sync requirements.txt requirements-dev.txt

## Dependency Changes

Runtime dependencies are declared in `requirements.in`.

Development dependencies are declared in `requirements-dev.in`.

After changing dependency inputs, regenerate the corresponding locked files and verify consistency:

    python -m piptools compile requirements.in
    python -m piptools compile requirements-dev.in
    make check

Do not edit generated lock files manually.

## Code Quality

Run Ruff before submitting changes:

    make lint

Run the test suite:

    make test

Run the coverage checks:

    make coverage

For the full local verification workflow:

    make check
    make lint
    make test
    make coverage

## Testing

Add or update tests when changing application behavior.

Tests should be deterministic and isolated from external services where possible. ML tests should use repository test fixtures instead of depending on large local datasets.

Generated model artifacts and local environment files must not be committed.

## Docker Validation

Validate the Compose configuration:

    make docker-config

Build the API image:

    make docker-build

## Pull Requests

Keep pull requests focused and small when possible.

Before opening a pull request:

- Ensure the working tree does not contain generated artifacts.
- Run dependency consistency checks.
- Run Ruff.
- Run the test suite.
- Run coverage checks.
- Update documentation when behavior or configuration changes.

Describe the purpose of the change and include relevant testing performed.

## Security

Do not report suspected security vulnerabilities through public issues.

See `SECURITY.md` for the project's security reporting policy.
