import subprocess
import re

def get_fail2ban_status() -> str:
    """
    Returns the output for: sudo fail2ban-client status sshd
    """
    result = subprocess.run(
        ["sudo", "fail2ban-client", "status", "sshd"],
        capture_output=True,
        text=True
    )
    return result.stdout or ""

def parse_status(output: str) -> dict:
    """
    Parses Fail2Ban jail status output for key counters.
    """
    currently_banned = re.search(r"Currently banned:\s*(\d+)", output)
    total_banned = re.search(r"Total banned:\s*(\d+)", output)

    currently_failed = re.search(r"Currently failed:\s*(\d+)", output)
    total_failed = re.search(r"Total failed:\s*(\d+)", output)

    return {
        "currently_failed": currently_failed.group(1) if currently_failed else "0",
        "total_failed": total_failed.group(1) if total_failed else "0",
        "currently_banned": currently_banned.group(1) if currently_banned else "0",
        "total_banned": total_banned.group(1) if total_banned else "0",
    }

def main():
    status_output = get_fail2ban_status()
    stats = parse_status(status_output)

    print("=== Raspberry Pi Security Monitor ===")
    print(f"Failed login attempts (current window): {stats['currently_failed']}")
    print(f"Failed login attempts (total observed): {stats['total_failed']}")
    print(f"Currently banned IPs: {stats['currently_banned']}")
    print(f"Total banned attackers: {stats['total_banned']}")

if __name__ == "__main__":
    main()
