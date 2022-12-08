
### Шаги запуска
1. Старт    
   ```bash
   docker-compose up --build
    ``` 
2. После успешного запуска необходимо - install extension for DB:
    ```bash
   docker-compose exec pg_db sh
   psql -U postgres --dbname=postgres
   ```
и далее
   ```sql
   CREATE EXTENSION IF NOT EXISTS ltree;
   ```
3.migrate:
   ```bash
   docker-compose exec app sh
   alembic upgrade head
   ```
Run tests:
   ```bash
   docker-compose exec pg_db sh
   psql -U postgres --dbname=postgres
   CREATE DATABASE postgres_test;
   ```
   ```bash
   docker-compose exec app sh
   pytest tests -v -s
   ```


### Описание АПИ
1. Отсортированное дерево сотрудников: GET /staff/
2. Получение конкретного сотрудника: GET /staff/id/
3. Добавление сотрудника : POST /staff/
   ```json
   {
      "last_name": "Ivanov", 
      "first_name": "Roman", 
      "parent_id": 1, 
      "wage_rate": 99777.01, 
      "position_id": 2,
      "birthdate": "2000-12-22"
   }
   ```
4. Редактирование сотрудника: PATCH /staff/id/
   ```json
   {
      "last_name": "Petrov", 
      "position_id": 3
   }
   ```
5. Наполнение БД (тестовое): GET /system/init_data/


### Миграции
   ```bash
   docker-compose exec app sh
   
   alembic init -t async migrations # инит
   alembic revision  --autogenerate -m "Add model" - созд. миграции
   alembic upgrade head # применение
   alembic downgrade 8ac14e223d1  # понижение
   alembic downgrade base  # This command will undo all migrations
   ```
