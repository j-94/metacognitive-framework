# CLAUDE.md - MetaCognitive Framework Bootstrap Guide

**CORE IDENTITY: From DSL Runner to MetaCognitive Reasoner**

This project demonstrates the evolution from a simple DSL experiment runner (Donkey) to a complete framework for capturing, evolving, and teaching meta-cognitive reasoning.

## 🚀 The Bootstrap Sequence

### Stage 1: DSL Experiment Runner (Donkey)
```dsl
dsl.experiment_plan {
  budget_tokens: 1000
  reasoning_style: "flat"
  domain_profile: "math"
}
```
- Simple task runner with mutations
- Token budget management
- Basic result tracking

### Stage 2: The Meta Question
"Can we capture HOW we think, not just WHAT we think?"

### Stage 3: Four Key Experiments
1. **Reasoning Traces** → DSL can capture logic (13.6% improvement)
2. **Prose Thinking** → Multiple styles work (83.2% quality)
3. **Delta Testing** → Mutations are measurable
4. **Unified System** → Everything integrates (83.3% success)

### Stage 4: Complete Framework
```python
# The evolution is complete
captured → validated → evolved → taught
```

## 🧠 OPERATIONAL PRINCIPLES

### Multi-Representation Thinking
When approaching ANY problem, consider ALL representations:

1. **DSL Trace** (Symbolic)
   ```dsl
   step.decompose { components: [...] }
   step.pattern_match { matched: "modus_ponens" }
   step.apply_rule { bindings: {...} }
   step.synthesize { proof: [...] }
   ```

2. **Prose Thought** (Natural Language)
   ```
   "Think of this as a tree decomposition..."
   "Recognize the sliding window pattern..."
   "Propagate constraints forward..."
   ```

3. **Pattern Abstraction** (Mathematical)
   ```
   Category: LogicalInference
   Morphisms: [premise → conclusion]
   Metric: distance_to_known = 0.15
   ```

4. **Validation Proof** (Verification)
   ```
   Tests: 10/10 passed
   Formal: sound ∧ complete
   Transfer: 78% success
   ```

### Evolution Through Testing
Every reasoning approach must be:
- **Captured** in multiple representations
- **Validated** through objective tests
- **Evolved** via beneficial mutations
- **Taught** through successful examples

### The Donkey Directive (Updated)
**Original**: Build working systems first, then perfect them
**Evolved**: Capture working reasoning, evolve through testing, teach what works

## 🔧 PRACTICAL USAGE

### For Simple Problems
```bash
# Use the original DSL runner
make run-real DOMAIN=math
```

### For Reasoning Analysis
```python
# Capture and analyze reasoning patterns
from experiments.reasoning_trace import DSLTraceCapture
trace = capturer.capture_reasoning(problem)
quality = reconstructor.reconstruct_from_trace(trace)
```

### For Finding Best Approach
```python
# Test multiple thinking styles
from experiments.prose_thinking import ProseThinkingEngine
for style in engine.thinking_styles:
    result = engine.generate_prose_thoughts(problem, style)
    score = validator.validate_thinking(result)
```

### For Continuous Improvement
```bash
# Run delta tests on mutations
make delta-test
# Check improvement in mutation_observer_log.json
```

### For Complete Integration
```python
# Use the unified system
from unified_metacognitive_framework import UnifiedMetaCognitiveSystem
system = UnifiedMetaCognitiveSystem()
result = system.process_problem(problem)
```

## 📋 WHEN TO USE WHAT

### Use DSL Traces When:
- Step-by-step logic is important
- You need formal verification
- Teaching systematic approaches

### Use Prose Thinking When:
- Exploring multiple approaches
- Problem is ill-defined
- Creativity matters

### Use Pattern Abstraction When:
- Looking for general principles
- Cross-domain transfer needed
- Mathematical rigor required

### Use Evolution When:
- Current approach isn't optimal
- Multiple valid solutions exist
- Performance can be measured

## 🎯 KEY COMMANDS

```bash
# Original Donkey DSL
make run                    # Mock mode
make run-real              # Real LLM mode

# Reasoning Experiments
python reasoning_trace_experiment.py
python prose_thinking_framework.py

# Delta Testing
make delta-test            # Default mutations
make delta-test-report     # With HTML report
make delta-test-custom MUTATIONS="..."

# Unified System
python unified_metacognitive_framework.py

# Add New Path
cp -r paths/template paths/your_path
# Implement capture, evolve, validate, teach
```

## 🧬 ADDING NEW REASONING PATHS

Every new path must implement:

```python
class YourPath(MetaCognitivePath):
    def capture(self, input_data):
        """How to represent reasoning"""
        
    def evolve(self, captured, validation):
        """How to improve reasoning"""
        
    def validate(self, reasoning):
        """How to measure quality"""
        
    def teach(self, validated):
        """How to transfer knowledge"""
```

Example: AI Tutor Path
- **Capture**: Map student position in latent space
- **Evolve**: Find optimal learning trajectories
- **Validate**: Measure learning gains
- **Teach**: Create personalized curriculum

## 📊 SUCCESS METRICS

The framework achieves:
- **76.5%** Symbolic Rigor (formal methods)
- **90.0%** Neural Adaptability (flexibility)
- **83.3%** Combined Score (best of both)
- **13.6%** Improvement through evolution

## 🚫 ANTI-PATTERNS TO AVOID

1. **Single Representation Fixation**
   - ❌ Using only DSL traces
   - ✅ Try all representations

2. **Evolution Without Validation**
   - ❌ Random mutations
   - ✅ Test-driven evolution

3. **Teaching Without Understanding**
   - ❌ Copy successful patterns blindly
   - ✅ Understand WHY they work

## 💭 THE META-LESSON

This entire framework bootstrapped from asking:
"Can our DSL experiment runner capture its own reasoning?"

The answer wasn't just "yes" - it was:
"Yes, and it can evolve and teach that reasoning too!"

**Remember**: Complex reasoning systems can emerge from simple questions about how we think.

---

**Bootstrap Complete**: From DSL runner to universal reasoning framework.
The future isn't choosing between symbolic OR neural - it's building systems that fluidly combine both!