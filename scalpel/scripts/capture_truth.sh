#!/usr/bin/env bash
# capture_truth.sh — run a probe list on the reference Pi and record
# stdout / stderr / exit code / latency for each run.
#
# Output: JSONL on stdout. One line per (command, run) pair.
# Progress is printed to stderr so it doesn't pollute the JSONL.
#
# Usage (run ON the reference Pi, not via ssh from a laptop — we want
# latency measured inside the shell, not round-tripped over the network):
#
#   bash capture_truth.sh > ground_truth.jsonl
#   RUNS=3 bash capture_truth.sh > ground_truth.jsonl      # fewer repeats
#   TIMEOUT=5 bash capture_truth.sh > ground_truth.jsonl   # kill slow probes sooner
#
# After running, copy ground_truth.jsonl back to the repo at
# scalpel/tests/ground_truth.jsonl so diff_pis.py can consume it.

set -u

RUNS="${RUNS:-5}"          # how many times to run each regular probe
TIMEOUT="${TIMEOUT:-10}"   # seconds before a probe is killed

# ---- Regular probes: run RUNS times each so we can tell deterministic
# outputs (Tier 1 lookup material) from variable ones (Tier 2 LLM material).
PROBES=(
  # identity / shell basics
  "whoami"
  "id"
  "pwd"
  "hostname"
  "hostnamectl"
  'echo $USER'
  'echo $HOME'
  'echo $SHELL'
  'echo $PATH'

  # system info — the ARM64/Debian fingerprint surface
  "uname -a"
  "uname -m"
  "uname -r"
  "uname -s"
  "uname -v"
  "arch"
  "cat /proc/cpuinfo"
  "cat /proc/version"
  "cat /proc/meminfo"
  "cat /etc/os-release"
  "cat /etc/debian_version"
  "cat /etc/issue"
  "lscpu"
  "lsb_release -a"
  "uptime"
  "date"

  # memory / disk
  "free -m"
  "free -h"
  "df -h"
  "df -i"
  "mount"

  # processes
  "ps aux"
  "ps -ef"
  "top -bn1"
  "w"
  "who"
  "users"
  "last -n 10"

  # filesystem listing
  "ls"
  "ls -la"
  "ls /"
  "ls -la /"
  "ls /home"
  "ls /root"
  "ls -la /root"
  "ls /tmp"
  "ls -la /tmp"
  "ls /var/log"
  "ls /etc"

  # common file contents
  "cat /etc/passwd"
  "cat /etc/group"
  "cat /etc/hosts"
  "cat /etc/resolv.conf"
  "cat /etc/shadow"             # should fail perm-denied — we want that exact error
  "stat /etc/passwd"
  "stat /root"

  # environment / history
  "env"
  "printenv"
  "history"
  "alias"

  # networking
  "ip a"
  "ip addr show"
  "ip route"
  "ip link"
  "arp -a"
  "ss -tulpn"
  "ss -tnp"
  "netstat -tulpn"              # may be missing — capture the "not found" error
  "hostname -I"

  # privilege recon
  "sudo -n -l"
  "cat /etc/sudoers"            # should fail
  "ls -la /etc/cron.d"
  "ls -la /etc/crontab"
  "ls -la /etc/cron.daily"
  "crontab -l"
  'cat /root/.bash_history'
  "ls -la /root/.ssh"
  "cat /root/.ssh/authorized_keys"

  # persistence recon
  "systemctl list-units --type=service --no-pager"
  "systemctl list-timers --no-pager"
  "ls /etc/systemd/system/"
  "cat /etc/rc.local"

  # package / tool inventory
  "dpkg -l"
  "which python"
  "which python3"
  "which python2"
  "which perl"
  "which ruby"
  "which gcc"
  "which make"
  "which curl"
  "which wget"
  "which nc"
  "which ncat"
  "which nmap"
  "which tcpdump"
  "which strace"
  "command -v bash"
  "bash --version"

  # SSH surface
  "ls /etc/ssh/"
  "cat /etc/ssh/sshd_config"

  # error-path probes — we need the honeypot to fail IDENTICALLY
  "nmap"
  "ncat"
  "nonexistentcmd12345"
  "cat /root/nothere"
  "ls /nothere"
  "cd /nothere"

  # misc
  "ls -la ~"
  "file /bin/bash"
  "readlink -f /bin/sh"
)

# ---- Slow probes: run ONCE because they take seconds and their output
# is generally stable enough that one sample is fine for a Tier 2 prompt.
SLOW_PROBES=(
  "find / -perm -4000 -type f 2>/dev/null"
  "find / -writable -type d 2>/dev/null"
  "getcap -r / 2>/dev/null"
  "grep -r password /etc 2>/dev/null"
  "apt list --installed 2>/dev/null"
  "du -sh /home/*"
  "find / -name '*.sql' 2>/dev/null"
)

# Emit one JSONL record. stdout/stderr are captured to tempfiles so
# newlines / quotes / non-UTF-8 bytes don't break JSON encoding.
run_probe() {
  local cmd="$1"
  local run="$2"
  local out_file err_file start end rc ns
  out_file="$(mktemp)"
  err_file="$(mktemp)"

  start="$(date +%s%N)"
  timeout "$TIMEOUT" bash -c "$cmd" >"$out_file" 2>"$err_file"
  rc=$?
  end="$(date +%s%N)"
  ns=$(( end - start ))

  python3 - "$cmd" "$run" "$rc" "$ns" "$out_file" "$err_file" <<'PY'
import json, sys
cmd, run, rc, ns, out_path, err_path = sys.argv[1:]
with open(out_path, 'r', encoding='utf-8', errors='replace') as f:
    stdout = f.read()
with open(err_path, 'r', encoding='utf-8', errors='replace') as f:
    stderr = f.read()
print(json.dumps({
    "cmd": cmd,
    "run": int(run),
    "rc": int(rc),
    "ns": int(ns),
    "stdout": stdout,
    "stderr": stderr,
}, ensure_ascii=False))
PY

  rm -f "$out_file" "$err_file"
}

total=$(( ${#PROBES[@]} * RUNS + ${#SLOW_PROBES[@]} ))
i=0

for cmd in "${PROBES[@]}"; do
  for run in $(seq 1 "$RUNS"); do
    i=$(( i + 1 ))
    printf '[%d/%d] %s (run %d)\n' "$i" "$total" "$cmd" "$run" >&2
    run_probe "$cmd" "$run"
  done
done

for cmd in "${SLOW_PROBES[@]}"; do
  i=$(( i + 1 ))
  printf '[%d/%d] %s (slow, 1 run)\n' "$i" "$total" "$cmd" >&2
  run_probe "$cmd" 1
done

printf 'done — %d records emitted\n' "$total" >&2
