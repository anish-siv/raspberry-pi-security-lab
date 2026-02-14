# Security+ Raspberry Pi Security Lab

## Overview
This repository documents a hands-on security lab built on a Raspberry Pi while studying for the CompTIA Security+ certification. The goal of this project is to reinforce core defensive security concepts through real system configuration, monitoring, and analysis.

This lab focuses on understanding *how* security controls work in practice, not just memorizing exam material.

## Current Focus
- Linux system hardening
- Secure remote access (SSH)
- User permissions and least privilege
- Firewall configuration
- Authentication logging and monitoring
- Automated brute-force protection (Fail2Ban)
- Python-based intrusion monitoring dashboard

## Why This Project
Rather than treating Security+ as a purely theoretical certification, this project applies concepts directly to a live Linux system to build real-world security intuition useful for both cybersecurity and software engineering roles.

## Project Status
### Phase 1 — System Hardening: Completed
- Disabled root SSH login
- Implemented least-privilege user model
- Configured UFW firewall (default deny incoming)
- Secured remote access and authentication

### Phase 2 — Automated Brute-Force Defense: Completed
- Implemented Fail2Ban for SSH brute-force protection
- Configured journald-based log monitoring
- Observed and verified automated IP banning
- Integrated Fail2Ban with firewall enforcement

### Monitoring System: Implemented
- Developed Python-based security monitoring script
- Built real-time GUI dashboard for intrusion monitoring
- Tracks failed login attempts, banned IPs, and suspicious activity

### Phase 3 — Network Intrusion Detection: In Progress
Upcoming goals:
- Detect port scans and suspicious network activity
- Analyze packet-level security events
- Implement intrusion detection using Suricata
- Expand monitoring beyond authentication-based attacks
