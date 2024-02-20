from datetime import date

from pytest import TempPathFactory, fixture
from db import Data
from models import Page

@fixture
def today() -> date:
    return date.today()

@fixture
def data(tmp_path_factory: TempPathFactory) -> Data:  # https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html#the-tmp-path-factory-fixture
    Page.data.filename=tmp_path_factory.mktemp('tmp') / 'pages.csv'
    Page.data.init()
    return Page.data

class TestPage:
    def test_save_stores_the_page_as_data(self, today: date, data: Data):
        page = Page(note='Hello', mood='happy')

        page.save()

        assert data.find(today) == { 'date': today, 'note': 'Hello', 'mood': 'happy' }

    def test_all_returns_all_stored_pages(self, today: date, data: Data):
        Page(note='Hello', mood='happy').save()
        Page(note='Hi', mood='neutral').save()

        pages = Page.all()

        assert vars(pages[0]) == { 'note': 'Hello', 'mood': 'happy', 'date': today }
        assert vars(pages[1]) == { 'note': 'Hi', 'mood': 'neutral', 'date': today }

    def test_find_returns_the_page_with_the_given_date_when_it_exists(self, today: date, data: Data):
        Page(note='Hello', mood='happy').save()

        page = Page.find(today)

        assert vars(page) == { 'date': today, 'note': 'Hello', 'mood': 'happy' }

    def test_find_returns_None_when_there_is_no_page_with_the_given_date(self, today: date, data: Data):
        assert Page.find(today) == None