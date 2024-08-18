
### `API_DOCS.md`

```markdown
Product Service API Documentation

Overview
API documentation for the Product Service, which manages product data and related operations.

Version: 1.0.0
API Specification: OpenAPI 3.1

Endpoints

Product Management Endpoints

List Products
- URL: /products/
- Method: GET
- Summary: Retrieve a list of all available products.
- Response:
  - 200 Successful Response:
    {
      "type": "array",
      "items": {
        "$ref": "#/components/schemas/Product"
      }
    }

Create Product
- URL: /products/
- Method: POST
- Summary: Create a new product.
- Request Body:
  {
    "$ref": "#/components/schemas/ProductCreate"
  }
- Response:
  - 201 Successful Response:
    {
      "$ref": "#/components/schemas/Product"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Get Product
- URL: /products/{product_id}
- Method: GET
- Summary: Retrieve details of a specific product by its ID.
- Parameters:
  - product_id (integer): The ID of the product.
- Response:
  - 200 Successful Response:
    {
      "$ref": "#/components/schemas/Product"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Update Product
- URL: /products/{product_id}
- Method: PUT
- Summary: Update the details of an existing product.
- Parameters:
  - product_id (integer): The ID of the product to update.
- Request Body:
  {
    "$ref": "#/components/schemas/ProductUpdate"
  }
- Response:
  - 200 Successful Response:
    {
      "$ref": "#/components/schemas/Product"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Delete Product
- URL: /products/{product_id}
- Method: DELETE
- Summary: Remove a product from the system by its ID.
- Parameters:
  - product_id (integer): The ID of the product to delete.
- Response:
  - 200 Successful Response
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Miscellaneous Endpoints

Read Root
- URL: /
- Method: GET
- Summary: Root endpoint.
- Response:
  - 200 Successful Response:
    {}
