import os

base_dir = "/tmp/claude_chive_system"

# 1. expert_guard_scanner.py
expert_guard = """#!/usr/bin/env python3
\"\"\"
expert_guard_scanner.py - Strict Blocking with Auto-Remediation Engine for Claude Code.
Enforces the Zero-Bypass Production Invariant Policy:
When an anti-pattern is detected:
1. Exits with code 2 to BLOCK the Edit/Write/Bash tool call immediately.
2. Emits an actionable, copy-paste-ready AUTO-REMEDIATION CODE TEMPLATE to stderr,
   forcing Claude Code to regenerate the implementation using resilient expert patterns.
\"\"\"

import sys
import json
import re

REMEDIATION_RULES = [
    {
        "id": "TRAP_01_SWALLOWED_ERROR",
        "name": "Silent Error Swallowing (Cordero #98)",
        "pattern": r"(except\s+Exception\s*:\s*pass|except\s*:\s*pass|catch\s*\([^)]*\)\s*\{\s*\}|catch\s*\([^)]*\)\s*\{\s*//[^\n]*\s*\})",
        "diagnosis": "Attempted to swallow an exception using an empty catch/except block. This conceals fatal failures and creates corrupt zombie states.",
        "remediation_template": \"\"\"
# ==============================================================================
# AUTO-REMEDIATION TEMPLATE: SPECIFIC ERROR HANDLING & TELEMETRY
# ==============================================================================
# Replace your empty catch/except block with one of the following structured patterns:

# OPTION A: Operational Error (Return Structured Result Type / Log with Trace ID)
try:
    result = perform_subsystem_operation()
except SpecificOperationalError as err:
    logger.warning("Subsystem operational failure", extra={
        "error_type": type(err).__name__,
        "reason": str(err),
        "trace_id": context.trace_id,
        "action": "graceful_fallback"
    })
    return Result.failure(code="OPERATION_FAILED", message=str(err))

# OPTION B: Invariant Violation (Let It Crash / Fail-Fast Pattern)
try:
    ledger.mutate_balance(account_id, delta)
except Exception as fatal_err:
    logger.critical("FATAL_INVARIANT_VIOLATION: Corrupted state. Terminating pod.", extra={
        "fatal_err": str(fatal_err),
        "stack_trace": traceback.format_exc()
    })
    raise  # Allow container supervisor (Kubernetes) to restart a clean pod
# ==============================================================================
\"\"\"
    },
    {
        "id": "TRAP_02_MISSING_TIMEOUT",
        "name": "Unbounded Remote Call Without Timeout (Cascading Meltdown)",
        "pattern": r"(requests\.(get|post|put|delete|patch)\([^)]*\)(?!.*timeout\s*=)|http\.Get\([^)]*\)|fetch\([^)]*\)(?!.*signal))",
        "diagnosis": "Network I/O invocation without an explicit timeout deadline. Risks thread-pool exhaustion during upstream slowdowns.",
        "remediation_template": \"\"\"
# ==============================================================================
# AUTO-REMEDIATION TEMPLATE: MANDATORY CONTEXT TIMEOUT & DEADLINE
# ==============================================================================
# Python (Requests with Connect and Read Timeouts):
response = requests.get(url, timeout=(3.05, 5.0)) # (connect timeout, read timeout)

# TypeScript / Node.js (Fetch with AbortSignal Deadline):
const response = await fetch(url, {
  signal: AbortSignal.timeout(5000), // 5 seconds deadline
  headers: { "X-Request-ID": traceId }
});

# Go (Context with Strict Timeout):
ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
defer cancel()
req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
resp, err := client.Do(req)
# ==============================================================================
\"\"\"
    },
    {
        "id": "TRAP_03_RETRY_STORM",
        "name": "Retry Storm Without Backoff/Jitter (Thundering Herd)",
        "pattern": r"(while\s+True\s*:[^}]*except[^}]*continue|for\s+\w+\s+in\s+range\(\s*\d+\s*\)\s*:[^}]*except[^}]*continue)",
        "diagnosis": "Retrying failed operations in a tight loop without exponential backoff and jitter. Causes Thundering Herd DDoS against recovering services.",
        "remediation_template": \"\"\"
# ==============================================================================
# AUTO-REMEDIATION TEMPLATE: EXPONENTIAL BACKOFF WITH FULL JITTER
# ==============================================================================
import time
import random

MAX_RETRIES = 3
BASE_DELAY_SEC = 0.5
MAX_DELAY_SEC = 5.0

for attempt in range(1, MAX_RETRIES + 1):
    try:
        return execute_transient_call()
    except TransientNetworkError as err:
        if attempt == MAX_RETRIES:
            logger.error("Retry limit exceeded, failing permanently", extra={"attempts": attempt})
            raise
        # Full Jitter formula: sleep = random between 0 and min(cap, base * 2^attempt)
        backoff = min(MAX_DELAY_SEC, BASE_DELAY_SEC * (2 ** (attempt - 1)))
        sleep_duration = random.uniform(0, backoff)
        logger.warning(f"Retry {attempt}/{MAX_RETRIES} after {sleep_duration:.2f}s", extra={"err": str(err)})
        time.sleep(sleep_duration)
# ==============================================================================
\"\"\"
    },
    {
        "id": "TRAP_04_NAKED_LOCK",
        "name": "Lock Without Guaranteed Release (Deadlock Hazard)",
        "pattern": r"(\.acquire\(\)(?![\s\S]{0,100}finally:)|mu\.Lock\(\)(?![\s\S]{0,100}defer\s+mu\.Unlock\(\)))",
        "diagnosis": "Mutex acquisition without guaranteed release. Early returns or unhandled exceptions will lock the resource permanently.",
        "remediation_template": \"\"\"
# ==============================================================================
# AUTO-REMEDIATION TEMPLATE: RAII & GUARANTEED LOCK RELEASE
# ==============================================================================
# Python (Use Context Manager):
with self._lock:
    # All state mutations are protected; automatically released even if exceptions occur
    self._mutate_protected_state()

# Go (Use Immediate Defer After Lock):
mu.Lock()
defer mu.Unlock() // Guaranteed to execute upon function return
# ==============================================================================
\"\"\"
    },
    {
        "id": "TRAP_05_DESTRUCTIVE_DDL",
        "name": "Destructive Database DDL Without Expand-Contract",
        "pattern": r"\b(DROP\s+TABLE|DROP\s+COLUMN|TRUNCATE\s+TABLE)\b",
        "diagnosis": "Destructive DDL executed directly. Breaks backward compatibility with active running application instances.",
        "remediation_template": \"\"\"
-- ==============================================================================
-- AUTO-REMEDIATION TEMPLATE: EXPAND-CONTRACT (TWO-PHASE DEPLOYMENT)
-- ==============================================================================
-- PHASE 1 (EXPAND): Add the new column/table without dropping the legacy schema.
ALTER TABLE orders ADD COLUMN status_v2 VARCHAR(32) DEFAULT 'PENDING';
-- Deploy application code that reads v2 and dual-writes to v1 & v2.

-- PHASE 2 (MIGRATE): Backfill legacy data asynchronously in batches.
UPDATE orders SET status_v2 = status WHERE status_v2 IS NULL;

-- PHASE 3 (CONTRACT): ONLY after all legacy instances are 100% decommissioned:
ALTER TABLE orders DROP COLUMN status; -- Execute in separate migration
-- ==============================================================================
\"\"\"
    }
]

def scan_content(content_str):
    if not content_str:
        return None
    for rule in REMEDIATION_RULES:
        if re.search(rule["pattern"], content_str, re.IGNORECASE):
            return rule
    return None

def main():
    try:
        input_data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    content = tool_input.get("content", "")
    command = tool_input.get("command", "")

    target_text = content if content else command

    trap = scan_content(target_text)
    if trap:
        err_msg = (
            f"\\n"
            f"********************************************************************************\\n"
            f"[CHIVE STRICT BLOCKING GATE] ACTION BLOCKED (EXIT CODE 2)\\n"
            f"Detected Anti-Pattern: {trap['name']} ({trap['id']})\\n"
            f"Diagnosis: {trap['diagnosis']}\\n"
            f"Mandatory Directive: You MUST NOT write this code to disk. You are REQUIRED to\\n"
            f"adopt the auto-remediation pattern below to generate resilient production code:\\n"
            f"********************************************************************************\\n"
            f"{trap['remediation_template']}\\n"
            f"********************************************************************************\\n"
        )
        sys.stderr.write(err_msg)
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
"""

with open(f"{base_dir}/.claude/hooks/expert_guard_scanner.py", "w", encoding="utf-8") as f:
    f.write(expert_guard)
os.chmod(f"{base_dir}/.claude/hooks/expert_guard_scanner.py", 0o755)

# 2. post_tool_self_heal.py
post_heal = """#!/usr/bin/env python3
\"\"\"
post_tool_self_heal.py - Automated Self-Healing & Diagnostic Recovery Engine.
Inspects post-tool execution results. If an error or failure is detected, it analyzes
the failure category and injects an actionable expert recovery strategy into Claude Code.
\"\"\"

import sys
import json
import re

DIAGNOSTIC_PLAYBOOK = [
    {
        "pattern": r"(SyntaxError|IndentationError)",
        "category": "SYNTAX_CORRUPTION",
        "action": (
            "DIAGNOSIS: Syntax or indentation error detected. "
            "SELF-HEAL ACTION: Inspect matching brackets, quotes, or indentation alignment on the indicated line before proceeding."
        )
    },
    {
        "pattern": r"(NameError|ImportError|ModuleNotFoundError)",
        "category": "MISSING_DEPENDENCY_OR_IMPORT",
        "action": (
            "DIAGNOSIS: Unimported symbol or missing module reference. "
            "SELF-HEAL ACTION: Add an explicit import statement at the top of the file and verify symbol name spelling."
        )
    },
    {
        "pattern": r"(DeadlockDetected|LockContention|OperationalError:.*deadlock)",
        "category": "CONCURRENCY_DEADLOCK",
        "action": (
            "DIAGNOSIS: Mutex lock contention or database deadlock detected during concurrent transactions. "
            "SELF-HEAL ACTION: Enforce monotonic lock acquisition ordering or migrate the pipeline to Single-Writer In-Memory Partitioning."
        )
    },
    {
        "pattern": r"(LedgerInvariantViolation|InvariantViolation|AssertionError)",
        "category": "INVARIANT_BREACH",
        "action": (
            "DIAGNOSIS: System invariant breach detected! Internal state is inconsistent. "
            "SELF-HEAL ACTION: Immediately roll back transaction to the last known checkpoint, log complete diagnostic telemetry, "
            "and fail fast (Let-It-Crash pattern) to prevent data corruption."
        )
    },
    {
        "pattern": r"(ConnectionResetError|TimeoutError|HTTPError: 50[234])",
        "category": "TRANSIENT_UPSTREAM_FAILURE",
        "action": (
            "DIAGNOSIS: Network interruption or transient upstream outage (502/503/504). "
            "SELF-HEAL ACTION: Activate Circuit Breaker and schedule retries with Exponential Backoff + Full Jitter."
        )
    }
]

def main():
    try:
        input_data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_output = input_data.get("tool_output", "")

    output_str = str(tool_output)

    for item in DIAGNOSTIC_PLAYBOOK:
        if re.search(item["pattern"], output_str, re.IGNORECASE):
            sys.stderr.write(f"\\n[CHIVE SELF-HEALING DIAGNOSTIC - {item['category']}]\\n")
            sys.stderr.write(f"{item['action']}\\n\\n")
            break

    sys.exit(0)

if __name__ == "__main__":
    main()
"""

with open(f"{base_dir}/.claude/hooks/post_tool_self_heal.py", "w", encoding="utf-8") as f:
    f.write(post_heal)
os.chmod(f"{base_dir}/.claude/hooks/post_tool_self_heal.py", 0o755)

# 3. router.py
router_py = """#!/usr/bin/env python3
\"\"\"
router.py - Central Dispatcher & Orchestration Engine for the CHIVE Skill System.
Evaluates project tasks, maps requirements to corresponding CHIVE skills,
validates hook prerequisites, and triggers the fact-confirmation gate.
\"\"\"

import sys
import re
import json

SKILL_REGISTRY = {
    "module-boundary-CHIVE": {
        "title": "Module Decomposition & Interface Boundaries",
        "keywords": ["module", "interface", "classitis", "pass-through", "information hiding", "temporal decomposition", "shallow", "deep module", "encapsulation", "refactor class"],
        "batch_ref": "Batch 1 (Skills 1-5)",
        "prerequisites": "Architecting new classes/modules or refactoring component boundaries."
    },
    "cognitive-cleanse-CHIVE": {
        "title": "Cognitive Ergonomics & Lexical Hygiene",
        "keywords": ["cognitive", "naming", "unknown unknowns", "dead code", "obvious code", "side effect", "clean code", "readability", "code review", "smell"],
        "batch_ref": "Batch 2 (Skills 6-10)",
        "prerequisites": "Code review, variable/function naming refactoring, or purging dead code."
    },
    "design-explorer-CHIVE": {
        "title": "Multi-Option Design & Architecture Decision Records",
        "keywords": ["design it twice", "comments-first", "adr", "architecture decision", "spec", "data structure", "brainstorm", "spike", "bounded"],
        "batch_ref": "Batch 3 (Skills 11-15)",
        "prerequisites": "Formulating new architectural decisions or selecting critical data structures."
    },
    "strategic-debt-CHIVE": {
        "title": "Strategic Engineering, Technical Debt & Testing Pyramids",
        "keywords": ["technical debt", "strategic programming", "10-20% rule", "pr", "pull request", "test pyramid", "regression", "blameless", "post-mortem"],
        "batch_ref": "Batch 4 (Skills 16-20)",
        "prerequisites": "Sprint planning, PR authoring, paying down technical debt, or organizing test suites."
    },
    "critical-resilience-CHIVE": {
        "title": "Critical-Path Performance & Fault-Tolerant Resilience",
        "keywords": ["performance", "critical path", "index", "b-tree", "sql", "let it crash", "fail-fast", "define errors out of existence", "distributed lock", "concurrency", "race condition"],
        "batch_ref": "Batch 5 (Skills 21-25)",
        "prerequisites": "Latency optimization, database indexing, fail-fast boundary design, or lock-free concurrency."
    },
    "topology-lifecycle-CHIVE": {
        "title": "Systems Topology, Observability & Product Lifecycle",
        "keywords": ["microservices", "monolith", "modular monolith", "observability", "wide events", "zero-trust", "api security", "disaster recovery", "chaos", "3x", "kent beck"],
        "batch_ref": "Batch 6 (Skills 26-30)",
        "prerequisites": "Service topology evaluation, observability instrumentation, internal security audit, or lifecycle alignment."
    },
    "fact-verifier-CHIVE": {
        "title": "Epistemic Fact Verification & Bayesian Calibration",
        "keywords": ["fact", "verify", "admiralty", "ach", "bayesian", "icd 203", "confidence", "evidence", "benchmark check"],
        "batch_ref": "Epistemic Gatekeeper",
        "prerequisites": "Mandatory for all empirical conclusions, performance claims, or diagnostic audits."
    }
}

def analyze_intent(query_text):
    query_lower = query_text.lower()
    matched_skills = []
    
    for skill_name, info in SKILL_REGISTRY.items():
        score = 0
        matched_kw = []
        for kw in info["keywords"]:
            if re.search(r'\\b' + re.escape(kw) + r'\\b', query_lower):
                score += 1
                matched_kw.append(kw)
        if score > 0:
            matched_skills.append((skill_name, score, matched_kw, info))
            
    # Always attach fact-verifier-CHIVE as mandatory post-execution gate
    if not any(s[0] == "fact-verifier-CHIVE" for s in matched_skills):
        matched_skills.append(("fact-verifier-CHIVE", 1, ["mandatory-epistemic-gate"], SKILL_REGISTRY["fact-verifier-CHIVE"]))
        
    matched_skills.sort(key=lambda x: x[1], reverse=True)
    return matched_skills

def main():
    if len(sys.argv) < 2:
        print("Usage: router.py \\\"<task description or user query>\\\"")
        sys.exit(1)
        
    query = " ".join(sys.argv[1:])
    matches = analyze_intent(query)
    
    print("=" * 70)
    print("  CHIVE SKILL SYSTEM - MASTER ORCHESTRATION ROUTE PLAN")
    print("=" * 70)
    print(f"Task Context: {query}\\n")
    print("Recommended Skill Execution Chain:")
    
    for i, (name, score, kws, info) in enumerate(matches, 1):
        role = "[PRIMARY SKILL]" if i == 1 and name != "fact-verifier-CHIVE" else "[SUPPORTING SKILL]"
        if name == "fact-verifier-CHIVE":
            role = "[MANDATORY FACT-CHECK GATE]"
        print(f"{i}. {name} {role}")
        print(f"   - Module: {info['title']} ({info['batch_ref']})")
        print(f"   - Prerequisites: {info['prerequisites']}")
        print(f"   - Trigger Signals: {', '.join(kws)}")
        print()
        
    print("Coordinated Execution Lifecycle:")
    print("1. [Pre-Execution Hook]   -> Validate architectural invariants and trigger prerequisites.")
    print("2. [Runtime Execution]    -> Execute selected skills sequentially within isolated boundaries.")
    print("3. [Post-Execution Hook]  -> Delegate results to fact-verifier-CHIVE for Admiralty 6x6 & ICD 203 verification.")
    print("=" * 70)

if __name__ == "__main__":
    main()
"""

with open(f"{base_dir}/.claude/skills/orchestrator-CHIVE/scripts/router.py", "w", encoding="utf-8") as f:
    f.write(router_py)
os.chmod(f"{base_dir}/.claude/skills/orchestrator-CHIVE/scripts/router.py", 0o755)

# 4. bayesian_admiralty.py
bayesian_admiralty = """#!/usr/bin/env python3
\"\"\"
bayesian_admiralty.py - Epistemic Fact-Checking & Bayesian Probability Engine.
Implements NATO STANAG 2064 / Admiralty 6x6 Matrix, Analysis of Competing Hypotheses (ACH),
Log-Space Likelihood Updating, Beta-Binomial Credibility, and ICD 203 Estimative Calibration.
\"\"\"

import math
import sys
import json

ADMIRALTY_RELIABILITY = {
    "A": ("Completely Reliable", 0.95),
    "B": ("Usually Reliable", 0.85),
    "C": ("Fairly Reliable", 0.70),
    "D": ("Not Usually Reliable", 0.50),
    "E": ("Unreliable", 0.20),
    "F": ("Reliability Cannot Be Judged", 0.50)
}

ADMIRALTY_CREDIBILITY = {
    "1": ("Confirmed by other independent sources", 15.0), # Likelihood Ratio ~15
    "2": ("Probably True", 6.0),                          # Likelihood Ratio ~6
    "3": ("Possibly True", 2.0),                          # Likelihood Ratio ~2
    "4": ("Doubtful", 0.5),                               # Likelihood Ratio ~0.5
    "5": ("Improbable", 0.1),                             # Likelihood Ratio ~0.1
    "6": ("Truth Cannot Be Judged", 1.0)                  # Likelihood Ratio ~1.0
}

def logit(p):
    p = max(0.001, min(0.999, p))
    return math.log(p / (1.0 - p))

def expit(x):
    return 1.0 / (1.0 + math.exp(-x))

def evaluate_claim(prior_prob, evidence_list):
    current_logit = logit(prior_prob)
    log_lrs = []
    
    for rel_code, cred_code, desc in evidence_list:
        rel_desc, rel_weight = ADMIRALTY_RELIABILITY.get(rel_code.upper(), ("Unknown", 0.5))
        cred_desc, raw_lr = ADMIRALTY_CREDIBILITY.get(str(cred_code), ("Unknown", 1.0))
        
        effective_lr = max(0.01, 1.0 + (raw_lr - 1.0) * rel_weight)
        log_lr = math.log(effective_lr)
        current_logit += log_lr
        log_lrs.append({
            "admiralty_code": f"{rel_code.upper()}{cred_code}",
            "description": desc,
            "reliability": rel_desc,
            "credibility": cred_desc,
            "effective_lr": round(effective_lr, 3),
            "log_lr": round(log_lr, 3)
        })
        
    posterior_prob = expit(current_logit)
    posterior_prob = max(0.01, min(0.99, posterior_prob))
    
    # ICD 203 Calibration (Words of Estimative Probability)
    wep = "Unknown"
    conf_level = "MODERATE"
    if posterior_prob >= 0.90:
        wep = "Almost Certain (>90%)"
        conf_level = "HIGH"
    elif posterior_prob >= 0.70:
        wep = "Highly Likely (70% - 85%)"
        conf_level = "HIGH"
    elif posterior_prob >= 0.55:
        wep = "Likely / Probable (55% - 70%)"
        conf_level = "MODERATE"
    elif posterior_prob >= 0.45:
        wep = "Roughly Even Chance (45% - 55%)"
        conf_level = "MODERATE"
    elif posterior_prob >= 0.20:
        wep = "Unlikely (20% - 40%)"
        conf_level = "LOW"
    else:
        wep = "Remote / Highly Improbable (<10%)"
        conf_level = "LOW"
        
    shadow_judgment = "CONSISTENT" if posterior_prob >= 0.70 else ("FRAGILE" if posterior_prob >= 0.45 else "REBUILD")
    
    return {
        "prior_prob": prior_prob,
        "posterior_prob": round(posterior_prob, 4),
        "confidence_percentage": round(posterior_prob * 100, 1),
        "icd_203_wep": wep,
        "confidence_level": conf_level,
        "shadow_judgment": shadow_judgment,
        "evidence_audit": log_lrs
    }

def main():
    sample_evidence = [
        ("A", "1", "Local deterministic test suite execution (100% pass on clean branch)"),
        ("B", "2", "Benchmark latency p99 < 5ms on database query execution plan"),
        ("B", "1", "Peer code review verification and consistency with Architecture Decision Record (ADR)")
    ]
    res = evaluate_claim(0.50, sample_evidence)
    print("=" * 70)
    print("  FACT-VERIFIER-CHIVE: BAYESIAN ADMIRALTY EVALUATION")
    print("=" * 70)
    print(f"Prior Probability       : {res['prior_prob'] * 100:.1f}%")
    print(f"Posterior Probability   : {res['confidence_percentage']}%")
    print(f"ICD 203 WEP Category    : {res['icd_203_wep']}")
    print(f"Confidence Level        : {res['confidence_level']}")
    print(f"Shadow Judgment         : {res['shadow_judgment']}\\n")
    print("Admiralty Evidence Audit (6x6 Matrix):")
    for ev in res["evidence_audit"]:
        print(f" - [{ev['admiralty_code']}] {ev['description']}")
        print(f"   Reliability: {ev['reliability']} | Credibility: {ev['credibility']} | Log(LR): {ev['log_lr']}")
    print("=" * 70)

if __name__ == "__main__":
    main()
"""

with open(f"{base_dir}/.claude/skills/fact-verifier-CHIVE/scripts/bayesian_admiralty.py", "w", encoding="utf-8") as f:
    f.write(bayesian_admiralty)
os.chmod(f"{base_dir}/.claude/skills/fact-verifier-CHIVE/scripts/bayesian_admiralty.py", 0o755)

print("All Python scripts rewritten in English.")
