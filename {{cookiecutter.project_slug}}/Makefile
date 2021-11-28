include makefile.env
export

PIP_COMPILE_ARGS := --generate-hashes --no-header --verbose
BLACK_RUN_ARGS := --generate-hashes --no-header --verbose

.PHONY: compile-requirements
compile-requirements:
	pip-compile $(PIP_COMPILE_ARGS) requirements.in
	test -f requirements.local.in && pip-compile $(PIP_COMPILE_ARGS) requirements.local.in || exit 0
	test -f requirements.linter.in && pip-compile $(PIP_COMPILE_ARGS) requirements.linter.in || exit 0

.PHONY: sync-requirements
sync-requirements:
	pip install pip-tools
	pip-sync requirements.txt requirements.*.txt

.PHONY: check
check:
	ec
	flake8
	isort -qc .

.PHONY: check-docker
check-docker:
	docker-compose -f $(DOCKER_COMPOSE_FILENAME) run --rm server sh -c "ec && flake8 && isort -qc ."

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
