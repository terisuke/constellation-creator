.PHONY: lint
lint:
	flake8 .

.PHONY: run
run:
	source venv/bin/activate && python -m uvicorn app.main:app --reload

.PHONY: install
install:
	source venv/bin/activate && pip install -r requirements.txt 