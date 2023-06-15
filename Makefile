.PHONY: all lint flake8 pylint

all:  lint

lint: flake8 pylint

flake8:
	flake8 bin/sanitize-annotations kconfig/run.py kconfig/annotations.py kconfig/version.py .

pylint:
	pylint bin/sanitize-annotations kconfig
