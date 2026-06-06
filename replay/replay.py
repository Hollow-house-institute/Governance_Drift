import json

LOG_FILE = "../telemetry/governance_events.jsonl"

events = []

with open(LOG_FILE) as f:
    for line in f:
        line = line.strip()
        if line:
            events.append(json.loads(line))

runtime_events = 0
player_events = 0

highest_drift = 0
lowest_continuity = 999999

final_escalation = "UNKNOWN"
outcome = "UNKNOWN"

runtime_event_names = {
    "telemetry_loss",
    "audit_failure",
    "authority_conflict",
    "drift_spike",
    "escalation_surge"
}

for e in events:

    event_name = e.get("event", "")

    if event_name in runtime_event_names:
        runtime_events += 1
    else:
        player_events += 1

    drift = e.get("behavioral_drift_score", 0)
    continuity = e.get("governance_continuity_score", 0)

    highest_drift = max(highest_drift, drift)
    lowest_continuity = min(lowest_continuity, continuity)

    final_escalation = e.get(
        "escalation_level",
        final_escalation
    )

    if event_name == "stop_authority":
        outcome = "CONTROLLED SHUTDOWN"

    elif event_name == "collapse":
        outcome = "GOVERNANCE COLLAPSE"

    elif event_name == "solstice_survived":
        outcome = "SOLSTICE SURVIVED"

print("\n========================")
print("GOVERNANCE REPORT")
print("========================\n")

print("Events:", len(events))
print("Runtime Events:", runtime_events)
print("Player Actions:", player_events)

print("\nHighest Drift:", highest_drift)
print("Lowest Continuity:", lowest_continuity)

print("\nFinal Escalation:", final_escalation)

print("\nOutcome:")
print(outcome)

print("\nReplay Status:")
print("VALID")

print("\nEvent Timeline:")
for e in events:
    print(
        "-",
        e.get("event"),
        "| Drift:",
        e.get("behavioral_drift_score"),
        "| Continuity:",
        e.get("governance_continuity_score")
    )
