# Release Bundle and Deployment

## GitHub Actions flow

The `Task Manager CI/CD` workflow is a dependency graph. Arrows in the GitHub Actions graph represent the `needs` relationships:

```text
Code quality and lint
        ├──> Backend tests (Python 3.12) ──┐
        ├──> Frontend tests and build ──────┼──> Browser integration tests ──┐
        ├──> Dependency security audit ─────┤                                ├──> Package release
        └──> Pending-test metadata check ───┘                                │
                                                                             └──> GitHub Release (version tags only)
```

Pull requests and branch pushes run the quality, backend, frontend, browser, dependency-audit, and pending-test checks. The package job runs only after every required stage succeeds. Each run uploads backend and browser reports, the built frontend, and a combined web-application bundle with a SHA-256 checksum. The package job writes a build summary to the Actions run.

Pushing a version tag such as `v1.0.0` runs the same checks and publishes the tested bundle and checksum as a GitHub Release. Ordinary pushes and pull requests only retain the bundle as a workflow artifact.

## Bundle contents

The release ZIP contains the compiled React/Vite frontend, the Flask application and migrations, production requirements, this guide, and a manifest with the version and source commit. It deliberately excludes local databases, virtual environments, dependency folders, and secrets.

This is a web application bundle, not a Python wheel: the project is a Flask API with a separately compiled React client, rather than a reusable Python library.

## Deployment requirements

No hosting provider is configured by this repository. To deploy the bundle, the selected host must:

1. Serve `client/dist` as the frontend.
2. Run the Flask API using a production WSGI server, not `python run.py` (that starts Flask's development server).
3. Route `/api` from the frontend's origin to the Flask API so session cookies and CSRF requests remain same-origin.
4. Set `FLASK_ENV=production`, a strong `SECRET_KEY`, an appropriate `DATABASE_URL`, and the desired `APP_TIMEZONE`.
5. Run `flask --app run.py db upgrade` from the packaged `server` directory before starting the API.

The GitHub Release step publishes a tested bundle; it does not deploy to a live host. Configure a host-specific deployment job only after the team selects a hosting service and its deployment credentials.
