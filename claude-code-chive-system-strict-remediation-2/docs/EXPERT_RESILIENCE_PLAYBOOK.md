# PLAYBOOK REKAYASA SISTEM TANGGUH & PEMULIHAN GALAT (EXPERT RESILIENCE & SELF-HEALING)
*Pengalaman Empiris Arsitektur Produksi Skala Tinggi: Mengatasi Kegagalan Alih-Alih Mengasumsikan Kesempurnaan*

---

## 1. Filosofi Rekayasa Veteran (Battle-Tested Axiom)

> *"Everything fails all the time."* — Werner Vogels  
> Rekayasawan pemula berupaya menulis kode yang diasumsikan tidak akan pernah gagal (ilusi kesempurnaan rapuh). Rekayasawan veteran merancang sistem yang sadar bahwa jaringan akan terputus, database akan mengalami deadlock, disk akan penuh, dan upstream akan timeout—namun sistem tetap mampu mendeteksi, mengisolasi ledakan masalah (*blast radius containment*), dan memulihkan diri secara elegan (*graceful self-healing*).

---

## 2. Katalog 10 Perangkap Nyata Produksi & Pola Penanggulangannya

```
+---------------------------------------------------------------------------------------------------------+
|                               10 PERANGKAP ARSITEKTUR & RESOLUSI EXPERT                                 |
+---------------------------------------------------------------------------------------------------------+
| 1. RETRY STORM (Thundering Herd):                                                                       |
|    - Masalah: Melakukan retry instan tanpa jeda saat upstream down, melumpuhkan server yang baru pulih. |
|    - Resolusi: Exponential Backoff dengan Full Jitter: sleep = min(cap, base * 2^attempt) * rand(0.5, 1.5)|
+---------------------------------------------------------------------------------------------------------+
| 2. UNBOUNDED REMOTE I/O (Cascading Meltdown):                                                           |
|    - Masalah: HTTP/RPC request tanpa batas waktu (timeout), menghabiskan seluruh thread pool sistem.    |
|    - Resolusi: Wajib menyematkan context deadline/timeout pada setiap operasi jaringan (max 2-5 detik). |
+---------------------------------------------------------------------------------------------------------+
| 3. DISTRIBUTED LOCK SPLIT-BRAIN:                                                                        |
|    - Masalah: Lease TTL kunci Redis kedaluwarsa saat GC pause, memicu eksekusi mutasi paralel ganda.    |
|    - Resolusi: Eliminasi kunci terdistribusi; gunakan Single-Writer In-Memory Partitioning lokal.        |
+---------------------------------------------------------------------------------------------------------+
| 4. DESTRUCTIVE SCHEMA MIGRATION:                                                                        |
|    - Masalah: DROP COLUMN / ALTER TYPE mengunci tabel dan merusak backward compatibility pod aktif.     |
|    - Resolusi: Pola Dua Tahap Expand-Contract (fase 1: tambah kolom baru, fase 2: migrasi, fase 3: drop)|
+---------------------------------------------------------------------------------------------------------+
| 5. SILENT ERROR SWALLOWING (Cordero #98):                                                               |
|    - Masalah: Menelan exception dengan catch-all kosong demi metrik uptime semu (membuat zombie state). |
|    - Resolusi: Bedakan Operational Error (Result Type) vs Invariant Violation (Let It Crash / Fail-Fast)|
+---------------------------------------------------------------------------------------------------------+
| 6. NAKED MUTEX & LOCK ORDERING HAZARDS:                                                                 |
|    - Masalah: Mengunci mutex tanpa jaminan pelepasan (defer/finally) atau urutan terbalik memicu deadlock|
|    - Resolusi: Penegakan Monotonic Lock Acquisition Hierarchy dan idiom RAII / context manager.         |
+---------------------------------------------------------------------------------------------------------+
| 7. UNBOUNDED QUEUES & OOM CRASHES:                                                                      |
|    - Masalah: Memori buffer pesan tak terbatas; saat beban melonjak, server kehabisan RAM (OOM-Killed).|
|    - Resolusi: Bounded Queues dengan mekanisme Backpressure aktif dan penolakan anggun (HTTP 429).      |
+---------------------------------------------------------------------------------------------------------+
| 8. POISON PILL & CACHE STAMPEDE:                                                                        |
|    - Masalah: Kunci cache kedaluwarsa serentak, jutaan request menyerbu database secara bersamaan.      |
|    - Resolusi: Cache-Aside dengan TTL acak (probabilistic early refresh / algoritma XFetch).           |
+---------------------------------------------------------------------------------------------------------+
| 9. INCONSISTENT CONCURRENT MUTATION:                                                                    |
|    - Masalah: Mutasi data paralel tanpa isolasi memicu saldo bocor atau race condition.                 |
|    - Resolusi: Optimistic Concurrency Control (OCC via version column) atau Database CAS atomik.        |
+---------------------------------------------------------------------------------------------------------+
| 10. RELEASING UNVERIFIED CODE (Subjectivity Trap):                                                      |
|     - Masalah: Menganggap kode siap produksi hanya karena "terasa benar" tanpa bukti empiris.           |
|     - Resolusi: Gerbang epistemologis fact-verifier-CHIVE (Admiralty 6x6 & pembaharuan log-odds Bayes). |
+---------------------------------------------------------------------------------------------------------+
```

---

## 3. Arsitektur Hook Penegak Otomatis (Pre-Tool Guard & Post-Tool Self-Heal)

Untuk mencegah rekayasawan dan agen AI mengulangi kesalahan di atas, sistem CHIVE menerapkan dua lapis hook aktif di `.claude/hooks/`:

1. **Pre-Tool Static Guard (`protect-invariants.sh` -> `expert_guard_scanner.py`)**:
   - Berjalan sebelum perintah `Edit`, `Write`, atau `Bash` dieksekusi oleh Claude Code.
   - Memindai pola berbahaya (catch-all kosong, missing timeout, naked locks, destructive DDL).
   - **Tindakan**: Jika terdeteksi, memblokir eksekusi (exit code 2) dan mengembalikan instruksi perbaikan konkret sehingga Claude Code otomatis memperbaiki kodenya sebelum disimpan ke disk.

2. **Post-Tool Self-Healing Diagnostic (`post-skill-verify.sh` -> `post_tool_self_heal.py`)**:
   - Berjalan segera setelah perintah selesai.
   - Jika terjadi galat (SyntaxError, DeadlockDetected, InvariantViolation, Timeout 502/504), hook mendiagnosis akar masalahnya dan menyuntikkan langkah pemulihan (*self-healing action*) langsung ke konteks sesi.
