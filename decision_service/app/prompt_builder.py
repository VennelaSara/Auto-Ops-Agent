def build_decision_prompt(data: dict) -> str:
    return f"""
You are an AIOps decision engine.

Analyze the following anomaly report and decide:
1. Severity (LOW, MEDIUM, HIGH, CRITICAL)
2. Probable root cause
3. Recommended action
4. Whether to notify on-call engineer
5. Whether to create a Jira ticket
6. Confidence score (0.0 to 1.0)

Context:
App Name: {data['app_name']}
App Type: {data['app_type']}

Metrics:
{data['metrics']}

Anomalies:
{data['anomalies']}

Anomaly Scores:
{data['scores']}

Respond ONLY in JSON with keys:
severity, root_cause, recommendation, notify, create_ticket, confidence
"""
