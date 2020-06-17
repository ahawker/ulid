.DEFAULT_GOAL := help

.PHONY: changelog
changelog:  ## Build CHANGELOG.md from git/github metadata. Assumes 'CHANGELOG_GITHUB_TOKEN in env.
	@github_changelog_generator -u ahawker -p ulid

.PHONY: test-install
test-install:  ## Install dependencies required for local test execution.
	@pip install -q -r requirements/test.txt

.PHONY: test
test: test-install  ## Run test suite.
	@py.test -v --ignore tests/benchmarks tests

.PHONY: benchmark
benchmark: test-install  ## Run performance suite.
	@py.test -v tests/benchmarks

.PHONY: scan
scan: test-install  ## Run security scan.
	@safety check

.PHONY: tox-install
tox-install:  ## Install dependencies required for local test execution using tox.
	@pip install -q -r requirements/tox.txt

.PHONY: tox
tox: tox-install  ## Run test suite using tox.
	@tox

.PHONY: travis-install
travis-install:  ## Install dependencies for travis-ci.org integration.
	@pip install -q -r requirements/travis.txt

.PHONY: travis-before-script
travis-before-script: travis-install  ## Entry point for travis-ci.org 'before_script' execution.
	@curl -s https://codecov.io/bash > ./codecov
	@chmod +x ./codecov

.PHONY: travis-script
travis-script: travis-install tox  ## Entry point for travis-ci.org execution.

.PHONY: travis-after-success
travis-after-success:  ## Entry point for travis-ci.org 'after_success' execution.
	@./codecov -e TOX_ENV

.PHONY: codeclimate
codeclimate:  ## Run codeclimate analysis.
	@docker run \
		--interactive --tty --rm \
		--env CODECLIMATE_CODE="$(shell pwd)" \
		--volume "$(shell pwd)":/code \
		--volume /var/run/docker.sock:/var/run/docker.sock \
		--volume /tmp/cc:/tmp/cc \
		codeclimate/codeclimate analyze

.PHONY: isort
isort:  ## Run isort on the package.
	@isort --recursive --check-only ulid tests

.PHONY: mypy
mypy:  ## Run mypy static analysis checks on the package.
	@mypy ulid --strict

.PHONY: pylint
pylint:  ## Run pylint on the package.
	@pylint --rcfile .pylintrc ulid

.PHONY: seclint
seclint:  ## Run bandit on the package.
	@bandit -v -r ulid

.PHONY: lint
lint:  pylint mypy seclint isort  ## Run mypy and pylint on the package.

.PHONY: bump-patch
bump-patch:  ## Bump package patch version, e.g. 0.0.1 -> 0.0.2.
	@bumpversion patch

.PHONY: bump-minor
bump-minor:  ## Bump package minor version, e.g. 0.1.0 -> 0.2.0.
	@bumpversion minor

.PHONY: bump-major
bump-major:  ## Bump package major version, e.g. 1.0.0 -> 2.0.0.
	@bumpversion major

.PHONY: git-push-with-tags
git-push-with-tags:  ## Push latest changes to remote with tags.
	@git push
	@git push --tags

.PHONY: push-patch
push-patch: bump-patch git-push-with-tags  ## Bump package patch version and push changes to remote.

.PHONY: push-minor
push-minor: bump-minor git-push-with-tags  ## Bump package minor version and push changes to remote.

.PHONY: push-major
push-major: bump-major git-push-with-tags  ## Bump package major version and push changes to remote.

.PHONY: clean-pyc
clean-pyc:  ## Remove local python cache files.
	@find . -name '__pycache__' -type d -exec rm -r {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

.PHONY: docs
docs:  ## Build project documentation.
	@make -C docs html

.phony: help
help: ## Print Makefile usage.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
