from aiogram_dialog import DialogManager

from src.dialogs.bot_menu.states import BotMenu


async def get_categories(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('session')
    repo:Repo = middleware_data.get('repo')
    db_categories = await repo.get_categories(session)

    data = {
        'categories': [
            (f'{category.name} ({len(category.items)})', category.category_id)
            for category in db_categories
        ]
    }

    return data

async def get_products(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('session')
    repo:Repo = middleware_data.get('repo')
    ctx = dialog_manager.current_context()
    category_id = ctx.dialog_data.get('category_id')
    if not category_id:
        await dialog_manager.event.answer('Please, select category first')
        await dialog_manager.switch_to(BotMenu.select_categories)
        return

    category_id = int(category_id)
    db_products = await repo.get_products(session, category_id)

    data = {
        'products': db_products
    }

    return data

async def get_product_info(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    product_id = ctx.dialog_data.get('product_id')
    if not product_id:
        await dialog_manager.event.answer('Please, select product first')
        await dialog_manager.switch_to(BotMenu.select_products)
        return

    session = middleware_data.get('session')
    repo:Repo = middleware_data.get('repo')
    product = await repo.get_product(session, product_id)

    data = {
        'product': product
    }

    return data

async def get_by_product(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    product_id = ctx.start_data.get('product_id')
    session = middleware_data.get('session')
    repo:Repo = middleware_data.get('repo')
    product = await repo.get_product(session, product_id)
    quantity = ctx.start_data.get('quantity')

    data = {
        'product': product,
        'quantity': quantity,
        'total_amount': quantity * product.price if quantity else None
    }
    return data