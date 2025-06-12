#!/usr/bin/env python3
"""
Donkey - Production runner with real LLM, budget enforcement, and mutations
"""
import json
import sys
import os
import argparse
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Load .env file if it exists
env_file = Path('.env')
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value.strip()

class LLMAdapter:
    """Real LLM adapter with token counting"""
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.token_count = 0
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        # Report API key status
        if self.api_key:
            print(f"✅ OpenAI API key found (using {model})")
        else:
            print("⚠️  No OPENAI_API_KEY found - using simulation mode")
        
    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation: ~4 chars per token"""
        return len(text) // 4
        
    def complete(self, prompt: str, max_tokens: int = 100) -> Dict[str, Any]:
        """Complete with real or simulated LLM"""
        prompt_tokens = self.estimate_tokens(prompt)
        
        if self.api_key:
            # Use OpenAI API
            try:
                from openai import OpenAI
                client = OpenAI(api_key=self.api_key)
                
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                
                response_text = response.choices[0].message.content
                prompt_tokens = response.usage.prompt_tokens
                response_tokens = response.usage.completion_tokens
                total_tokens = response.usage.total_tokens
                
            except ImportError:
                response_text = self._simulate_llm_response(prompt)
                response_tokens = self.estimate_tokens(response_text)
                total_tokens = prompt_tokens + response_tokens
                print("⚠️  OpenAI library not installed. Using simulation. Install with: pip install openai")
            except Exception as e:
                response_text = self._simulate_llm_response(prompt)
                response_tokens = self.estimate_tokens(response_text)
                total_tokens = prompt_tokens + response_tokens
                print(f"⚠️  API call failed: {e}. Using simulation.")
        else:
            response_text = self._simulate_llm_response(prompt)
            response_tokens = self.estimate_tokens(response_text)
            total_tokens = prompt_tokens + response_tokens
            
        self.token_count += total_tokens
        
        return {
            "text": response_text,
            "prompt_tokens": prompt_tokens,
            "response_tokens": response_tokens,
            "total_tokens": total_tokens
        }
    
    def _simulate_llm_response(self, prompt: str) -> str:
        """Simulate realistic responses based on prompt type"""
        if "prove" in prompt.lower() and "even" in prompt.lower():
            return "Let n and m be even integers. Then n = 2k and m = 2j for some integers k, j. Therefore n + m = 2k + 2j = 2(k + j), which is even. QED."
        elif "capital" in prompt.lower() and "france" in prompt.lower():
            return "The capital of France is Paris."
        else:
            return "This is a simulated response demonstrating token usage and batching."

class BatchOptimizer:
    """Batch multiple tasks to optimize token usage"""
    def __init__(self, max_batch_tokens: int = 2048):
        self.max_batch_tokens = max_batch_tokens
        
    def create_batches(self, tasks: List[Dict], estimator) -> List[List[Dict]]:
        """Group tasks into batches that fit within token limit"""
        batches = []
        current_batch = []
        current_tokens = 0
        
        for task in tasks:
            task_tokens = estimator(task['prompt']) + 100  # estimate response
            
            if current_tokens + task_tokens > self.max_batch_tokens and current_batch:
                batches.append(current_batch)
                current_batch = [task]
                current_tokens = task_tokens
            else:
                current_batch.append(task)
                current_tokens += task_tokens
                
        if current_batch:
            batches.append(current_batch)
            
        return batches

class MutationEngine:
    """Apply live mutations to tasks"""
    def __init__(self):
        self.mutations_applied = []
        
    def mutate_task(self, task: Dict, domain: str) -> Dict:
        """Apply domain-specific mutations"""
        mutated = task.copy()
        
        # Live mutation rule: Add reasoning chain for math domain
        if domain == "math" and "prove" in task['prompt'].lower():
            mutated['prompt'] = f"Step by step, {task['prompt']} Show your reasoning."
            self.mutations_applied.append({
                "task_id": task['id'],
                "mutation": "reasoning_chain",
                "original": task['prompt'],
                "mutated": mutated['prompt']
            })
            
        # Live mutation rule: Add context request for RAG domain
        elif domain == "rag" and "context" in task:
            mutated['prompt'] = f"Based on the provided context, {task['prompt']}"
            self.mutations_applied.append({
                "task_id": task['id'],
                "mutation": "context_prefix",
                "original": task['prompt'],
                "mutated": mutated['prompt']
            })
            
        return mutated

class BudgetEnforcer:
    """Strict budget enforcement with pre-flight checks"""
    def __init__(self, budget: int, estimator):
        self.budget = budget
        self.used = 0
        self.estimator = estimator
        self.blocked_tasks = []
        
    def check_task(self, task: Dict) -> bool:
        """Pre-flight check if task fits in budget"""
        estimated = self.estimator(task['prompt']) + 150  # buffer
        
        if self.used + estimated > self.budget:
            self.blocked_tasks.append({
                "task_id": task['id'],
                "estimated_tokens": estimated,
                "budget_remaining": self.budget - self.used
            })
            return False
        return True
        
    def consume(self, tokens: int):
        """Track token consumption"""
        self.used += tokens
        if self.used > self.budget:
            raise RuntimeError(f"BUDGET EXCEEDED: {self.used} > {self.budget}")

class DonkeyRunner:
    def __init__(self, config_path="dsl.experiment_plan.dsl"):
        self.config = self._load_config(config_path)
        self.adapter = LLMAdapter()
        self.batch_optimizer = BatchOptimizer(max_batch_tokens=2048)
        self.mutation_engine = MutationEngine()
        self.budget_enforcer = BudgetEnforcer(
            self.config['budget_tokens'],
            self.adapter.estimate_tokens
        )
        self.trace = []
        
    def _load_config(self, path):
        """Parse DSL config with all settings"""
        config = {
            "id": "donkey_first_principles_boot",
            "budget_tokens": 1000,
            "domain_profile": "math",
            "batch_optimizer_enabled": True,
            "mutations_enabled": True
        }
        
        if Path(path).exists():
            with open(path, 'r') as f:
                content = f.read()
                
            # Parse budget
            if 'budget_tokens:' in content:
                for line in content.split('\n'):
                    if 'budget_tokens:' in line:
                        config['budget_tokens'] = int(line.split(':')[1].strip())
                    elif 'domain_profile:' in line:
                        config['domain_profile'] = line.split(':')[1].strip().strip('"')
        
        # Load batch optimizer settings
        patch_path = "dsl_thin_slice_patch.dsl"
        if Path(patch_path).exists():
            with open(patch_path, 'r') as f:
                patch_content = f.read()
                if 'batch_optimizer' in patch_content and 'enabled: true' in patch_content:
                    config['batch_optimizer_enabled'] = True
                    
        return config
    
    def _load_tasks(self, domain):
        """Load tasks for domain"""
        tasks = []
        task_dir = Path(f"tasks/{domain}")
        
        if task_dir.exists():
            for task_file in task_dir.glob("*.json"):
                with open(task_file, 'r') as f:
                    tasks.append(json.load(f))
        
        return tasks
    
    def run(self, domain=None):
        """Execute experiment plan with real components"""
        domain = domain or self.config['domain_profile']
        start_time = time.time()
        
        print(f"🚀 Donkey starting with domain: {domain}")
        print(f"💰 Budget: {self.config['budget_tokens']} tokens")
        print(f"🔧 Batch optimizer: {'enabled' if self.config['batch_optimizer_enabled'] else 'disabled'}")
        print(f"🧬 Mutations: enabled")
        
        # Load and mutate tasks
        tasks = self._load_tasks(domain)
        print(f"📋 Loaded {len(tasks)} tasks")
        
        # Apply mutations
        mutated_tasks = []
        for task in tasks:
            mutated = self.mutation_engine.mutate_task(task, domain)
            mutated_tasks.append(mutated)
        
        # Batch optimization
        if self.config['batch_optimizer_enabled']:
            batches = self.batch_optimizer.create_batches(
                mutated_tasks,
                self.adapter.estimate_tokens
            )
            print(f"📦 Created {len(batches)} batches")
        else:
            batches = [[task] for task in mutated_tasks]
        
        # Execute batches
        for batch_idx, batch in enumerate(batches):
            print(f"\n🔄 Processing batch {batch_idx + 1}/{len(batches)} ({len(batch)} tasks)")
            
            for task in batch:
                # Budget pre-flight check
                if not self.budget_enforcer.check_task(task):
                    print(f"⛔ Task {task['id']} blocked - would exceed budget")
                    continue
                    
                self._execute_task(task, domain)
        
        # Final report
        elapsed = time.time() - start_time
        self._print_trace(elapsed)
        self._generate_html_trace(elapsed)
        
    def _execute_task(self, task: Dict, domain: str):
        """Execute single task with real LLM"""
        print(f"  • Task {task['id']}: {task['prompt'][:40]}...")
        
        # Execute with adapter
        result = self.adapter.complete(task['prompt'])
        
        # Enforce budget
        self.budget_enforcer.consume(result['total_tokens'])
        
        # Record trace
        self.trace.append({
            "timestamp": datetime.now().isoformat(),
            "task_id": task['id'],
            "domain": domain,
            "prompt_tokens": result['prompt_tokens'],
            "response_tokens": result['response_tokens'],
            "total_tokens": result['total_tokens'],
            "response": result['text'][:100],
            "mutated": task['id'] in [m['task_id'] for m in self.mutation_engine.mutations_applied]
        })
        
        print(f"    ✅ {result['total_tokens']} tokens")
        
    def _print_trace(self, elapsed_time: float):
        """Print detailed execution trace"""
        print("\n" + "="*60)
        print("📊 EXECUTION TRACE")
        print("="*60)
        
        # Mutations applied
        if self.mutation_engine.mutations_applied:
            print("\n🧬 Mutations Applied:")
            for mutation in self.mutation_engine.mutations_applied:
                print(f"  - Task {mutation['task_id']}: {mutation['mutation']}")
        
        # Task execution
        print("\n📝 Task Execution:")
        for entry in self.trace:
            print(f"\n[{entry['timestamp']}] Task {entry['task_id']} ({'mutated' if entry['mutated'] else 'original'})")
            print(f"  Tokens: {entry['prompt_tokens']} + {entry['response_tokens']} = {entry['total_tokens']}")
            print(f"  Response: {entry['response']}")
        
        # Budget summary
        print("\n💰 Budget Summary:")
        print(f"  Allocated: {self.config['budget_tokens']} tokens")
        print(f"  Used: {self.budget_enforcer.used} tokens")
        print(f"  Remaining: {self.config['budget_tokens'] - self.budget_enforcer.used} tokens")
        
        if self.budget_enforcer.blocked_tasks:
            print(f"\n⛔ Blocked Tasks ({len(self.budget_enforcer.blocked_tasks)}):")
            for blocked in self.budget_enforcer.blocked_tasks:
                print(f"  - {blocked['task_id']}: needed {blocked['estimated_tokens']} tokens")
        
        # Performance
        print(f"\n⏱️  Execution time: {elapsed_time:.2f}s")
        print("="*60)
    
    def _generate_html_trace(self, elapsed_time: float):
        """Generate HTML trace viewer"""
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Donkey Trace - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: #333; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .section {{ background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .task {{ border-left: 4px solid #007aff; padding-left: 15px; margin: 15px 0; }}
        .mutated {{ border-left-color: #ff9500; }}
        .blocked {{ border-left-color: #ff3b30; opacity: 0.7; }}
        .token-bar {{ background: #e0e0e0; height: 20px; border-radius: 4px; margin: 5px 0; position: relative; }}
        .token-fill {{ background: #007aff; height: 100%; border-radius: 4px; }}
        .token-text {{ position: absolute; top: 0; left: 5px; line-height: 20px; font-size: 12px; }}
        .mutation {{ background: #fff3cd; padding: 10px; margin: 10px 0; border-radius: 4px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .stat-box {{ background: #f8f9fa; padding: 15px; border-radius: 4px; text-align: center; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #333; }}
        .stat-label {{ color: #666; font-size: 14px; }}
        pre {{ background: #f5f5f5; padding: 10px; border-radius: 4px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Donkey Execution Trace</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Duration: {elapsed_time:.2f}s</p>
        </div>
        
        <div class="section">
            <h2>📊 Summary Statistics</h2>
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-value">{len(self.trace)}</div>
                    <div class="stat-label">Tasks Executed</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{self.budget_enforcer.used}</div>
                    <div class="stat-label">Tokens Used</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{self.config['budget_tokens']}</div>
                    <div class="stat-label">Token Budget</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{len(self.mutation_engine.mutations_applied)}</div>
                    <div class="stat-label">Mutations Applied</div>
                </div>
            </div>
        </div>
"""
        
        if self.mutation_engine.mutations_applied:
            html_content += """
        <div class="section">
            <h2>🧬 Mutations Applied</h2>"""
            for mutation in self.mutation_engine.mutations_applied:
                html_content += f"""
            <div class="mutation">
                <strong>Task {mutation['task_id']}</strong> - {mutation['mutation']}
                <pre>Original: {mutation['original']}</pre>
                <pre>Mutated: {mutation['mutated']}</pre>
            </div>"""
            html_content += """
        </div>"""
        
        html_content += """
        <div class="section">
            <h2>📝 Task Execution Timeline</h2>"""
        
        for entry in self.trace:
            task_class = "task mutated" if entry['mutated'] else "task"
            token_percent = (entry['total_tokens'] / self.config['budget_tokens']) * 100
            
            html_content += f"""
            <div class="{task_class}">
                <h3>Task {entry['task_id']} {'🧬' if entry['mutated'] else ''}</h3>
                <p><strong>Time:</strong> {entry['timestamp']}</p>
                <p><strong>Tokens:</strong> {entry['prompt_tokens']} (prompt) + {entry['response_tokens']} (response) = {entry['total_tokens']} total</p>
                <div class="token-bar">
                    <div class="token-fill" style="width: {token_percent}%"></div>
                    <span class="token-text">{entry['total_tokens']} / {self.config['budget_tokens']}</span>
                </div>
                <p><strong>Response:</strong></p>
                <pre>{entry['response']}</pre>
            </div>"""
        
        if self.budget_enforcer.blocked_tasks:
            html_content += """
        </div>
        <div class="section">
            <h2>⛔ Blocked Tasks</h2>"""
            for blocked in self.budget_enforcer.blocked_tasks:
                html_content += f"""
            <div class="task blocked">
                <h3>Task {blocked['task_id']}</h3>
                <p>Would have needed {blocked['estimated_tokens']} tokens</p>
                <p>Budget remaining: {blocked['budget_remaining']} tokens</p>
            </div>"""
        
        html_content += """
        </div>
    </div>
</body>
</html>"""
        
        # Write to file
        with open("trace_latest.html", "w") as f:
            f.write(html_content)
        
        print(f"\n📄 HTML trace saved to: trace_latest.html")

def main():
    parser = argparse.ArgumentParser(description='Donkey Production Runner')
    parser.add_argument('command', nargs='?', default='run', help='Command to run')
    parser.add_argument('--domain', help='Domain profile to use')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        runner = DonkeyRunner()
        runner.run(domain=args.domain)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)

if __name__ == "__main__":
    main()