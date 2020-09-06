# -*- coding: utf-8 -*-
class Community:
    """
    A community of Python users.

    Attributes
    ----------
    name : str
        Name of the community
    """
    name = "Python User Group Freiburg"

    @classmethod
    def organize_python_meetup(cls, subject):
        """
        Organizes a Python Meetup.

        Parameters
        ----------
        subject : str
            Subject of the Meetup

        Examples
        --------
        >>> Community.organize_python_meetup(subject='some Meetup')
        Wow cool, thanks for organizing the Python Meetup "some Meetup" 🐔!
        """
        print(f'Wow cool, thanks for organizing the Python Meetup "{subject}" 🐔!')
