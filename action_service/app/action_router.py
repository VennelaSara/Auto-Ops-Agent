from app.slack_client import send_slack_alert
from app.jira_client import create_jira_ticket
from app.remediation import auto_remediate

def execute_actions(input_data):
    actions = []

    if input_data.notify:
        send_slack_alert(
            f"🚨 {input_data.severity} | {input_data.app_name}\n"
            f"Cause: {input_data.root_cause}\n"
            f"Action: {input_data.recommendation}"
        )
        actions.append("slack_alert")

    if input_data.create_ticket:
        create_jira_ticket(
            summary=f"{input_data.severity} issue in {input_data.app_name}",
            description=input_data.root_cause
        )
        actions.append("jira_ticket")

    if auto_remediate(input_data.app_name, input_data.severity):
        actions.append("auto_remediation")

    return actions
