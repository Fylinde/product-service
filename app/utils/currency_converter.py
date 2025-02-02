import requests

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Convert an amount from one currency to another.
    For simplicity, use a free currency conversion API.
    """
    if from_currency == to_currency:
        return amount  # No conversion needed
    
    # Replace with a real API endpoint
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Failed to fetch exchange rates.")
    
    rates = response.json().get("rates", {})
    conversion_rate = rates.get(to_currency)
    if not conversion_rate:
        raise ValueError(f"Exchange rate for {to_currency} not found.")
    
    return round(amount * conversion_rate, 2)
