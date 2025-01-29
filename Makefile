activate:
	source venv/bin/activate

serve:
	docker compose up --build

develop:
	python3 manage.py runserver
