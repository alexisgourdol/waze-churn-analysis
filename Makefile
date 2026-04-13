.PHONY: lint clean

lint:
	uv run ruff check --fix notebooks/
	uv run ruff format notebooks/

clean:
	rm -rf .venv __pycache__
