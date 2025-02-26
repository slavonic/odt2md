.PHONY := all clean build test

all: wheel

test:
	python -m pytest odt2md/test

wheel: test
	pip wheel -w dist --no-deps .

clean:
	rm -rf dist