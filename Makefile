# 開発用コマンド集
up:
	docker-compose up -d

down:
	docker-compose down

lint:
	docker-compose exec api ruff check --fix

format:
	docker-compose exec api ruff format

migrate-generate:
	docker-compose exec api alembic revision --autogenerate -m "auto migration"

migrate-upgrade:
	docker-compose exec api alembic upgrade head
