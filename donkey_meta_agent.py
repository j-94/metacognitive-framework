#!/usr/bin/env python3
"""
Donkey Meta-Agent - High-level DSL instruction processor
Converts DSL commands into concrete repository operations
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

class DSLParser:
    """Parse and validate DSL commands"""
    
    def __init__(self):
        self.patterns = {
            'experiment_plan': r'dsl\.experiment_plan\s*{([^}]+)}',
            'domain_profiles': r'dsl\.domain_profiles\s*{([^}]+)}',
            'batch_optimizer': r'dsl\.batch_optimizer\s*{([^}]+)}',
            'budget_estimator': r'dsl\.budget_estimator\s*{([^}]+)}',
            'command': r'/project:(\w+)(?:\s+(.*))?',
            'include': r'include\s+"([^"]+)"'
        }
        
    def parse_file(self, filepath: Path) -> Dict[str, Any]:
        """Parse a DSL file and extract all configurations"""
        if not filepath.exists():
            raise FileNotFoundError(f"DSL file not found: {filepath}")
            
        with open(filepath, 'r') as f:
            content = f.read()
            
        result = {'includes': [], 'configs': {}}
        
        # Parse includes
        for match in re.finditer(self.patterns['include'], content):
            result['includes'].append(match.group(1))
            
        # Parse each configuration block
        for config_type, pattern in self.patterns.items():
            if config_type in ['command', 'include']:
                continue
                
            match = re.search(pattern, content, re.DOTALL)
            if match:
                config_content = match.group(1)
                result['configs'][config_type] = self._parse_config_block(config_content)
                
        return result
        
    def _parse_config_block(self, content: str) -> Dict[str, Any]:
        """Parse configuration block content"""
        config = {}
        
        # Simple key-value parsing
        for line in content.split('\n'):
            line = line.strip()
            if ':' in line and not line.startswith('#'):
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().rstrip(',')
                
                # Handle different value types
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                elif value.isdigit():
                    value = int(value)
                elif '.' in value and value.replace('.', '').isdigit():
                    value = float(value)
                    
                config[key] = value
                
        return config


class RepoOperator:
    """Execute repository operations based on DSL commands"""
    
    def __init__(self, root_path: Path):
        self.root_path = root_path
        
    def create_domain(self, domain_name: str) -> Dict[str, Any]:
        """Scaffold a new domain with DSL plan and task directory"""
        result = {
            'domain': domain_name,
            'created': [],
            'errors': []
        }
        
        # Create domain plan
        plan_path = self.root_path / 'examples' / f'{domain_name}_plan.dsl'
        if not plan_path.exists():
            plan_content = f"""# {domain_name.title()} Domain Plan
dsl.domain_plan {{
  domain: "{domain_name}"
  description: "Tasks for {domain_name} domain"
  default_budget: 500
  tasks: []
}}
"""
            plan_path.parent.mkdir(exist_ok=True)
            plan_path.write_text(plan_content)
            result['created'].append(str(plan_path))
            
        # Create task directory
        task_dir = self.root_path / 'tasks' / domain_name
        if not task_dir.exists():
            task_dir.mkdir(parents=True, exist_ok=True)
            result['created'].append(str(task_dir))
            
            # Create example task
            example_task = task_dir / 'task1.json'
            example_task.write_text(json.dumps({
                'id': f'{domain_name[0]}1',
                'domain': domain_name,
                'prompt': f'Example {domain_name} task',
                'max_tokens': 100
            }, indent=2))
            result['created'].append(str(example_task))
            
        return result
        
    def analyze_budget(self, domain: Optional[str] = None) -> Dict[str, Any]:
        """Analyze token budget usage across domains"""
        result = {
            'domains': {},
            'total_budget': 0,
            'total_tasks': 0
        }
        
        task_dirs = [self.root_path / 'tasks' / domain] if domain else \
                   [d for d in (self.root_path / 'tasks').iterdir() if d.is_dir()]
                   
        for task_dir in task_dirs:
            if not task_dir.exists():
                continue
                
            domain_name = task_dir.name
            domain_stats = {
                'tasks': 0,
                'estimated_tokens': 0,
                'task_details': []
            }
            
            for task_file in task_dir.glob('*.json'):
                try:
                    with open(task_file) as f:
                        task = json.load(f)
                        
                    tokens = task.get('max_tokens', 100)
                    prompt_tokens = len(task.get('prompt', '')) // 4  # Rough estimate
                    
                    domain_stats['tasks'] += 1
                    domain_stats['estimated_tokens'] += tokens + prompt_tokens
                    domain_stats['task_details'].append({
                        'id': task.get('id', 'unknown'),
                        'tokens': tokens + prompt_tokens
                    })
                except Exception as e:
                    pass
                    
            result['domains'][domain_name] = domain_stats
            result['total_tasks'] += domain_stats['tasks']
            result['total_budget'] += domain_stats['estimated_tokens']
            
        return result


class DonkeyMetaAgent:
    """Main meta-agent orchestrator"""
    
    def __init__(self, root_path: Path = Path.cwd()):
        self.root_path = root_path
        self.parser = DSLParser()
        self.operator = RepoOperator(root_path)
        self.trace = []
        
    def execute_command(self, command: str) -> Dict[str, Any]:
        """Execute a slash command"""
        match = re.match(r'/project:(\w+)(?:\s+(.*))?', command)
        if not match:
            return {'error': f'Invalid command format: {command}'}
            
        cmd_name = match.group(1)
        args = match.group(2) or ''
        
        handlers = {
            'add_domain': lambda: self.operator.create_domain(args),
            'analyze_budget': lambda: self.operator.analyze_budget(args if args else None),
            'validate': lambda: self.validate_dsl_files(),
            'run': lambda: self.run_experiment(args)
        }
        
        if cmd_name not in handlers:
            return {'error': f'Unknown command: {cmd_name}'}
            
        return handlers[cmd_name]()
        
    def validate_dsl_files(self) -> Dict[str, Any]:
        """Validate all DSL files in the project"""
        result = {
            'valid': [],
            'invalid': [],
            'errors': []
        }
        
        dsl_files = list(self.root_path.glob('**/*.dsl'))
        
        for dsl_file in dsl_files:
            try:
                parsed = self.parser.parse_file(dsl_file)
                result['valid'].append(str(dsl_file))
                
                # Validate includes exist
                for include in parsed['includes']:
                    include_path = dsl_file.parent / include
                    if not include_path.exists():
                        result['errors'].append(f"Missing include: {include} in {dsl_file}")
            except Exception as e:
                result['invalid'].append(str(dsl_file))
                result['errors'].append(f"{dsl_file}: {str(e)}")
                
        return result
        
    def run_experiment(self, domain: str = 'math') -> Dict[str, Any]:
        """Run an experiment for a specific domain"""
        # Parse main experiment plan
        main_plan = self.root_path / 'dsl.experiment_plan.dsl'
        config = self.parser.parse_file(main_plan)
        
        # Get experiment configuration
        exp_config = config['configs'].get('experiment_plan', {})
        exp_config['domain_profile'] = domain
        
        # Load domain configuration
        domain_plan_path = self.root_path / 'examples' / f'{domain}_plan.dsl'
        if domain_plan_path.exists():
            domain_config = self.parser.parse_file(domain_plan_path)
            exp_config.update(domain_config['configs'].get('domain_plan', {}))
            
        # Execute with donkey_real.py
        cmd = [
            sys.executable,
            str(self.root_path / 'donkey_real.py'),
            '--domain', domain
        ]
        
        if 'budget_tokens' in exp_config:
            cmd.extend(['--budget', str(exp_config['budget_tokens'])])
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return {
            'domain': domain,
            'config': exp_config,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
        
    def get_trace(self) -> List[Dict[str, Any]]:
        """Get execution trace"""
        return self.trace


def main():
    """CLI interface for meta-agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Donkey Meta-Agent')
    parser.add_argument('command', help='Command to execute (e.g., /project:add_domain newdom)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    agent = DonkeyMetaAgent()
    result = agent.execute_command(args.command)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        # Pretty print result
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
        elif 'created' in result:
            print(f"✅ Created domain '{result['domain']}':")
            for path in result['created']:
                print(f"  • {path}")
        elif 'domains' in result:
            print("📊 Budget Analysis:")
            for domain, stats in result['domains'].items():
                print(f"\n{domain}:")
                print(f"  Tasks: {stats['tasks']}")
                print(f"  Estimated tokens: {stats['estimated_tokens']}")
        elif 'valid' in result:
            print(f"✅ Valid DSL files: {len(result['valid'])}")
            if result['invalid']:
                print(f"❌ Invalid DSL files: {len(result['invalid'])}")
                for error in result['errors']:
                    print(f"  • {error}")
        else:
            print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()