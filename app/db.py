from csv import DictReader, DictWriter
from pathlib import Path

import sqlite3


class Data:
    '''Store data in a Sqlite file'''

    def __init__(self, columns: tuple[str, ...], filename: Path):
        self.columns = columns
        self.key = columns[0] 
        self.filename = filename
        self.table = filename.stem 

    def init(self):
        self.connection = sqlite3.connect(self.filename)
        self.connection.row_factory = sqlite3.Row
        self.db = self.connection.cursor()
        create_table = 'CREATE TABLE IF NOT EXISTS {}{}'.format(self.table, repr(self.columns))
        create_index = 'CREATE UNIQUE INDEX IF NOT EXISTS index_{} ON {} ({})'.format(self.key, self.table, self.key)
        for command in (create_table, create_index): self.db.execute(command)
    
    def all(self):
        query = 'SELECT * FROM {} ORDER BY {} DESC'.format(self.table, self.key)

        return (dict(row) for row in self.db.execute(query).fetchall())

    def find(self, key: str) -> dict:
        query = "SELECT * FROM {} WHERE {} = '{}'".format(self.table, self.key, key)

        if row := self.db.execute(query).fetchone():
            return dict(row)

    def write(self, row: dict) -> None:
        columns = repr(tuple(row.keys()))
        values = repr(tuple(row.values()))
        command = 'INSERT INTO {}{} VALUES {}'.format(self.table, columns, values)
        self.db.execute(command)
        self.connection.commit()