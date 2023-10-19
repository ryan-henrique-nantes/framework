from tkinter import Menu
from tkinter.ttk import Combobox, Style

class TComboBox(Combobox):
    def __init__(self, master: any = None, callback_prefix: str = '', **kwargs) -> None:
        self.callback_prefix = callback_prefix
        super().__init__(master)
        self.cor_fundo = kwargs.get('bg_color', '#F0F0F0')
        self.cor_fonte = kwargs.get('fg_color', '#000000')
        self.__draged = False
        self.__bind_events()

    def __bind_events(self):
        """"Private method.: Cria os eventos do botão."""
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
            '<Key>': 'on_key_press',
            '<KeyRelease>': 'on_key_release',
            '<Leave>': 'on_exit',
            '<Return>': 'on_enter_press',
            '<Tab>': 'on_tab_press',
        }
        self.bind('<B1-Motion>', self.on_drag)
        self.bind('<ButtonRelease-1>', self.on_button_release)

        for event, event_type in events.items():
            self.bind(event, self.__create_event_handler(event_type))

    @property
    def cor_fundo(self):
        return self.__cor
    
    @cor_fundo.setter
    def cor_fundo(self, color_hex: str):
        self.__cor = color_hex
        if self.__cor is not None:
            Style().configure("TCombobox", fieldbackground=self.__cor)
            Style().configure("TListbox", background=self.__cor)

    @property
    def cor_fonte(self):
        return self.__cor_font
    
    @cor_fonte.setter
    def cor_fonte(self, color_hex: str):
        self.__cor_font = color_hex
        if self.__cor_font is not None:
            Style().configure("TCombobox", background=color_hex)
            Style().configure("TListbox", foreground=color_hex)



    def add_sub_menu(self, label: str, menu: Menu):
        """Adiciona um submenu ao menu."""
        self[label] = menu

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