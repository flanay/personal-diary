import pyjokes
from collections import Counter
from datetime import date
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap import Button, DateEntry, Label, LabelFrame, Notebook, Frame, StringVar, Radiobutton, Text, Window
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.constants import *
from typing import Callable

from models import Page


class DateField:
    def __init__(self, parent: Frame, label='Date'):
        self.label_frame = LabelFrame(parent, text=label, borderwidth=0)
        self.var = StringVar(value=date.today().isoformat())
        self.date_entry = DateEntry(self.label_frame, dateformat='%Y-%m-%d')
        self.date_entry.entry.configure(textvariable=self.var)

    def render(self):
        self.label_frame.pack(fill=X, expand=True, padx=10, pady=10)
        self.date_entry.pack(side=LEFT, padx=10, pady=10)

    def get(self): return self.var.get()
    def set(self, value: str): self.var.set(value)

class NoteField:
    def __init__(self, parent: Frame, label='Tell me about your day'):
        self.label_frame = LabelFrame(parent, text=label, borderwidth=0)
        self.text = Text(self.label_frame, height=10)

    def render(self):
        self.label_frame.pack(fill=X, expand=True, padx=10, pady=10)
        self.text.pack(side=LEFT, fill=X, expand=True,padx=10, pady=10)

    def get(self): return self.text.get('1.0', END).strip()
    def set(self, value: str):
        self.text.delete('1.0', END)
        self.text.insert(END, value)

class MoodField:
    moods = ('neutral', 'happy', 'sad')  # class attribute

    def __init__(self, parent: Frame, label='How is your mood?'):
        self.var = StringVar(value=self.moods[0])
        self.label_frame = LabelFrame(parent, text=label, borderwidth=0)
        self.mood_buttons = (self.build_mood_button(
            self.label_frame, mood) for mood in self.moods)

    def render(self):
        self.label_frame.pack(fill=X, expand=True, padx=10, pady=10)
        for button in self.mood_buttons:
            button.pack(side='left', padx=10, pady=(10, 0))

    def get(self): return self.var.get()
    def set(self, value: str): self.var.set(value)

    def build_mood_button(self, parent: Frame, mood: str):
        return Radiobutton(parent, text=mood.capitalize(), variable=self.var, value=mood)
    

class SaveButton:
    def __init__(self, parent: Frame, command: Callable, text='Save'):
        self.command = command
        self.button = Button(parent, text=text, command=self.command, style=SUCCESS)

    def render(self):
        self.button.pack(side='right', padx=20, pady=(0, 20))


class PageForm:
    def __init__(self, parent: Notebook, title='Page', on_save=lambda: {}):
        self.title = title
        self.parent = parent
        self.frame = Frame(parent)
        self.date_field = DateField(self.frame)
        self.date_field.var.trace_add('write', callback=lambda *args: {self.update_fields()})
        self.note_field = NoteField(self.frame)
        self.mood_field = MoodField(self.frame)
        self.on_save = on_save
        self.save_button = SaveButton(self.frame, command=lambda: {self.save()})

    def render(self):
        self.update_fields()
        self.date_field.render()
        self.note_field.render()
        self.mood_field.render()
        self.save_button.render()
        self.frame.pack(fill='both', expand=True)
        self.parent.add(self.frame, text=self.title)

    def save(self):
        self.on_save()
        Page(date=self.date_field.get(), note=self.note_field.get(), mood=self.mood_field.get()).save()

        mood = self.mood_field.get()

        if mood == 'sad':
            message = "Here is a joke to lift your mood:\n" + pyjokes.get_joke()
        elif mood == 'neutral':
            message = "Neutral is better than sad"
        elif mood == 'happy':
            message = "I'm glad to hear that you are happy"
        Messagebox.show_info(title="Save", message=message)

    def update_fields(self):
        if page := Page.find(self.date_field.get()):
            self.note_field.set(page.note)
            self.mood_field.set(page.mood)
        else:
            self.note_field.set('')
            self.mood_field.set('')


class LogNote:
    def __init__(self, parent: Frame, note: str):
        self.frame = Frame(parent)
        self.note_label = Label(self.frame, text='Note: ')
        self.note_text = Label(self.frame, text=note, width=70, wraplength=550)

    def render(self):
        self.frame.pack(fill=X)
        self.note_label.pack(side='left', padx=10)
        self.note_text.pack(side='left')


class LogMood:
    def __init__(self, parent: Frame, mood: str):
        self.frame = Frame(parent)
        self.mood_label = Label(self.frame, text='Mood: ')
        self.mood_text = Label(self.frame, text=mood)

    def render(self):
        self.frame.pack(fill=X, padx=10, pady=10)
        self.mood_label.pack(side='left')
        self.mood_text.pack(side='left')


class LogEntry:
    def __init__(self, parent: Frame, page: Page):
        self.frame = LabelFrame(parent, text=page.date, width=500)
        self.note = LogNote(self.frame, page.note)
        self.mood = LogMood(self.frame, page.mood.capitalize())

    def render(self):
        self.frame.pack(fill=X, expand=True, padx=20, pady=10)
        self.note.render()
        self.mood.render()


class PageLog:
    def __init__(self, parent: Frame, title='Log'):
        self.parent = parent
        self.title = title
        self.frame = Frame(parent)
        self.scrolled_frame = ScrolledFrame(self.frame, autohide=True)

    def render(self):
        self.refresh_entries()
        self.scrolled_frame.pack(fill='both', expand=True)
        self.frame.pack(fill='both', expand=True)
        self.parent.add(self.frame, text=self.title)

    def refresh_entries(self):
        for widget in self.scrolled_frame.winfo_children():
            widget.destroy()

        for entry in (LogEntry(self.scrolled_frame, page) for page in Page.all()):
            entry.render()


class Metrics:
    def __init__(self, parent: Notebook, title='Metrics'):
        self.parent = parent
        self.title = title
        self.frame = Frame(parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.refresh_axes()
        self.chart = FigureCanvasTkAgg(self.figure, self.frame)

    def render(self):
        self.frame.pack()
        self.parent.add(self.frame, text=self.title)
        self.figure.subplots_adjust(left=0.3, right=0.5, top=0.7, bottom=0.5)
        self.chart.get_tk_widget().pack(fill=BOTH, expand=True)

    def refresh_axes(self):
        self.axes.clear()
        occurrences = dict(Counter(page.mood for page in Page.all()))
        self.axes.pie(occurrences.values(), labels=occurrences.keys(), autopct="%1.1f%%", radius=3)

class App:
    def __init__(self, title='Personal Diary'):
        self.root = Window(title=title, size=(700, 600))
        self.notebook = Notebook(self.root)
        self.metrics = Metrics(self.notebook)
        self.log = PageLog(self.notebook)
        self.form = PageForm(self.notebook, on_save=self.update_tabs)
        
    def render(self):
        self.form.render()
        self.metrics.render()
        self.log.render()
        self.notebook.pack(fill='both', expand=True)
        self.root.mainloop()
    
    def update_tabs(self):
        self.log.refresh_entries()
        self.metrics.refresh_axes()