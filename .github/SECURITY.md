# Security Policy

## Supported Versions

Security fixes are applied to the current `main` branch.

## Reporting a Vulnerability

Do not open a public issue for a suspected security vulnerability.

Please report the issue privately to the repository maintainers and include:

- A description of the vulnerability
- Steps to reproduce the issue
- The affected files or components
- Potential impact
- Any suggested mitigation, if available

Please avoid including credentials, API keys, passwords, private certificates,
or other sensitive data in the report.

## Secret Handling

This repository must not contain:

- Production passwords
- API keys
- Private keys
- Service account credentials
- `.env` files containing real secrets
- Generated model artifacts containing sensitive data

Use environment variables and local configuration files for secrets. Keep real
credentials outside version control.

## Dependency Security

Dependencies are locked through the repository requirements files and are
checked in CI. Dependabot is configured to monitor supported dependency
ecosystems for updates.
