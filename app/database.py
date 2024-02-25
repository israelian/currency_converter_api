import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    poolclass=NullPool,
)

AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
