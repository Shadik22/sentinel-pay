import json
import random

reasons = ["INSUFFICIENT_FUNDS", "GATEWAY_TIMEOUT", "CARD_EXPIRED", "MANDATE_DECLINED"]
batch = []

for i in range(1, 101):
    batch.append({
        "payment_id": f"pay_{i:04d}",
        "customer_id": f"cust_{i:04d}",
        "amount": round(random.uniform(500, 15000), 2),
        "failure_reason": random.choice(reasons),
        "contact_attempts": random.choice([0, 1, 2, 3])
    })

with open("evals/batch_100.json", "w") as f:
    json.dump(batch, f, indent=2)
print("Generated evals/batch_100.json with 100 transactions.")