from aiogram_dialog import Window, Data, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Back, Button
from aiogram_dialog.widgets.text import Const, Format

from src.dialogs.bot_menu import keyboards, selected, states, getters
from src.misc.constants import SwitchToWindow


def categories_window():
    return Window(
        Const('Choose category that you want to see'),
        keyboards.paginated_categories(selected.on_chosen_category),
        Cancel(Const('Exit')),
        state=states.BotMenu.select_categories,
        getter=getters.get_categories
    )

def products_window():
    return Window(
        Const('Choose product that you want to see'),
        keyboards.paginated_products(selected.on_chosen_product),
        Back(Const('<< Select another category')),
        state=states.BotMenu.select_products,
        getter=getters.get_products
    )

def product_info_window():
    return Window(
        Format('''
        Product: {product.name}
        Price: {product.price}
        In Stock: {product.stock} pcs
        '''),
        Button(
            Const('Buy'),
            id='b_buy_product',
            on_click=selected.on_buy_product,

        ),
        Back(Const('<< Select another product')),
        state=states.BotMenu.product_info,
        getter=getters.get_product_info
    )

def buy_product_window():
    return Window(
        Format('''How many {product.name} do you want to buy?
        in stock: {product.stock} pcs'''),
        TextInput(
            id='enter_amount',
            on_success=selected.on_entered_amount,
        ),
        Cancel(Const('Cancel')),
        Cancel(
            Const('<< Select another product'),
            id='cancel_s_t_select_pr',
            result={'switch_to': SwitchToWindow.SelectProducts}
        ),
        state=states.BuyProduct.enter_amount,
        getter=getters.get_by_product
    )

def confirm_buy_window():
    return Window(
        Format('''
        You are going to buy {quantity} {product.name} for {total_amount}$
        Are you sure?
        '''),
        Button(
            Const('Yes'),
            id='b_confirm_buy',
            on_click=selected.on_confirm_buy,
        ),
        Back(Const('<< Change amount')),
        Cancel(
            Const('<< Select another product'),
            id='cancel_s_t_select_pr',
            result={'switch_to': SwitchToWindow.SelectProducts},
        ),
        state=states.BuyProduct.confirm,
        getter=getters.get_by_product,
    )

async def on_process_result(data:Data, result:dict, manager:DialogManager):
    if result:
        switch_to_window = result.get('switch_to_window')
        if switch_to_window == SwitchToWindow.SelectProducts:
            await manager.switch_to( states.BotMenu.select_products)