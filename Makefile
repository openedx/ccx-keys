.DEFAULT_GOAL := test

.PHONY: html_coverage, quality, requirements

html_coverage:
	coverage html && open htmlcov/index.html

quality:
	pep8 --config=.pep8 ccx_keys
	pylint --rcfile=pylintrc ccx_keys

requirements:
	pip install -r requirements.txt

test:
	tox
