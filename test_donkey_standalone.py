#!/usr/bin/env python3
"""
Standalone test suite for Donkey (no pytest dependency)
"""
import json
import subprocess
from pathlib import Path

def test_roundtrip_guard():
    """Test 1: DSL files can be parsed and validated"""
    print("🧪 Test 1: Round-trip guard...", end=" ")
    
    dsl_files = [
        "dsl.experiment_plan.dsl",
        "dsl_thin_slice_patch.dsl",
        "examples/math_plan.dsl",
        "examples/rag_plan.dsl"
    ]
    
    for dsl_file in dsl_files:
        assert Path(dsl_file).exists(), f"DSL file missing: {dsl_file}"
        
        with open(dsl_file, 'r') as f:
            content = f.read()
            assert '{' in content and '}' in content, f"Invalid DSL syntax in {dsl_file}"
    
    with open("dsl.experiment_plan.dsl", 'r') as f:
        assert 'include "dsl_thin_slice_patch.dsl"' in f.read()
    
    print("✅ PASS")
    return True

def test_budget_estimator():
    """Test 2: Budget enforcement works"""
    print("🧪 Test 2: Budget estimator...", end=" ")
    
    result = subprocess.run(
        ["python3", "donkey.py", "run"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, "Donkey runner failed"
    assert "Budget: 1000 tokens" in result.stdout, "Budget not set to 1k"
    assert "Total tokens used:" in result.stdout, "No token tracking"
    
    output_lines = result.stdout.split('\n')
    for line in output_lines:
        if "Total tokens used:" in line:
            tokens_part = line.split(':')[1].strip()
            used_tokens = int(tokens_part.split('/')[0])
            assert used_tokens <= 1000, f"Budget exceeded: {used_tokens} > 1000"
    
    print("✅ PASS")
    return True

def test_dual_domains():
    """Test 3: Both math and RAG domains work"""
    print("🧪 Test 3: Dual domains...", end=" ")
    
    domains = ["math", "rag"]
    
    for domain in domains:
        task_dir = Path(f"tasks/{domain}")
        assert task_dir.exists(), f"Task directory missing: {task_dir}"
        assert len(list(task_dir.glob("*.json"))) > 0, f"No tasks in {domain}"
        
        result = subprocess.run(
            ["python3", "donkey.py", "run", "--domain", domain],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Failed to run {domain} domain"
        assert f"domain: {domain}" in result.stdout, f"Domain {domain} not loaded"
        assert "Execution Trace:" in result.stdout, f"No trace for {domain}"
    
    print("✅ PASS")
    return True

def run_all_tests():
    """Run all tests and report results"""
    print("🚀 Running Donkey test suite\n")
    
    tests = [
        test_roundtrip_guard,
        test_budget_estimator,
        test_dual_domains
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ FAIL: {str(e)}")
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)