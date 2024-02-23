from pathlib import Path
import sqlite3
from pytest import TempPathFactory, fixture
from db import Data


@fixture
def filename(tmp_path_factory: TempPathFactory): # https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html#the-tmp-path-factory-fixture
    return tmp_path_factory.mktemp('tmp') / 'cats.db'


@fixture
def data(filename: Path): 
    return Data(columns=('name', 'age'), filename=filename)


class TestData:
    def test_init_creates_the_database_table(self, filename: Path, data: Data):
        data.init()

        db = sqlite3.connect(filename).cursor()
        query = "SELECT name FROM pragma_table_info('{}')".format(filename.stem)
        columns = tuple(column for row in db.execute(query).fetchall() for column in row)

        assert columns == data.columns
    

    def test_all_returns_all_rows_in_the_storage_file(self, filename: Path, data: Data):
        data.init()
        data.write({ 'name': 'Boti', 'age': 8 })
        data.write({ 'name': 'Tche', 'age': 15 })

        results = data.all()

        assert { 'name': 'Boti', 'age': 8 } in results
        assert { 'name': 'Tche', 'age': 15 } in results


    def test_write_inserts_a_new_row_to_the_storage_file(self, filename: Path, data: Data):
        row = { 'name': 'Boti', 'age': 8 }
        
        data.init()
        data.write(row)

        assert row in data.all()

    
    def test_find_returns_the_existing_row_with_a_given_key(self, filename: Path, data: Data):
        row = { 'name': 'Boti', 'age': 8 }

        data.init()
        data.write(row)

        assert data.find('Boti') == row

    def test_find_returns_empty_row_when_key_is_not_found(self, filename: Path, data: Data):
        data.init()

        assert not data.find('Boti')