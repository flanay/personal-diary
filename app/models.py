from pathlib import Path
from db import Data
from datetime import date


class Page:
    """Represents a page in the diary, and can be saved or retrieved."""
    # class attribute
    data = Data(columns=('date', 'note', 'mood'), filename=Path('db/pages.db'))

    def __init__(self, note: str, mood: str, date=date.today().isoformat()):
        self.note = note
        self.mood = mood
        self.date = date
    
    def save(self):
        """Stores itself."""
        self.data.write(vars(self))

    @classmethod # https://docs.python.org/3/library/functions.html#classmethod
    def all(cls):
        """Returns all stored pages."""
        return tuple(cls(**row) for row in cls.data.all())

    @classmethod
    def find(cls, date: date):
        """Finds a stored Page with the given date and returns it when found. Otherwise, returns None."""
        if row := cls.data.find(date): # https://docs.python.org/3/reference/expressions.html#assignment-expressions
            return cls(**row) # dict unpacking: https://peps.python.org/pep-0448/