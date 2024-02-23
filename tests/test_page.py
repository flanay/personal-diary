from datetime import date

from pytest import TempPathFactory, fixture
from db import Data
from models import Page

@fixture
def today() -> str:
    return date.today().isoformat()

@fixture
def data(tmp_path_factory: TempPathFactory) -> Data:  # https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html#the-tmp-path-factory-fixture
    Page.data.filename=tmp_path_factory.mktemp('tmp') / 'pages.db'
    Page.data.init()
    return Page.data

class TestPage:
    def test_save_stores_the_page_as_data(self, today: str, data: Data):
        page = Page(note='Hello', mood='happy')

        page.save()

        assert data.find(today) == { 'date': today, 'note': 'Hello', 'mood': 'happy' }

    def test_all_returns_all_stored_pages(self, today: str, data: Data):
        Page(note='Hello', mood='happy', date='2024-02-20').save()
        Page(note='Hi', mood='neutral', date='2024-02-21').save()

        pages = Page.all()

        assert vars(pages[0]) == { 'note': 'Hello', 'mood': 'happy', 'date': '2024-02-20' }
        assert vars(pages[1]) == { 'note': 'Hi', 'mood': 'neutral', 'date': '2024-02-21' }

    def test_find_returns_the_page_with_the_given_date_when_it_exists(self, today: str, data: Data):
        Page(note='Hello', mood='happy').save()

        page = Page.find(today)

        assert vars(page) == { 'date': today, 'note': 'Hello', 'mood': 'happy' }

    def test_find_returns_None_when_there_is_no_page_with_the_given_date(self, today: str, data: Data):
        assert Page.find(today) == None