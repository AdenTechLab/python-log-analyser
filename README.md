# Python Log Analyser

A Python security tool for analysing Linux authentication logs, detecting failed login attempts and flagging potentially suspicious IP addresses.

This project combines Python, Linux, Docker, security hardening, automated testing and CI/CD.

## Overview

- Detects failed and successful SSH login attempts.
- Tracks failed logins by IP address and username.
- Flags IP addresses that exceed a configurable threshold.
- Generates reports in the terminal or saves them to a file.
- Runs in a Docker container as a non-root user.
- Uses GitHub Actions to run tests and build the Docker image.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Log analysis and report generation |
| Linux | Authentication log analysis |
| Docker | Application containerisation |
| pytest | Automated testing |
| GitHub Actions | Continuous integration |
| Git and GitHub | Version control |

## Project Structure

```text
python-log-analyser/
├── .github/workflows/
│   └── python-tests.yml
├── sample_logs/
│   └── auth.log
├── src/
│   └── log_analyser.py
├── tests/
│   └── test_log_analyser.py
├── reports/ # Generated reports
├── .dockerignore
├── .gitignore
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AdenTechLab/python-log-analyser.git
cd python-log-analyser
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run the analyser

Analyse the included sample log:

```bash
python src/log_analyser.py
```

Set a custom failed-login threshold:

```bash
python src/log_analyser.py --threshold 2
```

Save the report locally:

```bash
python src/log_analyser.py --report reports/summary.txt
```

## Docker

### Build the image

```bash
docker build -t python-log-analyser:latest .
```

### Run the container

```bash
docker run --rm python-log-analyser:latest
```

### Save a persistent report

A bind mount makes reports available in your workspace after the container stops.

```bash
mkdir -p reports

docker run --rm \
  -v "$PWD/reports:/app/reports" \
  python-log-analyser:latest \
  python src/log_analyser.py \
  --report /app/reports/summary.txt
```

View the report:

```bash
cat reports/summary.txt
```

## Container Security

The Docker image runs the application as a dedicated non-root user named `appuser`, following the principle of least privilege.

```dockerfile
RUN useradd --create-home --uid 1000 appuser
USER appuser
```

Verify the container user:

```bash
docker run --rm --entrypoint id python-log-analyser:latest
```

The expected UID is `1000`, rather than `0` (`root`).

The report directory must be writable by the container user. The current Codespaces setup uses UID `1000` for both the host user and `appuser`.

## Testing

Run the automated test suite:

```bash
python -m pytest -v
```

The four tests cover:

1. Counting failed and successful logins.
2. Flagging IP addresses at the configured threshold.
3. Leaving IP addresses below the threshold unflagged.
4. Handling empty log files.

**Current result:** 4 tests passing.

## CI/CD

GitHub Actions runs the workflow defined in `.github/workflows/python-tests.yml` when changes are pushed to `main` or a pull request targets `main`.

The pipeline:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs dependencies.
4. Runs the automated tests.
5. Builds the Docker image.

**Status:** The pipeline is passing. The image is built in CI but is not published to Docker Hub.

## Security Notes

- The analyser identifies potentially suspicious activity but does not block IP addresses.
- Sample logs are provided for testing.
- Only analyse real logs you are authorised to access.
- Alerts indicate activity worth investigating, not proof of an attack.
- Running as a non-root user reduces privileges but does not eliminate all container security risks.

## Author

**Aden Ibrahim**

[GitHub: @AdenTechLab](https://github.com/AdenTechLab)

Building practical projects in DevOps, cloud infrastructure, Linux automation and DevSecOps.