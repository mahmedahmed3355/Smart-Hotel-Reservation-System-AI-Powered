# Security Policy

## Supported Versions

Security fixes are applied to the current `main` branch.

## Reporting a Vulnerability

Do not open a public issue for a suspected security vulnerability.

Please report the issue privately to the repository maintainers and include:

- A clear description of the vulnerability.
- Steps to reproduce the issue.
- The affected files, components, or configuration.
- The potential security impact.
- Any suggested mitigation, if available.

Please do not include credentials, private keys, access tokens, or other sensitive information that is not required to understand the issue.

## Response Process

The maintainers will review the report and assess the impact.

If the issue is confirmed, remediation will be prepared for the current supported branch. The timing of a fix may depend on severity, reproducibility, and the scope of the affected components.

Please avoid public disclosure until the issue has been reviewed and a remediation plan has been established.

## Dependency Security

Runtime and development dependencies are managed through:

- `requirements.in`
- `requirements-dev.in`

Resolved dependency versions are recorded in:

- `requirements.txt`
- `requirements-dev.txt`

Dependency consistency is checked in CI with `pip check` and `pip-tools`.

## Repository Hygiene

The repository must not contain:

- Production credentials.
- Private keys.
- API tokens.
- Local `.env` files.
- Generated model artifacts.
- Local coverage artifacts.

Repository checks in CI help detect selected hardcoded secrets and forbidden generated artifacts.

## Security-Related Changes

Security-sensitive changes should include focused tests and clear documentation when configuration, authentication, secrets handling, dependency management, or deployment behavior is affected.
