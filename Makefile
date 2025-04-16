.PHONY: lint
lint:
	cd frontend && npm run lint
	cd backend && make lint

.PHONY: run
run:
	cd frontend && npm run start

.PHONY: install
install:
	cd frontend && npm install
	cd backend && make install 