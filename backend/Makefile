pip_freeze:
	pip freeze > requirements.txt

setup_dev_db:
	createdb nfp_boilerplate_dev
	createuser nfp_boilerplate_user -P

init_alembic:
	alembic init alembic

run_migrations:
	alembic upgrade head --sql

run_dev_db:
	psql nfp_boilerplate_dev

dev_server:
	uvicorn main:app --reload