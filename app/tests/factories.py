import factory
from faker import Faker
from app.models.product import ProductModel
from app.database import BaseModel as Base

faker = Faker()

class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ProductModel
        sqlalchemy_session = Base.metadata.bind

    name = factory.LazyAttribute(lambda _: faker.name())
    description = factory.LazyAttribute(lambda _: faker.text())
    seller_price = factory.LazyAttribute(lambda _: faker.random_number(digits=5))
    seller_currency = "USD"
    is_in_stock = True
    total_stock = factory.LazyAttribute(lambda _: faker.random_number(digits=2))
