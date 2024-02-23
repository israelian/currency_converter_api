import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

SQLALCHEMY_DATABASE_URL = os.environ['DATABASE_URL']

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True,
)

AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session