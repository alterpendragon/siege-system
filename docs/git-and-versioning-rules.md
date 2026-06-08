# Git and Versioning Rules - Siege System

## 1. Commit Message Format
All commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification to ensure a clear project history.

* **Format:** `<type>: <short description in imperative mood>`
* **Types:**
    * `feat`: Adding a new feature.
    * `fix`: Resolving a bug.
    * `docs`: Updating documentation.
    * `test`: Adding or updating tests.
    * `refactor`: Restructuring code without changing functionality.
* **Imperative Mood Rule:** Always use the imperative mood (e.g., "add RAWG client", not "added" or "adding").

## 2. Branching Strategy
To maintain a clean and professional workflow, the project uses a two-branch model:

* **`main`:** Stable branch. Contains only release-ready code. No direct commits allowed.
* **`dev`:** Active development branch. All daily coding happens here. Once a major version (v1.0.0, v2.0.0, etc.) is complete, `dev` is merged into `main`.

## 3. Release Policy
* A release corresponds strictly to major versions as defined in the roadmap.
* Once a version is feature complete and tested, merge `dev` into `main` and apply an annotated tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`.
* No intermediate or minor tags (e.g., no `v1.0.1`) are permitted.

## 4. .gitignore Rules
The following files and folders must be excluded from version control to prevent security risks and repository bloat:

* **Environment files:** `.env` (contains API keys/credentials).
* **Python artifacts:** `__pycache__/`, `*.pyc`.
* **Dependencies:** `.venv/`.
* **Database files:** `*.db` (contains machine-specific local data).
* **System files:** `.DS_Store` (macOS metadata).
