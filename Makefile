.PHONY: lint clean report report_with_code executive_summary

lint:
	uv run ruff check --fix notebooks/
	uv run ruff format notebooks/

clean:
	rm -rf .venv __pycache__

# Generate slides (HTML + PPTX) and executive summary from the EDA notebook.
# Requires ANTHROPIC_API_KEY for the executive summary step.
# Safe ways to provide the key:
#   1. export ANTHROPIC_API_KEY=sk-ant-... && make report   (ephemeral, recommended)
#   2. echo 'ANTHROPIC_API_KEY=sk-ant-...' > .env && make report  (.env is gitignored)
report:
	@[ -f .env ] && set -a && . ./.env && set +a; \
	uv run --with anthropic --with python-pptx \
		python /workspace/tools/generate_report.py \
		--notebook notebooks/eda.ipynb \
		--output-dir reports/ \
		--format all

report_with_code:
	@[ -f .env ] && set -a && . ./.env && set +a; \
	uv run --with anthropic --with python-pptx \
		python /workspace/tools/generate_report.py \
		--notebook notebooks/eda.ipynb \
		--output-dir reports/ \
		--format all \
		--with-code

# Generate only the executive summary (skips slides). Requires ANTHROPIC_API_KEY.
executive_summary:
	@[ -f .env ] && set -a && . ./.env && set +a; \
	uv run --with anthropic \
		python /workspace/tools/generate_report.py \
		--notebook notebooks/eda.ipynb \
		--output-dir reports/ \
		--format summary
