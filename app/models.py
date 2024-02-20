from pathlib import Path
from db import Data
from datetime import date


class Page:
    """Represents a page in the diary, and can be saved or found."""
    # class attribute
    # date.fromisoformat: https://note.nkmk.me/en/python-datetime-isoformat-fromisoformat/
    data = Data(columns={ 'date': date.fromisoformat, 'note': str, 'mood': str }, primary_key='date', filename=Path('db/pages.csv'))

    def __init__(self, note: str, mood: str, date=date.today()):
        self.note = note
        self.mood = mood
        self.date = date
    
    def save(self):
        """Stores itself in a file."""
        self.data.write(vars(self))

    @classmethod
    def all(cls):
        return tuple(Page(**row) for row in cls.data.all())

    @classmethod
    def find(cls, date: date):
        """Finds a stored Page with the given date and returns it when found. Otherwise, returns None."""
        if row := cls.data.find(date): # https://docs.python.org/3/reference/expressions.html#assignment-expressions
            return cls(**row) # dict unpacking: https://peps.python.org/pep-0448/