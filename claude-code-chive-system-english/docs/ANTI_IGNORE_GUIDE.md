# TECHNICAL GUIDE: PREVENTING CLAUDE CODE SKILL IGNORANCE
*Based on Official Claude Code Docs (code.claude.com/docs/en/skills) & Community Research (LazySkills.sh)*

---

## 1. Root Causes Behind Ignored Skills & Concrete Engineering Solutions

Based on official Anthropic documentation and ecosystem findings, skill trigger failures (*Skill Not Triggering / Ignored*) stem from 8 primary breakdown points:

1. **Directory Structure & Nesting Depth**:
   - *Cause*: `SKILL.md` placed too deep (e.g., `.claude/skills/deploy/deploy/SKILL.md`) or placed directly in the root `.claude/skills/SKILL.md`. The scanner only inspects exactly 1 level deep.
   - *CHIVE Fix*: Every skill sits exactly 1 level deep at `.claude/skills/<skill-name>/SKILL.md`.
2. **Case Sensitivity (Filename & Folder Case)**:
   - *Cause*: Named `skill.md` (lowercase) or folder containing capital letters on case-sensitive filesystems (Linux/macOS).
   - *CHIVE Fix*: Filename is guaranteed uppercase **`SKILL.md`**, and each `(function)-CHIVE` folder is paired with an automatic lowercase symlink (`(function)-chive`).
3. **Broken YAML Frontmatter**:
   - *Cause*: Missing closing `---`, multi-line unquoted strings, or unescaped colons and XML tags.
   - *CHIVE Fix*: All frontmatter is verified through strict YAML linting with clean closing fences.
4. **The 1,536-Character Truncation Cap**:
   - *Cause*: The combined `description` + `when_to_use` field exceeds 1,536 characters, getting truncated and losing trigger keywords.
   - *CHIVE Fix*: Descriptions are tightly scoped between 346–463 characters, leading with high-intent action verbs ("Use when the user asks to...").
5. **Model Invocation Disabled (`disable-model-invocation: true`)**:
   - *Cause*: Setting this flag forces manual slash-command invocation only.
   - *CHIVE Fix*: Explicitly set `disable-model-invocation: false` across all auto-invocable skills.
6. **Soft Prompting Ignored by LLM**:
   - *Cause*: Large models occasionally skip soft conversational instructions under context fatigue.
   - *CHIVE Fix*: Enforce the **Zero-Bypass Policy** inside **`CLAUDE.md`**, which is persistently loaded into context on every turn.
7. **Bypassing Architectural Steps via Direct Edits**:
   - *Cause*: The agent attempts to edit files directly without invoking architectural skills.
   - *CHIVE Fix*: Enforced via **Deterministic OS Hooks** (`PreToolUse` in `.claude/settings.json`) that intercept invalid actions at the shell process level (exit code 2).
8. **Stale Session**:
   - *Cause*: Adding skills mid-session. The scanner only indexes descriptions during initial launch.
   - *CHIVE Fix*: Always restart the CLI session (`claude`) after extracting the archive.

---

## 2. Three-Layer Anti-Ignorance Defense Architecture

```
+-------------------------------------------------------------------------------+
| LAYER 1: PERSISTENT SYSTEM CONTEXT (CLAUDE.md)                                |
|   - Injected into Claude Code's session context on EVERY turn.                |
|   - Enforces the Zero-Bypass Policy and Mandatory Trigger Table.              |
+-------------------------------------------------------------------------------+
                                    │
                                    v
+-------------------------------------------------------------------------------+
| LAYER 2: AGENT SKILLS DISCOVERY ENGINE (.claude/skills/*/SKILL.md)            |
|   - Valid YAML frontmatter safely under the 1,536-char cap (346-463 chars).  |
|   - High-Intent Trigger Phrasing and Dual-Case Symlinks.                      |
+-------------------------------------------------------------------------------+
                                    │
                                    v
+-------------------------------------------------------------------------------+
| LAYER 3: DETERMINISTIC OS HOOK GATE (.claude/settings.json)                   |
|   - Executes at the OS shell process level outside LLM discretion.            |
|   - PreToolUse enforces hard block (exit code 2) + Auto-Remediation Template. |
|   - PostToolUse runs automated self-healing diagnostic recovery.              |
+-------------------------------------------------------------------------------+
```
