# SentinelPay: Autonomous & Policy-Bounded Revenue Recovery Engine

**SentinelPay** is an agentic payment recovery and dunning engine designed for high-throughput merchants on Razorpay. It diagnoses failed transactions, prevents customer harassment via strict retry ceilings, and maximizes gross merchandise value (GMV) recovery through intelligent discounting and multi-channel routing.

---

## Key Features

- **Root-Cause Diagnostics:** Classifies failure reasons (`INSUFFICIENT_FUNDS`, `GATEWAY_TIMEOUT`, `CARD_EXPIRED`) into optimal recovery actions.
- **Deterministic Guardrails:** Hard-coded compliance ceilings (max 3 retry attempts) to eliminate infinite loops and merchant policy breaches.
- **Dynamic Incentive Engine:** Applies bounded retention discounts (capped at 5-10%) only when order value and recovery probability warrant it.
- **Immutable Audit Trail:** Logs every decision, policy check, and contact attempt directly to the transaction state.

---

## System Architecture

```text
[ Razorpay Failed Webhook ]
            │
            ▼
   [ Diagnose Node ] ──── (Attempts >= 3) ────► [ TERMINATED / Compliant Stop ]
            │
      (Valid State)
            │
            ▼
 [ Execute Recovery Node ] ──► (Dispatches Dynamic Link / Discount) ──► [ END / Ledger Updated ]
