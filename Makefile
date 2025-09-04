# バックグラウンドタスクワーカー起動
process-tasks:
	docker-compose exec api python manage.py process_tasks
up:
	docker compose up -d

down:
	docker compose down

lint:
	ruff check .

format:
	ruff format .

makemigrations:
	docker compose exec api python manage.py makemigrations

migrate:
	docker compose exec api python manage.py migrate

createsuperuser:
	docker compose exec api python manage.py createsuperuser