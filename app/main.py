from models import Page
from views import App


if __name__ == '__main__':
    Page.data.init()
    App('Personal Diary').render()