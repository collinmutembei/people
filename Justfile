serve:
	@cd src && uvicorn app.main:api --host 0.0.0.0 --port 8000 --reload
check:
	@pre-commit run --all
make-env:
	@cp .env.example .env
shell:
	@cd src && ipython
setup-precommit:
	@pre-commit install -t pre-commit -t pre-push
