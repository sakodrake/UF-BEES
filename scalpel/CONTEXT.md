# SCALPEL Team Context

> **Purpose:** paste into Claude/ChatGPT/Cursor/etc. at the start of any conversation during the hackathon to bring the AI up to speed on the project. Update this file as the project evolves so future context loads stay accurate.

---

## Event Overview

**Project SCALPEL** is the cybersecurity hackathon at eMERGE Americas 2026 in Miami Beach. Hosted by USF Institute of Applied Engineering (IAE) and DEVCOM Army Research Lab, with partners eMERGE Americas, Amazon AWS, and Florida High Tech Corridor.

**Dates:** April 22–24, 2026
- **April 22 (Day 1):** Travel/arrival day. Optional Spookstock social concert 5–10 PM.
- **April 23 (Hackathon Day 1):** Badge pickup 8:30-9:00, opening 9:30-9:45, hacking 10 AM – 6:30 PM hard stop.
- **April 24 (Hackathon Day 2):** Work 9 AM – 12 PM, then presentations + Red Team testing 12–3 PM simultaneously, awards 4–5 PM.

**Location:** Miami Beach Convention Center, 1901 Convention Ctr Dr, Miami Beach, FL 33139. First Floor, near the National Security Stage.

**Prize:** 1st place = **$5,000 in AWS credits**. 2nd and 3rd also recognized.

**Primary contact:** Victoria Jolly, jollyv@usf.edu, 919.886.8963

---

## The Challenge

> *Can you build an edge honeypot system that's so convincing a skilled attacker can't tell it's fake?*

Design a **Hybrid Deception Platform** on Raspberry Pi 5 hardware using the **Cowrie** honeypot framework, blending realistic local and cloud intelligence. A dedicated Red Team (run by the event organizers) will attempt to expose each honeypot using standardized probing scripts.

**Scored on three dimensions (100-point weighted scale):**

| Weight | Category | How Measured |
|--------|----------|--------------|
| **40%** | **Interaction Realism** | Stability, consistency, responsiveness, accuracy vs. a standard Linux reference. Teams start with 50 points; each finding = −1 point. System crash during testing = −10 points. |
| **40%** | **Edge Efficiency** | % of probes handled locally vs. escalated to the cloud |
| **20%** | **Presentation + Design Rationale** | 10-min team presentation + 5-min Q&A. Judge awards 0–100 points. |

**Formula:**
```
realism_points    = 100 × (total_probes − demerits) / total_probes
efficiency_points = 100 × (total_probes − escalations) / total_probes
presentation      = 0–100 (judge-determined)

final_score = 0.4 × realism + 0.4 × efficiency + 0.2 × presentation
```

**Tiebreakers (in order):** Edge Efficiency → Realism → Presentation → judge + Red Team decision. **Edge Efficiency is the #1 tiebreaker — when in doubt, handle it locally.**

**Concrete example from organizer doc:**
30 probes, 9 realism findings, 6 escalations, 90 presentation points →
- Realism: 100 × (30−9)/30 = 70
- Efficiency: 100 × (30−6)/30 = 80
- Final: 0.4(70) + 0.4(80) + 0.2(90) = **78 points**

---

## Judges

DEVCOM Army Research Lab members will participate in observation and judging. ARL researchers proposed this hackathon topic in alignment with DoD modernization priorities.

---

## Official Hackathon Rules

From the brief (Section 8) and hints doc:

- **MUST** use Cowrie for the honeypot framework
- **MUST NOT** reimage the Raspberry Pis
- **MUST NOT** change the honeypot credentials (port 2222, root/root) — system cannot be scored if changed
- **MUST NOT** hack other teams or steal another team's work → **automatic dismissal with zero points**
- **MUST NOT** probe or attack other teams' systems → instant DQ
- **MUST NOT** "phone a friend" — no contacting humans outside the team by phone/text/messaging
- **MUST** send honeypot IP address to Slack group chat by **10:20 AM each day** or **lose points**
- **MAY** use the web or LLMs to help
- **MAY** use any programming languages or libraries

---

## Critical Deadlines

| When | What |
|------|------|
| **4/17/2026** | Slack invite sent to school emails |
| **4/17/2026** | eMERGE 2026 hackathon registration code sent |
| **4/20/2026 5 PM** | Spookstock social registration closes (optional event) |
| **4/22** | Travel & hotel check-in (no required check-in with IAE/eMERGE) |
| **4/23 8:30 AM** | Convention center opens; badge pickup begins |
| **4/23 9:30 AM** | Opening session & welcome remarks |
| **4/23 10:00 AM** | Hackathon begins |
| **4/23 10:20 AM** | **HARD DEADLINE** — honeypot IP must be in Slack |
| **4/23 6:30 PM** | Hard stop — must vacate venue. **NO Pi access after this.** |
| **4/24 9:00 AM** | Convention center reopens, teams resume |
| **4/24 10:20 AM** | **HARD DEADLINE** — honeypot IP must be in Slack (again) |
| **4/24 12:00 PM** | **ALL development work STOPS.** Presentations + Red Team testing begin simultaneously |
| **4/24 3:00 PM** | Presentations and testing end; judges deliberate |
| **4/24 4:10 PM** | Be at National Security Stage for awards ceremony |
| **4/24 5:30 PM** | Convention center closes |

---

## Organizer-Stated Requirements (MUSTs from the brief)

**Edge Agent (Section 3.1) — the Pi-side software must:**
1. Host a realistic decoy service using Cowrie for SSH/SFTP
2. Run a locally-deployed intelligence (logic, ML, AI, LLM) for dynamic, contextually-appropriate responses
3. Intercept and handle **the majority** of Red Team interactions without escalating
4. Implement a filesystem and environment that is **consistent, realistic, and resistant to probing**
5. Escalate to the Cloud when a query/attack pattern is too complex for the local model

**Cloud Application (Section 3.2) — the AWS-side must:**
1. Provide Tier-2 intelligence for interactions exceeding local model capability
2. **Aggregate logs and telemetry from the edge and provide a summary dashboard** of edge/cloud interactions and performance (real deliverable, not optional)
3. Communication must be designed thoughtfully — minimize traffic while maintaining realism

**Escalation Policy (Section 3.3) — must:**
1. Intercept and handle routine Linux commands entirely locally with quick response times
2. Escalate complex/suspicious interactions to the cloud **only when the fidelity improvement justifies the detection risk**
3. Transmit escalated queries **securely and with minimal bandwidth footprint**
4. Maintain **consistent response timing** so escalated vs non-escalated interactions are indistinguishable to latency analysis

---

## Architecture (Three-Tier Intelligence)

```
[Red Team] --ssh root@pi -p 2222--> [Raspberry Pi 5 — HONEYPOT]
                                     |
                                     v
                                  [Cowrie SSH/SFTP]
                                     |
                                     v
                          [Command Intercept Hook]
                                     |
                                     v
                    +---------------[ROUTER]---------------+
                    |                 |                    |
                    v                 v                    v
             TIER 1 (~1ms)     TIER 2 (~500ms)      TIER 3 (~1-3s)
             Lookup table      Ollama local LLM     AWS Bedrock LLM
             Predictable cmds  Variable/state cmds  Complex escalation
                                                    + OpenSearch RAG
```

**Tier 1 — Static lookup table.** Predictable commands (`whoami`, `uname -a`, `pwd`) → hardcoded responses sourced from the reference Pi. Zero latency, zero cost.

**Tier 2 — Ollama local LLM.** Commands with variable output (`ls /tmp`, `ps aux`, `cat /var/log/syslog`). Small model on-Pi (qwen2.5:1.5b recommended), pinned in memory with `keep_alive=-1`.

**Tier 3 — AWS Bedrock.** Complex or novel commands. Expensive — used sparingly, ideally only during naturally-slow commands where latency is invisible.

**The router (escalation policy)** decides which tier handles each command. Its design is the centerpiece of the presentation.

---

## Hardware / Environment

**Provided by organizers:**
- Two Raspberry Pi 5s per team (pre-imaged, 64-bit headless Raspberry Pi OS)
  - Pi #1: honeypot (Cowrie pre-installed)
  - Pi #2: clean reference Debian — our test oracle
- Two keyboards and monitors
- Access to shared AWS environment
- Network infrastructure
- Slack channel for comms (invite sent 4/17)

**AWS services available:** Amazon Bedrock (managed LLMs), EC2 C6i/C7i (custom model deployment), Amazon OpenSearch Serverless (for RAG), CloudWatch (logging/telemetry dashboard).

**Fixed access (DO NOT change):**
- SSH port: **2222**
- Username: **root**, password: **root**
- Command: `ssh root@<pi_ip> -p 2222`

**Other credentials:**
- Cowrie admin: `cowrie` / `honeypot` (for managing the daemon)
- Reference Pi: `pi` / `raspberry` on port 22

---

## Key File Locations (Honeypot Pi)

| Path | Purpose |
|------|---------|
| `~/cowrie/etc/cowrie.cfg` | Main Cowrie configuration |
| `~/cowrie/etc/userdb.txt` | Honeypot user credentials |
| `~/cowrie/share/cowrie/fs.pickle` | Virtual filesystem (critical to harden) |
| `~/cowrie/var/log/cowrie/cowrie.log` | Live event log |
| `~/cowrie/var/lib/cowrie/tty/` | Recorded attacker sessions |
| `~/cowrie/bin/fsctl` | Tool for inspecting/editing the virtual filesystem |
| `~/cowrie/bin/playlog` | Replay a recorded session |
| `~/cowrie/bin/cowrie` | start/stop/status/restart |

Run Cowrie from its Python venv:
```bash
cd ~/cowrie
source cowrie-env/bin/activate
./run.sh   # starts daemon
```

---

## Local LLM (Ollama) — Models Tested on Pi 5

| Model | Speed | Quality | Notes |
|-------|-------|---------|-------|
| `qwen2.5:0.5b` | Fastest | Low | For tightly constrained outputs |
| `qwen2.5:1.5b` | Good | Good | **Recommended starting point** |
| `phi3:mini` | Slower | High | Better instruction following |
| `phi3.5:latest` | ~phi3 | High | More recent training |
| `gemma2:2b` | Moderate | Good | Strong instruction follower |
| `tinyllama` | Very fast | Limited | Weak instruction following |

**CRITICAL — the 30-40 second reload penalty:** If the model unloads, reloading takes 30–40 seconds, which will be instantly flagged by Red Team latency analysis. Pin it with Ollama's `keep_alive: -1`. Verify with:
```bash
curl http://localhost:11434/api/ps
```

**Ollama management:**
```bash
sudo systemctl status ollama       # check service
journalctl -u ollama -f            # live logs
ollama list                        # available models
ollama pull <model>                # download
```

---

## Red Team Probe Dimensions

The Red Team probes in four explicit categories:

1. **Pre-Authentication Fingerprinting** — SSH banner, login messages, protocol quirks
2. **Behavioral Accuracy & Consistency** — responses to standard Linux commands
3. **Filesystem Integrity** — file contents, timestamps, structure, persistence
4. **Latency Analysis** — timing of every command response

Each confirmed finding = −1 point from realism pool.

---

## The #1 Constraint: Debian on ARM64

Our honeypot is compared against a clean Pi running **64-bit Raspberry Pi OS (Debian, aarch64)**. Every response must match:
- `uname -m` → `aarch64`
- `uname -a` → Raspberry Pi OS kernel strings
- `/proc/cpuinfo` → ARM Cortex processors
- `/proc/version` → Debian kernel build
- `lscpu`, `arch`, `dmesg` → all ARM Debian consistent

**There is no option to fake x86 Ubuntu.** The architecture is predetermined by the reference Pi.

---

## Escalation Policy — The Timing Hide-in-Plain-Sight Trick

| Command | Expected Latency | Escalation Safety |
|---------|------------------|-------------------|
| `whoami`, `id`, `pwd` | < 10ms | **Never escalate** — Tier 1 only |
| `ls /tmp`, `ps aux` | 50–200ms | **Local LLM only** — Tier 2 |
| `find / -name ...` | several seconds | **Safe to escalate** — Tier 3 cover |
| `apt list --installed` | 1–2 seconds | **Safe to escalate** |
| `dpkg -l` | 1–2 seconds | **Safe to escalate** |
| `cat /var/log/syslog` | 100ms–1s | Context-dependent |

**Heuristic:** route to the cheapest tier that produces a correct answer, and when we must escalate, hide it inside a command that's expected to be slow.

---

## Team Structure

Hints doc explicitly recommends Day 1 morning team split: one sub-team on Cowrie config + filesystem hardening, one sub-team on local intelligence + integration. Both need working, testable components by end of Day 1.

**Confirmed role split:**

| Role | Files Owned | Day 1 Deliverable |
|------|-------------|-------------------|
| **Cowrie / Filesystem Lead** | `cowrie/cowrie.cfg`, `scripts/harden_fs.py`, `scripts/banner.py` | Fake filesystem matches reference Pi; SSH banner customized |
| **Local LLM Lead (Ollama)** | `local_llm/client.py`, `local_llm/prompt.py`, `local_llm/benchmark.py` | Ollama pinned with keep_alive=-1; `generate()` returns realistic bash in < 800ms |
| **Cloud / AWS Lead** | `aws/lambda_function.py`, `aws/client.py`, `aws/deploy.sh` | Bedrock Lambda deployed; HTTPS endpoint reachable from Pi |
| **Router / Integration Lead** | `router/handle_command.py`, `router/lookup_table.py`, `router/session_state.py`, `cowrie_hook.py` | Cowrie hook wired in; three-tier routing works end-to-end |
| **Test + Presentation Lead** | `tests/attacker_sim.py`, `tests/diff_pis.py`, `slides.pptx`, `notes/decisions.md` | Diff script comparing both Pis; slides 1–2 done |

**Rule:** if anyone is blocked, pair them up. Blocked team members are wasted capacity.

**Code-sharing rules:**
- Each person owns their listed files. Never edit someone else's files without asking.
- Commit to git every 30 minutes (small commits = easy rollbacks)
- Push to `main` only if your code runs. Use branches for experiments.
- Integration Lead pulls changes onto the Pi — nobody else touches the Pi's git checkout
- If you break the Pi: `git reset --hard HEAD~1`, restart Cowrie, tell team

---

## Agreed Function Signatures

These were locked in at kickoff. Don't change them mid-day — it breaks everyone downstream.

```python
# Tier 1: lookup table
lookup_table.get(command: str) -> str | None
# Returns canned response if command is in table, else None

# Tier 2: local LLM
local_llm.generate(command: str, session_state: dict) -> str
# Returns LLM-generated bash output. Blocking call, ~500ms.

# Tier 3: AWS Bedrock
aws_client.escalate(command: str, session_history: list) -> str
# Returns cloud-generated bash output. Blocking call, ~1-3s.

# Main entry point (called by Cowrie hook):
router.handle_command(command: str, session_id: str) -> str
# Routes command through tiers 1→2→3 based on escalation policy
```

---

## Integration Checkpoints (Day 1)

Every 2 hours the team stops and tests the full pipeline together. No checkpoint = no integration = catastrophic merge at hour 8.

- **12:30 PM** — Cowrie running, Ollama loaded, AWS reachable, 10+ Tier 1 commands working
- **2:30 PM** — All 20 Tier 1 commands match reference Pi, Tier 2 working for 5 cmds, escalation policy v1 drafted
- **4:30 PM** — Pipeline stable for 10 min continuous probing, no crashes on edge commands, session state persists
- **6:00 PM** — Final test, commit clean state, plan Day 2

---

## Red Team Defense — Lateral Movement Prep

Lateral movement on a single Linux box (since attackers will be root via root/root login) mostly looks like privilege/credential/network recon. Categories to prepare for, beyond basic identity commands:

**Privilege escalation recon:**
- `sudo -l`, `find / -perm -4000 2>/dev/null`, `find / -writable -type d 2>/dev/null`
- `cat /etc/sudoers` (perm denied), `ls -la /etc/cron*`, `crontab -l`
- `getcap -r / 2>/dev/null`, `cat ~/.bash_history`, `cat ~/.ssh/authorized_keys`

**Network discovery (looking to pivot):**
- `ip a`, `ip route`, `arp -a`, `cat /etc/hosts`, `cat /etc/resolv.conf`
- `netstat -tulpn`, `ss -tulpn`, `ss -tnp`
- `ping <gateway>`, ping sweeps with bash loops

**Persistence mechanism recon:**
- `systemctl list-units --type=service`, `systemctl list-timers`
- `ls /etc/systemd/system/`, `cat /etc/rc.local`

**Credential hunting:**
- `grep -r password /etc 2>/dev/null`
- `find / -name "*.conf" -readable 2>/dev/null | xargs grep -l password`
- `ls -la /var/backups/`, `cat /var/log/auth.log`

**Data exfil prep:**
- `ls /home/*/`, `du -sh /home/*`
- `find / -name "*.sql" -o -name "*.csv" -o -name "*.json" 2>/dev/null`

**Defense strategy: capture ground truth from reference Pi.** Run every command above against the reference Pi (Pi #2) and save the exact output + exit code. Then:
- Deterministic outputs → Tier 1 lookup table
- State-dependent outputs → Tier 2 LLM with examples in prompt
- Commands that fail on real Pi → make sure honeypot fails the SAME way (same error, same exit code)

**Critical: handle "command not found" correctly.** Half of attacker commands will fail. If `nmap` isn't on the reference Pi, our honeypot must say `bash: nmap: command not found`, not pretend nmap is running. Mismatch = burned in seconds.

---

## Hackathon Day 1 (April 23) — Real Schedule

| Time | Activity |
|------|----------|
| 8:30–9:00 AM | Badge pickup & convention center entry |
| 9:30–9:45 AM | Opening session & welcome remarks |
| **10:00 AM** | **Hackathon begins** |
| **10:20 AM** | **HARD DEADLINE: honeypot IP in Slack or lose points** |
| 12:00–1:00 PM | Working lunch (boxed meals provided, no formal break) |
| **6:30 PM** | **HARD STOP — must vacate venue, NO Pi access after this** |

**Day 1 MVP target (by 6:30 PM):** attacker SSHes in on 2222 with root/root → runs `whoami`, `uname -a`, `ls` → gets convincing Tier 1 responses → complex commands fall through to Tier 2 → cloud fallback exists and works. Even if rough around the edges, pipeline must be end-to-end working.

**After 6:30 PM:** teams can continue planning/slide work but have no Pi access. Good time to: document decisions, build slides, analyze logs we captured.

---

## Hackathon Day 2 (April 24) — Real Schedule

| Time | Activity |
|------|----------|
| 9:00 AM | Convention center reopens |
| 9:00 AM–12:00 PM | Final development & presentation prep |
| **10:20 AM** | **HARD DEADLINE: honeypot IP in Slack (again)** |
| **12:00 PM** | **ALL DEVELOPMENT WORK STOPS** |
| 12:00–3:00 PM | Working lunch + team presentations + Red Team testing (simultaneously) |
| 3:00–4:00 PM | Judges deliberate |
| 4:00 PM | Must be at National Security Stage for awards |
| 4:10–5:00 PM | Closing remarks & awards ceremony |
| 5:30 PM | Convention center closes |

**CODE FREEZE = 12:00 PM NOON DAY 2.** No new features after this — fix catastrophic bugs only.

**Important:** presentations run simultaneously with Red Team testing 12–3 PM. This means while part of the team is presenting, the Red Team is hitting our honeypot. **The honeypot must be stable and run without intervention.** Test this carefully before noon.

---

## Presentation Requirements (20% of score)

**10 minutes + 5 minutes Q&A = 15 minutes total. Strictly timed.**

A presentation template will be provided by organizers.

**Required content:**
1. Overall architecture — Edge, Cloud, Escalation Policy
2. Why we chose our local intelligence approach (model selection, lookup strategy, classifier design)
3. How we designed the escalation policy and what triggers a cloud call
4. Tradeoffs between response quality and latency
5. What we discovered during testing that surprised us
6. What we'd do differently with more time

**Build-as-you-go:** one slide per architectural decision, added as decisions are made. Do not leave to the end.

---

## Self-Test Checklist (from hints doc Section 6)

Run through these every few hours:

- What kinds of commands do hackers try when they gain SSH access?
- Do our filesystems look realistic?
- Does our system behave and respond **consistently** across repeated tests?
- Does our system **persist** state when it should persist? (`touch /tmp/x; ls /tmp` → shows `x`; reconnect and check again)
- Do commands a hacker might utilize actually work?
- Do error messages appear realistic (format, exit codes, line numbers)?

**Ground truth testing:** the reference Pi is our oracle. Script a diff between both Pis across every probe command.

---

## Test Oracle Strategy

Build a script that:
1. SSHes into both the honeypot (port 2222) and reference Pi (port 22)
2. Runs every probe command from our test list
3. Diffs the output
4. Flags commands where outputs differ
5. Also flags commands where timing differs by > N milliseconds

Run repeatedly throughout Day 1 and Day 2 morning. Every diff we find is a demerit we can fix before the Red Team finds it.

---

## Operational / Communications

- **Slack channel:** eMERGE 2026 Hackathon. Invite sent 4/17 to school email. Monitor for scoring updates, clarifications, IP changes, schedule changes.
- **Technical questions during event:** post in Slack.
- **AWS experts on-site:** hands-on technical support available.
- **Primary contact:** Victoria Jolly, jollyv@usf.edu, 919.886.8963

---

## Open Questions (resolve Day 1 morning)

1. **Local LLM choice** — start with `qwen2.5:1.5b` or benchmark multiple first?
2. **MVP scope** — confirm minimum demoable system by 6:30 PM Day 1
3. **RAG or no RAG** — OpenSearch Serverless available; worth it or scope creep?
4. **Filesystem strategy** — wholesale copy from reference Pi or selective hardening?
5. **Network behavior for `ping`/`curl`** — real outbound or faked?
6. **Interactive commands** (`vim`, `nano`, `top`) — error, fake, or block?
7. **Day 2 presenter assignments** — who speaks to which section?
8. **How we keep the honeypot running unattended** while team presents 12–3 PM Day 2

---

## Running Decision Log

> Format: `[YYYY-MM-DD HH:MM] DECISION — rationale`

- `[pending]` Local LLM model choice — TBD based on Day 1 benchmarks
- `[pending]` Escalation thresholds — TBD after test probes
- `[pending]` Interactive command handling — TBD
- `[pending]` Network behavior — TBD

---

## Running Lessons Learned

> Populate as we discover things. Feeds into the "surprises" slide.

- *[empty — populate during hackathon]*

---

## Glossary

- **Cowrie** — open-source SSH/Telnet honeypot framework (required)
- **Edge Agent** — software on the Pi (Cowrie + our intelligence layer)
- **Cloud Brain** — AWS-side LLM backend
- **Escalation** — handing off a command from Pi to AWS
- **Demerit** — detectable difference between our honeypot and reference Pi, −1 point each
- **Ground Truth Pi / Reference Pi** — the second Pi running clean Debian, used as the comparison baseline
- **Gauntlet** — the 12–3 PM Day 2 window when Red Team probes our honeypot
- **fs.pickle** — Cowrie's virtual filesystem, stored as a Python pickle file
- **Ollama** — local LLM runtime recommended for the Pi
- **Bedrock** — AWS managed LLM service
- **IAE** — USF Institute of Applied Engineering (event host)
- **ARL** — DEVCOM Army Research Lab (main sponsor, provides judges)

---

## Key URLs

- Cowrie docs: https://docs.cowrie.org/en/stable/
- Ollama API: https://docs.ollama.com/api/introduction
- Ollama models: https://ollama.com/library
- MBCC parking: https://www.miamibeachconvention.com/center-info/directions-parking

---

*Last updated: April 21, 2026 — pre-hackathon planning*
