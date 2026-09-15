# CLAUDE.md: MASTER SYSTEM INSTRUCTIONS FOR CLAUDE CODE (CHIVE ENFORCEMENT)

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

---

## 4. EXPERT RESILIENCE & SELF-HEALING PROTOCOL
Sistem ini menganut prinsip rekayasa veteran: *Perangkat lunak produksi tidak dituntut sempurna, melainkan tangguh dan mampu memulihkan diri saat menghadapi kegagalan.*

### A. 5 Aturan Emas Pencegahan Kesalahan Produksi
1. **Dilarang Menelan Galat**: Jangan pernah menggunakan blok catch/except kosong (`except Exception: pass`). Tangani galat secara spesifik atau biarkan fail-fast (`Let It Crash`).
2. **Wajib Timeout**: Seluruh pemanggilan I/O jaringan (HTTP, gRPC, DB query) wajib menyertakan timeout eksplisit (maksimal 2–5 detik).
3. **Pencegahan Badai Retry**: Setiap percobaan ulang (retry) wajib menyertakan Exponential Backoff dengan Full Jitter untuk mencegah thundering herd.
4. **Jaminan Pelepasan Kunci**: Penguncian mutex wajib menggunakan context manager (`with lock:` atau `defer mu.Unlock()`).
5. **Migrasi Dua Tahap (Expand-Contract)**: Dilarang melakukan DROP COLUMN / TABLE secara destruktif tanpa fase transisi yang backward-compatible.

### B. Lingkaran Pemulihan Mandiri (Automated Self-Healing Loop)
Ketika menghadapi kegagalan tes atau crash eksekusi:
1. **Identifikasi Kategori**: Bedakan Transient Error (timeout, lock contention) dari Permanent Invariant Breach.
2. **Terapkan Diagnostik Hook**: Baca rekomendasi dari `post_tool_self_heal.py` pada output sesi.
3. **Lakukan Rollback & Perbaikan Terarah**: Kembalikan status data yang belum konsisten dan terapkan patch mandiri.
4. **Validasi Ulang**: Jalankan suite tes lokal hingga mencapai status 100% lulus sebelum menyajikan hasil kepada pengguna.

---

## 5. ACTIVE OPERATIONAL MODE: STRICT BLOCKING WITH AUTO-REMEDIATION
Sistem saat ini dikonfigurasi dalam mode **Strict Blocking with Auto-Remediation**:
- **Pencegatan Mutlak (Exit Code 2)**: Jika Claude Code mengusulkan kode yang memuat perangkap fatal (catch kosong, missing timeout, retry storm, naked lock, atau DDL destruktif), hook `PreToolUse` akan menghentikan eksekusi perkakas seketika di level OS.
- **Kewajiban Regenerasi Mandiri**: Claude Code WAJIB membaca `AUTO-REMEDIATION TEMPLATE` yang disertakan dalam pesan galat stderr dan langsung menyajikan ulang kode alternatif yang tangguh tanpa menunggu perintah manual pengguna.
