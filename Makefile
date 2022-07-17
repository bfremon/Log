sudo = /usr/bin/sudo
apt_install = /usr/bin/apt-get install
python3 = /usr/bin/python3
rm = /bin/rm -fr
pip = /usr/bin/pip3

packages = python3-pip

test:
	if [ -x tmp ]; then rm -fr tmp; fi
	if [ -x test_dbg.py ]; then rm -f test_dbg.py; fi
	if [ -x test_log.py ]; then rm -f test_log.py; fi
	if [ -x test_err.py ]; then rm -f test_err.py; fi
	if [ -x test_warn.py ]; then rm -f test_warn.py; fi
	$(python3) -m unittest discover

pip: README.md setup.py .VERSION LICENCE Log/__init__.py pre
	$(python3) ./setup.py --set-build
	$(pip) install .

clean:
	$(rm) __pycache__ Log/__pycache__  Log/tests/__pycache__

pre:
	$(sudo) $(apt_install) python3-pip

.PHONY: pip clean test
