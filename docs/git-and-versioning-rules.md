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
    * `chore`: Maintaining dependencies, configuration, or repository files.
* **Imperative Mood Rule:** Always use the imperative mood (e.g., "add RAWG client", not "added" or "adding").

## 2. Branching Strategy
Keep `main` stable and test changes before merging them.

* **`main`:** Stable, release-ready code.
* **`dev`:** Integration branch for changes being prepared for `main`.
* **Short-lived branches:** When useful, create branches from `dev` using
  descriptive prefixes such as `feat/`, `fix/`, `refactor/`, `test/`, or
  `docs/`. Merge them back into `dev` after review and testing.
* Review changes and run the test suite before merging. This is the project
  workflow, not a claim of automated branch protection.

## 3. Release Policy
* Tag a tested release when a version is ready.
* Use semantic `vX.Y.Z` version tags, including minor or patch versions when
  appropriate.
* Apply an annotated tag with
  `git tag -a vX.Y.Z -m "Release vX.Y.Z"`.

## 4. .gitignore Rules
The following files and folders must be excluded from version control to prevent security risks and repository bloat:

* **Environment files:** Local `.env` variants contain credentials.
  `.env.example` is the safe template and remains tracked.
* **Python artifacts:** `__pycache__/`, `*.pyc`.
* **Dependencies:** `.venv/`.
* **Database files:** `*.db` (contains machine-specific local data).
* **System files:** `.DS_Store` (macOS metadata).
* **Test artifacts:** `.pytest_cache/`, `.coverage*`, `coverage.xml`, and
  `htmlcov/`.
