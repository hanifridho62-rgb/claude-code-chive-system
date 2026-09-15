"""
test_wallet_settlement.py - Professional Test Suite for WalletSettlementEngine
Covers Unit, Invariant, Concurrency Stress, and Observability tests.
"""

import unittest
import threading
import random
import uuid
from wallet_engine import (
    WalletSettlementEngine, TransferRequest, LedgerInvariantViolation, WideSettlementEvent
)

class TestWalletSettlementEngine(unittest.TestCase):

    def setUp(self):
        self.sink = []
        self.engine = WalletSettlementEngine(wide_event_sink=self.sink)
        self.engine.register_account("acc_alice", 100_000) # $1,000.00
        self.engine.register_account("acc_bob", 50_000)    # $500.00
        self.engine.register_account("acc_charlie", 0)     # $0.00

    def test_successful_transfer(self):
        req = TransferRequest(
            source_account_id="acc_alice",
            target_account_id="acc_bob",
            amount_cents=25_000,
            idempotency_key="idemp_001"
        )
        res = self.engine.transfer(req)
        self.assertTrue(res.is_success)
        self.assertEqual(self.engine.get_balance("acc_alice"), 75_000)
        self.assertEqual(self.engine.get_balance("acc_bob"), 75_000)
        self.assertTrue(self.engine.verify_system_invariants())
        self.assertEqual(len(self.sink), 1)
        self.assertEqual(self.sink[0].event_name, "wallet.transfer.success")

    def test_insufficient_funds(self):
        req = TransferRequest(
            source_account_id="acc_charlie",
            target_account_id="acc_bob",
            amount_cents=5_000,
            idempotency_key="idemp_002"
        )
        res = self.engine.transfer(req)
        self.assertFalse(res.is_success)
        self.assertEqual(res.error_code, "INSUFFICIENT_FUNDS")
        self.assertEqual(self.engine.get_balance("acc_charlie"), 0)
        self.assertTrue(self.engine.verify_system_invariants())

    def test_idempotency_replay(self):
        req = TransferRequest(
            source_account_id="acc_alice",
            target_account_id="acc_bob",
            amount_cents=10_000,
            idempotency_key="idemp_repeat"
        )
        res1 = self.engine.transfer(req)
        self.assertTrue(res1.is_success)
        balance_alice_after_first = self.engine.get_balance("acc_alice")

        # Replay same request
        res2 = self.engine.transfer(req)
        self.assertTrue(res2.is_success)
        self.assertEqual(res1.transaction_id, res2.transaction_id)
        # Balance must NOT be deducted twice
        self.assertEqual(self.engine.get_balance("acc_alice"), balance_alice_after_first)
        self.assertTrue(self.engine.verify_system_invariants())

    def test_concurrency_stress_conservation_of_money(self):
        """
        Stress test: 10 accounts, 50 worker threads performing 2,000 random transfers.
        Guarantees:
        1. No negative balances.
        2. Total money in the system is invariant (exactly conserved).
        3. Zero deadlocks or race condition panics.
        """
        accounts = [f"stress_acc_{i}" for i in range(10)]
        initial_balance_per_account = 100_000 # 1,000.00 each -> Total 10,000.00
        stress_engine = WalletSettlementEngine()
        for acc in accounts:
            stress_engine.register_account(acc, initial_balance_per_account)

        total_minted = initial_balance_per_account * len(accounts)

        def worker():
            for _ in range(40):
                src, tgt = random.sample(accounts, 2)
                amt = random.randint(100, 2000) # $1 to $20
                req = TransferRequest(
                    source_account_id=src,
                    target_account_id=tgt,
                    amount_cents=amt,
                    idempotency_key=str(uuid.uuid4())
                )
                stress_engine.transfer(req)

        threads = [threading.Thread(target=worker) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Audit System Invariants
        self.assertTrue(stress_engine.verify_system_invariants())
        final_total = sum(stress_engine.get_balance(acc) for acc in accounts)
        self.assertEqual(final_total, total_minted, "Total money must be conserved!")
        for acc in accounts:
            self.assertGreaterEqual(stress_engine.get_balance(acc), 0, "No account can have negative balance")

    def test_let_it_crash_invariant_violation(self):
        """Verify that invariant corruption triggers immediate fail-fast exception."""
        # Intentionally tamper private state to simulate hardware/bit-flip corruption
        self.engine._balances["acc_alice"] += 500
        with self.assertRaises(LedgerInvariantViolation):
            self.engine.verify_system_invariants()

if __name__ == "__main__":
    unittest.main()
