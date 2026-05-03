import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

DATABASE_URL = os.getenv("METAAUTH_DB_URL", "sqlite+aiosqlite:///db/metaauth.db")

enable_echo = os.getenv("SQLALCHEMY_ECHO", "0") == "1"

enable_future = True

engine = create_async_engine(
    DATABASE_URL,
    echo=enable_echo,
    poolclass=NullPool,
    future=enable_future,
)

AsyncSessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
