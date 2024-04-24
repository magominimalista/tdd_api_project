run:
	@uvicorn store.main:app --reload

precomit-install:
	@poetry run pre-commit install