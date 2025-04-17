.PHONY: lint
lint:
	cd frontend && npm run lint
	cd backend && make lint

.PHONY: run
run:
	cd frontend && npm install && npm run start

.PHONY: install
install:
	cd frontend && npm install
	cd backend && make install

.PHONY: setup
setup:
	cd backend && python3.11 -m venv venv
	cd backend && . venv/bin/activate && pip install --upgrade pip && make install
	cd frontend && npm install

.PHONY: clean
clean:
	cd frontend && rm -rf node_modules
	cd backend && rm -rf venv 