import pytest
from httpx import AsyncClient
from app.main import app
from app.database import get_async_session
from unittest.mock import AsyncMock


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def override_get_async_session():
    async def _override_dependency():
        async with get_async_session() as session:
            yield session
    app.dependency_overrides[get_async_session] = _override_dependency
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def clear_database():
    async with get_async_session() as session:
        await session.execute(
            "TRUNCATE TABLE currencies RESTART IDENTITY CASCADE"
        )
        await session.commit()


@pytest.fixture
def mock_fetch_exchange_rates(monkeypatch):
    async def mock(*args, **kwargs):
        return {"rates": {"USD": 1.0, "EUR": 0.9}}
    monkeypatch.setattr(
        "app.utils.fetch_exchange_rates", AsyncMock(side_effect=mock)
    )


@pytest.mark.asyncio
async def test_update_rates_success(client, mock_fetch_exchange_rates):
    response = await client.post("/update-rates/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Exchange rates updated successfully."
    }


@pytest.mark.asyncio
async def test_convert_currency_success(client, override_get_async_session):
    async with get_async_session() as session:
        await session.execute(
            "INSERT INTO currencies (code, rate) "
            "VALUES ('USD', 1.0), ('EUR', 0.9)"
        )
        await session.commit()

    response = await client.get("/convert/?source=USD&target=EUR&amount=100")
    assert response.status_code == 200
    assert "converted_amount" in response.json()


@pytest.mark.asyncio
async def test_convert_currency_not_found(client):
    response = await client.get("/convert/?source=XXX&target=YYY&amount=100")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_last_update_success(client, override_get_async_session):
    async with get_async_session() as session:
        await session.execute(
            "INSERT INTO currencies (code, rate, last_updated) "
            "VALUES ('USD', 1.0, NOW())"
        )
        await session.commit()
    response = await client.get("/last-update/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_last_update_no_rates(client):
    response = await client.get("/last-update/")
    assert response.status_code == 404
