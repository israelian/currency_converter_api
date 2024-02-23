import os
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func


Base = declarative_base()


class Currency(Base):
    __tablename__ = "currencies"

    code = Column(String, primary_key=True)
    name = Column(String)
    rate = Column(Float)
    last_updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def async_init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
