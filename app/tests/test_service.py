from app.services.product_service import (
    fetch_product_details,
    create_new_product, 
    remove_product, 
    fetch_products_by_category, 
    get_localized_pricing, 
    update_existing_product,
    fetch_products_by_type,
    fetch_products_by_brand,
)
from app.schemas.product  import ProductCreate, ProductUpdate
from app.services.product_rating_service import fetch_product_rating, submit_product_rating, fetch_top_rated_products
from app.schemas.rating import RatingCreate
from app.services.tag_service import(
    fetch_related_products, 
    fetch_all_tags, 
    fetch_featured_products,
    fetch_products_by_tag,
    fetch_flash_deals,
    fetch_new_arrivals,
)
from datetime import datetime
from tests.factories import ProductFactory


def test_fetch_product_details(db):
    product = ProductFactory.create()
    db.add(product)
    db.commit()

    product_detail = fetch_product_details(db, product.id)
    assert product_detail.id == product.id
    assert product_detail.name == product.name

def test_create_new_product(db_session):
    product_data = ProductCreate(
        name="Test Product",
        seller_price=100.0,
        seller_currency="USD",
        total_stock=50,
        is_in_stock=True
    )
    product_detail = create_new_product(db_session, product_data)
    assert product_detail.name == "Test Product"
    assert product_detail.seller_price == 100.0

def test_remove_product(db_session, sample_product):
    product_id = sample_product.id
    result = remove_product(db_session, product_id)
    assert result is True

def test_fetch_product_rating(db_session, sample_product, sample_ratings):
    product_id = sample_product.id
    result = fetch_product_rating(db_session, product_id)
    assert result.average > 0
    assert result.count == len(sample_ratings)


def test_submit_product_rating(db_session, sample_product):
    product_id = sample_product.id
    rating_data = RatingCreate(rating=4.5, review="Great product!")
    rating_response = submit_product_rating(db_session, product_id, rating_data)
    assert rating_response.product_id == product_id
    assert rating_response.rating == 4.5
    assert rating_response.review == "Great product!"

def test_fetch_products_by_category(db_session, sample_products):
    category_id = sample_products[0].category_id
    response = fetch_products_by_category(db_session, category_id, page=1, page_size=10)
    assert response.total_count > 0
    assert all(product.category_id == category_id for product in response.products)

def test_fetch_related_products(db_session, sample_product, related_products):
    product_id = sample_product.id
    results = fetch_related_products(db_session, product_id, limit=5)
    assert len(results) > 0
    assert all(product.id != product_id for product in results)


def test_fetch_all_tags(db_session, sample_tags):
    tags = fetch_all_tags(db_session)
    assert len(tags) > 0
    assert "example-tag" in tags


def test_get_localized_pricing(db_session, sample_product, mock_currency_converter):
    buyer_currency = "EUR"
    localized_pricing = get_localized_pricing(db_session, sample_product.id, buyer_currency)
    assert localized_pricing.localized_price > 0
    assert localized_pricing.buyer_currency == "EUR"

def test_update_existing_product(db_session, sample_product):
    product_id = sample_product.id
    update_data = ProductUpdate(name="Updated Product", seller_price=200.0)
    updated_product = update_existing_product(db_session, product_id, update_data)
    assert updated_product.name == "Updated Product"
    assert updated_product.seller_price == 200.0

def test_fetch_featured_products(db_session, sample_featured_products):
    featured_products = fetch_featured_products(db_session, limit=5)
    assert len(featured_products) <= 5
    assert all(product.is_featured for product in featured_products)

def test_fetch_products_by_type(db_session, sample_products):
    product_type = "electronics"
    products = fetch_products_by_type(db_session, product_type)
    assert len(products) > 0
    assert all(product.type == product_type for product in products)

def test_fetch_products_by_tag(db_session, sample_products_with_tags):
    tag = "electronics"
    products = fetch_products_by_tag(db_session, tag)
    assert len(products) > 0
    assert all(tag in [t.tag for t in product.tags] for product in products)

def test_fetch_flash_deals(db_session, sample_flash_deals):
    flash_deals = fetch_flash_deals(db_session)
    assert len(flash_deals) > 0
    assert all("flash-deal" in [tag.tag for tag in product.tags] for product in flash_deals)

def test_fetch_top_rated_products(db_session, sample_products_with_ratings):
    products = fetch_top_rated_products(db_session, limit=5)
    assert len(products) > 0
    assert sorted(products, key=lambda p: p.average_rating, reverse=True) == products

def test_fetch_new_arrivals(db_session, sample_products):
    new_arrivals = fetch_new_arrivals(db_session, limit=5)
    assert len(new_arrivals) > 0
    assert all(isinstance(product.created_at, datetime) for product in new_arrivals)

def test_fetch_products_by_brand(db_session, sample_products):
    brand = "Apple"
    products = fetch_products_by_brand(db_session, brand)
    assert len(products) > 0
    assert all(product.brand == brand for product in products)
