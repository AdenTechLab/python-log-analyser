
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from log_analyser import analyse_log


def test_counts_failed_and_successful_logins(tmp_path):
    log_file = tmp_path / "auth.log"
    log_file.write_text(
        "Failed password for admin from 192.168.1.10 port 1234 ssh2\n"
        "Failed password for root from 192.168.1.10 port 1235 ssh2\n"
        "Accepted publickey for aden from 192.168.1.20 port 1236 ssh2\n",
        encoding="utf-8",
    )

    result = analyse_log(log_file)

    assert result["total_lines"] == 3
    assert result["failed_logins"] == 2
    assert result["successful_logins"] == 1


def test_flags_ip_at_threshold(tmp_path):
    log_file = tmp_path / "auth.log"
    log_file.write_text(
        "Failed password for admin from 10.0.0.5 port 1234 ssh2\n"
        "Failed password for admin from 10.0.0.5 port 1235 ssh2\n"
        "Failed password for root from 10.0.0.5 port 1236 ssh2\n",
        encoding="utf-8",
    )

    result = analyse_log(log_file, threshold=3)

    assert result["suspicious_ips"] == {"10.0.0.5": 3}


def test_ip_below_threshold_is_not_flagged(tmp_path):
    log_file = tmp_path / "auth.log"
    log_file.write_text(
        "Failed password for admin from 10.0.0.5 port 1234 ssh2\n"
        "Failed password for root from 10.0.0.5 port 1235 ssh2\n",
        encoding="utf-8",
    )

    result = analyse_log(log_file, threshold=3)

    assert result["suspicious_ips"] == {}


def test_empty_log(tmp_path):
    log_file = tmp_path / "auth.log"
    log_file.write_text("", encoding="utf-8")

    result = analyse_log(log_file)

    assert result["total_lines"] == 0
    assert result["failed_logins"] == 0
    assert result["successful_logins"] == 0
    assert result["suspicious_ips"] == {}
