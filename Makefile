.DEFAULT_GOAL := test

.PHONY: html_coverage quality requirements test upgrade

html_coverage:
	coverage html && open htmlcov/index.html

quality:
	tox -e quality

requirements: ## install development environment requirements
	pip install -qr requirements/pip-tools.txt
	pip-sync requirements/dev.txt requirements/private.*

test:
	tox

COMMON_CONSTRAINTS_TXT=requirements/common_constraints.txt
.PHONY: $(COMMON_CONSTRAINTS_TXT)
$(COMMON_CONSTRAINTS_TXT):
	wget -O "$(@)" https://raw.githubusercontent.com/edx/edx-lint/master/edx_lint/files/common_constraints.txt || touch "$(@)"

upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
upgrade: $(COMMON_CONSTRAINTS_TXT)  ## update the requirements/*.txt files with the latest packages satisfying requirements/*.in
	pip install -qr requirements/pip-tools.txt
	pip-compile --rebuild --upgrade -o requirements/pip-tools.txt requirements/pip-tools.in
	pip-compile --rebuild --upgrade -o requirements/base.txt requirements/base.in
	pip-compile --rebuild --upgrade -o requirements/test.txt requirements/test.in
	pip-compile --rebuild --upgrade -o requirements/ci.txt requirements/ci.in
	pip-compile --rebuild --upgrade -o requirements/dev.txt requirements/dev.in
