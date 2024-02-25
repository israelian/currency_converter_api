import os
from sqlalchemy import func
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_async_session
from . import crud, models
from sqlalchemy.future import select
from .utils import fetch_exchange_rates
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Logic before app starts (e.g., database initialization)
    await models.async_init_db()
    yield


app = FastAPI(lifespan=lifespan)


EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/update-rates/")
async def update_rates(db: AsyncSession = Depends(get_async_session)):
    rates = await fetch_exchange_rates(EXCHANGE_API_KEY)
    if rates.get("rates"):
        for code, rate in rates["rates"].items():
            await crud.update_currency_rate(db, code, rate)
        return {"message": "Exchange rates updated successfully."}
    raise HTTPException(
        status_code=400, detail="Failed to fetch exchange rates."
    )


@app.get("/convert/")
async def convert_currency(
    source: str,
    target: str,
    amount: float,
    db: AsyncSession = Depends(get_async_session)
):
    async with db as session:
        async with session.begin():
            query = select(models.Currency).where(
                models.Currency.code.in_([source, target])
            )
            result = await session.execute(query)
            currencies = result.scalars().all()

            if len(currencies) != 2:
                raise HTTPException(
                    status_code=404,
                    detail="One or both currency codes not found."
                )

            source_rate = next(
                (c.rate for c in currencies if c.code == source), None
            )
            target_rate = next(
                (c.rate for c in currencies if c.code == target), None
            )
            last_updated_time = next(
                (c.last_updated for c in currencies), None
            )
            if source_rate is None or target_rate is None:
                raise HTTPException(
                    status_code=404,
                    detail="Currency conversion rate not found."
                )

            converted_amount = (amount / source_rate) * target_rate
            return {
                "converted_amount": converted_amount,
                "last_updated": last_updated_time
            }


@app.get("/last-update/")
async def get_last_update(db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        async with session.begin():
            query = select(func.max(models.Currency.last_updated))
            result = await session.execute(query)
            last_update = result.scalar_one_or_none()

            if last_update is None:
                raise HTTPException(
                    status_code=404, detail="No currency rates found."
                )

            return {"last_update": last_update}
