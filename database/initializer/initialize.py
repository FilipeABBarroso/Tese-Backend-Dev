from os import walk
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://fb:root@localhost:3306/test', echo=True)

def create_async_engine():
  return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@asynccontextmanager
async def get_session():
  try:
    async_session = create_async_engine()
    async with async_session() as session:
      yield session
  except:
    await session.rollback()
    raise
  finally:
    await session.close()
