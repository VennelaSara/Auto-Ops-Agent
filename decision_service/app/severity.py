def apply_guardrails(llm_output: dict, scores: dict) -> dict:
    max_score = max(scores.values()) if scores else 0.0

    if max_score > 0.8:
        llm_output["severity"] = "CRITICAL"
        llm_output["notify"] = True
        llm_output["create_ticket"] = True

    if max_score < 0.1:
        llm_output["severity"] = "LOW"
        llm_output["notify"] = False

    return llm_output
