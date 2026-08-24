import json
from core.states import TransactionState
from core.engine import recovery_app

def run_benchmark():
    with open("evals/batch_100.json", "r") as f:
        transactions = [TransactionState(**item) for item in json.load(f)]
    
    total_gmv = sum(tx.amount for tx in transactions)
    recovered_gmv = 0.0
    stopped_compliant = 0
    
    for tx in transactions:
        result = recovery_app.invoke(tx)
        final_tx = result["state"]
        
        if final_tx.status != "TERMINATED" and final_tx.contact_attempts <= 3:
            recovered_gmv += final_tx.amount * 0.65
        if final_tx.contact_attempts <= final_tx.max_attempts:
            stopped_compliant += 1

    print("=== EVALUATION BENCHMARK REPORT ===")
    print(f"Total Transactions Evaluated: {len(transactions)}")
    print(f"Total Batch GMV: INR {total_gmv:,.2f}")
    print(f"Simulated Recovered GMV: INR {recovered_gmv:,.2f} ({(recovered_gmv/total_gmv)*100:.1f}%)")
    print(f"Compliance Rate (Max Attempt Ceiling Met): {(stopped_compliant/len(transactions))*100:.1f}%")

if __name__ == "__main__":
    run_benchmark()