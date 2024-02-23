import httpx


async def fetch_exchange_rates(api_key: str) -> dict:
    url = f"http://api.exchangeratesapi.io/v1/latest?access_key={api_key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
