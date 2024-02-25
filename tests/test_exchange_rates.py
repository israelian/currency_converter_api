import pytest
from app.main import app
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport


@pytest.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.mark.asyncio
async def test_update_rates_success():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/update-rates/")
        assert response.status_code == 200
        assert response.json() == {
            "message": "Exchange rates updated successfully."
        }


@pytest.mark.asyncio
async def test_convert_currency_success():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        source_currency = "USD"
        target_currency = "EUR"
        amount = 100
        response = await ac.get(
            f"/convert/?source={source_currency}&"
            f"target={target_currency}&amount={amount}"
        )
        assert response.status_code == 200
        response_json = response.json()
        assert "converted_amount" in response_json
        assert "last_updated" in response_json


@pytest.mark.asyncio
async def test_convert_currency_missing_codes():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        source_currency = "XXX"
        target_currency = "YYY"
        amount = 100
        response = await ac.get(
            f"/convert/?source={source_currency}&"
            f"target={target_currency}&amount={amount}"
        )
        assert response.status_code == 404
        assert response.json() == {
            "detail": "One or both currency codes not found."
            }


@pytest.mark.asyncio
async def test_get_last_update_success():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/last-update/")
        assert response.status_code == 200
        response_json = response.json()
        assert "last_update" in response_json
