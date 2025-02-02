import pytest
from unittest.mock import patch
from app.utils.currency_converter import convert_currency

# Test convert_currency function with mocked API response
@patch("app.utils.currency_converter.requests.get")
def test_convert_currency(mock_get):
    """
    Test currency conversion using a mocked external API response.
    """
    # Mock the API response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "rates": {"EUR": 0.85, "USD": 1.0},
        "base": "USD",
    }

    # Test conversion
    amount = 100
    from_currency = "USD"
    to_currency = "EUR"
    converted_amount = convert_currency(amount, from_currency, to_currency)

    # Assertions
    assert converted_amount == 85.0  # 100 USD -> 85 EUR (1 USD = 0.85 EUR)
    mock_get.assert_called_once_with("https://api.exchangerate-api.com/v4/latest/USD")

# Test case when the from_currency and to_currency are the same
def test_convert_currency_same_currency():
    """
    Test currency conversion when both currencies are the same.
    """
    amount = 100
    from_currency = "USD"
    to_currency = "USD"
    converted_amount = convert_currency(amount, from_currency, to_currency)

    # Assertions
    assert converted_amount == 100.0  # No conversion needed

# Test case for missing exchange rate
@patch("app.utils.currency_converter.requests.get")
def test_convert_currency_missing_rate(mock_get):
    """
    Test currency conversion when the target exchange rate is missing in the API response.
    """
    # Mock the API response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "rates": {"USD": 1.0},  # No rate for EUR
        "base": "USD",
    }

    # Test conversion
    amount = 100
    from_currency = "USD"
    to_currency = "EUR"

    with pytest.raises(ValueError, match="Exchange rate for EUR not found."):
        convert_currency(amount, from_currency, to_currency)

# Test case for failed API request
@patch("app.utils.currency_converter.requests.get")
def test_convert_currency_api_failure(mock_get):
    """
    Test currency conversion when the external API request fails.
    """
    # Mock a failed API response
    mock_get.return_value.status_code = 500

    amount = 100
    from_currency = "USD"
    to_currency = "EUR"

    with pytest.raises(ValueError, match="Failed to fetch exchange rates."):
        convert_currency(amount, from_currency, to_currency)
