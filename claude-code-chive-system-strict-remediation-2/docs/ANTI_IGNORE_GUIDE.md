# PANDUAN TEKNIS MENCEGAH PENGABAIAN SKILL OLEH CLAUDE CODE
*Berdasarkan Dokumentasi Resmi Claude Code (code.claude.com/docs/en/skills) & Investigasi Komunitas (LazySkills.sh)*

---

## 1. Anatomi Mengapa Claude Code Mengabaikan Skill

Berdasarkan dokumentasi teknis resmi Anthropic dan investigasi mendalam ekosistem Claude Code, kegagalan pemanggilan skill (*Skill Not Triggering / Ignored*) bersumber dari 8 titik kegagalan utama:

1. **Struktur Direktori & Kedalaman Folder (Nesting Level)**:
   - *Penyebab*: Berkas `SKILL.md` diletakkan terlalu dalam (misal: `.claude/skills/deploy/deploy/SKILL.md`) atau langsung di root `.claude/skills/SKILL.md`.
   - *Solusi CHIVE*: Setiap skill berada tepat 1 tingkat di bawah `.claude/skills/<skill-name>/SKILL.md`.
2. **Sensitivitas Huruf Besar/Kecil (Filename & Folder Case)**:
   - *Penyebab*: Berkas dinamai `skill.md` (huruf kecil) atau folder memakai huruf besar pada sistem operasi case-sensitive (Linux/macOS).
   - *Solusi CHIVE*: Nama berkas dijamin **`SKILL.md`** (huruf kapital), dan setiap folder skill `(nama fungsi)-CHIVE` dilengkapi *symlink* otomatis ke versi huruf kecil (`(nama-fungsi)-chive`) untuk kompatibilitas 100%.
3. **Kerusakan Frontmatter YAML (Broken Frontmatter)**:
   - *Penyebab*: Ketiadaan penutup `---`, deskripsi multi-baris tanpa indentasi valid, atau tag XML di dalam frontmatter.
   - *Solusi CHIVE*: Seluruh frontmatter diverifikasi melalui linter YAML otomatis dengan pagar pembatas baris pertama dan penutup yang presisi.
4. **Batas Pemotongan 1.536 Karakter (The 1,536-Character Truncation Cap)**:
   - *Penyebab*: Gabungan field `description` dan `when_to_use` melebihi 1.536 karakter, sehingga terpotong di tengah jalan dan kehilangan frasa pemicu (*trigger keywords*).
   - *Solusi CHIVE*: Seluruh deskripsi dioptimasi padat pada rentang 350-465 karakter dengan mendahulukan kata kerja aksi ("Use when the user asks to...").
5. **Flag Non-Aktif Model (`disable-model-invocation`)**:
   - *Penyebab*: Nilai `disable-model-invocation: true` mematikan pemanggilan otomatis oleh Claude Code.
   - *Solusi CHIVE*: Ditetapkan eksplisit `disable-model-invocation: false` pada seluruh skill yang ditujukan untuk deteksi otomatis.
6. **Sesi Usang (Stale Session)**:
   - *Penyebab*: Skill ditambahkan saat sesi Claude Code sedang berjalan. Claude Code hanya membaca katalog skill pada inisialisasi awal sesi.
   - *Solusi CHIVE*: Panduan mewajibkan me-restart sesi (`claude`) setelah mengekstrak ZIP.
7. **Pelemahan Semantik Prompt (Vague Prompting)**:
   - *Penyebab*: Model LLM mengabaikan instruksi lunak (*soft prompt*) jika tidak ditegakkan di level sistem.
   - *Solusi CHIVE*: Menempatkan direktif penegakan tanpa-kompromi (*Zero-Bypass Policy*) di dalam berkas **`CLAUDE.md`** yang dibaca Claude Code pada setiap giliran percakapan.
8. **Pengabaian Eksekusi oleh Model**:
   - *Penyebab*: Model memilih jalur termudah tanpa menggunakan alat bantu.
   - *Solusi CHIVE*: Penegakan melalui **Hook Deterministik OS** (`PreToolUse` di `.claude/settings.json`) yang berjalan di level shell dan memblokir modifikasi kode sebelum aturan dipatuhi.

---

## 2. Arsitektur Pertahanan 3-Lapis Anti-Pengabaian

```
+-------------------------------------------------------------------------------+
| LAPIS 1: PERSISTENT SYSTEM CONTEXT (CLAUDE.md)                                |
|   - Dimuat ke konteks sesi Claude Code pada SETIAP pergantian giliran.         |
|   - Berisi Zero-Bypass Policy dan Matriks Pemicu Wajib yang mengikat model.   |
+-------------------------------------------------------------------------------+
                                    │
                                    ▼
+-------------------------------------------------------------------------------+
| LAPIS 2: AGENT SKILLS DISCOVERY ENGINE (.claude/skills/*/SKILL.md)            |
|   - YAML frontmatter valid dengan kuota <= 1.536 karakter.                    |
|   - Frasa pemicu berdensitas tinggi (High-Intent Trigger Phrasing).           |
|   - Symlink dual-case (mendukung pemanggilan huruf besar & huruf kecil).      |
+-------------------------------------------------------------------------------+
                                    │
                                    ▼
+-------------------------------------------------------------------------------+
| LAPIS 3: DETERMINISTIC OS HOOK GATE (.claude/settings.json)                   |
|   - Berjalan di level shell Linux/macOS di luar kendali subjektif LLM.        |
|   - PreToolUse memblokir aksi tak sah (exit code 2).                          |
|   - PostToolUse memverifikasi sintaksis dan memicu fact-verifier-CHIVE.       |
+-------------------------------------------------------------------------------+
```
