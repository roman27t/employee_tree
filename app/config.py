# import os
#
#
# class Config:
#     HOST = os.environ.get('HOST', 'localhost')
#     PORT = int(os.environ.get('PORT', 8000))
#     DEBUG = bool(os.environ.get('DEBUG', False))
#     POSTGRES_USER = os.environ.get('POSTGRES_USER', 'user')
#     POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'user')
#     POSTGRES_DB = os.environ.get('POSTGRES_DB', 'db_name')
#     DB_URL = os.environ.get('DB_URL', 'postgresql+asyncpg://postgres:postgres@pg_db/db_name')
#
#     @property
#     def BASE_URL(self):
#         return f'http://{self.HOST}:{self.PORT}'
#
#
# config = Config()
