from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button

from src.dialogs.bot_menu.states import BotMenu, BuyProduct


async def on_chosen_category(
        c: CallbackQuery,
        widget:Select,
        manager:DialogManager,
        item_id:str):
    ctx = manager.current_context()
    ctx.dialog_data.update(category_id=item_id)
    await manager.switch_to(BotMenu.select_products)

async def on_chosen_product(c: CallbackQuery, widget:Select, manager:DialogManager, item_id:str):
    ctx = manager.current_context()
    ctx.dialog_data.update(product_id=item_id)
    await manager.switch_to(BotMenu.product_info)

async def on_buy_product(c: CallbackQuery, widget:Button, manager:DialogManager):
    ctx = manager.current_context()
    product_id = ctx.dialog_data.get('product_id')
    await manager.start(BuyProduct.enter_amount,data={'product_id':product_id})