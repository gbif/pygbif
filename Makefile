all: build install

.PHONY: build install

build:
	python setup.py build

install:
	python setup.py install
