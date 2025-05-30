from aiogram.fsm.state import StatesGroup, State


class BotMenu(StatesGroup):
    select_categories = State()
    select_products = State()
    product_info = State()

class BuyProduct(StatesGroup):
    enter_amount = State()
    confirm = State()

class MySG(StatesGroup):
    main = State()