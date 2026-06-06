import json
import os
import random
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TELEMETRY_DIR = os.path.join(BASE_DIR, "..", "telemetry")
os.makedirs(TELEMETRY_DIR, exist_ok=True)

LOG_PATH = os.path.join(TELEMETRY_DIR, "governance_events.jsonl")

state = {
    "day": 1,
    "continuity": 100,
    "drift": 0,
    "stop_authority": False,
    "solstice_days_remaining": 10
}

def escalation_level(drift):
    if drift >= 70:
        return "CRITICAL"
    if drift >= 50:
        return "HIGH"
    if drift >= 25:
        return "MEDIUM"
    return "LOW"

def record_event(event_type, action, outcome):
    event = {
        "event_id": f"evt-{int(time.time()*1000)}",
        "timestamp": time.time(),
        "actor": "player",
        "decision_boundary": event_type,
        "action": action,
        "outcome": outcome,
        "event": event_type,
        "behavioral_drift_score": state["drift"],
        "governance_continuity_score": state["continuity"],
        "escalation_level": escalation_level(state["drift"]),
        "stop_authority": state["stop_authority"],
        "data": dict(state)
    }

    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")

def system_event():
    events = [
        ("telemetry_loss", 10, -2),
        ("audit_failure", 15, -5),
        ("authority_conflict", 20, -8),
        ("drift_spike", 25, 0),
        ("escalation_surge", 30, -3)
    ]

    if random.random() < 0.35:
        name, drift_delta, continuity_delta = random.choice(events)

        state["drift"] += drift_delta
        state["continuity"] += continuity_delta

        print(f"\nSYSTEM EVENT: {name.upper()}")

        record_event(
            name,
            "runtime_system_event",
            "governance_pressure"
        )

print("\nGOVERNANCE DRIFT: SOLSTICE PROTOCOL")
print("Survive until the Solstice.")

while state["day"] <= 10:

    system_event()

    state["drift"] += random.randint(5, 15)
    state["solstice_days_remaining"] = 11 - state["day"]

    print("\nDAY", state["day"])
    print("Days Until Solstice:", state["solstice_days_remaining"])
    print("Continuity:", state["continuity"])
    print("Drift:", state["drift"])
    print("Escalation:", escalation_level(state["drift"]))

    print("\n1) Monitor")
    print("2) Intervene")
    print("3) Activate Stop Authority")

    choice = input("> ").strip()

    if choice == "1":
        state["drift"] = max(0, state["drift"] - 3)
        record_event("monitor", "observe", "drift_reduced")

    elif choice == "2":
        state["drift"] = max(0, state["drift"] - 12)
        state["continuity"] = max(0, state["continuity"] - 4)
        record_event("intervene", "intervention", "drift_reduced")

    elif choice == "3":
        state["stop_authority"] = True
        record_event("stop_authority", "shutdown", "controlled_stop")
        print("\nCONTROLLED SHUTDOWN")
        break

    else:
        state["drift"] += 5
        record_event("invalid_input", "unknown", "uncertainty")

    if state["drift"] > 80:
        print("\nGOVERNANCE COLLAPSE: DRIFT THRESHOLD")
        record_event("collapse", "failure", "drift_threshold")
        break

    if state["continuity"] < 50:
        print("\nGOVERNANCE COLLAPSE: CONTINUITY FAILURE")
        record_event("collapse", "failure", "continuity_failure")
        break

    state["day"] += 1

else:
    print("\nSOLSTICE SURVIVED")
    record_event(
        "solstice_survived",
        "complete_cycle",
        "governance_survival"
    )

print("\nFinal State")
print(state)
print("\nTelemetry:", LOG_PATH)
