Add a new domain profile to the Donkey experiment framework.

Domain name: $ARGUMENTS

Steps:
1. Create new domain plan file in examples/${domain}_plan.dsl
2. Create tasks directory at tasks/${domain}/
3. Add sample task1.json in the tasks directory
4. Update dsl_thin_slice_patch.dsl to include the new domain profile
5. Validate the configuration

Ensure the new domain follows existing patterns and conventions.