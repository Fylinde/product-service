from app.crud.product_crud import(
    get_product_details, 
    create_product, 
    delete_product, 
    get_products_by_category, 
    get_product_pricing, 
    update_product,
    get_products_by_type,
    get_products_by_brand,
)   
from tests.factories import ProductFactory
from app.schemas.product import ProductCreate
from app.models.product import ProductModel
from app.crud.product_rating import get_product_rating, add_product_rating, get_top_rated_products
from app.schemas.rating import RatingCreate
from app.crud.product_tags import(
    get_related_products, 
    get_all_tags,
    get_featured_products,
    get_products_by_tag,
    get_flash_deals,
    get_new_arrivals,
)
from datetime import datetime


def test_get_product_details(db):
    product = ProductFactory.create()
    db.add(product)
    db.commit()

    fetched_product = get_product_details(db, product.id)
    assert fetched_product is not None
    assert fetched_product.id == product.id
    assert fetched_product.name == product.name

def test_create_product(db_session):
    product_data = ProductCreate(
        name="Test Product",
        seller_price=100.0,
        seller_currency="USD",
        total_stock=50,
        is_in_stock=True
    )
    product = create_product(db_session, product_data)
    assert product.name == "Test Product"
    assert product.seller_price == 100.0

def test_delete_product(db_session, sample_product):
    product_id = sample_product.id
    result = delete_product(db_session, product_id)
    assert result is True
    assert db_session.query(ProductModel).filter(ProductModel.id == product_id).first() is None

def test_get_product_rating(db_session, sample_product, sample_ratings):
    product_id = sample_product.id
    result = get_product_rating(db_session, product_id)
    assert result["average"] > 0
    assert result["count"] == len(sample_ratings)

def test_add_product_rating(db_session, sample_product):
    product_id = sample_product.id
    rating_data = RatingCreate(rating=4.5, review="Excellent product!")
    rating = add_product_rating(db_session, product_id, rating_data)
    assert rating.product_id == product_id
    assert rating.rating == 4.5
    assert rating.review == "Excellent product!"


def test_get_products_by_category(db_session, sample_products):
    category_id = sample_products[0].category_id
    products = get_products_by_category(db_session, category_id, page=1, page_size=10)
    assert len(products) > 0
    assert all(product.category_id == category_id for product in products)

def test_get_related_products(db_session, sample_product, related_products):
    product_id = sample_product.id
    results = get_related_products(db_session, product_id, limit=5)
    assert len(results) > 0
    assert all(product.id != product_id for product in results)


def test_get_all_tags(db_session, sample_tags):
    tags = get_all_tags(db_session)
    assert len(tags) > 0
    assert "example-tag" in tags

def test_get_product_pricing(db_session, sample_product):
    product = get_product_pricing(db_session, sample_product.id)
    assert product is not None
    assert product.seller_price == sample_product.seller_price


def test_update_product(db_session, sample_product):
    product_id = sample_product.id
    update_data = {"name": "Updated Product", "seller_price": 200.0}
    updated_product = update_product(db_session, product_id, update_data)
    assert updated_product.name == "Updated Product"
    assert updated_product.seller_price == 200.0

def test_get_featured_products(db_session, sample_featured_products):
    featured_products = get_featured_products(db_session, limit=5)
    assert len(featured_products) <= 5
    assert all(product.is_featured for product in featured_products)

def test_get_products_by_type(db_session, sample_products):
    product_type = "electronics"
    products = get_products_by_type(db_session, product_type)
    assert len(products) > 0
    assert all(product.type == product_type for product in products)
def test_get_products_by_tag(db_session, sample_products_with_tags):
    tag = "electronics"
    products = get_products_by_tag(db_session, tag)
    assert len(products) > 0
    assert all(tag in [t.tag for t in product.tags] for product in products)

def test_get_flash_deals(db_session, sample_flash_deals):
    flash_deals = get_flash_deals(db_session)
    assert len(flash_deals) > 0
    assert all("flash-deal" in [tag.tag for tag in product.tags] for product in flash_deals)

def test_get_top_rated_products(db_session, sample_products_with_ratings):
    products = get_top_rated_products(db_session, limit=5)
    assert len(products) > 0
    assert sorted(products, key=lambda p: p.average_rating, reverse=True) == products

def test_get_new_arrivals(db_session, sample_products):
    new_arrivals = get_new_arrivals(db_session, limit=5)
    assert len(new_arrivals) > 0
    assert all(isinstance(product.created_at, datetime) for product in new_arrivals)

def test_get_products_by_brand(db_session, sample_products):
    brand = "Apple"
    products = get_products_by_brand(db_session, brand)
    assert len(products) > 0
    assert all(product.brand == brand for product in products)

