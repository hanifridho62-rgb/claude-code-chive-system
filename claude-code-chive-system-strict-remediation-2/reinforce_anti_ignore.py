import os

base_dir = "/tmp/claude_chive_system"
skills_dir = f"{base_dir}/.claude/skills"

# 1. Create lowercase symlinks for every skill folder to guarantee 100% case-insensitive resolution
for item in os.listdir(skills_dir):
    full_item = os.path.join(skills_dir, item)
    if os.path.isdir(full_item) and item.endswith("-CHIVE"):
        lower_name = item.lower()
        symlink_path = os.path.join(skills_dir, lower_name)
        if not os.path.exists(symlink_path):
            os.symlink(item, symlink_path)
            print(f"Created symlink: {lower_name} -> {item}")

# 2. Update CLAUDE.md with Hard Deterministic Enforcement Directives
claude_md_content = """# CLAUDE.md: MASTER SYSTEM INSTRUCTIONS FOR CLAUDE CODE (CHIVE ENFORCEMENT)

## CRITICAL DIRECTIVE: MANDATORY SKILL ENFORCEMENT (ZERO-BYPASS POLICY)
Claude Code MUST NOT bypass or ignore the CHIVE Skill System under any circumstances.
Every user request touching software engineering, architecture, code modification, refactoring, testing, or code review MUST activate the appropriate CHIVE skill pipeline before generating code.

### 1. Mandatory Trigger & Routing Table (Guaranteed Execution)
When a request matches any of the criteria below, you MUST load and execute the designated skill:

| User Request / Trigger Context | Mandatory Skill to Invoke | Location & Command |
| :--- | :--- | :--- |
| Any multi-step task, new project, complex request, or ambiguous goal | `orchestrator-CHIVE` | `/orchestrator-CHIVE` |
| Designing classes, refactoring interfaces, extracting modules, fixing pass-throughs | `module-boundary-CHIVE` | `/module-boundary-CHIVE` |
| Variable/function naming, reducing cognitive load, code review, deleting dead code | `cognitive-cleanse-CHIVE` | `/cognitive-cleanse-CHIVE` |
| Planning new features, evaluating 2-3 design options (Design It Twice), writing ADRs | `design-explorer-CHIVE` | `/design-explorer-CHIVE` |
| Writing Pull Requests (4-Pillar PR), local test pyramid, managing technical debt | `strategic-debt-CHIVE` | `/strategic-debt-CHIVE` |
| Optimizing latency, SQL composite indexing, fail-fast / Let-It-Crash, concurrency | `critical-resilience-CHIVE` | `/critical-resilience-CHIVE` |
| Microservices vs Modular Monolith, Wide Events logging, Zero-Trust API, 3X lifecycle | `topology-lifecycle-CHIVE` | `/topology-lifecycle-CHIVE` |
| **ALL empirical claims, benchmark figures, bug root causes, and PR closures** | **`fact-verifier-CHIVE`** | **MANDATORY POST-GATE** |

---

## 2. Hard Invariant Protection (Deterministic Hooks)
Claude Code operates under deterministic OS-level hooks configured in `.claude/settings.json`:
1. **PreToolUse Hook (`protect-invariants.sh`)**: Automatically aborts (exit code 2) any attempt to edit protected files (`.env`, `.git/`, lockfiles, and architectural contracts).
2. **PostToolUse Hook (`post-skill-verify.sh`)**: Automatically compiles and validates syntax immediately after any `Edit` or `Write` operation.
3. **SessionStart Hook (`pre-skill-check.sh`)**: Pre-loads active CHIVE registry and verification status at the start of every session.

---

## 3. Mandatory Output Contract (Fact Verification Gate)
No architectural change or technical conclusion may be presented to the user without completing the `fact-verifier-CHIVE` assessment:
```markdown
### BIDANG PENILAIAN KRITIS (FACT-VERIFIER-CHIVE)
- **KEYAKINAN**: [X%] — [Kategori WEP ICD 203] (Level Keyakinan: High / Moderate / Low)
- **PUTUSAN BAYANGAN**: [KONSISTEN / RAPUH / BANGUN ULANG]
- **TITIK BUTA / TIDAK DIKETAHUI**: [Data yang belum diverifikasi]
- **KONDISI GAGAL**: [Kondisi batas di mana solusi ini tidak berlaku]
```
"""

with open(f"{base_dir}/CLAUDE.md", "w", encoding="utf-8") as f:
    f.write(claude_md_content.strip() + "\n")

print("CLAUDE.md updated with Zero-Bypass policy.")
