class Brain():
    """
    Creates a brain for a human.

    Attributes
    ----------
    nb_neurons : int
        See Parameters

    Parameters
    ----------
    nb_neurons : int, default 8.6e10
        Number of neurons of the brain.

    Examples
    --------
    >>> brain = Brain()
    >>> brain.execute_command('do stuff')
    do stuff
    """
    def __init__(self, nb_neurons:int=8.6e10):
        self.number_of_neurons = nb_neurons

    def execute_command(self, command):
        print(command)
