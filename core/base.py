"""
Base classes for MetaCognitive Framework
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any

class MetaCognitivePath(ABC):
    """Base class for all metacognitive reasoning paths"""
    
    def __init__(self, name: str):
        self.name = name
        self.metrics = {}
        
    @abstractmethod
    def capture(self, input_data: Any) -> Dict[str, Any]:
        """Capture reasoning in this path's representation"""
        pass
        
    @abstractmethod
    def evolve(self, captured_data: Dict[str, Any], 
               validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Evolve the reasoning approach"""
        pass
        
    @abstractmethod
    def validate(self, reasoning: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the reasoning quality"""
        pass
        
    @abstractmethod
    def teach(self, validated_reasoning: Dict[str, Any]) -> Dict[str, Any]:
        """Create teaching materials"""
        pass

class MetaCognitiveSystem:
    """Main system for managing paths"""
    
    def __init__(self):
        self.paths = {}
        
    def register_path(self, name: str, path: MetaCognitivePath):
        """Register a new reasoning path"""
        self.paths[name] = path
        
    def process(self, input_data: Any, path_name: str) -> Dict[str, Any]:
        """Process input through a specific path"""
        if path_name not in self.paths:
            raise ValueError(f"Unknown path: {path_name}")
            
        path = self.paths[path_name]
        
        # Full pipeline
        captured = path.capture(input_data)
        validated = path.validate(captured)
        evolved = path.evolve(captured, validated)
        teaching = path.teach(evolved)
        
        return {
            "captured": captured,
            "validated": validated,
            "evolved": evolved,
            "teaching": teaching
        }
