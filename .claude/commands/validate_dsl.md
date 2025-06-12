Run the DSL validation test suite.

Execute: make validate

This will check:
1. All DSL files have valid syntax
2. Referenced files (tasks, includes) exist
3. Budget constraints are reasonable
4. Domain profiles are properly configured
5. All safeguards are enabled

The validation is integrated into the Makefile for easy testing.