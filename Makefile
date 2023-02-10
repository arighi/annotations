.PHONY: all lint

all:  lint

lint:
	flake8 annotations .
