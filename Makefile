PY=python3

.PHONY: setup test spec-check

setup:
	@echo "Installing Python dependencies..."
	$(PY) -m pip install --upgrade pip
	@if [ -f requirements.txt ]; then \
		$(PY) -m pip install -r requirements.txt; \
	else \
		echo "No requirements.txt found, skipping."; \
	fi

test:
	@echo "Building Docker image and running tests inside container..."
	docker build -t chimera-test .
	docker run --rm chimera-test pytest -q

spec-check:
	@echo "Running spec checks..."
	bash scripts/spec_check.sh
