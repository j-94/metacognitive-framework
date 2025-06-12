.PHONY: init run test validate clean help install-deps check-env setup-env run-real add-domain analyze-budget delta-test delta-test-report delta-test-custom

# Default target
all: test

# Initialize environment
init: install-deps setup-env check-env
	@echo "✅ Environment initialized!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Set your OpenAI API key (optional):"
	@echo "     export OPENAI_API_KEY=sk-your-key-here"
	@echo "     # or edit .env file"
	@echo ""
	@echo "  2. Run the system:"
	@echo "     make run        # Mock mode"
	@echo "     make run-real   # Production mode"
	@echo ""
	@echo "  3. View results:"
	@echo "     open trace_latest.html"

# Set up environment files
setup-env:
	@if [ ! -f .env ]; then \
		echo "📄 Creating .env from template..."; \
		cp .env.example .env; \
		echo "✅ Created .env file - edit it to add your API key"; \
	else \
		echo "✅ .env file already exists"; \
	fi

# Install dependencies
install-deps:
	@echo "📦 Installing dependencies..."
	@pip install -q pytest || echo "⚠️  Failed to install pytest"
	@pip install -q openai || echo "⚠️  Failed to install openai"
	@echo "✅ Dependencies installed"

# Check environment
check-env:
	@echo "🔍 Checking environment..."
	@python3 -c "import sys; print(f'  Python: {sys.version.split()[0]}')"
	@python3 -c "import pytest; print(f'  pytest: {pytest.__version__}')" 2>/dev/null || echo "  pytest: not installed"
	@python3 -c "import openai; print(f'  openai: {openai.__version__}')" 2>/dev/null || echo "  openai: not installed"
	@if [ -n "$$OPENAI_API_KEY" ]; then echo "  API Key: ✅ Set"; else echo "  API Key: ❌ Not set"; fi

# Run donkey with default domain
run:
	@python3 donkey.py run

# Run production donkey with real components
run-real:
	@python3 donkey_real.py run --domain $(or $(DOMAIN),math)

# Run donkey with specific domain
run-math:
	@python3 donkey.py run --domain math

run-rag:
	@python3 donkey.py run --domain rag

# Run all tests
test:
	@python3 test_donkey_standalone.py

# Run tests with pytest
pytest:
	@python3 -m pytest -q test_donkey.py || echo "Note: Install pytest with 'pip install pytest' for better test output"

# Validate DSL files
validate:
	@python3 test_donkey.py validate 2>/dev/null || python3 -c "from test_donkey import validate_dsl; validate_dsl()"

# Clean up
clean:
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete

# Help
help:
	@echo "Donkey Bootstrap - Available targets:"
	@echo ""
	@echo "  Quick start:"
	@echo "    make init      - Initialize environment (run this first!)"
	@echo ""
	@echo "  Running:"
	@echo "    make run       - Run with mock adapter (demo)"
	@echo "    make run-real  - Run with production components"
	@echo "    make run-math  - Run with math domain"
	@echo "    make run-rag   - Run with RAG domain"
	@echo ""
	@echo "  Testing:"
	@echo "    make test      - Run all three milestone tests"
	@echo "    make pytest    - Run tests with pytest"
	@echo "    make validate  - Validate DSL files"
	@echo ""
	@echo "  Meta-Agent Commands:"
	@echo "    make add-domain DOMAIN=foo  - Create new domain scaffold"
	@echo "    make analyze-budget         - Analyze token usage across domains"
	@echo ""
	@echo "  Delta Testing:"
	@echo "    make delta-test             - Run default delta tests"
	@echo "    make delta-test-report      - Run tests and generate HTML report"
	@echo "    make delta-test-custom MUTATIONS='...' - Test specific mutations"
	@echo ""
	@echo "  Utilities:"
	@echo "    make check-env - Check environment status"
	@echo "    make clean     - Clean up Python cache files"
	@echo "    make help      - Show this help message"

# Meta-Agent Commands
add-domain:
	@if [ -z "$(DOMAIN)" ]; then \
		echo "❌ Error: DOMAIN not specified"; \
		echo "Usage: make add-domain DOMAIN=your_domain_name"; \
		exit 1; \
	fi
	@python3 donkey_meta_agent.py "/project:add_domain $(DOMAIN)"

analyze-budget:
	@python3 donkey_meta_agent.py "/project:analyze_budget $(DOMAIN)"

# Delta Testing
delta-test:
	@echo "🔬 Running Delta Test Framework..."
	@python3 delta_test_framework.py --tasks-file formal_tasks_set.json

delta-test-report:
	@echo "🔬 Running Delta Test with HTML Report..."
	@python3 delta_test_framework.py --tasks-file formal_tasks_set.json --report

delta-test-custom:
	@if [ -z "$(MUTATIONS)" ]; then \
		echo "❌ Error: MUTATIONS not specified"; \
		echo "Usage: make delta-test-custom MUTATIONS='adjust_recursion_depth modify_batch_size'"; \
		exit 1; \
	fi
	@python3 delta_test_framework.py --mutations $(MUTATIONS) --tasks-file formal_tasks_set.json