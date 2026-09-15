# Claude Code CHIVE Skill System

Paket sistem skill profesional berformat modular untuk **Claude Code**, mengintegrasikan sintesis karya John Ousterhout (*A Philosophy of Software Design*), Luis Cordero (*100 Mistakes in Software Engineering*), serta mesin konfirmasi fakta epistemologis *First Principle Codex OS (FPCOS)* & *Possibility-Hive*.

---

## 1. Fitur Utama
- **Arsitektur Modular 8-Skill**: Pemisahan tegas antara orkestrasi, desain antarmuka, ergonomi kognitif, dokumentasi keputusan, manajemen utang teknis, kinerja ekstrem, topologi sistem, dan verifikasi fakta.
- **Hook Terpadu**: Integrasi hook bawaan Claude Code (`PreToolUse`, `PostToolUse`, `SessionStart`) dengan skrip bash penegak integritas berkas dan pencegah modifikasi berbahaya.
- **Format Sesuai Standar Claude Code**: Menggunakan format `SKILL.md` resmi dengan frontmatter YAML, pendukung skrip python otomatis, dan konfigurasi `.claude/settings.json`.
- **Konfirmasi Fakta Epistemologis**: Setiap penarikan kesimpulan teknis diverifikasi menggunakan standar intelijen NATO STANAG 2064 / Admiralty Code 6x6, Analysis of Competing Hypotheses (ACH), dan kalibrasi WEP ICD 203.

---

## 2. Panduan Pemasangan (Installation)

### Opsi A: Ekstraksi Langsung ke Repositori Proyek
Ekstrak isi berkas `claude-code-chive-system.zip` langsung ke direktori akar (*root*) proyek Anda:
```bash
unzip claude-code-chive-system.zip -d /path/to/your/project/
```
Struktur `.claude/`, `CLAUDE.md`, dan `ARCHITECTURE.md` akan langsung aktif secara otomatis saat Anda menjalankan perintah `claude`.

### Opsi B: Pemasangan Global Personal Skill
Salin folder skill ke direktori konfigurasi global Claude Code:
```bash
mkdir -p ~/.claude/skills/
cp -r .claude/skills/* ~/.claude/skills/
```

---

## 3. Contoh Alur Kerja Profesional (Workflow)

```bash
# 1. Jalankan Claude Code di repositori proyek Anda
claude

# 2. Minta Claude mengorkestrasi perancangan modul pembayaran baru
/orchestrator-CHIVE Rancang modul pemrosesan pembayaran skala tinggi dengan antarmuka yang bersih dan bebas deadlock

# 3. Claude Code secara otomatis:
#    - Memeriksa hook pre-execution
#    - Memicu module-boundary-CHIVE untuk desain antarmuka
#    - Memicu critical-resilience-CHIVE untuk optimasi konkurensi tanpa distributed lock
#    - Memicu fact-verifier-CHIVE untuk mengonfirmasi keamanan dan kestabilan desain
```
