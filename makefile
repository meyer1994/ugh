
SRC_DIR = ugh/
TEST_DIR = tests/

# Check for sytnax errors
compile:
	python -m compileall -f $(SRC_DIR) $(TEST_DIR)


# Run tests
test:
	coverage run --source=$(SRC_DIR) -m unittest discover -vb $(TEST_DIR)


# Show tests coverage
coverage: test
	coverage report -mi


# Lint code
lint:
	flake8 ugh/ tests/ --statistics
