run-backend:
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

run-dashboard:
	python dashboard/main.py

lint:
	flake8 backend dashboard

format:
	black backend dashboard

test:
	pytest test/ 