# 開発用コマンド集
up:
	docker-compose up -d

down:
	docker-compose down

lint:
	docker-compose run --rm api ruff check app

format:
	docker-compose run --rm api ruff format app

migrate-generate:
	docker-compose run --rm api alembic revision --autogenerate -m "auto migration"

migrate-upgrade:
	docker-compose run --rm api alembic upgrade head
