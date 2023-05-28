import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_create_orders_view(api_client):
    url = '/api/create_orders/'

    data = {
        "volume": 10000.0,
        "number": 5,
        "amountDif": 50.0,
        "side": "SELL",
        "priceMin": 200.0,
        "priceMax": 300.0
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == 201

    orders = response.data.get('orders')
    assert len(orders) == data['number']

    for order in orders:
        assert 'order_id' in order
        assert 'symbol' in order
        assert 'side' in order
        assert 'quantity' in order
        assert 'price' in order
