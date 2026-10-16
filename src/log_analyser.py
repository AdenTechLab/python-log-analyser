
#!/usr/bin/env python3

import argparse
import re
from collections import Counter
from pathlib import Path

FAILED_LOGIN_PATTERN = re.compile(
    r"Failed password for (?:invalid user )?(\S+) from (\S+)"
)

SUCCESSFUL_LOGIN_PATTERN = re.compile(
    r"Accepted (?:password|publickey) for (\S+) from (\S+)"
)


def analyse_log(log_path: Path, threshold: int = 3) -> dict:
    """Analyse an authentication log and return a security summary."""
    failed_by_ip = Counter()
    failed_by_user = Counter()
    successful_by_ip = Counter()
    total_lines = 0

    with log_path.open("r", encoding="utf-8", errors="replace") as log_file:
        for line in log_file:
            total_lines += 1

            failed_match = FAILED_LOGIN_PATTERN.search(line)
            if failed_match:
                username, ip_address = failed_match.groups()
                failed_by_ip[ip_address] += 1
                failed_by_user[username] += 1
                continue

            successful_match = SUCCESSFUL_LOGIN_PATTERN.search(line)
            if successful_match:
                _, ip_address = successful_match.groups()
                successful_by_ip[ip_address] += 1

    suspicious_ips = {
        ip_address: count
        for ip_address, count in failed_by_ip.items()
        if count >= threshold
    }

    return {
        "total_lines": total_lines,
        "failed_logins": sum(failed_by_ip.values()),
        "successful_logins": sum(successful_by_ip.values()),
        "failed_by_ip": dict(failed_by_ip.most_common()),
        "failed_by_user": dict(failed_by_user.most_common()),
        "successful_by_ip": dict(successful_by_ip.most_common()),
        "suspicious_ips": suspicious_ips,
    }


def print_report(summary: dict) -> None:
    """Print the analysis results in a readable format."""
    print("\n=== Linux Authentication Log Report ===")
    print(f"Log lines analysed: {summary['total_lines']}")
    print(f"Failed logins: {summary['failed_logins']}")
    print(f"Successful logins: {summary['successful_logins']}")

    print("\nFailed logins by IP:")
    if summary["failed_by_ip"]:
        for ip_address, count in summary["failed_by_ip"].items():
            print(f"  {ip_address}: {count}")
    else:
        print("  None")

    print("\nSuspicious IPs:")
    if summary["suspicious_ips"]:
        for ip_address, count in summary["suspicious_ips"].items():
            print(f"  ALERT: {ip_address} had {count} failed login attempts")
    else:
        print("  No IPs met the alert threshold")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyse Linux authentication logs for failed logins."
    )
    parser.add_argument(
        "logfile",
        nargs="?",
        type=Path,
        default=Path("sample_logs/auth.log"),
        help="Path to the authentication log file",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=3,
        help="Failed attempts from one IP required to flag it (default: 3)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Optional path to save the report",
    )
    args = parser.parse_args()

    if args.threshold < 1:
        parser.error("--threshold must be at least 1")

    if not args.logfile.is_file():
        parser.error(f"log file does not exist: {args.logfile}")

    summary = analyse_log(args.logfile, args.threshold)
    print_report(summary)

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        with args.report.open("w", encoding="utf-8") as report_file:
            report_file.write("Linux Authentication Log Report\n")
            report_file.write(f"Log lines analysed: {summary['total_lines']}\n")
            report_file.write(f"Failed logins: {summary['failed_logins']}\n")
            report_file.write(
                f"Successful logins: {summary['successful_logins']}\n"
            )
            report_file.write(f"Suspicious IPs: {summary['suspicious_ips']}\n")
        print(f"\nReport saved to: {args.report}")


if __name__ == "__main__":
    main()
