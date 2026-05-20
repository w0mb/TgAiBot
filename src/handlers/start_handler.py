from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from src.keyboards.inline import activity_level_kb, sex_kb
from src.utils.db_manager import DataBaseManager
from src.schemas.users import UsersAdd, UsersUpdate
from src.utils.calorie_calculator import calculate_daily_norm
from src.keyboards.main_menu import main_kb
from src.filters.first_user_filter import IsFirstLaunch
from src.utils.states import RegisterState

router = Router()


@router.message(Command(commands=["start"]), IsFirstLaunch())
async def start_new_user(
    message: Message,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    await db_manager.users.add(UsersAdd(user_id=message.from_user.id))
    await state.set_state(RegisterState.waiting_for_name)
    await message.answer("Добро пожаловать!\nВведите ваше имя для профиля:")


@router.message(Command(commands=["start"]))
async def start_existing_user(
    message: Message,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    await state.clear()
    total = await db_manager.cache.get_daily_calories(message.from_user.id)
    await message.answer(f"Ваш прогресс за сегодня: {total} ккал.", reply_markup=main_kb())


@router.message(Command(commands=["cancel"]), StateFilter(RegisterState))
async def cancel_registration(
    message: Message,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    await state.clear()
    await db_manager.users.delete(user_id=message.from_user.id)
    await message.answer("Регистрация отменена.", reply_markup=main_kb())


@router.message(RegisterState.waiting_for_name, F.text)
async def process_name(
    message: Message,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    name = message.text.strip()
    await db_manager.users.update(UsersUpdate(profile_name=name), user_id=message.from_user.id)
    await state.set_state(RegisterState.waiting_for_sex)
    await message.answer(f"Приятно познакомиться, {name}!\nВыберите ваш пол:", reply_markup=sex_kb())



@router.callback_query(F.data.startswith("edit_sex"), RegisterState.waiting_for_sex)
async def process_sex(
    callback: CallbackQuery,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    sex = callback.data.split(":")[1]
    await db_manager.users.update(UsersUpdate(sex=sex), user_id=callback.from_user.id)
    await state.set_state(RegisterState.waiting_for_age)
    await callback.message.delete()
    await callback.message.answer(f"Пол: {sex}.\nВведите ваш возраст:")
    await callback.answer()


@router.message(RegisterState.waiting_for_age, F.text)
async def process_age(
    message: Message,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    try:
        age = int(message.text.strip())
    except ValueError:
        await message.answer("Пожалуйста, введите число (например: 25):")
        return
    await db_manager.users.update(UsersUpdate(age=age), user_id=message.from_user.id)
    await state.set_state(RegisterState.waiting_for_height)
    await message.answer(f"Ваш возраст: {age}.\nВведите ваш рост (см):")


@router.message(RegisterState.waiting_for_height, F.text)
async def process_height(
    message: Message,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    try:
        height = int(message.text.strip())
    except ValueError:
        await message.answer("Пожалуйста, введите число (например: 175):")
        return

    await db_manager.users.update(UsersUpdate(height=height), user_id=message.from_user.id)
    await state.set_state(RegisterState.waiting_for_activity_level)
    await message.answer(f"Ваш рост: {height} см.\nВыберите ваш уровень активности:", reply_markup=activity_level_kb())


@router.callback_query(F.data.startswith("edit_activity_level"), RegisterState.waiting_for_activity_level)
async def process_activity_level(
    callback: CallbackQuery,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    activity_level = callback.data.split(":")[1]
    await db_manager.users.update(UsersUpdate(activity_level=activity_level), user_id=callback.from_user.id)
    await state.set_state(RegisterState.waiting_for_current_weight)
    await callback.message.delete()
    await callback.message.answer(f"Уровень активности: {activity_level}.\nВведите ваш текущий вес (кг):")
    await callback.answer()


@router.message(RegisterState.waiting_for_current_weight, F.text)
async def process_current_weight(
    message: Message,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    try:
        weight = float(message.text.strip().replace(",", "."))
    except ValueError:
        await message.answer("Пожалуйста, введите число (например: 75.5):")
        return

    await db_manager.users.update(UsersUpdate(current_weight=weight), user_id=message.from_user.id)
    await state.set_state(RegisterState.waiting_for_goal_weight)
    await message.answer(f"Текущий вес: {weight} кг.\nВведите ваш целевой вес (кг):")


@router.message(RegisterState.waiting_for_goal_weight, F.text)
async def process_goal_weight(
    message: Message,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    try:
        goal = float(message.text.strip().replace(",", "."))
    except ValueError:
        await message.answer("Пожалуйста, введите число (например: 70.0):")
        return

    await db_manager.users.update(UsersUpdate(goal_weight=goal), user_id=message.from_user.id)

    user = await db_manager.users.get_filtred(user_id=message.from_user.id)
    daily_norm = calculate_daily_norm(user.current_weight, user.goal_weight, user.age, user.height, user.activity_level, user.sex)
    goal_direction = "похудение" if user.goal_weight < user.current_weight else "набор массы" if user.goal_weight > user.current_weight else "поддержание веса"
    await state.clear()
    await message.answer(
        f"Регистрация завершена!\n"
        f"Цель: {goal} кг ({goal_direction}).\n"
        f"Пол: {user.sex}\n"
        f"Возраст: {user.age}\n"
        f"Рост: {user.height} см\n"
        f"Уровень активности: {user.activity_level}\n"
        f"Ваша дневная норма калорий: <b>{daily_norm}</b> ккал.\n"
        f"Удачи в достижении цели!",
        parse_mode="HTML",
        reply_markup=main_kb(),
    )
