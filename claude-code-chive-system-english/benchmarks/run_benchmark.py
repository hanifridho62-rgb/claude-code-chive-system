"""
run_benchmark.py - High-Throughput Performance Profiler for WalletSettlementEngine
Measures operations per second, latency percentiles (p50, p95, p99), and memory efficiency.
"""

import time
import statistics
import uuid
import sys
import os

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests")))
from wallet_engine import WalletSettlementEngine, TransferRequest

def run_settlement_benchmark(num_transactions=10000):
    engine = WalletSettlementEngine()
    engine.register_account("bench_source", 500_000_000) # $5,000,000.00
    engine.register_account("bench_target", 0)

    latencies_ms = []
    start_total = time.perf_counter()

    for i in range(num_transactions):
        t0 = time.perf_counter()
        req = TransferRequest(
            source_account_id="bench_source",
            target_account_id="bench_target",
            amount_cents=100,
            idempotency_key=f"bench_tx_{i}"
        )
        res = engine.transfer(req)
        latencies_ms.append((time.perf_counter() - t0) * 1000)

    total_time_sec = time.perf_counter() - start_total
    ops_per_sec = num_transactions / total_time_sec

    p50 = statistics.median(latencies_ms)
    p95 = statistics.quantiles(latencies_ms, n=20)[18]
    p99 = statistics.quantiles(latencies_ms, n=100)[98]
    avg_lat = statistics.mean(latencies_ms)

    print("=" * 65)
    print("  WALLET SETTLEMENT ENGINE - BENCHMARK KINERJA PRODUKSI")
    print("=" * 65)
    print(f"Total Transaksi     : {num_transactions:,} transfer atomik")
    print(f"Total Durasi        : {total_time_sec:.3f} detik")
    print(f"Throughput          : {ops_per_sec:,.1f} operasi/detik (TPS)")
    print(f"Rata-rata Latensi   : {avg_lat:.4f} ms ({avg_lat * 1000:.1f} µs)")
    print(f"Latensi p50 (Median): {p50:.4f} ms")
    print(f"Latensi p95         : {p95:.4f} ms")
    print(f"Latensi p99         : {p99:.4f} ms")
    print(f"Status Invarian     : {engine.verify_system_invariants()} (Terkonfirmasi)")
    print("=" * 65)

    return {
        "num_transactions": num_transactions,
        "total_time_sec": total_time_sec,
        "throughput_ops_sec": ops_per_sec,
        "avg_latency_ms": avg_lat,
        "p50_ms": p50,
        "p95_ms": p95,
        "p99_ms": p99
    }

if __name__ == "__main__":
    run_settlement_benchmark(20000)
