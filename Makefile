setup:
python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt

lint:
ruff check .

format:
black .

lint-fix: format lint

test:
pytest
