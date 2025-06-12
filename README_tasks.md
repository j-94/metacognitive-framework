# Donkey Task JSON Schema Documentation

This document explains the JSON schema for creating valid task definitions in the Donkey experiment framework.

## Overview

Tasks are JSON files stored in domain-specific directories under `tasks/{domain}/`. Each task represents a single unit of work that the experiment framework will execute.

## Task Schema

### Core Fields (Required)

All tasks MUST include these fields:

```json
{
  "id": "unique_task_identifier",
  "prompt": "The instruction or question for the model"
}
```

### Domain-Specific Fields

#### Math Domain Tasks

Math tasks typically include:

```json
{
  "id": "m1",
  "prompt": "Prove that the sum of two even numbers is even.",
  "ground_truth": "formal_proof_stub",
  "difficulty": "easy|medium|hard",
  "topic": "number_theory|algebra|calculus|geometry",
  "expected_approach": "induction|direct_proof|contradiction"
}
```

**Fields:**
- `ground_truth`: Expected solution or proof (can be stub for development)
- `difficulty`: Task complexity level (optional)
- `topic`: Mathematical domain (optional)
- `expected_approach`: Suggested proof method (optional)

#### RAG (Retrieval-Augmented Generation) Domain Tasks

RAG tasks typically include:

```json
{
  "id": "r1",
  "prompt": "What is the capital of France?",
  "context": "stub",
  "ground_truth": "Paris",
  "document_ids": ["doc1", "doc2"],
  "retrieval_strategy": "semantic|keyword|hybrid"
}
```

**Fields:**
- `context`: Retrieved context or document content
- `ground_truth`: Expected answer
- `document_ids`: References to source documents (optional)
- `retrieval_strategy`: How to retrieve relevant context (optional)

## Task Naming Conventions

1. **File Names**: Use descriptive names like `task1.json`, `algebra_proof.json`, or `capital_cities.json`
2. **Task IDs**: 
   - Math tasks: Prefix with `m` (e.g., `m1`, `m_algebra_01`)
   - RAG tasks: Prefix with `r` (e.g., `r1`, `r_geography_01`)
   - Custom domains: Use appropriate prefix

## Creating New Tasks

### Step 1: Choose the Correct Directory

Place your task file in the appropriate domain directory:
- Math tasks: `tasks/math/`
- RAG tasks: `tasks/rag/`
- New domains: `tasks/{domain_name}/`

### Step 2: Create Valid JSON

Example math task:
```json
{
  "id": "m_fibonacci_01",
  "prompt": "Prove that every third Fibonacci number is even.",
  "ground_truth": "proof_by_induction",
  "difficulty": "medium",
  "topic": "number_theory"
}
```

Example RAG task:
```json
{
  "id": "r_history_01",
  "prompt": "When was the Treaty of Versailles signed?",
  "context": "The Treaty of Versailles was signed on June 28, 1919...",
  "ground_truth": "June 28, 1919",
  "document_ids": ["wwi_treaties"]
}
```

### Step 3: Validate Your Task

Before committing:
1. Ensure JSON is valid (use a JSON validator)
2. Check all required fields are present
3. Verify the task ID is unique within the domain
4. Test with a small budget to ensure it executes

## Advanced Task Features

### Multi-Step Tasks

For complex tasks requiring multiple steps:

```json
{
  "id": "m_complex_01",
  "prompt": "Solve the system of equations and verify the solution.",
  "steps": [
    {"step": 1, "instruction": "Set up the system"},
    {"step": 2, "instruction": "Solve using elimination"},
    {"step": 3, "instruction": "Verify the solution"}
  ],
  "ground_truth": "x=2, y=3"
}
```

### Tasks with Constraints

Add execution constraints:

```json
{
  "id": "r_constrained_01",
  "prompt": "Summarize this document in 50 words or less.",
  "context": "...",
  "constraints": {
    "max_output_tokens": 75,
    "required_format": "bullet_points"
  }
}
```

### Tasks with Metadata

Include experiment metadata:

```json
{
  "id": "m_tracked_01",
  "prompt": "Derive the quadratic formula.",
  "metadata": {
    "created_by": "contributor_name",
    "created_date": "2024-01-15",
    "tags": ["algebra", "formula_derivation"],
    "estimated_tokens": 500
  }
}
```

## Best Practices

1. **Keep prompts clear and unambiguous**
2. **Include ground truth for evaluation** (even if stubbed initially)
3. **Use consistent ID patterns** within each domain
4. **Add optional fields** that help with analysis and debugging
5. **Test tasks individually** before bulk execution
6. **Document complex tasks** with comments in a separate file
7. **Version control** all task changes

## Validation Checklist

Before submitting new tasks:
- [ ] Valid JSON syntax
- [ ] Unique task ID
- [ ] Required fields present (`id`, `prompt`)
- [ ] Appropriate domain placement
- [ ] Ground truth included (or explicitly marked as stub)
- [ ] Reasonable token estimation
- [ ] No sensitive information in prompts or context

## Common Errors to Avoid

1. **Missing commas** between JSON fields
2. **Duplicate task IDs** within a domain
3. **Incorrect escaping** of quotes in prompts
4. **Missing required fields**
5. **Placing tasks in wrong domain directory**
6. **Extremely long prompts** that exceed token budgets

## Contributing New Task Types

If you need a new task schema:
1. Document the new fields in this file
2. Create example tasks demonstrating the schema
3. Update the validation logic if automated
4. Consider backward compatibility

For questions or to propose schema changes, open an issue in the repository.