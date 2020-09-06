# -*- coding: utf-8 -*-
# +
from brain import Brain
from community import Community
from legs import Legs

class Human():
    """
    Example that demonstrates how to split a class in multiple modules.
    The human belongs to a community, has a pair of legs and the legs
    need a brain to work.

    Attributes
    ----------
    legs : legs.Legs
        An instance of the class legs.Legs, see its docstring
    community : community.Community
        The class community.Community, see its docstring

    Examples
    --------
    >>> from human import Human
    >>> human = Human()
    >>> human.legs.move()
    ᕕ( ᐛ )ᕗ

    >>> human.community.name
    'Python User Group Freiburg'

    >>> human.community.organize_python_meetup(subject='pandas crash course')
    Wow cool, thanks for organizing the Python Meetup "pandas crash course" 🐔!
    """
    # everyone has the same community so this can be a class attribute
    community = Community

    # however every individual has a different brain and a different pair of legs
    # so they both have to belong to the instance
    def __init__(self):
        # we do not need to expose this to the user ('_X' means its private and not supposed to be used)
        self._brain = Brain() 
        self.legs = Legs(brain=self._brain)
