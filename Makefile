MIGRATION_MESSAGE ?= "initial"

server:
	@cd src && uvicorn app.main:api --host 0.0.0.0 --port 8000 --reload
migration:
	@cd src && aerich migrate --name ${MIGRATION_MESSAGE}
migrate:
	@cd src && aerich upgrade
checks:
	@pre-commit run --all
	# @pytest --cov=src
env:
	@cp .env.example .env
shell:
	@cd src && ipython
db-shell:
	@cd src && TORTOISE_ORM=app.settings.orm.TORTOISE_ORM tortoise-cli shell
git-hook:
	@pre-commit install -t pre-commit -t pre-push
reset-migrations:
	@cd src && rm -rf aerich.ini migrations && aerich init -t app.settings.orm.TORTOISE_ORM && aerich init-db
