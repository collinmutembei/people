MIGRATION_MESSAGE ?= "initial"

server:
	@cd src && uvicorn app.main:api --host 0.0.0.0 --port 8000 --reload
checks:
	@pre-commit run --all
env:
	@cp .env.example .env
shell:
	@cd src && ipython
git-hook:
	@pre-commit install -t pre-commit -t pre-push
