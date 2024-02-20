from pathlib import Path
from pytest import TempPathFactory, fixture
from db import Data


@fixture
def filename(tmp_path_factory: TempPathFactory): # https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html#the-tmp-path-factory-fixture
    return tmp_path_factory.mktemp('tmp') / 'cats.csv'


@fixture
def data(filename: Path): 
    return Data(columns={ 'name': str, 'age': int }, primary_key='name', filename=filename)


def read_lines(filename: str):
    with open(filename, 'r') as file:
        return file.readlines()


class TestData:
    def test_init_creates_an_empty_file_with_the_specified_columns_as_header(self, filename: Path, data: Data):
        data.init()

        assert read_lines(filename) == ['name,age\n']
    

    def test_all_returns_all_rows_in_the_storage_file(self, filename: Path, data: Data):
        data.init()
        data.write({ 'name': 'Boti', 'age': 8 })
        data.write({ 'name': 'Tche', 'age': 15 })

        assert data.all() == ({ 'name': 'Boti', 'age': 8 }, { 'name': 'Tche', 'age': 15 })


    def test_write_inserts_a_new_row_to_the_storage_file(self, filename: Path, data: Data):
        data.write({ 'name': 'Boti', 'age': 8 })

        assert 'Boti,8\n' in read_lines(filename)

    
    def test_find_returns_the_existing_row_with_a_given_key(self, filename: Path, data: Data):
        data.init()
        data.write({ 'name': 'Boti', 'age': 8 })

        assert data.find('Boti') == { 'name': 'Boti', 'age': 8 }

    def test_find_returns_empty_row_when_key_is_not_found(self, filename: Path, data: Data):
        data.init()

        assert not data.find('Boti')