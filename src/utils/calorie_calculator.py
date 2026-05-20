_ACTIVITY_MULTIPLIER = {
    "сидячий": 1.2,
    "обычный": 1.55,
    "активный": 1.725,
}


def calculate_daily_norm(current_weight: float, goal_weight: float, age: int, height: int, activity_level: str, sex: str) -> int:
    sex_constant = -161 if sex == "Женщина" else 5
    bmr = 10 * current_weight + 6.25 * height - 5 * age + sex_constant
    multiplier = _ACTIVITY_MULTIPLIER.get(activity_level, 1.2)
    tdee = bmr * multiplier

    if goal_weight < current_weight:
        return int(tdee - 500)
    elif goal_weight > current_weight:
        return int(tdee + 300)
    else:
        return int(tdee)
