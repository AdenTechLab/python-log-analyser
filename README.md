# Python Log Analyser 🔍

A Python-based security log analysis tool that examines Linux authentication logs to identify failed login attempts, track successful logins and flag potentially suspicious IP addresses.

This project demonstrates practical Python scripting, Linux log analysis, automated testing and CI/CD using GitHub Actions.

## 🚀 Features

- **Failed Login Detection:** Identifies failed SSH login attempts from authentication logs.
- **Successful Login Tracking:** Counts successful password and public key logins.
- **IP Address Analysis:** Groups failed login attempts by IP address.
- **Suspicious IP Detection:** Flags IP addresses that reach a configurable failed-login threshold.
- **Username Analysis:** Tracks failed login attempts by username.
- **Custom Thresholds:** Choose how many failed attempts trigger an alert.
- **Report Generation:** Displays a readable summary in the terminal and optionally saves it to a file.
- **Automated Testing:** Uses pytest to verify the analysis functionality.
- **CI/CD Pipeline:** GitHub Actions automatically runs the test suite when changes are pushed or pull requests are opened.

## 🛠️ Technologies Used

- Python 3
- Linux authentication logs
- Regular expressions
- pytest
- Git and GitHub
- GitHub Actions (CI/CD)

## 📁 Project Structure

```text
python-log-analyser/
├── src/
│   └── log_analyser.py
├── tests/
│   └── test_log_analyser.py
├── sample_logs/
│   └── auth.log
├── reports/
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## ⚙️ Getting Started

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

```bash
python src/log_analyser.py
```

The tool uses `sample_logs/auth.log` by default.

### 4. Set a custom alert threshold

For example, flag an IP address after two or more failed login attempts:

```bash
python src/log_analyser.py --threshold 2
```

### 5. Save a report

```bash
python src/log_analyser.py --report reports/summary.txt
```

### 6. Analyse a different log file

```bash
python src/log_analyser.py /path/to/auth.log
```

Use a log file you are authorised to access.

## 🧪 Automated Testing

Run the test suite locally:

```bash
python -m pytest -v
```

The current test suite contains four tests covering:

- Counting failed and successful login attempts.
- Flagging an IP address that reaches the alert threshold.
- Ensuring IP addresses below the threshold are not flagged.
- Handling an empty log file.

**Current status:** All four tests pass locally, and the GitHub Actions CI pipeline is green.

## 🔄 CI/CD Pipeline

GitHub Actions automatically runs the pytest suite when code is pushed to the `main` branch or a pull request targets `main`.

This helps catch regressions and verifies that the automated tests continue to pass as the project evolves.

## 🔐 Security Considerations

- This tool analyses log entries; it does not block IP addresses or prevent login attempts.
- The included authentication logs are sample data for testing.
- Real authentication logs may contain sensitive information. Handle them responsibly and only analyse files you are authorised to access.
- Suspicious activity alerts are indicators for investigation, not proof of an attack.

## 🎯 Project Goals

This project is part of my hands-on learning in Python, Linux, security automation and DevOps practices.

It helps develop practical skills in:

- Python scripting and file handling.
- Linux authentication log analysis.
- Regular expressions and data aggregation.
- Automated testing with pytest.
- CI/CD automation with GitHub Actions.
- Identifying potentially suspicious login activity.

## 👨‍💻 Author

**Aden Ibrahim**

GitHub: [@AdenTechLab](https://github.com/AdenTechLab)

Exploring DevOps, cloud infrastructure, Linux automation and DevSecOps through practical projects.
