# CHIVE SKILL SYSTEM ARCHITECTURE & TOPOLOGY BLUEPRINT (CLAUDE CODE SPECIFICATION)

This document establishes the structural topology, hook lifecycles, inter-skill interface protocols, and epistemic governance of the **(function)-CHIVE** skill system engineered for full compatibility with **Claude Code**.

---

## 1. Directory Structure & Filesystem Layout

```
claude-code-chive-system/
├── CLAUDE.md                               # Master session instructions for Claude Code
├── ARCHITECTURE.md                         # Structural blueprint & domain disambiguation contract
├── README.md                               # Production setup, quickstart & engineering workflows
├── .claude-plugin/
│   └── plugin.json                         # Native Claude Code plugin manifest
├── .claude/
│   ├── settings.json                       # Claude Code lifecycle hook registrations
│   ├── hooks/                              # Deterministic OS-level shell hooks
│   │   ├── protect-invariants.sh           # PreToolUse hook (edit/write guard & static inspection)
│   │   ├── expert_guard_scanner.py         # Static AST trap detector with auto-remediation templates
│   │   ├── post-skill-verify.sh            # PostToolUse hook (syntax & self-healing diagnostics)
│   │   ├── post_tool_self_heal.py          # Diagnostic recovery engine
│   │   ├── pre-skill-check.sh              # SessionStart hook (registry injection)
│   │   └── fact-check-gate.sh              # CLI runner for fact verification
│   └── skills/                             # Agent Skills open-standard modules
│       ├── orchestrator-CHIVE/             # Master Dispatcher & Task Router
│       │   ├── SKILL.md
│       │   └── scripts/router.py
│       ├── module-boundary-CHIVE/          # Deep Modules & Information Hiding
│       │   └── SKILL.md
│       ├── cognitive-cleanse-CHIVE/        # Cognitive Ergonomics & Lexical Hygiene
│       │   └── SKILL.md
│       ├── design-explorer-CHIVE/          # Multi-Option Design & ADRs
│       │   └── SKILL.md
│       ├── strategic-debt-CHIVE/           # Strategic Engineering & PR Discipline
│       │   └── SKILL.md
│       ├── critical-resilience-CHIVE/      # Critical Path Tuning & Fail-Fast
│       │   └── SKILL.md
│       ├── topology-lifecycle-CHIVE/       # Systems Topology & Wide Events
│       │   └── SKILL.md
│       └── fact-verifier-CHIVE/            # Epistemic Fact-Verification Gate
│           ├── SKILL.md
│           └── scripts/bayesian_admiralty.py
├── tests/                                  # Concurrency & invariance test suites
├── benchmarks/                             # Critical-path performance profilers
├── scripts/                                # Automated validation harnesses
└── docs/                                   # Architectural playbooks & deep references
    ├── EXPERT_RESILIENCE_PLAYBOOK.md
    ├── ANTI_IGNORE_GUIDE.md
    └── VALIDATION_REPORT.md
```

---

## 2. Inter-Skill Interaction & Routing Model

The CHIVE system operates under a centralized hierarchical control plane:

```
                  +-----------------------------------+
                  |        User / Client Goal         |
                  +-----------------+-----------------+
                                    |
                                    v
                  +-----------------------------------+
                  |        orchestrator-CHIVE         |
                  |     (Intent Analysis & Router)    |
                  +-----------------+-----------------+
                                    |
      +-----------------------------+-----------------------------+
      |                             |                             |
      v                             v                             v
+-------------------+     +-------------------+         +-------------------+
|  module-boundary- |     |design-explorer-   |  .....  |critical-resilience|
|      CHIVE        |     |      CHIVE        |         |      CHIVE        |
+---------+---------+     +---------+---------+         +---------+---------+
          |                         |                             |
          +-------------------------+-----------------------------+
                                    |
                                    v
                  +-----------------------------------+
                  |        fact-verifier-CHIVE        |
                  | (Admiralty 6x6, ACH & ICD 203 WEP)|
                  +-----------------+-----------------+
                                    |
                                    v
                  +-----------------------------------+
                  | Validated Professional Deliverable|
                  +-----------------------------------+
```

---

## 3. Domain Disambiguation Contract (Cross-Skill Boundary Arbitration)

To eliminate jurisdictional ambiguity and overlapping responsibilities between skills:

| Conflict Scenario | Skill A vs Skill B | Absolute Demarcation Rule |
| :--- | :--- | :--- |
| **Component Refactoring** | `module-boundary-CHIVE` vs `cognitive-cleanse-CHIVE` | **Public Interface vs Internal Logic**: If the edit touches public signatures, visibility, class boundaries, or coupling -> Governed by `module-boundary-CHIVE`. If the edit is purely intra-function (local variable names, dead code deletion, boolean traps) -> Governed by `cognitive-cleanse-CHIVE`. |
| **Readability vs Performance** | `cognitive-cleanse-CHIVE` (Immutability) vs `critical-resilience-CHIVE` (Zero-Allocation) | **The 5% Critical Path Exemption Rule**: On cold paths (normal business logic), immutability is strictly enforced. On critical hot paths (driving 95% of latency), in-place buffer mutation is allowed provided it is encapsulated inside the module and never leaks references outside. |
| **Design vs Technical Debt** | `design-explorer-CHIVE` vs `strategic-debt-CHIVE` | **Prospective vs Retrospective**: `design-explorer-CHIVE` handles future architecture (evaluating 2-3 design options via *Design It Twice* and authoring ADRs). `strategic-debt-CHIVE` manages past legacy debt and process governance (10-20% investment quotas, 4-Pillar PRs, test pyramids). |
| **Local vs Distributed** | `critical-resilience-CHIVE` vs `topology-lifecycle-CHIVE` | **In-Process Priority Rule**: High throughput and concurrency contention MUST be resolved via local in-memory partitioning or database indexing before considering distributed locks or microservice network splits. |

---

## 4. Error Taxonomy: Operational Error vs Invariant Violation

```
                                  [Error Condition Occurs]
                                             │
               ┌─────────────────────────────┴─────────────────────────────┐
               ▼                                                           ▼
    [OPERATIONAL ERROR]                                         [INVARIANT VIOLATION]
(Business Domain / Anticipated Edge Case)                   (System Axiom / Invariant Breach)
   - Invalid input validation                                  - Balance conservation delta != 0
   - Insufficient funds                                        - Nil pointer on logically mandatory state
   - External dependency timeout                               - Internal memory index corruption
   - Target account not found                                  - Invalid state machine transition
               │                                                           │
               ▼                                                           ▼
    [RETURN RESULT TYPE]                                        [LET IT CRASH (FAIL-FAST)]
Return structured error code / result object.               Abort process immediately (panic / exit(1)).
DO NOT throw unhandled panic.                               MUST NOT be swallowed by catch-all blocks.
System continues serving subsequent requests.               Allow container supervisor to restart clean pod.
```

---

## 5. Mandatory Output Contract
Every task completion must conclude with the formal assessment block:
```markdown
### CRITICAL EVALUATION FIELD (FACT-VERIFIER-CHIVE)
- **CONFIDENCE**: [X%] — [ICD 203 WEP Category] (Confidence Level: High / Moderate / Low)
- **SHADOW JUDGMENT**: [CONSISTENT / FRAGILE / REBUILD]
- **BLIND SPOTS / UNKNOWNS**: [Specific unverified parameters or missing data]
- **FAILURE CONDITIONS**: [Boundary scenarios where this solution breaks down]
```
