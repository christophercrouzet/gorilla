clean:
	@find . \( \
		-type d -name "__pycache__" \
		-or -type d -name ".tox" \
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
	@python -m coverage run --branch --source gorilla \
		-m unittest discover -s tests
	@coverage report
	@coverage html

dist:
	@python setup.py bdist_wheel sdist

doc:
	@$(MAKE) -C doc html

env:
	virtualenv env

test:
	@python -m unittest discover -s tests -v

upload:
	@twine upload dist/*

.PHONY: clean coverage dist doc env test upload
