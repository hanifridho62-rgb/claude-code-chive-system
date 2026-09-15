# DENAH & ARSITEKTUR SISTEM SKILL CHIVE (CLAUDE CODE SPECIFICATION)

Dokumen ini mendefinisikan topologi struktural, siklus hidup *hooks*, protokol interaksi antarmuka, dan tata kelola epistemologis sistem skill **(nama fungsi)-CHIVE** yang dirancang untuk kompatibilitas penuh dengan **Claude Code**.

---

## 1. Topologi Direktori & Tata Letak Berkas (Filesystem Layout)

```
claude-code-chive-system/
├── CLAUDE.md                               # Panduan master sesi untuk Claude Code
├── ARCHITECTURE.md                         # Denah dan topologi arsitektur sistem skill ini
├── README.md                               # Panduan instalasi dan operasional tim
├── .claude-plugin/
│   └── plugin.json                         # Manifest plugin resmi Claude Code
├── .claude/
│   ├── settings.json                       # Konfigurasi hook siklus hidup Claude Code
│   ├── hooks/                              # Shell script deterministik untuk pengamanan kode
│   │   ├── protect-invariants.sh           # PreToolUse hook (Edit/Write guard)
│   │   ├── post-skill-verify.sh            # PostToolUse hook (Syntax & linter check)
│   │   ├── pre-skill-check.sh              # SessionStart hook (Status injeksi)
│   │   └── fact-check-gate.sh              # CLI runner untuk verifikasi fakta
│   └── skills/                             # Modul skill mandiri berstandar Agent Skills
│       ├── orchestrator-CHIVE/             # Master Dispatcher & Task Router
│       │   ├── SKILL.md
│       │   └── scripts/router.py
│       ├── module-boundary-CHIVE/          # Dekomposisi & Batas Antarmuka Modul
│       │   └── SKILL.md
│       ├── cognitive-cleanse-CHIVE/        # Ergonomi Kognitif & Kebersihan Leksikal
│       │   └── SKILL.md
│       ├── design-explorer-CHIVE/          # Metodologi Desain & ADR
│       │   └── SKILL.md
│       ├── strategic-debt-CHIVE/           # Pemrograman Strategis & PR Discipline
│       │   └── SKILL.md
│       ├── critical-resilience-CHIVE/      # Kinerja Ekstrem & Fail-Fast
│       │   └── SKILL.md
│       ├── topology-lifecycle-CHIVE/       # Topologi & Operasi Produksi
│       │   └── SKILL.md
│       └── fact-verifier-CHIVE/            # Gerbang Konfirmasi Fakta Epistemologis
│           ├── SKILL.md
│           └── scripts/bayesian_admiralty.py
```

---

## 2. Model Komunikasi Antar-Skill (Inter-Skill Interaction)

Sistem CHIVE beroperasi menggunakan model hierarkis terpusat:

```
                  +-----------------------------------+
                  |        Permintaan Pengguna        |
                  +-----------------+-----------------+
                                    |
                                    v
                  +-----------------------------------+
                  |        orchestrator-CHIVE         |
                  |     (Analisis Intent & Rute)      |
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
                  | Output Terkonfirmasi ke Pengguna  |
                  +-----------------------------------+
```

### A. Protokol Pemanggilan
1. Pengguna atau agen memicu `orchestrator-CHIVE` (secara langsung melalui `/orchestrator-CHIVE` atau otomatis saat prompt menyentuh tugas rekayasa).
2. `orchestrator-CHIVE` menjalankan skrip pendukung `scripts/router.py` untuk mengidentifikasi kata kunci dan memetakan dependensi skill.
3. Skill spesialis dijalankan secara terisolasi untuk menangani domain kode yang relevan.
4. Seluruh keluaran wajib melewati `fact-verifier-CHIVE` untuk pengujian fakta dan kalibrasi tingkat keyakinan sebelum respons final diserahkan kepada pengguna.

---

## 3. Siklus Hidup Hook (Hook Lifecycle & Invariant Protection)

Sistem CHIVE mengintegrasikan dua lapis hook:
1. **Lapis Deterministik (Claude Code Native Hooks di `.claude/settings.json`)**:
   - `SessionStart`: Memvalidasi lingkungan proyek dan menginjeksi status aktif modul CHIVE ke konteks sesi.
   - `PreToolUse` (`protect-invariants.sh`): Mencegah modifikasi yang tidak disengaja pada berkas konfigurasi kritis (`.env`, `.git/`, berkas arsitektur).
   - `PostToolUse` (`post-skill-verify.sh`): Memeriksa keabsahan sintaksis dan integritas berkas segera setelah perkakas `Edit` atau `Write` selesai dijalankan.
2. **Lapis Epistemologis (Mind Hive Hooks di `fact-verifier-CHIVE`)**:
   - Menerapkan protokol FPCOS (First Principle Codex OS 2.0).
   - Menghitung rasio kemungkinan log-space (*Log-Space Likelihood Ratio*) dan memperbarui probabilitas posterior.
   - Menerapkan batasan keyakinan (*shadow judgment*): jika hipotesis tandingan kuat, batasi keyakinan $\le 70\%$ (*RAPUH*).

---

## 4. Format Keluaran Profesional Standar
Setiap skill CHIVE mematuhi standar keluaran objektif, padat, dan bebas dari kepastian semu, ditutup dengan:
```markdown
### BIDANG PENILAIAN KRITIS (FACT-VERIFIER-CHIVE)
- **KEYAKINAN**: [X%] — [Kategori WEP ICD 203] (Level Keyakinan: High / Moderate / Low)
- **PUTUSAN BAYANGAN**: [KONSISTEN / RAPUH / BANGUN ULANG]
- **TITIK BUTA / TIDAK DIKETAHUI**: [Data spesifik yang belum diverifikasi]
- **KONDISI GAGAL**: [Skenario batas di mana solusi ini runtuh]
```

---

# BAB 4: MATRIKS DISAMBIGUASI & KONTRAK BATAS DOMAIN (DOMAIN DISAMBIGUATION CONTRACT)

Untuk mencegah tumpang tindih wewenang, kebocoran batas abstraksi, dan ambiguitas operasional antar-skill, sistem CHIVE menegakkan 6 Ketetapan Disambiguasi Mutlak:

## 1. Matriks Arbitrase Tumpang Tindih Antar-Skill (Cross-Skill Boundary Arbitration)

| Skenario Konflik | Skill A vs Skill B | Ketetapan Arbitrase & Garis Demarkasi Mutlak |
| :--- | :--- | :--- |
| **Refactoring Modul** | `module-boundary-CHIVE` vs `cognitive-cleanse-CHIVE` | **Batas Antarmuka vs Internal Fungsi**: Jika perubahan menyentuh *signature publik*, visibilitas kelas, atau dekomposisi tanggung jawab modul -> Wewenang mutlak milik `module-boundary-CHIVE`. Jika perubahan murni bersifat *intra-fungsi* (penamaan variabel lokal, pembersihan dead code, ekstraksi one-liner, eliminasi boolean flag) -> Wewenang milik `cognitive-cleanse-CHIVE`. |
| **Konflik Kinerja vs Keterbacaan** | `cognitive-cleanse-CHIVE` (Immutability) vs `critical-resilience-CHIVE` (Zero-Allocation) | **The 5% Critical Path Exemption Rule**: Pada jalur dingin (*cold path* / business logic normal), Immutability ditegakkan 100% tanpa kompromi. Pada jalur kritis (*hot loop* / throughput tinggi yang menyumbang 95% latency), mutasi in-place diperbolehkan DENGAN SYARAT dienkapsulasi rapat di dalam modul tanpa pernah membocorkan referensi buffer internal ke pemanggil luar. |
| **Perencanaan & Arsitektur** | `design-explorer-CHIVE` vs `strategic-debt-CHIVE` | **Prospektif vs Retrospektif**: `design-explorer-CHIVE` menangani keputusan *masa depan* (eksplorasi 2-3 alternatif desain sebelum kode ditulis via Design It Twice dan penulisan ADR). `strategic-debt-CHIVE` menangani tata kelola *masa lalu dan proses* (alokasi kuota 10-20% utang teknis, format 4-Pilar PR, dan penataan piramida tes). |
| **Skalabilitas & Topologi** | `critical-resilience-CHIVE` vs `topology-lifecycle-CHIVE` | **In-Process Priority Rule**: Sebelum memecah layanan menjadi arsitektur mikroservis atau distributed locking, masalah konkurensi dan throughput WAJIB diselesaikan terlebih dahulu di tingkat in-memory partition / database indexing lokal. Dilarang menaikkan masalah ke level topologi terdistribusi jika optimasi lokal belum tuntas. |

## 2. Taksonomi Penanganan Galat: Invariant Violation vs Operational Error

Dilarang mencampuradukkan penanganan galat normal dengan kegagalan fatal:

```
                                  [Terjadi Galat / Error]
                                             │
               ┌─────────────────────────────┴─────────────────────────────┐
               ▼                                                           ▼
    [OPERATIONAL ERROR]                                         [INVARIANT VIOLATION]
(Domain Bisnis / Kasus Batas Terduga)                       (Aksioma Sistem Terlanggar)
   - Input validasi gagal                                      - Delta neraca saldo != 0
   - Saldo tidak mencukupi                                     - Nil pointer pada state yang wajib ada
   - Timeout dependensi luar                                   - Korupsi indeks memori
   - Rekening tujuan tidak ditemukan                           - Unhandled state machine transition
               │                                                           │
               ▼                                                           ▼
    [KEMBALIKAN RESULT TYPE]                                    [LET IT CRASH (FAIL-FAST)]
Tolak dengan error code terstruktur.                        Hentikan eksekusi seketika (panic / exit(1)).
Dilarang melempar panic / crash.                            DILARANG ditelan oleh blok catch-all.
Sistem tetap melayani request lain.                         Biarkan supervisor merestart container bersih.
```

## 3. Disambiguasi Tiga Jalur Eksekusi (Spike vs Bounded vs Architectural)

1. **Spike**:
   - *Kriteria*: Pertanyaan kelayakan ("Apakah library X mendukung fitur Y pada runtime ini?").
   - *Artefak*: Ringkasan 2-3 kalimat di obrolan. Kode yang dihasilkan dilabeli *throwaway* (sekali pakai) dan tidak boleh di-merge ke branch utama.
2. **Bounded**:
   - *Kriteria*: Perubahan terbatas pada alur kode yang sudah ada (misal: penambahan parameter, perbaikan bug di 1 berkas, endpoint CRUD turunan).
   - *Artefak*: Desain singkat di obrolan, tanpa dokumen spesifikasi terpisah. Persetujuan manusia tetap wajib sebelum coding dimulai.
3. **Architectural**:
   - *Kriteria*: Modul baru, subsistem baru, perubahan skema database multi-tabel, atau perubahan kontrak antarmuka yang dipakai modul lain.
   - *Artefak*: Dokumen spesifikasi lengkap (`docs/superpowers/specs/`), Architecture Decision Record (`docs/adr/`), dan review gate formal.

## 4. Disambiguasi Pembobotan Bukti Admiralty 6x6 & Nilai Prior Bayes

Untuk memastikan objektivitas evaluasi bukti pada `fact-verifier-CHIVE`:
- **Prior Awal Default**: $P(H_0) = 0.50$ (ketiadaan bias konfirmasi).
- **Pemetaan Bukti Empiris**:
  - `A1`: Log eksekusi tes otomatis lokal yang lulus 100% atau benchmark CPU reproducible.
  - `B2`: Profiling telemetri produksi representatif atau metrik p99 query plan database.
  - `C3`: Analisis teoritis kompleksitas algoritma Big-O tanpa benchmark fisik.
  - `D4`-`F6`: Asumsi verbal atau klaim tanpa verifikasi (tidak dihitung dalam penarikan kesimpulan).
- **Shadow Judgment Gate**:
  - Jika terdapat bukti tandingan kredibel $\ge C3$, putusan bayangan otomatis diturunkan menjadi **RAPUH** dan batas keyakinan dikunci $\le 70\%$.
