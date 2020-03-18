.DEFAULT_GOAL := test

.PHONY: html_coverage quality requirements test upgrade

html_coverage:
	coverage html && open htmlcov/index.html

quality:
	pycodestyle --config=.pep8 ccx_keys
	pylint --rcfile=pylintrc ccx_keys

requirements: ## install development environment requirements
	pip install -qr requirements/pip-tools.txt
	pip-sync requirements/dev.txt requirements/private.*

test:
	tox

upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
upgrade: ## update the requirements/*.txt files with the latest packages satisfying requirements/*.in
	pip install -qr requirements/pip-tools.txt
	pip-compile --rebuild --upgrade -o requirements/pip-tools.txt requirements/pip-tools.in
	pip-compile --rebuild --upgrade -o requirements/base.txt requirements/base.in
	pip-compile --rebuild --upgrade -o requirements/test.txt requirements/test.in
	pip-compile --rebuild --upgrade -o requirements/travis.txt requirements/travis.in
	pip-compile --rebuild --upgrade -o requirements/dev.txt requirements/dev.in
