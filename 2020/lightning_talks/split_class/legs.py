# -*- coding: utf-8 -*-
# +
from brain import Brain # this is only used for type hints

class Legs():
    """
    Legs of a human.

    Parameters
    ----------
    brain: brain.Brain
        Brain that is used to order the legs to move.

    Examples
    --------
    >>> from brain import Brain
    >>>
    >>> brain = Brain()
    >>> legs = Legs(brain=brain)
    >>> legs.move()
    ᕕ( ᐛ )ᕗ
    """
    def __init__(self, brain:Brain):
        self.brain = brain
    
    def move(self):
        self.brain.execute_command('ᕕ( ᐛ )ᕗ')
