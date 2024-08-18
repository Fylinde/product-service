# Product Service

## Overview

The Product Service is a crucial component of our microservices architecture, responsible for managing product data and related operations. This service provides functionalities to create, read, update, and delete products, as well as list all available products.

## Features

- **List Products**: Retrieve a list of all available products.
- **Create Product**: Create a new product with specified details such as name, description, and price.
- **Get Product**: Retrieve details of a specific product by its ID.
- **Update Product**: Update the details of an existing product, including name, description, and price.
- **Delete Product**: Remove a product from the system by its ID.

## Purpose

The Product Service is designed to manage the lifecycle of product data within the application. It serves as the central point for all product-related operations, ensuring that the product catalog is up-to-date and accessible to other services and the frontend.

## Usage

This service will be used by the frontend application and other services to manage product data. It allows the application to interact with the product catalog, providing users with the ability to view, add, update, and remove products.

## Endpoints Overview

For a detailed list of available endpoints, including request and response formats, please refer to the [API Documentation](./API_DOCS.md).

## Technologies

- **REST API**: The service exposes a RESTful API for interaction with other services and clients.

## Setup and Configuration

To set up the Product Service, follow these steps:

1. **Clone the repository**:  
   ```bash
   git clone https://github.com/your-org/product-service.git
