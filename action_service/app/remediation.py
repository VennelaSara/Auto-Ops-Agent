def auto_remediate(app_name: str, severity: str):
    if severity == "CRITICAL":
        print(f"[REMEDIATE] Restarting {app_name}")
        return True
    return False
