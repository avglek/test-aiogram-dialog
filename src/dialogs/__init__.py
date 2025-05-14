from aiogram import Router
from aiogram_dialog import setup_dialogs

from . import bot_menu


def register_dialogs(router: Router):
    for dialog in [ *bot_menu.bot_menu_dialog() ]:
        router.include_router(dialog)

    setup_dialogs(router)