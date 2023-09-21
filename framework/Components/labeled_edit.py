import tkinter as tk
import sys
sys.path.append('utils')
from Frames_Enums.enums import Align_Text, LabelPosition

class TLabeledEntry(tk.Frame):
    def __init__(self, master,  callback_prefix: str ='', label_position: LabelPosition = LabelPosition.ABOVE, label_alignment: Align_Text = Align_Text.CENTER, label_text="", **kwargs):
        super().__init__(master, **kwargs)
        self.callback_prefix = callback_prefix
        self.__draged = False
        self.label_position = label_position
        self.label_alignment = label_alignment
        self.label = tk.Label(self)
        self.entry = tk.Entry(self)
        self.label_text = label_text
        self.entry_width = kwargs.get('width', 20)
        self.__position_widgets(label_position.value).__align_label(label_alignment, label_position)
        self.__bind_events()

    @property
    def entry_width(self):
        """Retorna a largura do campo de entrada."""
        return self.entry['width']

    @entry_width.setter
    def entry_width(self, value: int):
        """Define a largura do campo de entrada."""
        self.entry.config(width=value)

    @entry_width.getter
    def entry_width(self) -> int:
        return self.entry['width']

    @property
    def label_text(self) -> str:
        """Retorna o texto do label."""
        return self.label['text']
    
    @label_text.setter
    def label_text(self, value: str):
        """Define o texto do label."""
        self.label.config(text=value)
        
    @label_text.getter
    def label_text(self) -> str:
        return self.label['text']
    
    @property
    def text(self) -> str:
        """Retorna o texto do campo de entrada."""
        return self.entry.get()
    
    @text.setter
    def text(self, value: str):
        """Define o texto do campo de entrada."""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
        
    @text.getter
    def text(self) -> str:
        return self.entry.get()

    def __bind_events(self):
        """Private method.: Cria os eventos do botão.""" 
        events = {
            '<BackSpace>': 'on_backspace_press',           
            '<Button-1>': 'on_click',
            '<Button-2>': 'on_mousewheel_click',
            '<Button-3>': 'on_left_click',
            '<Double-Button-1>': 'on_double_click',
            '<Enter>': 'on_enter',
            '<Escape>': 'on_escape_press',
            '<FocusIn>': 'on_focus',
            '<FocusOut>': 'on_leave_focus',
            '<KeyRelease>': 'on_key_release',
            '<Leave>': 'on_exit',
            '<Return>': 'on_enter_press',
            '<Tab>': 'on_tab_press',
        }
        self.entry.bind('<B1-Motion>', self.on_drag)
        self.entry.bind('<ButtonRelease-1>', self.on_button_release)
        self.entry.bind('<Key>', self.on_key_press)

        for event, event_type in events.items():
            self.entry.bind(event, self.__create_event_handler(event_type))

    def clear(self):
        """Limpa o texto."""
        self.entry.delete(0, tk.END)

    def length(self):
        """Retorna o tamanho do texto."""
        return len(self.entry.get())

    def is_empty(self):
        """Retorna True se o texto estiver vazio."""
        return self.length() == 0

    def on_button_release(self, event):
        """Evento disparado quando o botão do mouse é solto."""
        self.__call_callback('on_button_release')
        if self.__draged:
            self.__call_callback('on_drop')
        self.__draged = False

    def on_drag(self, event):
        """Evento disparado quando o mouse é arrastado."""
        self.__call_callback('on_drag')
        self.__draged = True

    def on_key_press(self, event):
        """Evento disparado quando uma tecla é pressionada."""
        self.__call_callback('on_key_press')
        self.__call_callback('on_change')

    def __create_event_handler(self, event_type):
        """Private method.: Cria o handler do evento."""
        def handler(event=None):
            self.__call_callback(event_type)
        return handler

    def __call_callback(self, event_type):
        """Private method.: Chama o callback."""
        method_name = f'{self.callback_prefix}_{event_type}'
        callback = getattr(self.master, method_name, None)
        if callback and callable(callback):
            callback()
    def __position_widgets(self, label_position):
        self.label.grid(row=label_position['label_row'], column=label_position['label_column'])
        self.entry.grid(row=label_position['entry_row'], column=label_position['entry_column'])
        self.grid_columnconfigure(label_position['index'], weight=label_position['weigth'])
        return self

    def __align_label(self, label_alignment, label_position):
        self.entry.config(justify=label_alignment.value['justify'])
        if label_position in (LabelPosition.ABOVE, LabelPosition.BELOW):
            self.label.config(anchor=label_alignment.value['anchor'], width=self.entry_width) 