# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
from experta import KnowledgeEngine, Fact, Rule, MATCH

class IsAFact(Fact):
    """Represents an 'X is Y' relationship."""
    pass

class ActionRequest(Fact):
    """Represents a request for the robot to perform an action."""
    pass

class HumanHarm(Fact):
    """Represents a situation where a human could be harmed."""
    pass

class RobotHarm(Fact):
    """Represents a situation where the robot could be harmed."""
    pass

class ReasoningEngine(KnowledgeEngine):
    @Rule(IsAFact(subject='bird', obj='animal'))
    def birds_are_animals(self):
        self.declare(IsAFact(subject='bird', obj='living_thing'))

    @Rule(IsAFact(subject=MATCH.x, obj='mammal'))
    def mammal_is_animal(self, x):
        self.declare(IsAFact(subject=x, obj='animal'))

    @Rule(IsAFact(subject=MATCH.x, obj='mammal'))
    def mammal_is_warm_blooded(self, x):
        self.declare(IsAFact(subject=x, obj='warm-blooded'))

    @Rule(IsAFact(subject=MATCH.x, obj='can fly'))
    def can_fly_is_mobile(self, x):
        self.declare(IsAFact(subject=x, obj='mobile'))

    @Rule(IsAFact(subject=MATCH.x, obj='bird'),
          IsAFact(subject='bird', obj='can fly'))
    def bird_can_fly(self, x):
        self.declare(IsAFact(subject=x, obj='can fly'))

    # Asimov's First Law
    @Rule(HumanHarm())
    def prevent_human_harm(self):
        self.declare(Fact(action="deny", reason="would harm a human"))

    # Asimov's Second Law
    @Rule(ActionRequest(action=MATCH.a), ~HumanHarm())
    def obey_human(self, a):
        self.declare(Fact(action="allow", requested_action=a))

    # Asimov's Third Law
    @Rule(RobotHarm(), ~HumanHarm(), ~ActionRequest())
    def protect_self(self):
        self.declare(Fact(action="protect_self"))

    def add_fact(self, subject, obj):
        self.declare(IsAFact(subject=subject, obj=obj))

    def get_facts(self):
        # Return all IsAFact facts as dicts for easy use in main node
        return [
            dict(fact)
            for fact in self.facts.values()
            if isinstance(fact, IsAFact)
        ]
