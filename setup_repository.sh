#!/bin/bash
# Setup script for MetaCognitive Framework repository

echo "🧠 Setting up MetaCognitive Framework Repository"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "unified_metacognitive_framework.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p core/{capture,evolution,validation,teaching}
mkdir -p experiments/{reasoning_trace,prose_thinking,delta_testing,unified_system}
mkdir -p domains/{math,logic,rag}
mkdir -p paths/{template,ai_tutor}
mkdir -p tools
mkdir -p tests
mkdir -p docs
mkdir -p benchmarks

# Move existing files to proper locations
echo "📦 Organizing existing files..."

# Move experiment files
[ -f "reasoning_trace_experiment.py" ] && mv reasoning_trace_experiment.py experiments/reasoning_trace/
[ -f "prose_thinking_framework.py" ] && mv prose_thinking_framework.py experiments/prose_thinking/
[ -f "delta_test_framework.py" ] && mv delta_test_framework.py experiments/delta_testing/
[ -f "unified_metacognitive_framework.py" ] && cp unified_metacognitive_framework.py experiments/unified_system/

# Move results
[ -f "reasoning_trace_experiment_results.json" ] && mv reasoning_trace_experiment_results.json experiments/reasoning_trace/
[ -f "prose_thinking_results.json" ] && mv prose_thinking_results.json experiments/prose_thinking/
[ -f "unified_metacognitive_results.json" ] && mv unified_metacognitive_results.json experiments/unified_system/

# Move visualizations
[ -f "trace_visualization.html" ] && mv trace_visualization.html experiments/reasoning_trace/
[ -f "prose_thinking_visualization.html" ] && mv prose_thinking_visualization.html experiments/prose_thinking/
[ -f "ultimate_answer_visualization.html" ] && mv ultimate_answer_visualization.html docs/

# Create core base module
echo "🔧 Creating core modules..."
cat > core/__init__.py << 'EOF'
"""
MetaCognitive Framework Core
"""
from .base import MetaCognitivePath, MetaCognitiveSystem

__version__ = "1.0.0"
__all__ = ["MetaCognitivePath", "MetaCognitiveSystem"]
EOF

cat > core/base.py << 'EOF'
"""
Base classes for MetaCognitive Framework
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any

class MetaCognitivePath(ABC):
    """Base class for all metacognitive reasoning paths"""
    
    def __init__(self, name: str):
        self.name = name
        self.metrics = {}
        
    @abstractmethod
    def capture(self, input_data: Any) -> Dict[str, Any]:
        """Capture reasoning in this path's representation"""
        pass
        
    @abstractmethod
    def evolve(self, captured_data: Dict[str, Any], 
               validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Evolve the reasoning approach"""
        pass
        
    @abstractmethod
    def validate(self, reasoning: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the reasoning quality"""
        pass
        
    @abstractmethod
    def teach(self, validated_reasoning: Dict[str, Any]) -> Dict[str, Any]:
        """Create teaching materials"""
        pass

class MetaCognitiveSystem:
    """Main system for managing paths"""
    
    def __init__(self):
        self.paths = {}
        
    def register_path(self, name: str, path: MetaCognitivePath):
        """Register a new reasoning path"""
        self.paths[name] = path
        
    def process(self, input_data: Any, path_name: str) -> Dict[str, Any]:
        """Process input through a specific path"""
        if path_name not in self.paths:
            raise ValueError(f"Unknown path: {path_name}")
            
        path = self.paths[path_name]
        
        # Full pipeline
        captured = path.capture(input_data)
        validated = path.validate(captured)
        evolved = path.evolve(captured, validated)
        teaching = path.teach(evolved)
        
        return {
            "captured": captured,
            "validated": validated,
            "evolved": evolved,
            "teaching": teaching
        }
EOF

# Create path template
echo "📝 Creating path template..."
cat > paths/template/README.md << 'EOF'
# Path Template

This is a template for creating new metacognitive reasoning paths.

## Structure

1. Copy this template directory to `paths/your_path_name/`
2. Rename `template_path.py` to `your_path_name.py`
3. Update the class name and implementation
4. Create tests in `tests/test_your_path_name.py`

## Files

- `__init__.py` - Path registration
- `your_path_name.py` - Main implementation
- `config.yaml` - Configuration
- `README.md` - Documentation
- `example.py` - Usage examples
EOF

# Create LICENSE
echo "📄 Creating LICENSE..."
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 MetaCognitive Framework Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Create .gitignore
echo "🚫 Creating .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.mypy_cache/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
trace_*.html
mutation_observer_log.json
*_results.json
.env

# Documentation
docs/_build/
docs/_static/
docs/_templates/
EOF

# Initialize Git repository
if [ ! -d ".git" ]; then
    echo "📂 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: MetaCognitive Framework"
else
    echo "✅ Git repository already initialized"
fi

# Create example usage script
echo "📚 Creating example usage..."
cat > example_usage.py << 'EOF'
"""
Example usage of MetaCognitive Framework
"""
from core.base import MetaCognitiveSystem
from experiments.unified_system.unified_metacognitive_framework import UnifiedMetaCognitiveSystem

def main():
    # Create system
    system = UnifiedMetaCognitiveSystem()
    
    # Example problem
    problem = {
        "type": "logical_inference",
        "premise": "All birds can fly",
        "fact": "Penguins are birds",
        "conclusion": "Penguins can fly"
    }
    
    # Process through system
    result = system.process_problem(problem)
    
    # Display results
    print("MetaCognitive Framework Demo")
    print("=" * 40)
    print(f"Problem: {problem['premise']} + {problem['fact']} → {problem['conclusion']}")
    print(f"Rigor Score: {result['achievement_metrics']['rigor']:.1%}")
    print(f"Adaptability: {result['achievement_metrics']['adaptability']:.1%}")
    print(f"Combined: {result['achievement_metrics']['combined']:.1%}")

if __name__ == "__main__":
    main()
EOF

# Final message
echo ""
echo "✅ Repository structure created successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Review and update README_METACOGNITIVE.md → README.md"
echo "2. Add your GitHub remote: git remote add origin https://github.com/yourusername/metacognitive-framework.git"
echo "3. Install dependencies: pip install -r requirements_full.txt"
echo "4. Run tests: pytest tests/"
echo "5. Try the example: python example_usage.py"
echo ""
echo "🚀 Ready to publish to GitHub!"
EOF

chmod +x setup_repository.sh