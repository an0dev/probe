# Release Notes

## 0.0.4 — 2026-02-28

Summary
- Rename distribution from `probe` → `prober(s)` during transition to new PyPI name `probers`.
- Update installation documentation and badges to use `pip install probers`.
- Bump package version to `0.0.4` and publish to PyPI as `probers`.
- Updated docs, installers and examples to reference the new package name.

Changes
- `pyproject.toml`: package `name` set to `probers`, version set to `0.0.4`.
- `README.md`: installation instructions and badges updated to refer to `probers`.
- Installers and examples updated to use `pip install probers`.

Notes
- The repository remains `anosd3v/probe` (source code name), while the PyPI distribution name is `probers` to avoid a name conflict.
- A GitHub release draft can be created from the `0.0.4` tag; if you want I can create the release entry on GitHub if you provide a GitHub token or allow me to use the `gh` CLI.

Published
- PyPI: https://pypi.org/project/probers/0.0.4/
## 0.0.7 — 2026-02-28

Summary
- Extend system prompt with operational protocols, exploitation tools/frameworks, and enforce critical constraints.
- Added sample capabilities including nmap, swlpmap, metasploit, Cobalt Strike, and more.
- Improved prompt length for better model performance.

Changes
- `probe/core/default_system_message.py` updated with detailed protocols, constraints, and sample tools.

Published
- pending upload to PyPI

## 0.0.6 — 2026-02-28

Summary
- Bump version to 0.0.6 following user request; no functional changes.

Changes
- Incremented package version.

Published
- pending upload to PyPI
## 0.0.5 — 2026-02-28

Summary
- Adjust README appearance: removed probe logo, centered title and badges for better layout.

Changes
- README.md: logo stripped, title and badges wrapped in centered HTML block.

Published
- pending upload to PyPI

