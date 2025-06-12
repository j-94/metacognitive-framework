"""
Example usage of MetaCognitive Framework
"""
from core.base import MetaCognitiveSystem
from experiments.unified_system.unified_metacognitive_framework import UnifiedMetaCognitiveSystem

def main():
    # Create system
    system = UnifiedMetaCognitiveSystem()
    
    # Example problem
    problem = {
        "type": "logical_inference",
        "premise": "All birds can fly",
        "fact": "Penguins are birds",
        "conclusion": "Penguins can fly"
    }
    
    # Process through system
    result = system.process_problem(problem)
    
    # Display results
    print("MetaCognitive Framework Demo")
    print("=" * 40)
    print(f"Problem: {problem['premise']} + {problem['fact']} → {problem['conclusion']}")
    print(f"Rigor Score: {result['achievement_metrics']['rigor']:.1%}")
    print(f"Adaptability: {result['achievement_metrics']['adaptability']:.1%}")
    print(f"Combined: {result['achievement_metrics']['combined']:.1%}")

if __name__ == "__main__":
    main()
