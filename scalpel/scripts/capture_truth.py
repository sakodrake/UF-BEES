#!/usr/bin/env python3
"""capture_truth.py — record (stdout, stderr, rc, latency) for each probe.

Intended to run ON the reference Pi. Streamed over SSH so nothing lands on
the Pi's disk and nothing contaminates /tmp:

    ssh pi@<ref_pi> 'python3 -' < scalpel/scripts/capture_truth.py \\
        > scalpel/tests/ground_truth.jsonl

Output is JSONL on stdout, one record per (command, run). Progress on stderr.
Environment knobs: RUNS (default 5), TIMEOUT seconds (default 10).
"""
import json
import os
import subprocess
import sys
import time

RUNS = int(os.environ.get("RUNS", "5"))
TIMEOUT = float(os.environ.get("TIMEOUT", "10"))

# Regular probes: run RUNS times each so we can distinguish deterministic
# output (Tier 1 lookup material) from variable output (Tier 2 LLM).
PROBES = [
    # identity / shell
    "whoami", "id", "pwd", "hostname", "hostnamectl",
    "echo $USER", "echo $HOME", "echo $SHELL", "echo $PATH",

    # ARM64/Debian fingerprint surface
    "uname -a", "uname -m", "uname -r", "uname -s", "uname -v", "arch",
    "cat /proc/cpuinfo", "cat /proc/version", "cat /proc/meminfo",
    "cat /etc/os-release", "cat /etc/debian_version", "cat /etc/issue",
    "lscpu", "lsb_release -a", "uptime", "date",

    # memory / disk
    "free -m", "free -h", "df -h", "df -i", "mount",

    # processes
    "ps aux", "ps -ef", "top -bn1", "w", "who", "users", "last -n 10",

    # filesystem listing
    "ls", "ls -la", "ls /", "ls -la /",
    "ls /home", "ls /root", "ls -la /root",
    "ls /tmp", "ls -la /tmp", "ls /var/log", "ls /etc",

    # common file contents (some should fail — we want the exact error text)
    "cat /etc/passwd", "cat /etc/group", "cat /etc/hosts",
    "cat /etc/resolv.conf", "cat /etc/shadow",
    "stat /etc/passwd", "stat /root",

    # environment / history
    "env", "printenv", "history", "alias",

    # networking
    "ip a", "ip addr show", "ip route", "ip link", "arp -a",
    "ss -tulpn", "ss -tnp", "netstat -tulpn", "hostname -I",

    # privilege recon
    "sudo -n -l", "cat /etc/sudoers",
    "ls -la /etc/cron.d", "ls -la /etc/crontab", "ls -la /etc/cron.daily",
    "crontab -l", "cat /root/.bash_history",
    "ls -la /root/.ssh", "cat /root/.ssh/authorized_keys",

    # persistence recon
    "systemctl list-units --type=service --no-pager",
    "systemctl list-timers --no-pager",
    "ls /etc/systemd/system/", "cat /etc/rc.local",

    # package / tool inventory
    "dpkg -l",
    "which python", "which python3", "which python2", "which perl",
    "which ruby", "which gcc", "which make", "which curl", "which wget",
    "which nc", "which ncat", "which nmap", "which tcpdump", "which strace",
    "command -v bash", "bash --version",
    "nc -h", "nc",

    # SSH surface
    "ls /etc/ssh/", "cat /etc/ssh/sshd_config",

    # error-path probes — honeypot must fail IDENTICALLY
    "nmap", "ncat", "nonexistentcmd12345",
    "cat /root/nothere", "ls /nothere", "cd /nothere",

    # misc
    "ls -la ~", "file /bin/bash", "readlink -f /bin/sh",
]

# Slow probes: run once — output is generally stable and full repeats
# would burn minutes on `find /` style commands.
SLOW_PROBES = [
    "find / -perm -4000 -type f 2>/dev/null",
    "find / -writable -type d 2>/dev/null",
    "getcap -r / 2>/dev/null",
    "grep -r password /etc 2>/dev/null",
    "apt list --installed 2>/dev/null",
    "du -sh /home/*",
    "find / -name '*.sql' 2>/dev/null",
]


def run_probe(cmd: str, run: int) -> None:
    t0 = time.perf_counter_ns()
    try:
        # -l: login shell, so /etc/profile + ~/.profile set PATH the way an
        # interactive SSH session sees it (includes /usr/sbin → arp, etc.).
        proc = subprocess.run(
            ["bash", "-lc", cmd],
            capture_output=True,
            timeout=TIMEOUT,
            text=True,
            errors="replace",
        )
        stdout, stderr, rc = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as e:
        stdout = e.stdout or ""
        stderr = (e.stderr or "") + f"\n[timeout after {TIMEOUT}s]"
        rc = 124
    t1 = time.perf_counter_ns()

    record = {
        "cmd": cmd,
        "run": run,
        "rc": rc,
        "ns": t1 - t0,
        "stdout": stdout,
        "stderr": stderr,
    }
    print(json.dumps(record, ensure_ascii=False), flush=True)


def main() -> None:
    total = len(PROBES) * RUNS + len(SLOW_PROBES)
    i = 0
    for cmd in PROBES:
        for run in range(1, RUNS + 1):
            i += 1
            print(f"[{i}/{total}] {cmd} (run {run})", file=sys.stderr, flush=True)
            run_probe(cmd, run)
    for cmd in SLOW_PROBES:
        i += 1
        print(f"[{i}/{total}] {cmd} (slow, 1 run)", file=sys.stderr, flush=True)
        run_probe(cmd, 1)
    print(f"done — {total} records emitted", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
