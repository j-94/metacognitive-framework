#!/usr/bin/env python3
"""
Test suite for Donkey experiment runner
"""
import pytest
import json
import subprocess
from pathlib import Path

class TestDonkey:
    """Core milestone tests"""
    
    def test_roundtrip_guard(self):
        """Test 1: DSL files can be parsed and validated"""
        # Check main DSL files exist and are valid
        dsl_files = [
            "dsl.experiment_plan.dsl",
            "dsl_thin_slice_patch.dsl",
            "examples/math_plan.dsl",
            "examples/rag_plan.dsl"
        ]
        
        for dsl_file in dsl_files:
            assert Path(dsl_file).exists(), f"DSL file missing: {dsl_file}"
            
            # Basic syntax check - file should contain valid DSL blocks
            with open(dsl_file, 'r') as f:
                content = f.read()
                assert '{' in content and '}' in content, f"Invalid DSL syntax in {dsl_file}"
                
        # Verify include works
        with open("dsl.experiment_plan.dsl", 'r') as f:
            assert 'include "dsl_thin_slice_patch.dsl"' in f.read()
    
    def test_budget_estimator(self):
        """Test 2: Budget enforcement works"""
        # Run donkey and verify it respects budget
        result = subprocess.run(
            ["python3", "donkey.py", "run"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, "Donkey runner failed"
        assert "Budget: 1000 tokens" in result.stdout, "Budget not set to 1k"
        assert "Total tokens used:" in result.stdout, "No token tracking"
        
        # Verify doesn't exceed budget
        output_lines = result.stdout.split('\n')
        for line in output_lines:
            if "Total tokens used:" in line:
                tokens_part = line.split(':')[1].strip()
                used_tokens = int(tokens_part.split('/')[0])
                assert used_tokens <= 1000, f"Budget exceeded: {used_tokens} > 1000"
    
    def test_dual_domains(self):
        """Test 3: Both math and RAG domains work"""
        domains = ["math", "rag"]
        
        for domain in domains:
            # Verify domain has tasks
            task_dir = Path(f"tasks/{domain}")
            assert task_dir.exists(), f"Task directory missing: {task_dir}"
            assert len(list(task_dir.glob("*.json"))) > 0, f"No tasks in {domain}"
            
            # Run with domain
            result = subprocess.run(
                ["python3", "donkey.py", "run", "--domain", domain],
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0, f"Failed to run {domain} domain"
            assert f"domain: {domain}" in result.stdout, f"Domain {domain} not loaded"
            assert "Execution Trace:" in result.stdout, f"No trace for {domain}"

def validate_dsl():
    """Command: /project:validate_dsl implementation"""
    print("🔍 Validating DSL files...")
    
    issues = []
    
    # Check all DSL files
    dsl_files = list(Path(".").glob("**/*.dsl"))
    
    for dsl_file in dsl_files:
        try:
            with open(dsl_file, 'r') as f:
                content = f.read()
                
            # Basic validation
            if content.count('{') != content.count('}'):
                issues.append(f"{dsl_file}: Mismatched braces")
                
            # Check for required elements in main config
            if "dsl.experiment_plan.dsl" in str(dsl_file):
                if "budget_tokens:" not in content:
                    issues.append(f"{dsl_file}: Missing budget_tokens")
                    
        except Exception as e:
            issues.append(f"{dsl_file}: {str(e)}")
    
    # Check task files
    for task_file in Path(".").glob("tasks/**/*.json"):
        try:
            with open(task_file, 'r') as f:
                task = json.load(f)
                
            if 'id' not in task:
                issues.append(f"{task_file}: Missing 'id' field")
            if 'prompt' not in task:
                issues.append(f"{task_file}: Missing 'prompt' field")
                
        except json.JSONDecodeError:
            issues.append(f"{task_file}: Invalid JSON")
        except Exception as e:
            issues.append(f"{task_file}: {str(e)}")
    
    # Report results
    if issues:
        print("❌ Validation failed:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ All DSL files valid!")
        return True

if __name__ == "__main__":
    # If run directly, execute validation
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "validate":
        sys.exit(0 if validate_dsl() else 1)