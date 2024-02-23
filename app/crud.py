from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Currency
import datetime

async def update_currency_rate(db: AsyncSession, currency_code: str, rate: float):
    async with db.begin():
        stmt = select(Currency).where(Currency.code == currency_code)
        result = await db.execute(stmt)
        currency = result.scalars().first()
        if currency:
            currency.rate = rate
        else:
            currency = Currency(code=currency_code, rate=rate)
            db.add(currency)
        currency.last_updated = datetime.datetime.utcnow()  # Assuming you have a last_updated field
        await db.commit()

