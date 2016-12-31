clean:
	@find . \( \
		-type d -name "__pycache__" \
		-or -type d -name "htmlcov" \
	\) -exec rm -rf {} +
	@find . \( \
		-type f -name "*.pyc" \
		-or -type f -name "*.pyo" \
		-or -type f -name "*.coverage" \
		-or -type f -name "*.lprof" \
	\) -delete
	@rm -rf *.egg-info
	@rm -rf build
	@rm -rf dist
	@rm -rf doc/_build/*

coverage:
	@python -m coverage run --branch --source gorilla tests/run.py
	@coverage report
	@coverage html

dist:
	@python setup.py bdist_wheel sdist

doc:
	@$(MAKE) -C doc html

env:
	virtualenv env

test.py2:
	@python tests/run.py

test.py3:
	@python3 tests/run.py

test: test.py2 test.py3

upload:
	@twine upload dist/*

.PHONY: clean coverage dist doc test test.py2 test.py3 upload
