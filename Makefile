python3 = /usr/bin/python3

.PHONY: all

test:
	for f in *.py;  do echo '\nTesting '$$f; $(python3) $$f; done

install:
