.PHONY: all lint flake8 pylint

all:  lint

lint: flake8 pylint

flake8:
	flake8 sanitize-annotations annotations .

pylint:
	pylint sanitize-annotations annotations kconfig
