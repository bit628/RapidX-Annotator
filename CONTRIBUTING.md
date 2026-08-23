# Contributing to RapidX Annotator

Thank you for helping improve RapidX Annotator. Bug reports, documentation corrections, reproducible examples, and focused code changes are welcome.

## Before you start

- Search the [existing issues](https://github.com/bit628/RapidX-Annotator/issues) before opening a new one.
- Use the structured [bug report](https://github.com/bit628/RapidX-Annotator/issues/new?template=01_bug_report.yml) or [feature request](https://github.com/bit628/RapidX-Annotator/issues/new?template=02_feature_request.yml).
- Keep one issue or pull request focused on one problem.
- For security-sensitive findings, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.

## Development setup

The current application is Windows-oriented because parts of the code depend on `pywin32`. The checked-in `requirements.txt` is a research dependency snapshot and contains legacy/model-specific pins; review it before installation and use an isolated environment.

```powershell
git clone https://github.com/bit628/RapidX-Annotator.git
cd RapidX-Annotator
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
cd src
python main.py
```

Model-assisted prediction also requires compatible model modules and trained weights that are not bundled with this repository.

## Making a change

1. Fork the repository and create a short-lived branch from `main`.
2. Keep changes small and explain the motivation in the pull request.
3. Run the relevant checks locally. At minimum, ensure all Python source files still parse.
4. Update the README or other documentation when behavior or setup changes.
5. Add a screenshot for visible UI changes.

## Data and repository hygiene

Do not commit:

- real usernames, passwords, tokens, or password hashes;
- local operation logs or machine-specific paths;
- confidential or restricted radiographic images;
- large model weights or generated artifacts without maintainer approval;
- third-party assets without clear redistribution permission.

Use only anonymized, redistribution-safe samples in issues and pull requests. Remove personal information from screenshots and logs.

## Pull request checklist

- The change has a clear purpose and a linked issue when appropriate.
- Source files parse and the changed workflow has been tested as far as practical.
- Documentation and screenshots are included where needed.
- No credentials, private data, generated logs, or model weights are included.
- The pull request does not claim a license, release, or compatibility status that the repository has not established.

Maintainers may ask for a smaller change, additional evidence, or revisions before merge.
