
SRC_DIR = ugh/
TEST_DIR = tests/

# Check for sytnax errors
compile:
	python -m compileall -f $(SRC_DIR) $(TEST_DIR)


# Run tests
test:
	coverage run -m unittest discover $(SRC_DIR)


# Show tests coverage
coverage: test
	coverage report -mi
