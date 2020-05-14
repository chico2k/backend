up-dev:
	docker-compose -f ./dev.yml up 

up-dev-b:
	docker-compose -f ./dev.yml up --build

el-create:
	docker-compose -f .\docker-compose.dev.yml run backend python manage.py search_index --create -f

el-rebuild:
	docker-compose -f .\docker-compose.dev.yml run backend python manage.py search_index --rebuild -f

el-pop:
	docker-compose -f .\docker-compose.dev.yml run backend python manage.py search_index --populate -f
	
django-superuser:
	docker-compose -f .\docker-compose.dev.yml run backend python manage.py createsuperuser

test-django:
	docker-compose -f ./docker-compose.dev.yml run backend pytest && flake8

test-data:
	docker-compose -f ./docker-compose.dev.yml run backend python manage.py testdata


