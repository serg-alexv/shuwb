.PHONY: validate test preview help

help:
	@echo "SHUWB Litigation Observatory — developer commands"
	@echo ""
	@echo "  make validate   Validate CSV data schemas (stdlib only, no extra deps)"
	@echo "  make test       Run all Python tests"
	@echo "  make preview    Serve dashboard locally at http://localhost:8000"

validate:
	python -m tests.validate_data

test:
	python -m tests.validate_data
	python -m unittest discover -s tests -p 'test_*.py' -v

preview:
	@echo "Serving dashboard at http://localhost:8000 …"
	python -m http.server 8000 --directory dashboard
