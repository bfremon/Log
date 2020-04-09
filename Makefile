python3 = /usr/bin/python3
rm = /bin/rm -fr
pip = /usr/local/bin/pip

test:
	$(python3) -m unittest discover

pip: README.md setup.py .VERSION LICENCE Log/__init__.py 
	$(python3) ./setup.py --set-build
	$(pip) install .

clean:
	$(rm) __pycache__ Log/__pycache__  Log/tests/__pycache__

.PHONY: pip clean test
