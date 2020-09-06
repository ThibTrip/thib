This demonstrates how to split a class in multiple modules (with an added difficulty as explained in the presentation "Python lightning talks" where a brain is required to move the legs).

# Usage

```python
from human import Human

human = Human()

human.legs.move()
'ᕕ( ᐛ )ᕗ'

human.community.name
'Python User Group Freiburg'

human.community.organize_python_meetup(subject='pandas crash course')
'Wow cool, thanks for organizing the Python Meetup "pandas crash course" 🐔!'
```

# Testing

You can test the examples in the docstrings with the awesome library <code>pytest</code> (install with <code>pip install pytest</code>). The name <code>doctest</code> in the commands refers to a library in the standard Python library that you can use to test examples in docstrings.

```
pytest -v --doctest-modules --doctest-continue-on-failure
```