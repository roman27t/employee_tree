import os


class Config:
    PORT = int(os.environ.get('PORT', 8000))
    DEBUG = bool(os.environ.get('DEBUG', False))
    DB_URL = os.environ.get('DB_URL', 'postgresql+asyncpg://postgres:1111111@pg_db/db_name')


i_config = Config()
