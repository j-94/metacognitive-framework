include "dsl_thin_slice_patch.dsl"

dsl.experiment_plan {
  id: "donkey_first_principles_boot"
  description: "Minimal boot plan proving round‑trip guard, budget estimator and dual domains work."
  budget_tokens: 1000
  reasoning_style: "flat"
  domain_profile: "math"
}
