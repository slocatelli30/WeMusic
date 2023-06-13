SOURCE = wmapp

run:
	python manage.py runserver

lint:
	pylint --rcfile=./.pylintrc --load-plugins pylint_django --output-format=colorized $(SOURCE)/

coverage:
	coverage run --source='$(SOURCE)' manage.py test $(SOURCE)
	coverage html