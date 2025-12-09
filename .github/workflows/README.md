# GitHub Actions Workflows

This directory contains automated workflows for the PhotosViewer project.

## Available Workflows

### 1. CI (Continuous Integration) - `ci.yml`
**Triggers:**
- Push to `main`, `master`, or `develop` branches
- Pull requests to `main`, `master`, or `develop` branches
- Manual trigger

**Purpose:**
- Runs automated tests across multiple Python versions (3.6-3.11)
- Tests on multiple operating systems (Ubuntu, Windows, macOS)
- Performs code linting with flake8
- Validates code quality and syntax

**Status Badge:**
```markdown
[![CI](https://github.com/MitaHill/PhotosViewer/actions/workflows/ci.yml/badge.svg)](https://github.com/MitaHill/PhotosViewer/actions/workflows/ci.yml)
```

### 2. Release - `release.yml`
**Triggers:**
- Push of version tags (e.g., `v2.9.0`, `v3.0.0`)
- Manual trigger with version input

**Purpose:**
- Builds executable files for Windows, Linux, and macOS
- Creates GitHub releases with downloadable binaries
- Automatically packages the application using PyInstaller

**Usage:**
To create a new release, push a tag:
```bash
git tag v2.9.0
git push origin v2.9.0
```

### 3. CodeQL Security Analysis - `codeql.yml`
**Triggers:**
- Push to `main`, `master`, or `develop` branches
- Pull requests
- Weekly schedule (Monday at 00:00 UTC)
- Manual trigger

**Purpose:**
- Performs automated security vulnerability scanning
- Detects potential security issues in Python code
- Provides code quality analysis

**Status Badge:**
```markdown
[![CodeQL](https://github.com/MitaHill/PhotosViewer/actions/workflows/codeql.yml/badge.svg)](https://github.com/MitaHill/PhotosViewer/actions/workflows/codeql.yml)
```

### 4. PR Labeler - `pr-labeler.yml`
**Triggers:**
- When pull requests are opened, synchronized, or reopened

**Purpose:**
- Automatically labels pull requests based on changed files
- Helps organize and categorize contributions
- Uses configuration from `.github/labeler.yml`

**Labels:**
- `documentation` - Changes to markdown or documentation files
- `dependencies` - Changes to requirements.txt or dependency files
- `tests` - Changes to test files
- `github-actions` - Changes to workflow files
- `python` - Changes to Python source files
- `config` - Changes to configuration files

## Configuration Files

### labeler.yml
Defines rules for automatic PR labeling based on file patterns.

## Adding Status Badges to README

You can add these badges to the main README.md to show workflow status:

```markdown
[![CI](https://github.com/MitaHill/PhotosViewer/actions/workflows/ci.yml/badge.svg)](https://github.com/MitaHill/PhotosViewer/actions/workflows/ci.yml)
[![CodeQL](https://github.com/MitaHill/PhotosViewer/actions/workflows/codeql.yml/badge.svg)](https://github.com/MitaHill/PhotosViewer/actions/workflows/codeql.yml)
[![Release](https://github.com/MitaHill/PhotosViewer/actions/workflows/release.yml/badge.svg)](https://github.com/MitaHill/PhotosViewer/actions/workflows/release.yml)
```

## Workflow Permissions

All workflows use appropriate GitHub token permissions:
- Read access to repository contents
- Write access only where needed (releases, security alerts, PR labels)
- Follows principle of least privilege

## Maintenance

These workflows use the latest stable versions of GitHub Actions:
- `actions/checkout@v4`
- `actions/setup-python@v5`
- `actions/cache@v4`
- `github/codeql-action@v3`

Workflows are configured to be maintainable and follow best practices.
