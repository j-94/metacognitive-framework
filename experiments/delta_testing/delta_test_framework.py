#!/usr/bin/env python3
"""
Delta Testing Framework - Measure impact of DSL mutations on system performance
"""
import json
import time
import subprocess
import statistics
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
import hashlib
import random

class BaselineCapture:
    """Capture system baseline before mutations"""
    
    def __init__(self):
        self.baseline_dir = Path("baselines")
        self.baseline_dir.mkdir(exist_ok=True)
        
    def capture_dsl_state(self) -> Dict[str, Any]:
        """Capture current DSL configuration state"""
        state = {
            "timestamp": datetime.now().isoformat(),
            "dsl_files": {},
            "config_hash": ""
        }
        
        # Read all DSL files
        for dsl_file in Path(".").glob("**/*.dsl"):
            with open(dsl_file, 'r') as f:
                content = f.read()
                state["dsl_files"][str(dsl_file)] = {
                    "content": content,
                    "hash": hashlib.md5(content.encode()).hexdigest()
                }
        
        # Generate overall config hash
        combined = "".join(state["dsl_files"][f]["content"] for f in sorted(state["dsl_files"]))
        state["config_hash"] = hashlib.md5(combined.encode()).hexdigest()
        
        return state
    
    def capture_metrics(self, tasks: List[Dict]) -> Dict[str, Any]:
        """Run tasks and capture baseline metrics"""
        metrics = {
            "alignment_score": 0.0,
            "novelty_gradient": 0.0,
            "resource_efficiency": 0.0,
            "success_rate": 0.0,
            "total_tokens": 0,
            "avg_response_time": 0.0,
            "task_results": []
        }
        
        # Run tasks and collect metrics
        start_time = time.time()
        successful_tasks = 0
        response_times = []
        
        for task in tasks:
            task_start = time.time()
            result = self._run_task(task)
            task_time = time.time() - task_start
            
            response_times.append(task_time)
            
            if result["success"]:
                successful_tasks += 1
                metrics["total_tokens"] += result.get("tokens_used", 0)
                
            metrics["task_results"].append({
                "task_id": task.get("id", "unknown"),
                "success": result["success"],
                "tokens": result.get("tokens_used", 0),
                "response_time": task_time
            })
        
        # Calculate aggregate metrics
        metrics["success_rate"] = successful_tasks / len(tasks) if tasks else 0
        metrics["avg_response_time"] = statistics.mean(response_times) if response_times else 0
        
        # Calculate synthetic metrics (in real system, these would be computed differently)
        metrics["alignment_score"] = self._calculate_alignment(metrics["task_results"])
        metrics["novelty_gradient"] = self._calculate_novelty(metrics["task_results"])
        metrics["resource_efficiency"] = self._calculate_efficiency(metrics)
        
        return metrics
    
    def _run_task(self, task: Dict) -> Dict[str, Any]:
        """Execute a single task"""
        try:
            # Simulate running through donkey_real.py
            cmd = [
                "python3", "donkey_real.py", 
                "--task", json.dumps(task),
                "--max-tokens", str(task.get("max_tokens", 100))
            ]
            
            # For now, simulate task execution
            success = random.random() > 0.2  # 80% success rate
            tokens = random.randint(50, 150)
            
            return {
                "success": success,
                "tokens_used": tokens,
                "response": "Simulated response"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tokens_used": 0
            }
    
    def _calculate_alignment(self, results: List[Dict]) -> float:
        """Calculate alignment score based on task results"""
        if not results:
            return 0.0
        
        # Synthetic calculation - in real system would measure semantic alignment
        success_count = sum(1 for r in results if r["success"])
        return success_count / len(results) * 0.85 + random.uniform(0.1, 0.15)
    
    def _calculate_novelty(self, results: List[Dict]) -> float:
        """Calculate novelty gradient"""
        # Synthetic - would measure response diversity in real system
        return random.uniform(0.3, 0.7)
    
    def _calculate_efficiency(self, metrics: Dict) -> float:
        """Calculate resource efficiency"""
        if metrics["total_tokens"] == 0:
            return 1.0
        
        # Efficiency = success_rate / normalized_token_usage
        normalized_tokens = min(metrics["total_tokens"] / 1000, 1.0)
        return metrics["success_rate"] / (normalized_tokens + 0.1)


class MutationEngine:
    """Apply controlled mutations to DSL configurations"""
    
    def __init__(self):
        self.mutations = {
            "adjust_recursion_depth": self._mutate_recursion_depth,
            "reweight_tool_efficiency": self._mutate_tool_weights,
            "modify_batch_size": self._mutate_batch_size,
            "toggle_optimization": self._mutate_optimization,
            "adjust_budget_factor": self._mutate_budget_factor
        }
        
    def apply_mutation(self, mutation_name: str, dsl_files: Dict[str, Any]) -> Dict[str, Any]:
        """Apply a named mutation to DSL configuration"""
        if mutation_name not in self.mutations:
            raise ValueError(f"Unknown mutation: {mutation_name}")
            
        # Create a deep copy of DSL files
        mutated_files = json.loads(json.dumps(dsl_files))
        
        # Apply the mutation
        self.mutations[mutation_name](mutated_files)
        
        return mutated_files
    
    def _mutate_recursion_depth(self, dsl_files: Dict):
        """Adjust recursion depth in configuration"""
        for file_path, file_data in dsl_files.items():
            if "recursion" in file_data["content"]:
                # Simple text replacement - in real system would parse properly
                content = file_data["content"]
                if "recursion_depth: 3" in content:
                    file_data["content"] = content.replace("recursion_depth: 3", "recursion_depth: 5")
                elif "recursion_depth:" in content:
                    # Increase by 1
                    import re
                    content = re.sub(r'recursion_depth: (\d+)', 
                                   lambda m: f'recursion_depth: {int(m.group(1)) + 1}', 
                                   content)
                    file_data["content"] = content
    
    def _mutate_tool_weights(self, dsl_files: Dict):
        """Adjust tool efficiency weights"""
        for file_path, file_data in dsl_files.items():
            if "tool" in file_data["content"] or "weight" in file_data["content"]:
                content = file_data["content"]
                # Add or modify tool weights
                if "tool_weights:" not in content:
                    # Add tool weights section
                    content += "\n\ndsl.tool_weights {\n  efficiency_multiplier: 1.2\n  preference_order: [\"fast\", \"accurate\"]\n}\n"
                else:
                    # Modify existing weights
                    content = content.replace("efficiency_multiplier: 1.0", "efficiency_multiplier: 1.2")
                file_data["content"] = content
    
    def _mutate_batch_size(self, dsl_files: Dict):
        """Modify batch processing size"""
        for file_path, file_data in dsl_files.items():
            if "batch" in file_data["content"]:
                content = file_data["content"]
                import re
                # Increase batch size by 50%
                content = re.sub(r'max_batch_tokens: (\d+)', 
                               lambda m: f'max_batch_tokens: {int(int(m.group(1)) * 1.5)}', 
                               content)
                file_data["content"] = content
    
    def _mutate_optimization(self, dsl_files: Dict):
        """Toggle optimization settings"""
        for file_path, file_data in dsl_files.items():
            if "optimizer" in file_data["content"] or "optimization" in file_data["content"]:
                content = file_data["content"]
                # Toggle enabled state
                if "enabled: true" in content:
                    content = content.replace("enabled: true", "enabled: false")
                elif "enabled: false" in content:
                    content = content.replace("enabled: false", "enabled: true")
                file_data["content"] = content
    
    def _mutate_budget_factor(self, dsl_files: Dict):
        """Adjust budget estimation factor"""
        for file_path, file_data in dsl_files.items():
            if "budget" in file_data["content"] or "fudge_factor" in file_data["content"]:
                content = file_data["content"]
                import re
                # Increase fudge factor by 10%
                content = re.sub(r'fudge_factor: ([\d.]+)', 
                               lambda m: f'fudge_factor: {float(m.group(1)) * 1.1:.2f}', 
                               content)
                file_data["content"] = content


class StatisticalValidator:
    """Validate delta significance using statistical methods"""
    
    def __init__(self, significance_level: float = 0.05):
        self.significance_level = significance_level
        
    def validate_delta(self, pre_metrics: Dict, post_metrics: Dict, 
                      method: str = "bootstrap") -> Dict[str, Any]:
        """Validate if delta is statistically significant"""
        validation_result = {
            "method": method,
            "significance_level": self.significance_level,
            "deltas": {},
            "significant_changes": []
        }
        
        # Calculate deltas for each metric
        metric_names = ["alignment_score", "novelty_gradient", "resource_efficiency", 
                       "success_rate", "total_tokens", "avg_response_time"]
        
        for metric in metric_names:
            if metric in pre_metrics and metric in post_metrics:
                delta = post_metrics[metric] - pre_metrics[metric]
                validation_result["deltas"][metric] = {
                    "pre": pre_metrics[metric],
                    "post": post_metrics[metric],
                    "delta": delta,
                    "percent_change": (delta / pre_metrics[metric] * 100) if pre_metrics[metric] != 0 else 0
                }
                
                # Determine significance (simplified)
                if abs(delta) > 0.1 * abs(pre_metrics[metric]):  # 10% change threshold
                    validation_result["significant_changes"].append(metric)
        
        # Apply statistical test
        if method == "bootstrap":
            validation_result["bootstrap_results"] = self._bootstrap_test(
                pre_metrics["task_results"], 
                post_metrics["task_results"]
            )
        
        return validation_result
    
    def _bootstrap_test(self, pre_results: List[Dict], post_results: List[Dict], 
                       n_iterations: int = 1000) -> Dict[str, Any]:
        """Perform bootstrap resampling test"""
        # Simplified bootstrap - in real system would be more sophisticated
        bootstrap_result = {
            "n_iterations": n_iterations,
            "confidence_intervals": {}
        }
        
        # Extract success rates for bootstrap
        pre_successes = [1 if r["success"] else 0 for r in pre_results]
        post_successes = [1 if r["success"] else 0 for r in post_results]
        
        # Bootstrap resampling
        delta_samples = []
        for _ in range(n_iterations):
            # Resample with replacement
            pre_sample = [random.choice(pre_successes) for _ in pre_successes]
            post_sample = [random.choice(post_successes) for _ in post_successes]
            
            # Calculate delta for this sample
            delta = statistics.mean(post_sample) - statistics.mean(pre_sample)
            delta_samples.append(delta)
        
        # Calculate confidence interval
        delta_samples.sort()
        lower_idx = int(n_iterations * (self.significance_level / 2))
        upper_idx = int(n_iterations * (1 - self.significance_level / 2))
        
        bootstrap_result["confidence_intervals"]["success_rate_delta"] = {
            "lower": delta_samples[lower_idx],
            "upper": delta_samples[upper_idx],
            "mean": statistics.mean(delta_samples),
            "significant": 0 < delta_samples[lower_idx] or 0 > delta_samples[upper_idx]
        }
        
        return bootstrap_result


class DeltaTestOrchestrator:
    """Main orchestrator for delta testing"""
    
    def __init__(self):
        self.baseline = BaselineCapture()
        self.mutator = MutationEngine()
        self.validator = StatisticalValidator()
        self.log_file = Path("mutation_observer_log.json")
        
        # Load existing log or create new
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                self.mutation_log = json.load(f)
        else:
            self.mutation_log = {"tests": []}
    
    def run_delta_test(self, mutations: List[str], tasks: List[Dict], 
                      validation_method: str = "bootstrap") -> Dict[str, Any]:
        """Execute complete delta test procedure"""
        test_result = {
            "test_id": datetime.now().isoformat(),
            "mutations": mutations,
            "results": []
        }
        
        # Step 1: Capture baseline
        print("📊 Capturing baseline...")
        baseline_state = self.baseline.capture_dsl_state()
        baseline_metrics = self.baseline.capture_metrics(tasks)
        
        # Step 2-7: Apply each mutation and test
        for mutation in mutations:
            print(f"\n🧬 Testing mutation: {mutation}")
            mutation_result = self._test_single_mutation(
                mutation, baseline_state, baseline_metrics, tasks, validation_method
            )
            test_result["results"].append(mutation_result)
        
        # Log results
        self._log_results(test_result)
        
        # Generate summary
        test_result["summary"] = self._generate_summary(test_result["results"])
        
        return test_result
    
    def _test_single_mutation(self, mutation: str, baseline_state: Dict, 
                            baseline_metrics: Dict, tasks: List[Dict], 
                            validation_method: str) -> Dict[str, Any]:
        """Test a single mutation"""
        result = {
            "mutation": mutation,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Apply mutation
            mutated_files = self.mutator.apply_mutation(mutation, baseline_state["dsl_files"])
            
            # Write mutated files temporarily
            self._apply_mutation_files(mutated_files)
            
            # Run tasks with mutation
            post_metrics = self.baseline.capture_metrics(tasks)
            
            # Validate delta
            validation = self.validator.validate_delta(
                baseline_metrics, post_metrics, validation_method
            )
            
            result["validation"] = validation
            result["success"] = True
            
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            
        finally:
            # Restore original files
            self._restore_files(baseline_state["dsl_files"])
        
        return result
    
    def _apply_mutation_files(self, mutated_files: Dict[str, Any]):
        """Write mutated DSL files to disk"""
        for file_path, file_data in mutated_files.items():
            with open(file_path, 'w') as f:
                f.write(file_data["content"])
    
    def _restore_files(self, original_files: Dict[str, Any]):
        """Restore original DSL files"""
        for file_path, file_data in original_files.items():
            with open(file_path, 'w') as f:
                f.write(file_data["content"])
    
    def _log_results(self, test_result: Dict):
        """Append results to mutation log"""
        self.mutation_log["tests"].append(test_result)
        
        with open(self.log_file, 'w') as f:
            json.dump(self.mutation_log, f, indent=2)
    
    def _generate_summary(self, results: List[Dict]) -> Dict[str, Any]:
        """Generate summary of test results"""
        summary = {
            "total_mutations": len(results),
            "successful_tests": sum(1 for r in results if r.get("success", False)),
            "significant_improvements": [],
            "significant_regressions": []
        }
        
        for result in results:
            if not result.get("success"):
                continue
                
            validation = result.get("validation", {})
            deltas = validation.get("deltas", {})
            
            # Check for significant improvements or regressions
            for metric, delta_info in deltas.items():
                if metric in validation.get("significant_changes", []):
                    delta = delta_info["delta"]
                    if metric in ["alignment_score", "novelty_gradient", "resource_efficiency", "success_rate"]:
                        # Higher is better
                        if delta > 0:
                            summary["significant_improvements"].append({
                                "mutation": result["mutation"],
                                "metric": metric,
                                "improvement": f"{delta_info['percent_change']:.1f}%"
                            })
                        else:
                            summary["significant_regressions"].append({
                                "mutation": result["mutation"],
                                "metric": metric,
                                "regression": f"{delta_info['percent_change']:.1f}%"
                            })
        
        return summary


def main():
    """CLI interface for delta testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Delta Testing Framework')
    parser.add_argument('--mutations', nargs='+', 
                       default=["adjust_recursion_depth", "reweight_tool_efficiency"],
                       help='Mutations to test')
    parser.add_argument('--tasks-file', default='formal_tasks_set.json',
                       help='JSON file containing test tasks')
    parser.add_argument('--method', default='bootstrap',
                       choices=['bootstrap', 'ttest'],
                       help='Statistical validation method')
    parser.add_argument('--report', action='store_true',
                       help='Generate HTML report')
    
    args = parser.parse_args()
    
    # Load tasks
    if Path(args.tasks_file).exists():
        with open(args.tasks_file, 'r') as f:
            tasks = json.load(f)
    else:
        # Default test tasks
        tasks = [
            {"id": "t1", "prompt": "Test task 1", "max_tokens": 100},
            {"id": "t2", "prompt": "Test task 2", "max_tokens": 100},
            {"id": "t3", "prompt": "Test task 3", "max_tokens": 100}
        ]
    
    # Run delta test
    orchestrator = DeltaTestOrchestrator()
    results = orchestrator.run_delta_test(args.mutations, tasks, args.method)
    
    # Print summary
    print("\n" + "="*60)
    print("📊 DELTA TEST SUMMARY")
    print("="*60)
    
    summary = results["summary"]
    print(f"Total mutations tested: {summary['total_mutations']}")
    print(f"Successful tests: {summary['successful_tests']}")
    
    if summary["significant_improvements"]:
        print("\n✅ Significant Improvements:")
        for imp in summary["significant_improvements"]:
            print(f"  • {imp['mutation']}: {imp['metric']} +{imp['improvement']}")
    
    if summary["significant_regressions"]:
        print("\n❌ Significant Regressions:")
        for reg in summary["significant_regressions"]:
            print(f"  • {reg['mutation']}: {reg['metric']} {reg['regression']}")
    
    # Generate report if requested
    if args.report:
        generate_html_report(results)
        print("\n📄 HTML report saved to: delta_test_report.html")


def generate_html_report(results: Dict):
    """Generate HTML report for delta test results"""
    html_template = """<!DOCTYPE html>
<html>
<head>
    <title>Delta Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .mutation {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; }}
        .significant {{ background: #ffe0e0; }}
        .improvement {{ color: green; }}
        .regression {{ color: red; }}
        table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #f0f0f0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Delta Test Report</h1>
        <p>Generated: {timestamp}</p>
    </div>
    
    <h2>Summary</h2>
    <ul>
        <li>Total mutations tested: {total_mutations}</li>
        <li>Successful tests: {successful_tests}</li>
    </ul>
    
    <h2>Mutation Results</h2>
    {mutation_details}
</body>
</html>"""
    
    # Build mutation details
    mutation_html = ""
    for result in results["results"]:
        if not result.get("success"):
            mutation_html += f'<div class="mutation"><h3>{result["mutation"]}</h3><p>Error: {result.get("error", "Unknown")}</p></div>'
            continue
            
        validation = result["validation"]
        deltas = validation["deltas"]
        
        mutation_html += f'<div class="mutation"><h3>{result["mutation"]}</h3><table>'
        mutation_html += "<tr><th>Metric</th><th>Pre</th><th>Post</th><th>Delta</th><th>% Change</th></tr>"
        
        for metric, delta_info in deltas.items():
            change_class = "improvement" if delta_info["delta"] > 0 else "regression"
            mutation_html += f"""
            <tr>
                <td>{metric}</td>
                <td>{delta_info['pre']:.3f}</td>
                <td>{delta_info['post']:.3f}</td>
                <td class="{change_class}">{delta_info['delta']:+.3f}</td>
                <td class="{change_class}">{delta_info['percent_change']:+.1f}%</td>
            </tr>
            """
        
        mutation_html += "</table></div>"
    
    # Format and save
    report = html_template.format(
        timestamp=results["test_id"],
        total_mutations=results["summary"]["total_mutations"],
        successful_tests=results["summary"]["successful_tests"],
        mutation_details=mutation_html
    )
    
    with open("delta_test_report.html", "w") as f:
        f.write(report)


if __name__ == "__main__":
    main()