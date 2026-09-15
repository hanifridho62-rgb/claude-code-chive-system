import os

base_skills = "/tmp/claude_chive_system/.claude/skills"

# 1. orchestrator-CHIVE
s_orchestrator = """---
name: orchestrator-CHIVE
description: Master Orchestrator and Dispatcher for the CHIVE Skill System. Analyzes complex engineering requests, detects architectural intent, coordinates multi-skill execution, and enforces the epistemic fact-verification gate.
when_to_use: Use when starting any non-trivial coding, refactoring, architectural planning, code review, or multi-faceted software engineering workflow.
argument-hint: [task-description-or-goal]
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# ORCHESTRATOR-CHIVE: Master Dispatcher & Workflow Engine

`orchestrator-CHIVE` serves as the central control plane (CPU/Dispatcher) for the entire CHIVE software engineering skill ecosystem. It analyzes project requirements, performs task decomposition, activates the appropriate domain-specialized skills, and governs the execution lifecycle using deterministic OS hooks and an epistemic fact-verification gate.

## 1. System Topology & Domain Mapping

```
                      +-----------------------------+
                      |     USER / CLAUDE CODE      |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |      orchestrator-CHIVE     |
                      |   (Dispatcher & Workflow)   |
                      +--------------+--------------+
                                     |
    +-----------------+--------------+---------------+------------------+
    |                 |                              |                  |
    v                 v                              v                  v
+-----------+   +-----------+                  +-----------+      +-----------+
|  module-  |   | cognitive-|                  | critical- |      | topology- |
| boundary- |   |  cleanse- |     ......       |resilience-|      |lifecycle- |
|   CHIVE   |   |   CHIVE   |                  |   CHIVE   |      |   CHIVE   |
+-----+-----+   +-----+-----+                  +-----+-----+      +-----+-----+
      |               |                              |                  |
      +---------------+--------------+---------------+------------------+
                                     |
                                     v
                      +-----------------------------+
                      |     fact-verifier-CHIVE     |
                      |   (Mandatory Epistemic Gate)|
                      +-----------------------------+
```

## 2. Invocation Prerequisites & Hooks

### A. Specific & General Trigger Conditions
- **General**: Triggered whenever the user requests architectural planning, new module implementation, medium-to-large scale refactoring, deep code reviews, or systems performance optimization.
- **Specific**:
  1. *Multi-domain Tasks*: Requests touching more than one engineering boundary (e.g., designing an API interface while optimizing compound database indices and setting up regression test suites).
  2. *Architectural Brainstorming*: Requests requiring path classification into Spike, Bounded, or Architectural workflows (following `user:brainstorming-hive`).
  3. *Fact-Intensive Assertions*: Any performance claim, latency benchmark, or bug root-cause analysis requiring independent empirical verification.

### B. Hook Execution Lifecycle
1. **Pre-Execution Hook (`pre_chive_hook`)**:
   - Executes automated intent analysis via the router script:
     ```bash
     python3 "$CLAUDE_PROJECT_DIR/.claude/skills/orchestrator-CHIVE/scripts/router.py" "$TASK_PROMPT"
     ```
   - Inspects repository status (git cleanliness, configuration files, test suite baseline).
   - Validates that no protected architectural invariants are being breached.
2. **Runtime Coordination Hook**:
   - Decomposes the task into modular, verifiable steps (*task decomposition*).
   - Sequentially dispatches the appropriate specialized skills.
   - Isolates code edits to maintain deep module boundaries.
3. **Post-Execution Hook (`post_chive_hook`)**:
   - **MANDATORY**: Triggers `fact-verifier-CHIVE` to audit empirical claims, test outcomes, and architectural impacts against NATO STANAG 2064 / Admiralty 6x6 matrices and ICD 203 Words of Estimative Probability (WEP).
   - Ensures all unit tests pass (100%) and linter checks are clean before presenting final results.

## 3. Skill Routing Matrix

| Project Requirement Signals | Primary Target Skill | Supporting Skill |
| :--- | :--- | :--- |
| New class design, decomposing monoliths, public API interfaces | `module-boundary-CHIVE` | `design-explorer-CHIVE` |
| Code review, variable naming, dead code audit, working memory load | `cognitive-cleanse-CHIVE` | `module-boundary-CHIVE` |
| New architectural plans, ADR documentation, data structure selection | `design-explorer-CHIVE` | `orchestrator-CHIVE` |
| PR creation, unit/integration test pyramids, technical debt management | `strategic-debt-CHIVE` | `fact-verifier-CHIVE` |
| Latency optimization, SQL indexing, fail-fast boundaries, lock contention | `critical-resilience-CHIVE` | `module-boundary-CHIVE` |
| Modular Monolith vs Microservices, Wide Events logging, Zero-Trust API | `topology-lifecycle-CHIVE` | `strategic-debt-CHIVE` |
| Empirical benchmark validation, technical assertion verification | `fact-verifier-CHIVE` | *(Mandatory Cross-Skill Gate)* |

## 4. Standard Professional Output Contract
Every orchestration turn must conclude with the mandatory assessment block:
```markdown
### CRITICAL EVALUATION FIELD (FACT-VERIFIER-CHIVE)
- **CONFIDENCE**: [X%] — [ICD 203 WEP Category] (Confidence Level: High / Moderate / Low)
- **SHADOW JUDGMENT**: [CONSISTENT / FRAGILE / REBUILD]
- **BLIND SPOTS / UNKNOWNS**: [Specific unverified parameters or missing data]
- **FAILURE CONDITIONS**: [Boundary scenarios where this solution breaks down]
```
"""

# 2. module-boundary-CHIVE
s_module_boundary = """---
name: module-boundary-CHIVE
description: Enforces deep module architecture, information hiding, high depth-to-interface ratio, and eliminates shallow boilerplate classes, pass-through layers, and temporal decomposition (Ousterhout Ch 4-8, Cordero #1, #12, #15, #23, #28, #31, #37).
when_to_use: Use when designing module interfaces, decomposing monolithic services, refactoring anemic domain models, or resolving leaky abstractions.
argument-hint: [file-or-module-path]
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write
---

# MODULE-BOUNDARY-CHIVE: Module Decomposition & Interface Boundaries

`module-boundary-CHIVE` guarantees that every software component is designed as a **Deep Module**: concealing massive implementation complexity behind a concise, intuitive, and stable public interface.

## 1. Invocation Prerequisites & Hooks

### A. Trigger Conditions
- **Specific**:
  - Detection of *pass-through methods* (methods that merely forward arguments to another function with an identical signature without transforming abstraction levels).
  - Detection of *information leakage* (internal data representations or storage choices exposed to external callers).
  - Proliferation of 10-line anemic classes loaded with mechanical getters/setters (*classitis*).
  - Business logic partitioned chronologically across time steps rather than knowledge domains (*temporal decomposition*).
- **General**: Designing new subsystems, restructuring domain services, or refactoring controller/service/repository layers.

### B. Hook Actions
- **Pre-Hook**: Audit the depth-to-interface ratio: `Depth Ratio = (Complexity of Implementation) / (Complexity of Interface)`. Reject shallow modules where the interface is as complex as the implementation.
- **Runtime Hook**:
  1. Pull complexity downward: encapsulate edge-case handling, retries, and synchronization inside the module.
  2. Design interfaces to be *somewhat general-purpose* (addressing current requirements while remaining adaptable to 2-3 natural variations without interface clutter).
- **Post-Hook**: Verify that internal data structures are completely shielded from external mutation. Delegate verification to `fact-verifier-CHIVE`.

## 2. Core Principles & Anti-Pattern Red Flags

1. **Deep Modules vs Shallow Modules (Ousterhout Ch 4)**:
   - Deep modules maximize functional leverage (e.g., Unix file I/O: `open`, `read`, `write`, `close`).
   - Red Flag: Proliferating mini-classes that add cognitive surface without abstractive power.
2. **Information Hiding vs Information Leakage (Ousterhout Ch 5, Cordero #15, #23)**:
   - Hide storage formats, serialization schemas, and algorithmic invariants.
   - Eliminate temporal decomposition (e.g., separate classes for `ReadPhase`, `ParsePhase`, `WritePhase` sharing naked state).
3. **Different Layers, Different Abstractions (Ousterhout Ch 7, Cordero #31)**:
   - Each architectural tier must fundamentally alter the level of abstraction. Eliminate pass-through methods and pass-through variables.
4. **Pull Complexity Downward (Ousterhout Ch 8, Cordero #37)**:
   - It is vastly more economical for the module author to solve complexity once internally than to force hundreds of callers to handle it externally.

## 3. Evaluation Checklist & Quality Gate
- [ ] Is the public interface surface < 15% of the total implementation line count?
- [ ] Are all pass-through methods eliminated or collapsed into a unified abstraction?
- [ ] Is internal state protected against direct external mutation?
"""

# 3. cognitive-cleanse-CHIVE
s_cognitive_cleanse = """---
name: cognitive-cleanse-CHIVE
description: Optimizes cognitive ergonomics, minimizes working-memory cognitive load, eliminates unknown unknowns, enforces semantic precision in naming, ensures codebase style consistency, and eliminates dead code (Ousterhout Ch 2, 14, 17, 18, Cordero #42, #44, #48, #51, #55, #59).
when_to_use: Use during code review, lexical refactoring, dead code cleanup, or when reducing cognitive overhead in complex functions.
argument-hint: [target-files]
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write
---

# COGNITIVE-CLEANSE-CHIVE: Cognitive Ergonomics & Lexical Hygiene

`cognitive-cleanse-CHIVE` targets human working-memory cognitive load. Its primary directive is to make code universally **obvious**, eliminate implicit side effects, and enforce semantic precision across the codebase.

## 1. Invocation Prerequisites & Hooks

### A. Trigger Conditions
- **Specific**:
  - Ambiguous or generic variable/function names (e.g., `data`, `info`, `manager`, `process`, `temp`, `flag`).
  - *Boolean parameter traps* (functions accepting raw boolean literals like `transferFunds(true, false)`).
  - Implicit side effects or in-place mutations on input arguments.
  - Dead code blocks, abandoned commented-out code, or obsolete TODO tags (*code hoarding*).
- **General**: Feature completion stages, pull request code reviews, or refactoring dense, hard-to-read functions.

### B. Hook Actions
- **Pre-Hook**: Scan files for *unknown unknowns* (hidden dependencies or assumptions not apparent from method signatures).
- **Runtime Hook**:
  1. Enforce precise naming with explicit physical units: durations (`_ms`, `_sec`), sizes (`_bytes`), or currencies (`_cents`).
  2. Enforce Command-Query Separation (CQS): mutator methods must not return covert state; query methods must be side-effect free.
  3. Replace raw boolean flags with explicit enums or typed option structs.
- **Post-Hook**: Purge all commented-out code permanently (rely on git history).

## 2. Core Principles & Anti-Pattern Red Flags

1. **Minimizing Cognitive Load & Unknown Unknowns (Ousterhout Ch 2, Cordero #42, #44)**:
   - Complexity peaks when an engineer must inspect five different files just to modify one line safely. Make components self-contained and explicit.
2. **Choosing Good Names as a Design Activity (Ousterhout Ch 14, Cordero #48)**:
   - Names are conceptual compressions. A precise name instantly communicates contracts, constraints, and boundaries.
3. **Consistency as a Leverage Multiplier (Ousterhout Ch 18, Cordero #51)**:
   - Repeated idioms must share identical structure across the entire repository.
4. **Eliminating Code Hoarding & Dead Code (Ousterhout Ch 17, Cordero #55)**:
   - Retaining dead code breeds developer hesitation and maintenance drag. Delete aggressively.

## 3. Evaluation Checklist & Quality Gate
- [ ] Are all functions free from in-place mutations on input parameters?
- [ ] Do all time and memory quantities carry explicit units in their names?
- [ ] Is the codebase completely free of commented-out dead code?
"""

# 4. design-explorer-CHIVE
s_design_explorer = """---
name: design-explorer-CHIVE
description: Guides architectural exploration via Design It Twice, Comments-First specification, Architecture Decision Records (ADR), task-list decomposition, and access-pattern-driven data structure selection (Ousterhout Ch 11, 12, 13, 15, 19, Cordero #62, #66, #68, #71, #74).
when_to_use: Use when evaluating architectural alternatives, selecting critical data structures, documenting major technical decisions, or planning non-trivial feature builds.
argument-hint: [feature-or-decision-name]
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write
---

# DESIGN-EXPLORER-CHIVE: Multi-Option Design & Architecture Decision Records

`design-explorer-CHIVE` breaks the bias of *first-idea cognitive fixation*. It enforces systematic exploration of alternative approaches (*Design It Twice*), API documentation before code (*Comments-First*), and formal Architecture Decision Records (ADR).

## 1. Invocation Prerequisites & Hooks

### A. Trigger Conditions
- **Specific**:
  - Making foundational architectural decisions with long-term lock-in (e.g., storage engine choice, interface topology, inter-service messaging protocols).
  - Mismatch between data structure selection and primary access patterns (e.g., linear array lookups inside high-throughput loops instead of hash maps or trees).
  - Writing code without written interface contracts and invariant documentation.
- **General**: Early feature design phases, brainstorming transitions, or authoring team ADRs.

### B. Hook Actions
- **Pre-Hook**: Classify the task path:
  - *Spike*: Feasibility probe, disposable throwaway artifact.
  - *Bounded*: Isolated change on an existing flow; no external spec doc needed.
  - *Architectural*: New subsystem or interface contract modification (ADR required).
- **Runtime Hook**:
  1. Produce at least 2 to 3 radically different architectural designs with a comparative trade-off matrix.
  2. Execute *Comments-First*: write public interface comments and invariants before implementing the logic.
- **Post-Hook**: Commit the ratified ADR to `docs/adr/` and trigger `fact-verifier-CHIVE`.

## 2. Core Principles & Anti-Pattern Red Flags

1. **Design It Twice (Ousterhout Ch 11, Cordero #62)**:
   - The initial design idea is almost always shallow because it follows the path of least cognitive resistance. Designing a second and third alternative invariably produces superior architectural clarity.
2. **Comments-First Methodology (Ousterhout Ch 12-13, Cordero #66)**:
   - Writing interface comments first acts as a canary in the coal mine: if an interface is awkward to describe in words, its design is fundamentally flawed.
3. **Cross-Module Decisions & ADRs (Ousterhout Ch 13, Cordero #68)**:
   - Decisions that cross component boundaries must reside in a centralized, versioned decision record rather than scattered inline comments.

## 3. Evaluation Checklist & Quality Gate
- [ ] Were 2-3 distinct approaches evaluated with explicit trade-offs before implementation?
- [ ] Were interface contracts and invariants documented prior to writing code?
- [ ] Does the selected data structure match the dominant access patterns in Big-O complexity?
"""

# 5. strategic-debt-CHIVE
s_strategic_debt = """---
name: strategic-debt-CHIVE
description: Implements strategic programming discipline (10-20% investment rule), systematic technical debt management, robust local test pyramid protection, 4-pillar PR descriptions, and blameless post-mortems (Ousterhout Ch 3, 13, 20, 21, Cordero #77, #80, #83, #87, #90).
when_to_use: Use when creating Pull Requests, preparing regression test suites, paying down technical debt, or planning sprint architectural investments.
argument-hint: [pr-or-sprint-goal]
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# STRATEGIC-DEBT-CHIVE: Strategic Engineering, Technical Debt & Testing Pyramids

`strategic-debt-CHIVE` instills sustainable engineering rigor. Through the 10-20% investment rule, it prevents teams from degenerating into *Tactical Tornadoes*, manages technical debt systematically, enforces local test pyramids, and ensures high-precision PR communication.

## 1. Invocation Prerequisites & Hooks

### A. Trigger Conditions
- **Specific**:
  - Rushed tactical implementations accumulating brittle hacks (*Tactical Tornado*).
  - Pull Requests submitted with vague or empty descriptions ("fix bug", "update logic").
  - Inverted test pyramids (*ice cream cone anti-pattern*): relying on slow, flaky E2E tests while lacking fast unit regression tests.
  - Incident post-mortems assigning individual blame instead of fixing systemic failure modes.
- **General**: Sprint planning, pull request authoring, test suite optimization, or engineering health audits.

### B. Hook Actions
- **Pre-Hook**: Ensure 10-20% of the task budget is allocated to architectural cleanup and refactoring of touched modules.
- **Runtime Hook**:
  1. Enforce the **4-Pillar PR Format**: Problem, Context/Why, Expected Behavior, and Technical Approach.
  2. Construct a robust Local Test Pyramid (Fast Deterministic Unit Tests -> Mocked Integration -> Minimal E2E).
- **Post-Hook**: Execute local test suites (100% pass required) and verify metric validity via `fact-verifier-CHIVE`.

## 2. Core Principles & Anti-Pattern Red Flags

1. **Strategic Programming vs Tactical Tornado (Ousterhout Ch 3, Cordero #77)**:
   - Tactical programming solves today's problem by crippling tomorrow's velocity. Strategic programming invests 10-20% in long-term architecture.
2. **Technical Debt Quadrant (Martin Fowler, Cordero #80)**:
   - Distinguish prudent/deliberate debt from reckless/inadvertent debt. Pay down high-interest architectural debt systematically.
3. **Communication Precision in PRs (Ousterhout Ch 13, Cordero #87)**:
   - High-quality PR descriptions explain *why* a change was made, drastically accelerating code reviews and preserving architectural intent.

## 3. Evaluation Checklist & Quality Gate
- [ ] Does the PR description adhere to all four pillars (Problem, Context, Expected, Approach)?
- [ ] Do local unit tests execute in under 5 seconds without external network dependencies?
- [ ] Does this change leave the codebase cleaner than it was found (Boy Scout Rule)?
"""

# 6. critical-resilience-CHIVE
s_critical_resilience = """---
name: critical-resilience-CHIVE
description: Optimizes critical-path systems performance, enforces database indexing (Equality-First, Range-Later), defines errors out of existence, applies Let-It-Crash fail-fast boundaries, and eliminates distributed lock contention (Ousterhout Ch 8, 10, 15, 19, Cordero #92, #94, #96, #98, #100).
when_to_use: Use when optimizing database queries, high-throughput pipelines, designing error-handling boundaries, or architecting concurrent lock-free systems.
argument-hint: [query-or-path]
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# CRITICAL-RESILIENCE-CHIVE: Critical-Path Performance & Fault-Tolerant Resilience

`critical-resilience-CHIVE` governs production system survivability under extreme workloads. It aligns critical-path optimization, B-Tree database indexing, revolutionary error reduction (*Define Errors Out of Existence*), fail-fast boundaries (*Let It Crash*), and lock-free concurrency.

## 1. Invocation Prerequisites & Hooks

### A. Trigger Conditions
- **Specific**:
  - Slow database queries caused by full table scans or inverted compound index column orders.
  - Defensive error-handling bloat (raising exceptions for states that could naturally be defined as normal cases).
  - Swallowing fatal errors using generic catch-all handlers (`except Exception: pass`).
  - Deploying heavyweight distributed locks (e.g., Redis Redlock) for problems solvable via local partitioning.
- **General**: High-throughput backend engineering, p99 latency optimization, or crash resilience auditing.

### B. Hook Actions
- **Pre-Hook**: Profile critical execution paths: ensure zero dynamic memory allocation inside high-frequency hot loops.
- **Runtime Hook**:
  1. Enforce B-Tree compound index order: `EQUALITY FIRST, RANGE LATER`.
  2. Redefine operation semantics to eliminate error states (e.g., idempotent deletions that succeed even if an item is already absent).
  3. Enforce *Let It Crash* (fail-fast) boundaries for invariant corruption: terminate immediately so container orchestrators restart a clean pod.
  4. Replace distributed locks with *Single-Writer In-Memory Partitioning*.
- **Post-Hook**: Verify explain query plans and benchmark results (p99 < 5ms target) via `fact-verifier-CHIVE`.

## 2. Core Principles & Anti-Pattern Red Flags

1. **Critical Path Optimization (Ousterhout Ch 19, Cordero #92)**:
   - Concentrate optimization strictly on the 5% of code that drives 95% of latency. Avoid premature optimization on cold paths.
2. **Define Errors Out of Existence (Ousterhout Ch 10, Cordero #96)**:
   - The cleanest way to handle errors is to design APIs such that edge conditions represent normal, well-defined behaviors rather than exceptions.
3. **Let It Crash & Fail-Fast (Ousterhout Ch 10, Cordero #98)**:
   - Never mask internal memory or state corruption with catch-all blocks. Fail fast to prevent silent database corruption.
4. **Problem Elimination Over Complex Solutions (Ousterhout Ch 8, Cordero #100)**:
   - Eliminating the need for distributed coordination is infinitely superior to optimizing a fragile distributed locking protocol.

## 3. Evaluation Checklist & Quality Gate
- [ ] Do compound database indices place equality filter columns before range filter columns?
- [ ] Have edge cases been redefined to eliminate unnecessary exception handling?
- [ ] Does the process terminate immediately upon detecting internal state invariant corruption?
"""

# 7. topology-lifecycle-CHIVE
s_topology_lifecycle = """---
name: topology-lifecycle-CHIVE
description: Governs Modular Monolith vs Microservices topologies (MonolithFirst), Observability 2.0 (Wide Structured Events), Zero-Trust internal API security, disaster recovery automated drills, and Kent Beck's 3X lifecycle alignment (Ousterhout Ch 1-4, 18, 20, 21, Cordero #3, #18, #35, #50, #75).
when_to_use: Use when designing system topologies, instrumenting logging/tracing, hardening API authorization, planning DR procedures, or matching engineering practices to product maturity.
argument-hint: [system-or-service]
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write
---

# TOPOLOGY-LIFECYCLE-CHIVE: Systems Topology, Observability & Product Lifecycle

`topology-lifecycle-CHIVE` guides macro-level system architecture: championing *Modular Monoliths* before microservices, modern Observability 2.0 (*Wide Structured Events*), Zero-Trust internal API security, automated Disaster Recovery drills, and lifecycle alignment (Kent Beck 3X: *Explore, Expand, Extract*).

## 1. Invocation Prerequisites & Hooks

### A. Trigger Conditions
- **Specific**:
  - Premature microservices adoption: fragmenting into network services before domain boundaries stabilize in a single database.
  - Fragmented string logging (generating dozens of disconnected log lines per transaction).
  - Internal APIs operating without authentication/authorization under the false premise of VPC perimeter security.
  - Untested disaster recovery procedures.
  - Mismatch between engineering formality and product lifecycle stage.
- **General**: Infrastructure planning, architectural migrations, security compliance, or observability strategy reviews.

### B. Hook Actions
- **Pre-Hook**: Assess current product phase: *Explore* (rapid hypothesis validation), *Expand* (scalability & bottleneck clearing), or *Extract* (99.999% reliability & cost efficiency).
- **Runtime Hook**:
  1. Architecture default: build a *Modular Monolith* with strict in-process package boundaries before network splitting.
  2. Implement *Wide Structured Events*: emit a single comprehensive JSON payload per transaction carrying rich contextual dimensions.
  3. Enforce internal Zero-Trust: validate identity and scope on every internal RPC boundary.
- **Post-Hook**: Validate event schemas and verify recovery protocols via `fact-verifier-CHIVE`.

## 2. Core Principles & Anti-Pattern Red Flags

1. **Modular Monolith vs Microservices (Ousterhout & Cordero #3)**:
   - In-process module boundaries are 1,000x cheaper and less error-prone than network boundaries. Always start with *MonolithFirst*.
2. **Observability 2.0 via Wide Events (Charity Majors, Cordero #18)**:
   - Discard unindexed string logs. Emit a single high-cardinality, high-dimensionality event at the end of every request execution.
3. **Zero-Trust Internal Security (Cordero #35)**:
   - Never trust an incoming request solely because it originated inside the internal VPC. Enforce mTLS and scoped authorization tokens.
4. **Kent Beck 3X Lifecycle Alignment (Cordero #75)**:
   - Practices that thrive in the *Extract* phase will strangle productivity in the *Explore* phase. Tailor engineering formality to the product lifecycle.

## 3. Evaluation Checklist & Quality Gate
- [ ] Does every transaction emit a single high-cardinality Wide Structured Event?
- [ ] Are internal API endpoints protected by explicit authorization checks?
- [ ] Does the engineering approach match the current product lifecycle phase (Explore/Expand/Extract)?
"""

# 8. fact-verifier-CHIVE
s_fact_verifier = """---
name: fact-verifier-CHIVE
description: Epistemic fact-verification and hypothesis testing engine using NATO STANAG 2064 / Admiralty Code 6x6 Matrix, Analysis of Competing Hypotheses (ACH), ICD 203 Analytic Standards, and Bayesian Probability Updates (FPCOS / think-hive / possibility-hive).
when_to_use: Mandatory post-execution verification gate for all CHIVE skills. Use whenever empirical claims, performance benchmarks, test assertions, or architectural hypotheses must be rigorously verified.
argument-hint: [claim-or-hypothesis]
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

# FACT-VERIFIER-CHIVE: Epistemic Fact Verification & Bayesian Calibration

`fact-verifier-CHIVE` represents the epistemic anchor of the CHIVE ecosystem. Synthesizing the *First Principle Codex OS (FPCOS)* from `user:think-hive` and the computational Bayesian mechanics of `user:possibility-hive`, it guarantees that no technical assertion or performance claim is presented without empirical evidence and mathematical calibration.

## 1. Invocation Prerequisites & Hooks

### A. Trigger Conditions
- **Specific**:
  - Asserting performance improvements (e.g., "this refactor makes queries 10x faster").
  - Post-mortem root-cause conclusions following incident investigations.
  - Completion of any execution by other CHIVE skills (serving as mandatory post-execution gate).
  - Detection of uncalibrated absolutist language ("always", "never", "guaranteed 100%").
- **General**: Before presenting any final conclusion, architectural recommendation, or pull request summary.

### B. Hook Actions
- **Pre-Hook**: Initialize Bayesian evidence scoring:
  ```bash
  python3 "$CLAUDE_PROJECT_DIR/.claude/skills/fact-verifier-CHIVE/scripts/bayesian_admiralty.py" "$CLAIM_TEXT"
  ```
- **Runtime Hook**:
  1. Categorize all assertions into **KNOWN**, **INFERRED**, or **UNKNOWN**.
  2. Grade evidence using the **Admiralty 6x6 Matrix** (Source Reliability A–F, Information Credibility 1–6).
  3. Subject assumptions to the **Analysis of Competing Hypotheses (ACH)** matrix.
  4. Calculate log-odds Bayesian updates with blind-spot sensitivity penalties.
- **Post-Hook**: Output the Critical Evaluation Field calibrated to **ICD 203 Words of Estimative Probability (WEP)**.

## 2. Evidence Grading & Analytic Standards

### A. Admiralty 6x6 Matrix (NATO STANAG 2064)
- **Source Reliability**:
  - `A`: Completely Reliable (Automated deterministic tests, reproducible benchmarks).
  - `B`: Usually Reliable (Official engine documentation, verified production telemetry).
  - `C`: Fairly Reliable (Third-party technical reports, empirical case studies).
  - `D`: Not Usually Reliable | `E`: Unreliable | `F`: Reliability Cannot Be Judged.
- **Information Credibility**:
  - `1`: Confirmed by independent sources.
  - `2`: Probably True.
  - `3`: Possibly True.
  - `4`: Doubtful | `5`: Improbable | `6`: Truth Cannot Be Judged.

### B. ICD 203 Confidence Calibration (Sherman Kent WEP)
- **Almost Certain (>90%)**: Deductive proof, 100% passing test suites, confirmed query plans.
- **Highly Likely (70% - 85%)**: Strong converging empirical evidence across multiple sources.
- **Likely / Probable (55% - 70%)**: Established architectural patterns; context-dependent.
- **Roughly Even Chance (45% - 55%)**: Balanced trade-off; requires spike investigation.
- **Unlikely (20% - 40%)** & **Remote (<10%)**: Fragile or contradicted assumptions.

## 3. Mandatory Output Contract (Fact Verification Gate)
Every task completion must conclude with this assessment block:
```markdown
### CRITICAL EVALUATION FIELD (FACT-VERIFIER-CHIVE)
- **CONFIDENCE**: [X%] — [ICD 203 WEP Category] (Confidence Level: High / Moderate / Low)
- **SHADOW JUDGMENT**: [CONSISTENT / FRAGILE / REBUILD]
- **BLIND SPOTS / UNKNOWNS**: [Specific unverified parameters or missing data]
- **FAILURE CONDITIONS**: [Boundary scenarios where this solution breaks down]
```
"""

skills_to_write = [
    ("orchestrator-CHIVE", s_orchestrator),
    ("module-boundary-CHIVE", s_module_boundary),
    ("cognitive-cleanse-CHIVE", s_cognitive_cleanse),
    ("design-explorer-CHIVE", s_design_explorer),
    ("strategic-debt-CHIVE", s_strategic_debt),
    ("critical-resilience-CHIVE", s_critical_resilience),
    ("topology-lifecycle-CHIVE", s_topology_lifecycle),
    ("fact-verifier-CHIVE", s_fact_verifier),
]

for skill_name, content in skills_to_write:
    path = os.path.join(base_skills, skill_name, "SKILL.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Rewrote {skill_name}/SKILL.md in English.")

