import subprocess
import re
import tkinter as tk
from tkinter import ttk
from datetime import datetime

JAIL_NAME = "sshd"
REFRESH_SECONDS = 3  # how often to poll fail2ban


def run_fail2ban_status() -> str:
    """
    Runs: sudo fail2ban-client status <jail>
    This assumes the user has passwordless sudo for the fail2ban-client (recommended).
    """
    result = subprocess.run(
        ["sudo", "fail2ban-client", "status", JAIL_NAME],
        capture_output=True, text=True
    )
    return result.stdout or ""


def parse_status(output: str) -> dict:
    currently_banned = re.search(r"Currently banned:\s*(\d+)", output)
    total_banned = re.search(r"Total banned:\s*(\d+)", output)
    currently_failed = re.search(r"Currently failed:\s*(\d+)", output)
    total_failed = re.search(r"Total failed:\s*(\d+)", output)
    banned_list = re.search(r"Banned IP list:\s*(.*)", output)

    banned_ips = (banned_list.group(1).strip() if banned_list else "")
    if banned_ips == "":
        banned_ips = "None"

    return {
        "currently_failed": currently_failed.group(1) if currently_failed else "0",
        "total_failed": total_failed.group(1) if total_failed else "0",
        "currently_banned": currently_banned.group(1) if currently_banned else "0",
        "total_banned": total_banned.group(1) if total_banned else "0",
        "banned_ips": banned_ips
    }


class MonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Raspberry Pi Security Monitor (Fail2Ban)")
        self.geometry("520x325")
        self.resizable(False, False)

        style = ttk.Style(self)

        available = style.theme_names()
        if "clam" in available:
            style.theme_use("clam")
        elif "alt" in available:
            style.theme_use("alt")

        style.configure("TButton", font=("Arial", 10))

        main = ttk.Frame(self, padding=14)
        main.pack(fill="both", expand=True)

        header = ttk.Label(main, text="Intrusion Detection Monitor", font=("Arial", 16, "bold"))
        header.pack(anchor="w", pady=(0, 10))

        # ASCII-safe (avoid smart punctuation)
        self.status_label = ttk.Label(main, text="Status: starting...")
        self.status_label.pack(anchor="w", pady=(0, 10))

        grid = ttk.Frame(main)
        grid.pack(fill="x", pady=(0, 10))

        self.var_current_failed = tk.StringVar(value="0")
        self.var_total_failed = tk.StringVar(value="0")
        self.var_current_banned = tk.StringVar(value="0")
        self.var_total_banned = tk.StringVar(value="0")
        self.var_banned_ips = tk.StringVar(value="None")
        self.var_last_update = tk.StringVar(value="-")  # ASCII-safe

        def row(r, label, var):
            ttk.Label(grid, text=label).grid(row=r, column=0, sticky="w", padx=(0, 10), pady=2)
            ttk.Label(grid, textvariable=var, font=("Arial", 11, "bold")).grid(row=r, column=1, sticky="w", pady=2)

        row(0, "Failed attempts (current window):", self.var_current_failed)
        row(1, "Failed attempts (total observed):", self.var_total_failed)
        row(2, "Currently banned IPs:", self.var_current_banned)
        row(3, "Total banned attackers:", self.var_total_banned)
        row(4, "Banned IP list:", self.var_banned_ips)

        ttk.Label(main, text="Last update:").pack(anchor="w")
        ttk.Label(main, textvariable=self.var_last_update).pack(anchor="w")

        btns = ttk.Frame(main)
        btns.pack(fill="x", pady=(12, 0))

        ttk.Button(btns, text="Refresh now", command=self.refresh).pack(side="left")
        ttk.Button(btns, text="Unban IP...", command=self.open_unban_dialog).pack(side="left", padx=8)
        ttk.Button(btns, text="Quit", command=self.destroy).pack(side="right")

        self.after(300, self.refresh)

    def refresh(self):
        try:
            out = run_fail2ban_status()
            if "Status for the jail" not in out:
                raise RuntimeError("Unexpected output from fail2ban-client")
            stats = parse_status(out)

            self.var_current_failed.set(stats["currently_failed"])
            self.var_total_failed.set(stats["total_failed"])
            self.var_current_banned.set(stats["currently_banned"])
            self.var_total_banned.set(stats["total_banned"])
            self.var_banned_ips.set(stats["banned_ips"])

            self.status_label.config(text=f"Status: monitoring jail '{JAIL_NAME}'")
            self.var_last_update.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        except Exception as e:
            self.status_label.config(text=f"Status: error ({e})")

        self.after(REFRESH_SECONDS * 1000, self.refresh)

    def open_unban_dialog(self):
        win = tk.Toplevel(self)
        win.title("Unban IP")
        win.geometry("420x140")
        win.resizable(False, False)

        frm = ttk.Frame(win, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Enter IP address to unban:").pack(anchor="w")
        ip_var = tk.StringVar()
        entry = ttk.Entry(frm, textvariable=ip_var)
        entry.pack(fill="x", pady=6)
        entry.focus_set()

        msg_var = tk.StringVar(value="")
        ttk.Label(frm, textvariable=msg_var).pack(anchor="w")

        def do_unban():
            ip = ip_var.get().strip()
            if not ip:
                msg_var.set("Please enter an IP address.")
                return

            if not re.match(r"^(?:\d{1,3}\.){3}\d{1,3}$", ip):
                msg_var.set("That doesn't look like an IPv4 address.")
                return

            cmd = ["sudo", "fail2ban-client", "set", JAIL_NAME, "unbanip", ip]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                msg_var.set(f"Unbanned: {ip}")
                self.refresh()
            else:
                msg_var.set(f"Failed: {res.stderr.strip() or res.stdout.strip()}")

        ttk.Button(frm, text="Unban", command=do_unban).pack(anchor="e", pady=(8, 0))


if __name__ == "__main__":
    app = MonitorApp()
    app.mainloop()
