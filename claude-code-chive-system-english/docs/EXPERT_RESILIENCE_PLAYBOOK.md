# EXPERT RESILIENCE & SELF-HEALING ARCHITECTURE PLAYBOOK
*High-Throughput Production Engineering: Mastering Failure Rather Than Assuming Perfection*

---

## 1. Veteran Engineering Axiom

> *"Everything fails all the time."* — Werner Vogels  
> Novice engineers attempt to write code that assumes errors never occur (the illusion of fragile perfection). Veteran engineers build systems that expect networks to partition, databases to deadlock, disks to fill, and upstreams to timeout—ensuring the system detects anomalies, contains the blast radius, and self-heals gracefully.

---

## 2. Catalog of 10 Production Traps & Resilient Solutions

```
+---------------------------------------------------------------------------------------------------------+
|                                10 PRODUCTION TRAPS & EXPERT RESOLUTIONS                                 |
+---------------------------------------------------------------------------------------------------------+
| 1. RETRY STORM (Thundering Herd):                                                                       |
|    - Trap: Immediate tight retry loops during upstream outages, DDOSing recovering dependencies.        |
|    - Fix: Exponential Backoff with Full Jitter: sleep = min(cap, base * 2^attempt) * rand(0.5, 1.5).     |
+---------------------------------------------------------------------------------------------------------+
| 2. UNBOUNDED REMOTE I/O (Cascading Meltdown):                                                           |
|    - Trap: HTTP/RPC invocations lacking timeouts, exhausting thread pools during latency spikes.        |
|    - Fix: Mandatory context deadlines/timeouts on all external network operations (max 2-5s).          |
+---------------------------------------------------------------------------------------------------------+
| 3. DISTRIBUTED LOCK SPLIT-BRAIN:                                                                        |
|    - Trap: Redis lock TTL expires during GC pause, triggering dual parallel mutations.                  |
|    - Fix: Eliminate distributed locks; adopt local Single-Writer In-Memory Partitioning.                |
+---------------------------------------------------------------------------------------------------------+
| 4. DESTRUCTIVE SCHEMA MIGRATION:                                                                        |
|    - Trap: DROP COLUMN / ALTER TYPE locks tables and breaks backward compatibility with live pods.      |
|    - Fix: Expand-Contract Two-Phase Deployment (Phase 1: expand, Phase 2: backfill, Phase 3: contract).|
+---------------------------------------------------------------------------------------------------------+
| 5. SILENT ERROR SWALLOWING (Cordero #98):                                                               |
|    - Trap: Swallowing exceptions with empty catch-all blocks for false uptime metrics (zombie states).   |
|    - Fix: Strict binary error taxonomy (Result Type for operational errors vs Let-It-Crash).            |
+---------------------------------------------------------------------------------------------------------+
| 6. NAKED MUTEX & LOCK ORDERING HAZARDS:                                                                 |
|    - Trap: Acquiring locks without guaranteed defer/finally release, leading to permanent deadlocks.     |
|    - Fix: Monotonic Lock Acquisition Hierarchy and RAII context managers.                               |
+---------------------------------------------------------------------------------------------------------+
| 7. UNBOUNDED QUEUES & OOM CRASHES:                                                                      |
|    - Trap: Unlimited in-memory buffers; sudden traffic spikes trigger kernel OOM kills.                 |
|    - Fix: Bounded Queues with active backpressure and graceful load shedding (HTTP 429).                |
+---------------------------------------------------------------------------------------------------------+
| 8. POISON PILL & CACHE STAMPEDE:                                                                        |
|    - Trap: Identical cache expiration times causes thundering herd cache stampedes on the database.     |
|    - Fix: Cache-Aside with randomized TTL jitter or probabilistic early recomputation (XFetch).         |
+---------------------------------------------------------------------------------------------------------+
| 9. INCONSISTENT CONCURRENT MUTATION:                                                                    |
|    - Trap: Parallel unsynchronized mutations cause dirty reads and balance leakage.                     |
|    - Fix: Optimistic Concurrency Control (version columns) or atomic database CAS updates.              |
+---------------------------------------------------------------------------------------------------------+
| 10. RELEASING UNVERIFIED CODE (Subjectivity Trap):                                                      |
|     - Trap: Deploying changes based on subjective intuition without empirical verification.             |
|     - Fix: Epistemic gatekeeper fact-verifier-CHIVE (Admiralty 6x6 & Bayesian log-odds updating).       |
+---------------------------------------------------------------------------------------------------------+
```

---

## 3. Strict Blocking with Auto-Remediation Mechanics

The system enforces resilience deterministically via two active hooks in `.claude/hooks/`:

1. **PreToolUse Static Inspector (`expert_guard_scanner.py`)**:
   - Inspects code proposed by `Edit` or `Write` tools.
   - If a production trap is detected, terminates with **Exit Code 2**.
   - Emits a complete, copy-paste-ready **Auto-Remediation Template** to `stderr`.
2. **PostToolUse Diagnostic Recovery (`post_tool_self_heal.py`)**:
   - Inspects execution results for runtime failures (deadlocks, syntax errors, invariant breaches).
   - Injects concrete self-healing advice directly into Claude Code's session.
