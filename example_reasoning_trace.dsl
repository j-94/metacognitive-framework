# Example DSL Reasoning Trace
# Task: Prove "If it rains, then the ground is wet" + "It is raining" → "The ground is wet"

dsl.reasoning_trace {
  meta {
    timestamp: "2025-06-12T16:10:09"
    recursion_depth: 5
    trace_version: "1.0"
    task_type: "implication_proof"
  }
  
  step.decompose {
    action: "identify_components"
    components {
      premise: "If it rains, then the ground is wet"
      given: "It is raining"
      goal: "The ground is wet"
    }
    pattern: "implication_resolution"
  }
  
  step.pattern_match {
    action: "recognize_inference_rule"
    matched_pattern: "modus_ponens"
    confidence: 0.95
    alternatives: ["hypothetical_syllogism", "contrapositive"]
  }
  
  step.apply_rule_depth_0 {
    action: "apply_modus_ponens"
    depth: 0
    bindings {
      P: "it rains"
      Q: "the ground is wet"
      P_truth: true
    }
    inference: "Q must be true"
  }
  
  step.verify_depth_0 {
    action: "check_consistency"
    method: "truth_table_verification"
    result: "consistent"
  }
  
  step.apply_rule_depth_1 {
    action: "apply_modus_ponens"
    depth: 1
    bindings {
      P: "it rains"
      Q: "the ground is wet"
      P_truth: true
    }
    inference: "Q must be true"
  }
  
  step.verify_depth_1 {
    action: "check_consistency"
    method: "truth_table_verification"
    result: "consistent"
  }
  
  step.apply_rule_depth_2 {
    action: "apply_modus_ponens"
    depth: 2
    bindings {
      P: "it rains"
      Q: "the ground is wet"
      P_truth: true
    }
    inference: "Q must be true"
  }
  
  step.synthesize {
    action: "construct_proof"
    proof_steps: [
      "1. Given: P → Q (If it rains, then the ground is wet)",
      "2. Given: P (It is raining)",
      "3. By modus ponens: Q (Therefore, the ground is wet)"
    ]
    conclusion: "The ground is wet"
    validity: "sound"
  }
  
  # Meta-reasoning enabled by higher recursion depth
  step.meta_reasoning {
    action: "reflect_on_process"
    observations: [
      "Direct application of modus ponens",
      "No contradictions found",
      "Proof is minimal and complete"
    ]
    quality_score: 0.92
  }
}

# This DSL trace can be:
# 1. Reconstructed - Extract the logical flow and verify correctness
# 2. Mutated - Change parameters like recursion_depth or inference methods
# 3. Evolved - Apply systematic improvements based on quality metrics
# 4. Taught - Use as training data for other reasoning systems