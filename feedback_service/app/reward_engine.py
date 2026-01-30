def compute_reward(feedback):
    reward = 0.0

    if feedback.success:
        reward += 1.0
    else:
        reward -= 1.0

    if feedback.manual_override:
        reward -= 0.5

    if feedback.user_rating:
        reward += (feedback.user_rating - 3) * 0.2

    return round(reward, 2)
