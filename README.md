Старт    
   ```bash
   docker-compose up --build
   ``` 

Run tests:
   ```bash
   docker-compose -f docker-compose-test.yml up --build 
   docker-compose -f docker-compose-test.yml run app-test pytest -s -v
   ```

### Web
http://localhost:8000/

### Swagger
http://localhost:8000/api/doc/

### PgAdmin
http://localhost:5050/

### Миграции
   ```bash
   docker-compose exec app sh
   
   alembic init -t async migrations # инит
   alembic revision  --autogenerate -m "Add model" - созд. миграции
   alembic upgrade head # применение
   alembic downgrade 8ac14e223d1  # понижение
   alembic downgrade base  # This command will undo all migrations
   ```
