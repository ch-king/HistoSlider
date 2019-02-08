.PHONY: clean

SOURCE_DIR = histoslider

init:
	pip install -e .[dev] .

clean: ## remove all build, test, coverage and Python artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .pytest_cache/
	rm -fr histoslider.egg-info/
	find $(SOURCE_DIR) -name '*.ui.py' -exec rm -f {} +
	find $(SOURCE_DIR) -name '*_rc.py' -exec rm -f {} +

lint: ## check style with flake8
	flake8 $(SOURCE_DIR) tests

test: ## run tests quickly with the default Python
	py.test

coverage: ## check code coverage
	pytest --cov=$(SOURCE_DIR) tests/

build_resources:
	pyrcc5 ./resources/resources.qrc -o $(SOURCE_DIR)/resources_rc.py

UI_FILES := $(shell find $(SOURCE_DIR) -name "*.ui")
build_ui:
	@for file in $(UI_FILES) ; do \
      	pyuic5 $$file -o "$(basename $$file .ui)_ui.py" ; \
    done
#	$(shell find $(SOURCE_DIR) -name "*.ui" -exec sh -c 'pyuic5 "{}" -o "$(basename "{}" .ui)_ui.py"' \;)
#	find $(SOURCE_DIR) -name "*.ui" -exec sh -c 'echo {} | sed -r "s/(.+)/\1/"' \;
build: build_resources build_ui

install: clean ## install the package to the active Python's site-packages
	python setup.py install
