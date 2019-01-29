.PHONY: clean

init:
	pip install -e .[dev] .

clean: ## remove all build, test, coverage and Python artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .pytest_cache/
	rm -fr app.egg-info/
	find app -name '*_ui.py' -exec rm -f {} +
	find app -name '*_rc.py' -exec rm -f {} +

lint: ## check style with flake8
	flake8 app tests

test: ## run tests quickly with the default Python
	py.test

coverage: ## check code coverage
	pytest --cov=app tests/

build:
	python setup.py build_res

install: clean ## install the package to the active Python's site-packages
	python setup.py install
