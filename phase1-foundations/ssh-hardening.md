# SSH Hardening

## What Was Done
- Disabled root login over SSH
- Used non-root user with sudo privileges
- Verified that root login attempts are rejected

## Why This Matters
SSH provides full remote command-line access. Allowing root login increases the risk of total system compromise if credentials are leaked or brute-forced.

## Verification
- Root SSH login attempts returned "Permission denied"
- Valid users were able to authenticate successfully
