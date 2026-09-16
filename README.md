# ShelfTrack API

ShelfTrack is a very small FastAPI inventory service built specifically for a real CI/CD demonstration with the existing hosted DeployPilot backend.

The important point is that the workflow does **not** send prepared/fake error messages. GitHub Actions runs normal commands, captures the real command output, and sends that real log to `POST /github/predict`.

## What the application contains

- `GET /health` - simple health endpoint.
- `GET /items` - returns the small in-memory inventory.
- `GET /items/{sku}` - returns one inventory item.
- Real Python dependency installation with `pip`.
- Real configuration validation.
- Real automated tests with `pytest`.
- A GitHub Actions workflow that sends the real result and log to the hosted DeployPilot API.

## Before pushing to GitHub

Create a new GitHub repository for this application and add the same API key used by your DeployPilot GitHub integration:

`Settings -> Secrets and variables -> Actions -> New repository secret`

Secret name:

`DEPLOYPILOT_API_KEY`

The workflow already points to:

`https://deploypilot-ai-api-korea-2026.azurewebsites.net`

## Demo 1 - Real Dependency Error

The supplied `requirements.txt` is intentionally in a broken state for the first run:

```text
fastapi==0.116.1
starlette==0.20.4
```

These versions are incompatible. When you push the project, `pip install -r requirements.txt` should fail during dependency resolution. The workflow captures the **actual pip output** from `ci-logs/dependency.log` and sends it to DeployPilot.

Expected CI behaviour:

1. GitHub Actions performs a real `pip install`.
2. pip reports conflicting dependencies / resolution failure.
3. The configuration and test stages are skipped because the dependency stage failed.
4. The real pip log is sent to `/github/predict`.
5. The failure-type model should classify the log as **Dependency Error**.
6. The workflow is marked failed because the real CI result is FAIL, regardless of the ML gate result.

### Fix it yourself

Open `requirements.txt` and remove this line:

```text
starlette==0.20.4
```

Do not replace it unless you specifically need to pin Starlette. FastAPI will install a compatible Starlette version automatically.

Then commit and push again, for example:

```bash
git add requirements.txt
git commit -m "Fix incompatible Starlette dependency"
git push
```

On the next run, dependency installation, configuration validation, and tests should all pass. The request sent to DeployPilot has an empty `error_log` and `actual_result: PASS`.

Because this is a small change with zero failed tests, no warnings, and no retry count, it is designed to produce a **LOW / ALLOW** result with the current risk model. The exact score is model-generated, so do not hard-code a score in your viva explanation.

## Demo 2 - Real Test Failure

Do this only after fixing the dependency issue and getting a green run.

In `app/service.py`, temporarily change:

```python
LOW_STOCK_THRESHOLD = 5
```

to:

```python
LOW_STOCK_THRESHOLD = 2
```

Commit and push. The application will now treat quantity `3` as `IN_STOCK`, while the real automated test expects it to be `LOW_STOCK`.

GitHub Actions will run `pytest`, which will produce a real assertion failure. The workflow captures the real pytest output and sends it to DeployPilot. The failure-type model should classify it as **Test Failure**.

To fix it, change the value back to `5`, commit, and push again.

## Optional Demo 3 - Real Configuration Error

The workflow currently sets both required variables:

```yaml
APP_ENV: test
INVENTORY_REGION: ap-south
```

To create a real configuration failure, temporarily remove or rename `INVENTORY_REGION` in `.github/workflows/shelftrack-ci.yml` and push.

`scripts/check_config.py` will fail because a required environment variable is missing. The workflow sends that real output to DeployPilot. The model should classify it as **Configuration Error**.

Restore `INVENTORY_REGION` and push again to fix the issue.

## Why this is better for your viva

This demo separates the real CI result from the AI prediction:

- GitHub Actions decides whether the dependency install, configuration check, and tests actually passed or failed.
- The workflow sends the measured metadata and real failure log to the hosted backend.
- Model 1 predicts pipeline failure risk from numeric/categorical CI features.
- Model 2 reads the cleaned real error log and predicts the failure type.
- The recommendation engine prepares the recommendation and preventive advice.
- The quality-gate logic returns ALLOW, WARN, or BLOCK.
- The workflow still fails whenever the real CI checks fail, so AI never hides a genuine build/test problem.

## Useful local commands after the dependency is fixed

Create an environment and install packages:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:APP_ENV="test"
$env:INVENTORY_REGION="ap-south"
python scripts/check_config.py
pytest -q
uvicorn app.main:app --reload
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
export APP_ENV=test
export INVENTORY_REGION=ap-south
python scripts/check_config.py
pytest -q
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs` if you want to show the tiny application's Swagger UI.
