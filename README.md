# 🧠 MetaCognitive Framework: From Bootstrap DSL to Universal Reasoning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Experiments](https://img.shields.io/badge/experiments-4-green.svg)](./experiments)

## 🚀 The Journey: From DSL Bootstrap to MetaCognitive Framework

This repository contains the complete evolution from a simple DSL experiment runner (Donkey) to a universal framework for capturing, evolving, and teaching meta-cognitive reasoning.

### The Bootstrap Story

1. **Started with**: Donkey Bootstrap DSL - A simple experiment runner
2. **Asked**: "Can we capture how we think in DSL?"
3. **Discovered**: We can capture, evolve, and teach reasoning patterns
4. **Built**: A complete metacognitive framework with 83.3% success rate

## 📚 Understanding the Full System

### Phase 1: The Original Bootstrap (Donkey)

The journey began with a DSL-based experiment runner:

```dsl
# Original dsl.experiment_plan.dsl
dsl.experiment_plan {
  id: "donkey_first_principles_boot"
  description: "Minimal boot plan proving round‑trip guard, budget estimator and dual domains work."
  budget_tokens: 1000
  reasoning_style: "flat"
  domain_profile: "math"
}
```

This simple system could:
- Run experiments with token budgets
- Apply mutations to prompts
- Track results in traces

### Phase 2: The MetaCognitive Question

We asked: **"Can we build a language-driven framework that captures, evolves, and teaches meta-cognitive reasoning?"**

This led to 4 key experiments:

1. **Reasoning Trace Experiment**: Can we capture logical reasoning in DSL?
   - Result: ✅ 100% reconstruction fidelity
   - Mutation improved quality by 13.6%

2. **Prose Thinking Framework**: Can we generate multiple thinking styles?
   - Result: ✅ Different styles optimal for different problems
   - Test suites provide objective quality metrics

3. **Delta Testing System**: Can we measure impact of mutations?
   - Result: ✅ Statistical validation of improvements
   - CI/CD ready with automated testing

4. **Unified System**: Can we combine everything?
   - Result: ✅ 76.5% rigor + 90% adaptability

### Phase 3: The Complete Framework

The final system integrates everything:

```python
# The Unified Pipeline
system = UnifiedMetaCognitiveSystem()

# 1. CAPTURE - Multiple representations
captured = {
    "symbolic_trace": dsl_steps,
    "prose_thought": natural_language,
    "pattern_abstraction": category_theory,
    "validation_proofs": formal_verification
}

# 2. EVOLVE - Multiple strategies
evolved = {
    "dsl_mutations": beneficial_changes,
    "prose_hybrids": combined_styles,
    "discovered_patterns": emergent_abstractions,
    "transfer_potential": cross_domain_ability
}

# 3. TEACH - Knowledge transfer
teaching = {
    "dsl_curriculum": learn_from_traces,
    "prose_templates": thinking_styles,
    "pattern_library": reusable_abstractions,
    "validation_exercises": test_understanding
}
```

## 🛠️ Complete Installation & Bootstrap

### Step 1: Initial Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/metacognitive-framework.git
cd metacognitive-framework

# Run the bootstrap setup
chmod +x setup_repository.sh
./setup_repository.sh

# Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements_full.txt
```

### Step 2: Understanding the Evolution

```bash
# 1. Try the original Donkey DSL system
make run-real  # Original experiment runner

# 2. Run the reasoning trace experiment
python experiments/reasoning_trace/reasoning_trace_experiment.py

# 3. Try prose thinking
python experiments/prose_thinking/prose_thinking_framework.py

# 4. Test delta mutations
make delta-test

# 5. Run the complete unified system
python unified_metacognitive_framework.py
```

## 📋 CLAUDE.md Integration

To use this framework effectively with Claude, add this to your CLAUDE.md:

```markdown
## MetaCognitive Framework Integration

This project uses the MetaCognitive Framework for reasoning about problems.

### Core Concepts

1. **Multi-Representation Capture**: Every problem can be represented as:
   - DSL trace (symbolic steps)
   - Prose thought (natural language)
   - Pattern abstraction (mathematical structure)
   - Validation proof (formal verification)

2. **Evolution Through Testing**: 
   - Mutations are validated by test suites
   - Only beneficial changes are kept
   - Quality metrics guide evolution

3. **Teaching Through Examples**:
   - Successful patterns become templates
   - Knowledge transfers across domains
   - Curriculum emerges from practice

### When to Use Each Representation

- **DSL Traces**: For step-by-step logical reasoning
- **Prose Thoughts**: For exploring multiple approaches
- **Pattern Abstractions**: For finding general principles
- **Validation Proofs**: For ensuring correctness

### Adding New Reasoning Paths

1. Create in `paths/your_path/`
2. Implement capture(), evolve(), validate(), teach()
3. Register with system
4. Test with multiple problems

### Key Commands

- `make run-real` - Run original DSL experiments
- `make delta-test` - Test reasoning mutations
- `python unified_metacognitive_framework.py` - Full system
```

## 🎯 The Bootstrap Philosophy

This framework embodies a key insight: **Complex reasoning systems can bootstrap from simple DSL experiments**.

### The Bootstrap Sequence:

1. **Start Simple**: Basic DSL runner (Donkey)
2. **Ask Big Questions**: Can we capture thinking itself?
3. **Experiment Rigorously**: Test each hypothesis
4. **Integrate Discoveries**: Build unified framework
5. **Enable Extension**: Make it easy to add new paths

### What Makes This Special:

- **Self-Improving**: The system can improve its own reasoning
- **Multi-Modal**: Combines symbolic and neural approaches
- **Teachable**: Transfers knowledge to new domains
- **Measurable**: Objective metrics for thinking quality

## 🏗️ Repository Structure Explained

```
metacognitive-framework/
├── 📁 Original Bootstrap Files
│   ├── dsl.experiment_plan.dsl      # Original Donkey DSL
│   ├── donkey_real.py               # Original runner
│   └── tasks/                       # Original task definitions
│
├── 🧪 Evolution Experiments
│   ├── reasoning_trace/             # Can we capture reasoning?
│   ├── prose_thinking/              # Multiple thinking styles?
│   ├── delta_testing/               # Measure improvements?
│   └── unified_system/              # Combine everything?
│
├── 🧠 Final Framework
│   ├── core/                        # Base classes
│   ├── paths/                       # Reasoning paths
│   └── unified_metacognitive_framework.py
│
└── 📚 Documentation
    ├── README.md                    # This file
    ├── CLAUDE.md                    # Integration guide
    └── CONTRIBUTING.md              # How to extend
```

## 🌟 Key Insights from the Journey

1. **DSL Can Capture Reasoning**: We proved reasoning can be represented in structured format
2. **Evolution Works**: Mutations with validation improve reasoning quality
3. **Multiple Representations Help**: Different problems benefit from different approaches
4. **Teaching Emerges Naturally**: Successful patterns become curriculum
5. **Rigor + Adaptability**: We achieved both (76.5% + 90%)

## 🎓 Adding New Paths (Complete Example)

Here's how to add a new reasoning path, using AI Tutor as an example:

```python
# paths/ai_tutor/ai_tutor_path.py
from core.base import MetaCognitivePath

class AITutorPath(MetaCognitivePath):
    """Maps student thinking in latent space"""
    
    def capture_student_state(self, response):
        """Find student's position in concept space"""
        # Map response to latent space
        embedding = self.embed_response(response)
        # Find nearest concepts
        concepts = self.find_nearest_concepts(embedding)
        return {"embedding": embedding, "concepts": concepts}
    
    def find_local_maximum(self, current_position):
        """Find optimal learning target"""
        # Compute gradient toward understanding
        gradient = self.compute_improvement_gradient(current_position)
        # Find reachable targets
        targets = self.find_reachable_maxima(current_position, gradient)
        # Select based on Zone of Proximal Development
        return self.select_optimal_target(targets)
```

## 🚀 Quick Start Examples

### Example 1: Capture Reasoning
```python
from experiments.reasoning_trace import DSLTraceCapture

capturer = DSLTraceCapture(recursion_depth=5)
trace = capturer.capture_reasoning(problem)
print(f"Captured {len(trace['steps'])} reasoning steps")
```

### Example 2: Test Multiple Thinking Styles
```python
from experiments.prose_thinking import ProseThinkingEngine

engine = ProseThinkingEngine()
for style in ["recursive", "pattern", "constraint"]:
    thought = engine.generate_prose_thoughts(problem, style)
    quality = validator.validate_thinking(thought)
    print(f"{style}: {quality['thinking_quality']:.2%}")
```

### Example 3: Evolve Better Reasoning
```python
from experiments.delta_testing import DeltaTestOrchestrator

orchestrator = DeltaTestOrchestrator()
results = orchestrator.run_delta_test(
    mutations=["increase_depth", "add_verification"],
    tasks=formal_tasks
)
print(f"Best mutation: {results['summary']['best_mutation']}")
```

## 📈 Performance Metrics

The complete system achieves:
- **Symbolic Rigor**: 76.5% (formal verification passes)
- **Neural Adaptability**: 90.0% (cross-domain transfer)
- **Combined Score**: 83.3% (both rigor AND flexibility)
- **Improvement Rate**: 13.6% through evolution

## 🤝 Contributing

We welcome contributions! The framework is designed for extension:

1. **New Paths**: Add reasoning approaches in `paths/`
2. **New Domains**: Add problem types in `domains/`
3. **New Experiments**: Test hypotheses in `experiments/`
4. **Better Evolution**: Improve mutation strategies

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

This framework emerged from a simple question about DSL experiment runners and evolved into a complete reasoning system. Special thanks to the insight that complex systems can bootstrap from simple beginnings.

---

<p align="center">
  <strong>From Bootstrap DSL to Universal Reasoning - The Future of AI is Evolutionary!</strong>
</p>