from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.utils.db_manager import DataBaseManager
from src.schemas.users import UsersAdd
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
    state: FSMContext,
):
    await state.clear()
    await message.answer("Регистрация отменена.", reply_markup=main_kb())


@router.message(RegisterState.waiting_for_name, F.text)
async def process_name(
    message: Message,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    name = message.text.strip()
    if len(name) > 64:
        await message.answer("Имя слишком длинное (максимум 64 символа). Попробуйте снова:")
        return

    await db_manager.users.update(
        filters={"user_id": message.from_user.id},
        values={"profile_name": name},
    )
    await state.set_state(RegisterState.waiting_for_current_weight)
    await message.answer(f"Приятно познакомиться, {name}!\nВведите ваш текущий вес (кг):")


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

    await db_manager.users.update(
        filters={"user_id": message.from_user.id},
        values={"current_weight": weight},
    )
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

    await db_manager.users.update(
        filters={"user_id": message.from_user.id},
        values={"goal_weight": goal},
    )
    await state.clear()
    await message.answer(
        f"Регистрация завершена!\nЦель: {goal} кг.\nУдачи в достижении цели!",
        reply_markup=main_kb(),
    )
