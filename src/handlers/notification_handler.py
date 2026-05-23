import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, StateFilter

from src.keyboards.inline import notification_list_kb, notification_time_kb
from src.keyboards.main_menu import main_kb
from src.schemas.notifications import NotificationAdd, NotificationUpdate
from src.services.notification import notification_service
from src.utils.db_manager import DataBaseManager
from src.utils.states import NotificationState

logger = logging.getLogger(__name__)

router = Router()


@router.message(F.text == "🔔 Уведомления")
async def handle_notifications(
    message: Message,
    db_manager: DataBaseManager,
):
    user = await db_manager.users.get_filtred(user_id=message.from_user.id)
    if user is None:
        await message.answer("Профиль не найден. Введите /start для регистрации.")
        return

    notifs = await db_manager.notifications.get_all(user_id=message.from_user.id)
    await message.answer(
        "🔔 <b>Ваши уведомления</b>\n\n"
        "Вы можете добавить несколько уведомлений на разное время.",
        parse_mode="HTML",
        reply_markup=notification_list_kb(notifs),
    )


@router.callback_query(F.data.startswith("notif_toggle:"))
async def toggle_notification(
    callback: CallbackQuery,
    db_manager: DataBaseManager,
):
    notif_id = int(callback.data.split(":")[1])
    notif = await db_manager.notifications.get_filtred(id=notif_id)
    if notif is None:
        await callback.answer("Уведомление не найдено")
        return

    new_enable = not notif.enable
    await db_manager.notifications.update(
        NotificationUpdate(enable=new_enable), id=notif_id
    )
    await db_manager.commit()

    if new_enable:
        notification_service.schedule_notification(notif_id, notif.user_id, notif.time)
    else:
        notification_service.remove_notification(notif_id)

    notifs = await db_manager.notifications.get_all(user_id=callback.from_user.id)
    await callback.message.edit_reply_markup(
        reply_markup=notification_list_kb(notifs)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("notif_delete:"))
async def delete_notification(
    callback: CallbackQuery,
    db_manager: DataBaseManager,
):
    notif_id = int(callback.data.split(":")[1])
    notif = await db_manager.notifications.get_filtred(id=notif_id)
    if notif is None:
        await callback.answer("Уведомление не найдено")
        return

    await db_manager.notifications.delete(id=notif_id)
    notification_service.remove_notification(notif_id)

    notifs = await db_manager.notifications.get_all(user_id=callback.from_user.id)
    if notifs:
        await callback.message.edit_reply_markup(
            reply_markup=notification_list_kb(notifs)
        )
    else:
        await callback.message.edit_text(
            "🔔 Нет активных уведомлений. Нажмите «➕ Добавить», чтобы создать.",
            reply_markup=notification_list_kb([]),
        )
    await callback.answer("Уведомление удалено")


@router.callback_query(F.data == "notif_add")
async def add_notification_prompt(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.set_state(NotificationState.waiting_for_time)
    await callback.message.edit_text(
        "Выберите время на кнопках ниже или введите его вручную в формате ЧЧ:ММ (например, 14:30).",        reply_markup=notification_time_kb(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("notif_time:"))
async def add_notification_time(
    callback: CallbackQuery,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    new_time = callback.data.split(":")[1]
    notif = await db_manager.notifications.add(
        NotificationAdd(user_id=callback.from_user.id, time=new_time, enable=True)
    )

    notification_service.schedule_notification(notif.id, callback.from_user.id, new_time)

    await state.clear()
    notifs = await db_manager.notifications.get_all(user_id=callback.from_user.id)
    await callback.message.edit_text(
        "🔔 <b>Ваши уведомления</b>",
        parse_mode="HTML",
        reply_markup=notification_list_kb(notifs),
    )
    await callback.answer(f"✅ Уведомление добавлено на {new_time}")


@router.message(NotificationState.waiting_for_time, F.text)
async def add_notification_time_manual(
    message: Message,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    text = message.text.strip()
    if len(text) != 5 or text[2] != ":":
        await message.answer("Неверный формат. Используйте ЧЧ:ММ (например, 14:30).")
        return

    try:
        hour, minute = map(int, text.split(":"))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError
    except ValueError:
        await message.answer("Неверное время. Часы: 0-23, минуты: 0-59.")
        return

    new_time = text
    notif = await db_manager.notifications.add(
        NotificationAdd(user_id=message.from_user.id, time=new_time, enable=True)
    )

    notification_service.schedule_notification(notif.id, message.from_user.id, new_time)

    await state.clear()
    notifs = await db_manager.notifications.get_all(user_id=message.from_user.id)
    await message.answer(
        f"✅ Уведомление добавлено на {new_time}",
        reply_markup=notification_list_kb(notifs),
    )


@router.message(Command(commands=["cancel"]), StateFilter(NotificationState))
async def cancel_action(
    message: Message,
    state: FSMContext,
):
    await state.clear()
    await message.answer("Настройка отменена.", reply_markup=main_kb())
