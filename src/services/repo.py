from dataclasses import dataclass


@dataclass
class Product:
    name: str
    product_id: int
    price: float
    stock: int

@dataclass
class Category:
    name: str
    category_id: int
    items: list[Product]

class Repo:
    categories: list[Category] = []

    def __init__(self,test_data:dict = None):
        for category in test_data.get('categories',[]):
            self.categories.append(Category(**category))

        for product in test_data.get('products',[]):
            category_name = product.pop('category')
            product = Product(**product)
            for category in self.categories:
                if category.name == category_name:
                    category.items.append(product)
                    break

    async def get_categories(self,session):
        return self.categories

    async def get_products(self,session,category_id):
        for category in self.categories:
            if category.category_id == category_id:
                return category.items
        return []

    async def get_product(self,session,product_id):
        for category in self.categories:
            for product in category.items:
                if product.product_id == product_id:
                    return product
        return None

    async def buy_product(self,session,product_id,quantity):
        for category in self.categories:
            for product in category.items:
                if product.product_id == product_id:
                    product.stock -= quantity
                    break