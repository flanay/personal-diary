from models import Page
from views import Window


if __name__ == '__main__':
    Page.data.init()
    Window('Personal Diary').render()