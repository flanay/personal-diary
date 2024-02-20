from csv import DictReader, DictWriter
from pathlib import Path


class Data:
    """Abstracts the interaction with a CSV file, to write and read data."""
    def __init__(self, columns: dict[str], primary_key: str, filename: Path):
        self.columns = columns
        self.primary_key = primary_key
        self.filename = filename

    def init(self):
        """Creates the storage file with the specified columns as header."""
        open(self.filename, 'a').close()

        with open(self.filename, "r+", newline='') as file:
            writer = DictWriter(file, fieldnames=self.columns.keys())
            writer.writeheader()

    
    def all(self):
        with open(self.filename, 'r') as file:
            reader = DictReader(file, fieldnames=self.columns.keys())
            next(reader)
            return tuple(self._with_typed_values(row) for row in reader)


    def find(self, key: str) -> dict:
        """Iterates over each row in the storage file and returns a row containing the given key as a dict when it exists, or an empty dict otherwise."""
        with open(self.filename, 'r') as file:
            for row in DictReader(file):
                row = self._with_typed_values(row)
                
                if row[self.primary_key] == key:
                    return row
        
        return {}

    def write(self, row: dict) -> None:
        """Writes the given `dict` as a row in the storage file."""
        with open(self.filename, 'a', newline='') as file:
            DictWriter(file, fieldnames=self.columns.keys()).writerow(row)
    
    def _with_typed_values(self, row: dict[str]) -> dict[str]:
        return { key : self.columns[key](value) for key, value in row.items() } # dict comprehension: https://peps.python.org/pep-0274/