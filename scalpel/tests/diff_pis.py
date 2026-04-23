#!/usr/bin/env python3
"""diff_pis.py — compare the cowrie honeypot's behavior against the reference
Pi ground truth and emit a list of demerits.

Reads ground_truth.jsonl (from capture_truth.py on the reference Pi), opens
an interactive shell on the cowrie honeypot (port 2222, root/root), runs each
unique command from the ground truth, and flags mismatches.

Cowrie does NOT support SSH's `exec` channel (the `ssh host "cmd"` form), so
we drive it through invoke_shell() like a real attacker would, send each
command, and read until output settles.

Usage:
    pip install paramiko
    python scalpel/tests/diff_pis.py --honeypot <HONEYPOT_IP>

Output:
    scalpel/tests/demerits.jsonl  — one JSON record per command with findings
    scalpel/tests/demerits.md     — human-readable report (share this)
    summary printed to stdout
"""
import argparse
import json
import re
import sys
import time
from collections import defaultdict
from datetime import datetime

try:
    import paramiko
except ImportError:
    sys.stderr.write("paramiko not installed. Run: pip install paramiko\n")
    sys.exit(1)


ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]")
PROMPT_RE = re.compile(r"^[^#$\n]*[#$]\s*$")


def load_ground_truth(path):
    by_cmd = defaultdict(list)
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            by_cmd[rec["cmd"]].append(rec)
    return by_cmd


def classify(records):
    sig = {(r["stdout"], r["stderr"], r["rc"]) for r in records}
    kind = "deterministic" if len(sig) == 1 else "variable"
    canon = records[0]
    ns_avg = sum(r["ns"] for r in records) // len(records)
    return kind, canon["stdout"], canon["stderr"], canon["rc"], ns_avg


def drain(channel, max_wait_s=2.0, quiet_ms=300):
    """Read and discard from channel until quiet for quiet_ms, or max_wait_s elapses."""
    buf = ""
    t0 = time.perf_counter()
    last_data = t0
    while time.perf_counter() - t0 < max_wait_s:
        if channel.recv_ready():
            buf += channel.recv(65536).decode("utf-8", errors="replace")
            last_data = time.perf_counter()
        elif (time.perf_counter() - last_data) * 1000 > quiet_ms:
            break
        else:
            time.sleep(0.02)
    return buf


def open_shell(client):
    channel = client.invoke_shell()
    channel.settimeout(0.5)
    # Let banner / motd / initial prompt settle.
    drain(channel, max_wait_s=3.0, quiet_ms=500)
    return channel


def clean_output(raw, cmd):
    """Strip the command echo and trailing prompt from interactive shell output."""
    text = raw.replace("\r\n", "\n").replace("\r", "\n")
    text = ANSI_RE.sub("", text)
    lines = text.split("\n")

    # First line is usually the shell echoing our command. Drop it if it
    # contains the command.
    if lines and cmd.strip() and cmd.strip() in lines[0]:
        lines = lines[1:]

    # Drop trailing prompt-looking lines and empty lines.
    while lines and (PROMPT_RE.match(lines[-1]) or not lines[-1].strip()):
        lines.pop()

    out = "\n".join(lines)
    if out and not out.endswith("\n"):
        out += "\n"
    return out


def run_in_shell(channel, cmd, timeout_s=15, quiet_ms=700):
    t0 = time.perf_counter_ns()
    channel.send(cmd + "\n")

    buf = ""
    sent_at = time.perf_counter()
    last_data = sent_at
    while time.perf_counter() - sent_at < timeout_s:
        if channel.recv_ready():
            buf += channel.recv(65536).decode("utf-8", errors="replace")
            last_data = time.perf_counter()
        elif (time.perf_counter() - last_data) * 1000 > quiet_ms:
            break
        else:
            time.sleep(0.02)
    t1 = time.perf_counter_ns()

    return clean_output(buf, cmd), "", -1, t1 - t0


def diff_one(expected, actual, kind):
    exp_out, exp_err, exp_rc, exp_ns = expected
    act_out, act_err, act_rc, act_ns = actual
    findings = []

    # Shell mode merges stdout+stderr onto the same terminal stream, so we
    # compare the concatenation.
    expected_combined = exp_out + exp_err
    actual_combined = act_out + act_err

    if kind == "deterministic":
        if expected_combined != actual_combined:
            findings.append("output mismatch")
    else:
        if bool(expected_combined.strip()) != bool(actual_combined.strip()):
            findings.append("output presence differs (one empty, other not)")
        exp_lines = expected_combined.count("\n")
        act_lines = actual_combined.count("\n")
        if exp_lines > 5 and abs(exp_lines - act_lines) > max(3, exp_lines // 2):
            findings.append(f"line count far off ({exp_lines} expected, {act_lines} got)")

    # Only flag rc when we actually captured one (exec-mode). In shell mode
    # act_rc is the -1 sentinel and rc comparison is skipped.
    if act_rc != -1 and exp_rc != act_rc:
        findings.append(f"exit code mismatch ({exp_rc} expected, {act_rc} got)")

    if act_ns > exp_ns * 3 and act_ns > 100_000_000:
        findings.append(f"slow ({exp_ns // 1_000_000}ms expected, {act_ns // 1_000_000}ms got)")

    return findings


def trim(s, n=400):
    return s if len(s) <= n else s[:n] + f"... [+{len(s)-n}B]"


def write_markdown(path, demerits, finding_counts, total, meta):
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Honeypot Demerit Report\n\n")
        f.write(f"**Honeypot:** `{meta['user']}@{meta['host']}:{meta['port']}`  \n")
        f.write(f"**Ground truth:** `{meta['input']}`  \n")
        f.write(f"**Generated:** {meta['timestamp']}\n\n")

        f.write("## Summary\n\n")
        f.write(f"- **Tested:** {total} commands\n")
        f.write(f"- **Clean:** {total - len(demerits)}\n")
        pct = 100 * len(demerits) / total if total else 0
        f.write(f"- **Flagged:** {len(demerits)} ({pct:.1f}%)\n\n")

        f.write("### Findings by type\n\n")
        f.write("| Count | Type |\n|-------|------|\n")
        for tag, count in sorted(finding_counts.items(), key=lambda x: -x[1]):
            f.write(f"| {count} | {tag} |\n")
        f.write("\n")

        f.write("## Flagged commands\n\n")
        for d in demerits:
            f.write(f"### `{d['cmd']}` — {d['kind']}\n\n")
            for finding in d["findings"]:
                f.write(f"- {finding}\n")
            f.write("\n**Expected:**\n```\n")
            f.write(d["expected"]["stdout"] + d["expected"]["stderr"])
            f.write("```\n\n**Got:**\n```\n")
            f.write(d["actual"]["stdout"] + d["actual"]["stderr"])
            f.write("```\n\n---\n\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--honeypot", required=True, help="cowrie honeypot IP")
    ap.add_argument("--port", type=int, default=2222)
    ap.add_argument("--user", default="root")
    ap.add_argument("--password", default="root")
    ap.add_argument("--input", default="scalpel/tests/ground_truth.jsonl")
    ap.add_argument("--output", default="scalpel/tests/demerits.jsonl")
    ap.add_argument("--markdown", default="scalpel/tests/demerits.md")
    ap.add_argument("--quiet-ms", type=int, default=700,
                    help="milliseconds of silence to consider command done")
    args = ap.parse_args()

    by_cmd = load_ground_truth(args.input)
    sys.stderr.write(f"loaded {len(by_cmd)} unique commands from {args.input}\n")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sys.stderr.write(f"connecting to {args.user}@{args.honeypot}:{args.port} ...\n")
    client.connect(
        args.honeypot, port=args.port, username=args.user, password=args.password,
        look_for_keys=False, allow_agent=False, timeout=10,
    )
    channel = open_shell(client)
    sys.stderr.write("shell opened\n\n")

    demerits = []
    finding_counts = defaultdict(int)

    with open(args.output, "w", encoding="utf-8") as out_f:
        for i, (cmd, records) in enumerate(by_cmd.items(), 1):
            kind, exp_out, exp_err, exp_rc, exp_ns = classify(records)
            expected = (exp_out, exp_err, exp_rc, exp_ns)
            try:
                actual = run_in_shell(channel, cmd, quiet_ms=args.quiet_ms)
                findings = diff_one(expected, actual, kind)
            except Exception as e:
                findings = [f"shell error: {e!r}"]
                actual = ("", "", -1, 0)

            status = "OK" if not findings else f"{len(findings)} finding(s)"
            sys.stderr.write(f"[{i}/{len(by_cmd)}] {cmd!r:<60} {status}\n")

            if findings:
                for f_ in findings:
                    tag = f_.split("(")[0].strip().split(":")[0]
                    finding_counts[tag] += 1
                record = {
                    "cmd": cmd,
                    "kind": kind,
                    "findings": findings,
                    "expected": {
                        "stdout": trim(exp_out), "stderr": trim(exp_err),
                        "rc": exp_rc, "ns": exp_ns,
                    },
                    "actual": {
                        "stdout": trim(actual[0]), "stderr": trim(actual[1]),
                        "rc": actual[2], "ns": actual[3],
                    },
                }
                out_f.write(json.dumps(record, ensure_ascii=False) + "\n")
                demerits.append(record)

    channel.close()
    client.close()

    total = len(by_cmd)
    bad = len(demerits)
    meta = {
        "host": args.honeypot, "port": args.port, "user": args.user,
        "input": args.input,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    write_markdown(args.markdown, demerits, finding_counts, total, meta)

    print()
    print(f"=== summary ===")
    print(f"commands tested:  {total}")
    print(f"commands clean:   {total - bad}")
    pct = 100 * bad / total if total else 0
    print(f"commands flagged: {bad}  ({pct:.1f}%)")
    print()
    print("findings by type:")
    for tag, count in sorted(finding_counts.items(), key=lambda x: -x[1]):
        print(f"  {count:4d}  {tag}")
    print()
    print(f"machine-readable: {args.output}")
    print(f"share with team:  {args.markdown}")


if __name__ == "__main__":
    main()
