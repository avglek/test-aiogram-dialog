from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Select, Button

from src.dialogs.bot_menu.states import BotMenu, BuyProduct
from src.misc.constants import SwitchToWindow
from src.services.repo import Repo


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

async def on_entered_amount(m: Message, widget:TextInput, manager:DialogManager,quantity:str):
    ctx = manager.current_context()

    if not quantity.isdigit():
        await m.answer('Please enter a number')
        return

    repo:Repo = manager.data.get('repo')
    quantity = int(quantity)
    product_id = ctx.start_data.get('product_id')
    session = manager.data.get('session')
    product_info = await repo.get_product_info(session,product_id)
    if product_info.stock < quantity:
        await m.answer('Not enough stock')
        return

    ctx.dialog_data.update(quantity=quantity)
    await manager.switch_to(BuyProduct.confirm)

async def on_confirm_buy(c: CallbackQuery, widget:Button, manager:DialogManager):
    ctx = manager.current_context()
    repo:Repo = manager.data.get('repo')
    session = manager.data.get('session')

    product_id = ctx.start_data.get('product_id')
    quantity = ctx.dialog_data.get('quantity')

    await repo.buy_product(session,product_id,quantity)
    product = await repo.get_product(session,product_id)
    await c.answer(f'You bought {quantity} {product.name}')
    await manager.done(
        result={
            'switch_to_window':SwitchToWindow.SelectProducts
        }
    )