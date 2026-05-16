from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    waiting_for_name = State()
    waiting_for_current_weight = State()
    waiting_for_goal_weight = State()


class CalorieState(StatesGroup):
    waiting_for_calories = State()
