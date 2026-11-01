# Contributing & Development Standards

## Git Branching Model
- `main`: Production/Stable integration branch. Direct pushes prohibited.
- `feature/<issue-number>-<description>`: For feature work (e.g. `feature/3-authentication`).
- `fix/<description>`: For bug fixes.
- `test/<description>`: For test additions and test infrastructure changes.

## Commit Guidelines
Use Conventional Commit prefixes:
- `feat:` for new features
- `fix:` for bug fixes
- `test:` for adding or updating tests
- `ci:` for CI/CD changes
- `docs:` for documentation updates

## Pull Request Rules
1. Every PR must be linked to a local backlog issue.
2. Fill out all sections of `.github/PULL_REQUEST_TEMPLATE.md`.
3. Ensure all CI jobs pass:
   - `backend` (Ruff & Pytest)
   - `frontend` (ESLint, Vitest & Build)
   - `pending-tests` (`scripts/check_test_placeholders.py`)
4. Obtain at least one review approval. Final merge coordinated by repository owner (Akash Pawar).

