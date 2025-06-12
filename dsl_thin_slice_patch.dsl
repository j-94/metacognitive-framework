# =============================================================
#  Donkey Thin-Slice Patch  v0.1.1
# -------------------------------------------------------------
#  Adds the three missing safeguards + lateral-thinking extras.
# =============================================================

include_guard: true

dsl.roundtrip_guard { enabled: true scope: "*.dsl" fail_action: "exit" }

dsl.budget_estimator { heuristic: "token_per_word" fudge_factor: 1.10 enforce_pre_call: true }

dsl.domain_profiles {
  default: "math"
  profiles: [
    { name: "math", plan_path: "examples/math_plan.dsl", task_glob: "tasks/math/*" },
    { name: "rag",  plan_path: "examples/rag_plan.dsl",  task_glob: "tasks/rag/*"  }
  ]
}

dsl.batch_optimizer { enabled: true max_batch_tokens: 2048 strategy: "greedy-fit" }

dsl.cross_domain_watchdog { threshold_pct: 10 action: "open_issue" compare_window: 1 }

dsl.schema_fingerprint { algorithm: "md5" include_in_trace: true }

dsl.mlflow_monitor {
  enabled: true
  backend: "native_logger"
  metrics: ["tokens_used","recursion_depth","task_success","reward_score","schema_md5"]
  params: ["policy_id","tool_used","dsl_branch","domain_profile","batch_size","est_tokens"]
  artifacts: ["mutation_log.json","policy_graph.json"]
  flush_interval: 1
}

dsl.delta_test {
  baseline_tags: ["policy_graph_v1"]
  mutations: ["adjust_recursion_depth", "reweight_tool_efficiency"]
  tasks: load("formal_tasks_set.json")
  metrics: ["alignment_score", "novelty_gradient", "resource_efficiency"]
  validation_method: "bootstrap(1000)"
  significance_level: 0.05
  log_to: "mutation_observer_log.json"
}
