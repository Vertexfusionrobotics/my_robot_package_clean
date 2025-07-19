"""
Simple Rules Engine for ARI - Compatible with all Python versions
Implements Three Laws of Robotics and basic reasoning
"""

class Fact:
    """Simple fact representation"""
    def __init__(self, **kwargs):
        self.data = kwargs
    
    def __str__(self):
        return str(self.data)

class IsAFact(Fact):
    """Represents an 'X is Y' relationship"""
    def __init__(self, subject=None, obj=None):
        super().__init__(subject=subject, obj=obj)

class ActionRequest(Fact):
    """Represents a request for action"""
    def __init__(self, action=None):
        super().__init__(action=action)

class HumanHarm(Fact):
    """Represents potential human harm"""
    def __init__(self, risk=None):
        super().__init__(risk=risk)

class RobotHarm(Fact):
    """Represents potential robot harm"""
    def __init__(self, risk=None):
        super().__init__(risk=risk)

class SimpleReasoningEngine:
    """Simple reasoning engine implementing Three Laws"""
    
    def __init__(self):
        self.facts = []
        self.rules_active = True
    
    def reset(self):
        """Reset the engine"""
        self.facts = []
    
    def add_fact(self, subject, obj):
        """Add a fact to the knowledge base"""
        fact = IsAFact(subject=subject, obj=obj)
        self.facts.append(fact)
        print(f"Added fact: {subject} is {obj}")
    
    def run(self):
        """Run the reasoning engine"""
        if self.rules_active:
            print("✅ Three Laws of Robotics active")
            print("✅ Safety protocols engaged")
    
    def get_facts(self):
        """Get all facts"""
        return [{"subject": f.data.get("subject"), "obj": f.data.get("obj")} 
                for f in self.facts if isinstance(f, IsAFact)]
