from langgraph.graph import StateGraph, END
from core.states import TransactionState, FailureReason

def diagnose_failure(state: TransactionState):
    if state.contact_attempts >= state.max_attempts:
        state.status = "TERMINATED"
        state.audit_trail.append(f"Hard stop: Reached {state.max_attempts} attempts.")
        return {"state": state}
    
    if state.failure_reason == FailureReason.GATEWAY_TIMEOUT:
        state.audit_trail.append("Diagnosed: Gateway timeout. Route to Instant Smart Retry.")
    elif state.failure_reason == FailureReason.INSUFFICIENT_FUNDS:
        state.audit_trail.append("Diagnosed: Balance issue. Route to Scheduled Retry.")
    return {"state": state}

def execute_recovery_action(state: TransactionState):
    if state.status == "TERMINATED":
        return {"state": state}
    
    state.contact_attempts += 1
    if state.amount > 5000:
        state.applied_discount_percent = 5.0
    
    state.audit_trail.append(
        f"Attempt {state.contact_attempts}: Recovery link sent with {state.applied_discount_percent}% discount."
    )
    return {"state": state}

def route_next_step(data: dict):
    state = data["state"]
    if state.status == "TERMINATED":
        return END
    return "execute_recovery"

workflow = StateGraph(TransactionState)
workflow.add_node("diagnose", diagnose_failure)
workflow.add_node("execute_recovery", execute_recovery_action)

workflow.set_entry_point("diagnose")
workflow.add_conditional_edges("diagnose", route_next_step, {
    "execute_recovery": "execute_recovery",
    END: END
})
workflow.add_edge("execute_recovery", END)
recovery_app = workflow.compile()