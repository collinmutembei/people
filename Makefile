MIGRATION_MESSAGE ?= "init"

server:
	@cd src && uvicorn app.api:api --host 0.0.0.0 --port 8000 --reload
migration:
	@cd src && alembic revision --autogenerate -m ${MIGRATION_MESSAGE}
migrate:
	@cd src && alembic upgrade head
checks:
	@pre-commit run --all
	@pytest --cov=src
