

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

test:
	PYTHONPATH=ethtx pipenv run python -m pytest tests

test-all:
	PYTHONPATH=ethtx pipenv run python -m pytest .

setup:
	pipenv install --dev
	pipenv run pre-commit install

build: clean
	pipenv run python3 setup.py sdist bdist_wheel

clean:
	rm -rf ./dist

get_last_changelog_entry:
	@pipenv run python3 scripts/get_last_changelog_entry.py
