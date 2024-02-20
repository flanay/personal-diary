from tkinter import Button, Frame, Label, LabelFrame, Message, Radiobutton, StringVar, Text, Tk, Toplevel, messagebox
from typing import Callable

from models import Page


class Centralizable:
    def center(self):
        screen_height = self.root.winfo_screenheight()
        screen_width = self.root.winfo_screenwidth()
        x = (screen_width / 2) - (self.width / 2)
        y = (screen_height / 2) - (self.height / 2)
        self.root.geometry("%dx%d+%d+%d" % (self.width, self.height, x, y))


class NoteField:
    def __init__(self, parent: Frame, label='Tell me about your day'):
        self.label_frame = LabelFrame(parent, text=label)
        self.text = Text(self.label_frame)
        
    def render(self):
        self.label_frame.pack()
        self.text.pack(padx=10, pady=10)

    def get(self): return self.text.get('1.0', 'end').strip()


class MoodField:
    moods = ('neutral', 'happy', 'sad')

    def __init__(self, parent: Frame, label='How is your mood?'):
        self.var = StringVar(value=self.moods[0])
        self.label_frame = LabelFrame(parent, text=label)
        self.mood_buttons = (self._build_mood_button(self.label_frame, mood) for mood in self.moods)

    def render(self):
        self.label_frame.pack(fill='x', expand=True)
        for button in self.mood_buttons: button.pack(side='left', padx=10, pady=10)
            
    def get(self): return self.var.get()

    def _build_mood_button(self, parent: Frame, mood: str):
        return Radiobutton(parent, text=mood.capitalize(), variable=self.var, value=mood)


class SaveButton:
    def __init__(self, parent: Frame, command: Callable, text='Save'):
        self.command = command
        self.button = Button(parent, text=text, command=self.command)
    
    def render(self):
        self.button.pack(side='right', pady=5)


class LogNote:
    def __init__(self, parent: Frame, note: str):
        self.frame = Frame(parent)
        self.note_label = Label(self.frame, text='Note: ')
        self.note_text = Message(self.frame, text=note, width=500)

    def render(self):
        self.frame.pack(fill='x', padx=10, pady=10)
        self.note_label.pack(side='left')
        self.note_text.pack(side='left')


class LogMood:
    def __init__(self, parent: Frame, mood: str):
        self.frame = Frame(parent)
        self.mood_label = Label(self.frame, text='Mood: ')
        self.mood_text = Message(self.frame, text=mood, width=500)

    def render(self):
        self.frame.pack(fill='x', padx=10, pady=10)
        self.mood_label.pack(side='left')
        self.mood_text.pack(side='left')


class LogEntry:
    def __init__(self, parent: Frame, page: Page):
        self.frame = LabelFrame(parent, text=page.date)
        self.note = LogNote(self.frame, page.note)
        self.mood = LogMood(self.frame, page.mood.capitalize())
    
    def render(self):
        self.frame.pack(side='top', fill="both", expand=True)
        self.note.render()
        self.mood.render()


class Log(Centralizable):
    def __init__(self, parent: Frame, height=550, width=600):
        self.width = width
        self.height = height
        self.root = Toplevel(parent, height=height, width=width)
        self.root.title('Page Log')
        self.frame = Frame(self.root)
        self.entries = (LogEntry(self.frame, page) for page in Page.all())

    def render(self):
        self.center()
        for entry in self.entries: entry.render()
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)


class ShowLogButton:
    def __init__(self, parent: Frame, text='Show log'):
        self.button = Button(parent, text=text, command=lambda: { Log(parent).render() })
    
    def render(self):
        self.button.pack(side='left', pady=5)


class PageForm:
    def __init__(self, parent: Frame, title='My Diary'):
        self.title = title
        self.note_field = NoteField(parent)
        self.mood_field = MoodField(parent)
        self.save_button = SaveButton(parent, command=lambda: { self.save() })
        self.show_log_button = ShowLogButton(parent)
    
    def render(self):
        self.note_field.render()
        self.mood_field.render()
        self.save_button.render()
        self.show_log_button.render()
    
    def save(self):
        Page(note=self.note_field.get(), mood=self.mood_field.get()).save()
        messagebox.showinfo("Save", "Your page was saved with success.")


class Window(Centralizable):
    def __init__(self, title='Personal Diary', height=550, width=600):
        self.root = Tk()
        self.root.title(title)
        self.root_frame = Frame(self.root)
        self.frame = PageForm(self.root_frame)
        self.height = height
        self.width = width
    
    def render(self):
        self.center()
        self.root_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.frame.render()
        self.root.mainloop()