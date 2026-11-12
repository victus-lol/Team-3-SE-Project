# Release Bundle and Deployment

## GitHub Actions flow

The `Task Manager CI/CD` workflow is a dependency graph. Arrows in the GitHub Actions graph represent the `needs` relationships:

```text
                         ┌──> 2. Backend API & Regression ──┐
                         │                                  │
1. Lint & Code Quality ─┼──> 3. Frontend & UX ─────────────┼──> 5. E2E & Latency ──┐
                         │                                  │                       │
                         └──> 4. Security & Privacy ────────┴───────────────────────┤
                                                                                     v
                                                              6. Coverage & Quality Gate
                                                                                     │
                                                                                     v
                                                              7. Packaging & Distribution
                                                                                     │
                                                                                     └──> GitHub Release (version tags only)
```

Pull requests and matching branch pushes run the seven numbered DAG stages. Each job writes a table-based report to its GitHub Actions Summary: lint and contract validation; backend test counts and artifacts; frontend tests/build; dependency audits; browser workflows and measured p50/p90/max/load; statement and branch coverage; and package version, checksum, and artifact link. The coverage gate requires at least 80% statement coverage and 60% branch coverage. The performance gate requires 20 authenticated users for 30 seconds, zero request failures, and p90 at or below 3,000 ms. The package stage runs only after all required checks pass.

The workflow retains JUnit and coverage reports, Playwright traces/screenshots, the measured performance JSON, the compiled frontend, and the versioned application bundle as downloadable run artifacts.

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
6. Configure `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, and `MAIL_FROM` to enable password-reset delivery. Use STARTTLS on the usual submission port or `MAIL_USE_SSL=true` for an SSL SMTP endpoint. Set `PUBLIC_APP_URL` to the deployed frontend origin and `PASSWORD_RESET_TOKEN_TTL_SECONDS` to the desired short token lifetime. Keep mail credentials in the host's secret store, never in Git.

The recovery request endpoint deliberately returns the same response for known and unknown addresses. Without SMTP settings, the UI still gives that generic response, but no reset email is delivered; configure a test SMTP sink (such as a local mail catcher) to exercise the full email journey in development.

The GitHub Release step publishes a tested bundle; it does not deploy to a live host. Configure a host-specific deployment job only after the team selects a hosting service and its deployment credentials.
