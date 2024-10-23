import pytest
import asyncio

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@pytest.fixture
def mock_requests(mocker):
    mocker.patch("tests.test_dashboard.client.get", return_value={
        "hotel_id": 1,
        "bookings_count": 1,
        "cancellations_count": 0
    })


def test_get_dashboard(mock_requests):
    response = client.get("/dashboard?hotel_id=1&period=2024-01-01&filter_by=month")
    
    assert isinstance(response, dict)
    assert response["hotel_id"] == 1
    assert response["bookings_count"] == 1
    assert response["cancellations_count"] == 0
    