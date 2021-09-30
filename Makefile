MIGRATION_MESSAGE ?= "initial"

server:
	@cd src && uvicorn app.main:api --host 0.0.0.0 --port 8000 --reload
migration:
	@cd src && aerich migrate --name ${MIGRATION_MESSAGE}
migrate:
	@cd src && aerich upgrade
checks:
	@pre-commit run --all
	@pytest --cov=src
shell:
	@cd src && ipython
git-hook:
	@pre-commit install -t pre-commit -t pre-push
