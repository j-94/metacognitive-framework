# 💪 Donkey Experiment Bootstrap (Phase 1–5)

This document defines a structured experiment plan to test the Donkey Meta-Agent with full DSL policy integration, recursion, and adaptation cycles.

---

## ✅ Phase 1: Initialization (User Input Required)

**1. Choose Your Target Domain:**
_Select what kind of problem the agent will tackle:_
- Code generation
- Math proofs
- Retrieval-Augmented QA
- Legal reasoning
- Other (please specify)

**2. Define Your Evaluation Metric:**
_How do you measure success?_ ✅
- Accuracy
- Novelty
- Speed (time-to-answer)
- DSL graph coverage

**3. Agent Reasoning Style:**
_Choose how deep the agent should think_
- [ ] Flat reasoning (1-pass)
- [ ] Reflexive (recurses up to 3 layers)

**4. Tools Required:**
_Tick any DSL modules or external capabilities needed:_
- [ ] DSL static analyzer
- [ ] Token logger + reward tracker
- [ ] API integration (external tools)
- [ ] Simulator / stub executor

> ✏️ Once filled, the system will auto-generate your `dsl.experiment_plan`, `policy_graph`, and `run_config`.

---

## ⚙️ Phase 2: System Setup

Once configured, the system creates these DSL modules:
- `dsl.experiment_plan {}` – task design and loop structure
- `dsl.policy_graph {}` – reasoning modes and allowed paths
- `dsl.meta_policy {}` – high-level agent control
- `dsl.execution_plan {}` – main runner loop

Includes:
- Budget/time/tokens
- Reasoning style (CoT, ReAct, RAG)
- Mutation every 2–3 tasks
- Optional: `dsl.temporal_model {}` for decay rules
- UI: `dsl.interface_graph {}` to grow node-by-node

```donkey
# Simple native monitor, no MLflow needed
dsl.mlflow_monitor {
  enabled: true
  backend: "native_logger"
  metrics: ["tokens_used", "recursion_depth", "task_success", "reward_score"]
  params: ["policy_id", "tool_used", "dsl_branch"]
  artifacts: ["mutation_log.json", "policy_graph.json"]
  flush_interval: 1
}
```

---

## 🔁 Phase 3: Task Loop

Each task:
1. Is scored for complexity
2. Triggers a policy
3. Logs:
   - Tokens used
   - Tools used
   - Depth of recursion
   - Time signals
4. Applies DSL mutation if stuck or reward plateaus
5. Updates the DSL graph

---

## 🧬 Phase 4: Mutation & Adaptation

Every 2–3 tasks:
- Measures ΔReward
- Suggests:
  - Prune weak nodes
  - Try different tools
  - Tune recursion depth
- Forks new DSL branch if needed
- Logs mutation to `dsl.policy_graph`

---

## 📈 Phase 5: Final Report

Auto-generated outputs:
- Task table: policies used, scores
- Mermaid graph of traversal path
- Mutation log
- DSL evolution summary

Output formats:
- JSON trace
- Markdown recap
- Mermaid diagram (task path or DSL graph)

---

## 🌐 Phase 6: DSL Explorer UI Prototype (10% Ship)

**Features:**
- Load `.dsl` file as node graph
- Expand node to show DSL block
- Show agent branches, active/inactive
- Time-based node fading (from `temporal_model`)
- Hints from `aisdk` for improving each DSL segment

> Once Phase 1 is filled in, the Donkey runtime will generate all DSLs, link the graph, and begin execution with graph explorer.

### 💡 Tip
Use `prompt_dsl_assistant("my.dsl")` to get real-time recommendations on DSL formatting, simplification, or extension.

---

## 🔍 Phase 14: Strategic Next Steps & SOTA Benchmarking

### 14.1 Expand Trace Collection
- **Objective:** Increase the diversity of reasoning traces to cover edge-case and high-complexity tasks.  
- **Actions:**  
  1. Run extended sessions across domains (math proofs, code synthesis, QA) to accumulate >1000 DSL trace examples.  
  2. Annotate each trace with outcome metrics (accuracy, alignment, novelty).

### 14.2 Data-Driven Mutation Analysis
- **Objective:** Leverage the collected traces for meta-learning.  
- **Actions:**  
  1. Store trace diffs and outcomes in a vector DB.  
  2. Use frozen LLM embedding to retrieve similar past mutations.  
  3. Evaluate mutation success rates and refine heuristics.

### 14.3 SOTA Comparison & Benchmarking
- **Objective:** Demonstrate superiority over baseline and existing systems.  
- **Actions:**  
  1. Define benchmark tasks (e.g., GSM8K for math, MBPP for code, SCQA for retrieval).  
  2. Compare:  
     - *Donkey DSL agent* vs *vanilla LLM* vs *toolformer/ReAct pipelines*.  
     - Metrics: task accuracy, latency, interpretability (trace reconstructibility).  
  3. Plot performance curves and generate a report.

### 14.4 Meta-Transformer Prototype
- **Objective:** Build a light-weight model that predicts optimal next mutations.  
- **Actions:**  
  1. Fine-tune a small transformer on `(DSL_state, mutation, outcome)` tuples.  
  2. Validate on held-out traces: measure prediction accuracy of beneficial mutations.  
  3. Integrate as `dsl.meta_mutator {}` in the runtime for live suggestions.

### 14.5 Continuous Evolution & Auto-Deployment
- **Objective:** Automate the full cycle from mutation to production.  
- **Actions:**  
  1. Configure CI/CD: on new trace data, retrain meta-transformer, update mutation_policy weights.  
  2. Deploy updated DSL modules automatically if delta thresholds are met.  
  3. Monitor long-term trends with the historical delta dashboard.

---

> These strategic steps ensure we not only gather richer data but also benchmark against SOTA, leverage meta-learning, and automate the evolution cycle end-to-end.

---

## 🚀 Phase 15: Repository Setup & AI Tutor Path

### 15.1 Repo Structure
```
DonkeyBootstrap/
├── README.md
├── LICENSE
├── dsl/
│   ├── experiment_plan.dsl
│   ├── policy_graph.dsl
│   ├── meta_policy.dsl
│   ├── execution_plan.dsl
│   ├── meta_schema/dsl.meta_schema.dsl
│   └── ai_tutor.dsl              # New AI Tutor path definitions
├── scripts/
│   ├── simulate_runner.py
│   ├── test_mvt_runner.py
│   └── analyze_budget.py
├── docs/
│   ├── CONTRIBUTING.md
│   └── USAGE.md
├── examples/
│   └── vision_plan.dsl
└── .github/
    ├── workflows/ci.yml
    └── ISSUE_TEMPLATE.md
```

### 15.2 README.md Highlights
- Project overview & research question
- Quickstart: install, load DSL, run `simulate_runner.py`
- AI Tutor example: how to extend via `ai_tutor.dsl`
- Contribution & issue guidelines

### 15.3 AI Tutor Path DSL (`ai_tutor.dsl`)
```donkey
# AI Tutor: Latent-Space Mapping & Local Maximum Finder

dsl.ai_tutor {
  name: "AI Tutor"
  description: "Maps student latent embeddings to personalized learning maxima"
  components: ["embedding_extractor", "maxima_selector", "feedback_generator"]
  policies: {
    embedding_extractor: rag_policy
    maxima_selector: pattern_matching_policy
    feedback_generator: cot_policy
  }
  budget: {tokens: 500, time_ms: 2000}
  metrics: ["local_max_score", "student_alignment"]
}
```

### 15.4 CONTRIBUTING.md Snippet
```markdown
# Contributing to DonkeyBootstrap

## Adding New Paths
1. Create a new DSL file under `dsl/`, e.g. `my_path.dsl`.
2. Follow `dsl.meta_schema.dsl` definitions for element types.
3. Add parsing & runner support in `scripts/` if custom logic is needed.
4. Write unit tests in `tests/` and update CI workflows.
5. Submit PR; delta-test will measure impact on metrics.
```

---

### 15.5 DSL Creation Utilities & Bootstrap Patch

To streamline new path creation, include utility functions in your Python SDK:

```python
# dsl_utils.py
from pathlib import Path

def create_dsl_block(name: str, content: str, directory: Path = Path('dsl')):
    """
    Boilerplate function to scaffold a new DSL block file.
    Args:
        name: Identifier for the DSL block (e.g., 'ai_tutor', 'my_path').
        content: The DSL content template to write.
        directory: DSL directory path.
    """
    directory.mkdir(exist_ok=True)
    file_path = directory / f"{name}.dsl"
    with open(file_path, 'w') as f:
        f.write(f"# Auto-generated DSL block: {name}
{content}
")
    return file_path
```

#### Bootstrap Patch Function

Use this patch at project startup to ensure all standard DSL modules exist:

```bash
# bootstrap_dsl.sh
#!/usr/bin/env bash
set -e

MODULES=(
  experiment_plan
  policy_graph
  meta_policy
  execution_plan
  ai_tutor
)

for mod in "${MODULES[@]}"; do
  if [ ! -f "dsl/${mod}.dsl" ]; then
    echo "Creating missing DSL block: $mod.dsl"
    python3 - << 'EOF'
from dsl_utils import create_dsl_block
create_dsl_block(
    name="$mod",
    content="dsl.${mod} { /* TODO: define ${mod} here */ }"
)
EOF
  fi
done

echo "DSL bootstrap complete."
```

Include these utilities in the repository (`<repo>/dsl_utils.py` and `bootstrap_dsl.sh`) and document their use in `README.md`. This ensures users can quickly scaffold and bootstrap DSL modules.  
