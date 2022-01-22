include makefile.env
export

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
	$(PIP_COMPILE) requirements.linter.in
	test -f $(REQUIREMENTS_DIR)/requirements.local.in && $(PIP_COMPILE) requirements.local.in || exit 0

.PHONY: sync-requirements
sync-requirements:
	pip install -U pip-tools
	cd $(REQUIREMENTS_DIR) && pip-sync requirements.txt requirements.*.txt

{% if cookiecutter.use_black == 'y' -%}
.PHONY: black
black:
	black . --check --line-length 120 --extend-exclude migrations

.PHONY: black-docker
black-docker:
	docker-compose -f $(DOCKER_COMPOSE_FILENAME) run --rm server sh -c "black . --check $(BLACK_RUN_ARGS)}"

.PHONY: black-reformat
black-reformat:
	black $(BLACK_RUN_ARGS) $(ARGS)

.PHONY: black-reformat-docker
black-reformat-docker:
	docker-compose -f $(DOCKER_COMPOSE_FILENAME) run --rm server sh -c "black $(BLACK_RUN_ARGS) $(ARGS)"
{%- endif %}

.DEFAULT_GOAL :=
