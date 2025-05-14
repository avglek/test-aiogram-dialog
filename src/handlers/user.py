from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from src.dialogs import register_dialogs
from src.dialogs.bot_menu.states import BotMenu, MySG

router: Router = Router()

register_dialogs(router)

@router.message(Command("menu"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)