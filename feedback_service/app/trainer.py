from app.policy_store import update_policy

def train_policy(app_name: str, reward: float):
    update_policy(app_name, reward)
    return True
