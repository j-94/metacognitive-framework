#!/usr/bin/env python3
"""
Donkey - Minimal hello-world runner with mock adapter
"""
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

class MockAdapter:
    """Mock LLM adapter that returns canned responses"""
    def __init__(self):
        self.token_count = 0
        
    def complete(self, prompt, max_tokens=100):
        response = f"Mock response to: {prompt[:50]}..."
        self.token_count += len(prompt.split()) + len(response.split())
        return response

class DonkeyRunner:
    def __init__(self, config_path="dsl.experiment_plan.dsl"):
        self.config = self._load_config(config_path)
        self.adapter = MockAdapter()
        self.trace = []
        
    def _load_config(self, path):
        """Parse DSL config (simplified)"""
        config = {
            "id": "donkey_first_principles_boot",
            "budget_tokens": 1000,
            "domain_profile": "math"
        }
        
        if Path(path).exists():
            with open(path, 'r') as f:
                content = f.read()
                if 'budget_tokens:' in content:
                    for line in content.split('\n'):
                        if 'budget_tokens:' in line:
                            config['budget_tokens'] = int(line.split(':')[1].strip())
                        elif 'domain_profile:' in line:
                            config['domain_profile'] = line.split(':')[1].strip().strip('"')
        
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
        """Execute experiment plan"""
        domain = domain or self.config['domain_profile']
        print(f"🚀 Donkey starting with domain: {domain}")
        print(f"💰 Budget: {self.config['budget_tokens']} tokens")
        
        # Load tasks
        tasks = self._load_tasks(domain)
        print(f"📋 Loaded {len(tasks)} tasks")
        
        # Execute tasks
        for task in tasks:
            self._execute_task(task)
            
            # Check budget
            if self.adapter.token_count > self.config['budget_tokens']:
                print(f"⚠️  Budget exceeded! Used {self.adapter.token_count} tokens")
                break
        
        # Print trace
        self._print_trace()
        
    def _execute_task(self, task):
        """Execute single task"""
        start_tokens = self.adapter.token_count
        
        print(f"\n🔄 Task {task['id']}: {task['prompt'][:50]}...")
        response = self.adapter.complete(task['prompt'])
        
        tokens_used = self.adapter.token_count - start_tokens
        
        self.trace.append({
            "timestamp": datetime.now().isoformat(),
            "task_id": task['id'],
            "tokens_used": tokens_used,
            "response": response[:100]
        })
        
        print(f"✅ Complete ({tokens_used} tokens)")
        
    def _print_trace(self):
        """Print execution trace"""
        print("\n📊 Execution Trace:")
        print("-" * 60)
        
        for entry in self.trace:
            print(f"[{entry['timestamp']}] Task {entry['task_id']}")
            print(f"  Tokens: {entry['tokens_used']}")
            print(f"  Response: {entry['response']}")
        
        print("-" * 60)
        print(f"Total tokens used: {self.adapter.token_count}/{self.config['budget_tokens']}")

def main():
    parser = argparse.ArgumentParser(description='Donkey Experiment Runner')
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