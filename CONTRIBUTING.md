# Contributing to MetaCognitive Framework

Thank you for your interest in contributing to the MetaCognitive Framework! This document provides guidelines for contributing new paths, improvements, and experiments.

## 🎯 Quick Start

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-path`)
3. Make your changes
4. Run tests (`make test`)
5. Commit your changes (`git commit -m 'Add amazing path'`)
6. Push to the branch (`git push origin feature/amazing-path`)
7. Open a Pull Request

## 📝 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Celebrate diverse thinking styles

## 🏗️ Adding a New Path

### 1. Path Structure

Every new path should follow this structure:

```
paths/your_path_name/
├── __init__.py              # Path registration
├── your_path_name.py        # Main implementation
├── config.yaml              # Configuration
├── README.md                # Path documentation
├── example.py               # Usage examples
├── capture/                 # Capture strategies
│   └── __init__.py
├── evolution/               # Evolution methods
│   └── __init__.py
├── validation/              # Validation logic
│   └── __init__.py
└── teaching/                # Teaching materials
    └── __init__.py
```

### 2. Path Implementation

Your path must inherit from `MetaCognitivePath`:

```python
from core.base import MetaCognitivePath

class YourPath(MetaCognitivePath):
    def __init__(self):
        super().__init__("your_path_name")
        
    def capture(self, input_data):
        """Capture reasoning in your representation"""
        pass
        
    def evolve(self, captured_data, validation_results):
        """Evolve the reasoning approach"""
        pass
        
    def validate(self, reasoning):
        """Validate the reasoning quality"""
        pass
        
    def teach(self, validated_reasoning):
        """Create teaching materials"""
        pass
```

### 3. Testing Requirements

Create comprehensive tests in `tests/test_your_path.py`:

```python
import pytest
from paths.your_path_name import YourPath

class TestYourPath:
    def test_capture(self):
        """Test capture functionality"""
        path = YourPath()
        result = path.capture(test_input)
        assert result is not None
        
    def test_evolution(self):
        """Test evolution strategies"""
        # Add evolution tests
        
    def test_validation(self):
        """Test validation metrics"""
        # Add validation tests
        
    def test_teaching(self):
        """Test teaching generation"""
        # Add teaching tests
```

### 4. Documentation

Include a README.md for your path:

```markdown
# Your Path Name

## Overview
Brief description of what your path does and why it's useful.

## Key Features
- Feature 1
- Feature 2
- Feature 3

## Usage Example
```python
# Show basic usage
```

## Configuration
Explain configuration options in config.yaml

## Theory
Brief explanation of the underlying theory/approach
```

## 🧪 Testing Guidelines

### Running Tests

```bash
# Run all tests
make test

# Run specific path tests
pytest tests/test_your_path.py -v

# Run with coverage
pytest --cov=paths/your_path_name tests/test_your_path.py
```

### Test Coverage Requirements

- Minimum 80% code coverage
- All public methods must have tests
- Include edge cases and error handling
- Test cross-path compatibility if applicable

## 📊 Performance Guidelines

### Benchmarking

Add benchmarks for your path:

```python
# benchmarks/bench_your_path.py
import time
from paths.your_path_name import YourPath

def benchmark_capture():
    path = YourPath()
    start = time.time()
    # Run capture operation
    elapsed = time.time() - start
    print(f"Capture time: {elapsed:.3f}s")
```

### Performance Targets

- Capture: < 1 second for standard input
- Evolution: < 10 seconds per generation
- Validation: < 0.5 seconds per item
- Teaching generation: < 5 seconds

## 🎨 Style Guide

### Python Style

We follow PEP 8 with these additions:

- Use type hints for all functions
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to all public methods

### Example:

```python
from typing import Dict, List, Any

def process_reasoning(
    input_data: Dict[str, Any],
    strategy: str = "default"
) -> Dict[str, Any]:
    """
    Process reasoning with specified strategy.
    
    Args:
        input_data: Input reasoning data
        strategy: Processing strategy to use
        
    Returns:
        Processed reasoning output
    """
    # Implementation
    pass
```

## 🔄 Pull Request Process

### Before Submitting

1. **Update documentation** - Add/update relevant docs
2. **Add tests** - Ensure comprehensive test coverage
3. **Run linters** - `make lint` should pass
4. **Update CHANGELOG.md** - Add your changes
5. **Check examples** - Ensure examples still work

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New path
- [ ] Bug fix
- [ ] Performance improvement
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Coverage maintained/improved

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Examples updated
```

## 🌟 Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation

## 💬 Getting Help

- **Discord**: [Join our community](https://discord.gg/metacognitive)
- **Discussions**: Use GitHub Discussions for questions
- **Issues**: Report bugs via GitHub Issues

## 🚀 Advanced Contributions

### Core Framework Changes

Changes to core framework require:
- RFC (Request for Comments) discussion
- Performance impact analysis
- Backward compatibility consideration
- Approval from 2+ maintainers

### New Experiments

To add an experiment:
1. Create in `experiments/your_experiment/`
2. Include hypothesis and methodology
3. Document results comprehensively
4. Add to experiments index

## 📅 Release Process

We use semantic versioning:
- **MAJOR**: Breaking changes
- **MINOR**: New features/paths
- **PATCH**: Bug fixes

Thank you for contributing to the future of AI reasoning! 🎉