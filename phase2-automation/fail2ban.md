
# Phase 2 - Fail2Ban SSH Brute Force Protection

## Goal
Protect SSH from brute force and password guessing attacks by automatically banning IP addresses after repeated failed login attempts.

This phase reinforces Security+ concepts:
- Secure remote access (SSH hardening)
- Monitoring and logging (audit trails)
- Automated mitigation and response
- Least privilege (non-root SSH access)

---

## Environment
- Device: Raspberry Pi 5
- OS: Raspberry Pi OS (journal-based logging)
- Protected service: SSH (sshd)

---

## How Fail2Ban Works (High Level)
1. SSH login attempts generate authentication events.
2. Fail2Ban monitors these events from the systemd journal (not /var/log/auth.log).
3. If an IP exceeds a threshold of failed attempts within a defined time window, Fail2Ban bans the IP using firewall rules.

Detection to response flow:
SSH authentication failures -> journald -> Fail2Ban filter -> firewall ban

---

## Configuration
Custom jail file:

/etc/fail2ban/jail.d/sshd.local

```
[sshd]
enabled = true
backend = systemd
port = ssh
maxretry = 5
findtime = 10m
bantime  = 30m
```

### What these settings mean
- maxretry: number of failed login attempts allowed before a ban
- findtime: time window Fail2Ban counts failures within
- bantime: duration the IP is blocked

---

## Validation and Evidence

### Jail status (shows failures and bans)
Command:
```
sudo fail2ban-client status sshd
```

Output (sanitized):
```
Status for the jail: sshd
|- Filter
|  |- Currently failed:	0
|  |- Total failed:	0
|  `- Journal matches:	_SYSTEMD_UNIT=ssh.service + _COMM=sshd
`- Actions
   |- Currently banned:	0
   |- Total banned:	0
   `- Banned IP list:	
```

### Fail2Ban service log (ban and unban events)
Command:
```
sudo journalctl -u fail2ban --since "5 minutes ago" --no-pager | grep -Ei "Ban|Unban|fail2ban\.actions"
```

Output (sanitized):
```
Feb 13 19:38:51 raspberrypi fail2ban.actions[193897]: NOTICE [sshd] Ban <MY_IP>
Feb 13 19:39:22 raspberrypi fail2ban.actions[193897]: NOTICE [sshd] Unban <MY_IP>
```

---

## What I Learned
- SSH authentication activity can be monitored through journald on newer Linux systems.
- Failed login patterns such as invalid user and failed password indicate brute force behavior.
- Fail2Ban provides defense in depth by automatically banning malicious IPs at the network level.
- Understanding log sources is important for configuring real security tools correctly.

---

## Commands Used (Quick Reference)
```
sudo apt install -y fail2ban
sudo systemctl enable --now fail2ban
sudo systemctl restart fail2ban
sudo fail2ban-client status
sudo fail2ban-client status sshd
sudo journalctl -u fail2ban --since "5 minutes ago" --no-pager | grep -Ei "Ban|Unban|fail2ban\.actions"


# Unban command (if accidentally banned)
sudo fail2ban-client set sshd unbanip <YOUR_PC_IP>
```
