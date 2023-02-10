.PHONY: all lint flake8 pylint

all:  lint

lint: flake8 pylint

flake8:
	flake8 annotations .

pylint:
	pylint annotations kconfig
