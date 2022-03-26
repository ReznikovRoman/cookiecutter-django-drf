include makefile.env
export

# TODO:
# 1. Add local configuration (settings/local.py)
# 2. Refactor .env file (add missing variables, remove redundant ones)
# 3. Change docs
# 4. Test project

REQUIREMENTS_DIR := requirements
{% if cookiecutter.use_black == 'y' -%}
BLACK_RUN_ARGS := --generate-hashes --no-header --verbose
{%- endif %}
PIP_COMPILE_ARGS := --generate-hashes --no-header --no-emit-index-url --verbose
PIP_COMPILE := cd $(REQUIREMENTS_DIR) && pip-compile $(PIP_COMPILE_ARGS)

.PHONY: fix
fix:
	isort .

.PHONY: lint
lint:
	ec
	flake8
	isort -qc .

.PHONY: compile-requirements
compile-requirements:
	pip install -U pip-tools
	$(PIP_COMPILE) requirements.in
	$(PIP_COMPILE) requirements.dev.in
	$(PIP_COMPILE) requirements.test.in
	$(PIP_COMPILE) requirements.lint.in
	test -f $(REQUIREMENTS_DIR)/requirements.local.in && $(PIP_COMPILE) requirements.local.in || exit 0

.PHONY: sync-requirements
sync-requirements:
	pip install -U pip-tools
	cd $(REQUIREMENTS_DIR) && pip-sync requirements.txt requirements.*.txt

{% if cookiecutter.use_black == 'y' -%}
.PHONY: black
black:
	black . --check --line-length 120 --extend-exclude migrations

.PHONY: black-reformat
black-reformat:
	black $(BLACK_RUN_ARGS) $(ARGS)
{%- endif %}

.DEFAULT_GOAL :=
