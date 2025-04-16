.PHONY: lint
lint:
	flake8 .

.PHONY: run
run:
	. venv/bin/activate && python -m uvicorn app.main:app --reload

.PHONY: install
install:
	. venv/bin/activate && pip install -r requirements.txt   