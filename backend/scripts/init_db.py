from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from data.models import Base
from config import settings

DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL)

# Перед созданием таблиц, нужно активировать расширение для векторов!
with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()

# Создаем все таблицы, которые мы описали в models.py
Base.metadata.create_all(bind=engine)

print("База данных и таблицы успешно созданы!")