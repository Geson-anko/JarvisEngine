FILE=. 

.PHONY: tests
tests:
	poetry run isort ${FILE}
	poetry run black ${FILE}
	poetry run mypy ${FILE}
	poetry run pflake8 ${FILE}
	poetry run pytest ./tests

	