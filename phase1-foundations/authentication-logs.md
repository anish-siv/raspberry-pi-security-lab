# Authentication Log Analysis

## Observations
- Invalid user attempts indicate username probing
- Failed password attempts suggest brute-force behavior
- Successful logins confirm authorized access

## Log Source
Authentication events were observed using journalctl on the SSH service.

## Why Logs Matter
Logs provide an audit trail that allows defenders to detect, investigate, and respond to suspicious activity.
