import tkinter as tk

class TLabel(tk.Label):
    def __init__(self, master: any = None, callback_prefix: str ='', caption: str ="", **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.caption = caption
        self.callback_prefix = callback_prefix
        self.__draged = False
        self.cor_fundo = kwargs.get('bg_color', '#F0F0F0')
        self.cor_fonte = kwargs.get('fg_color', '#000000')

    @property
    def cor_fundo(self):
        return self.__cor

    @cor_fundo.setter
    def cor_fundo(self, color_hex: str):
        self.__cor = color_hex
        if self.__cor is not None:
            self.config(bg=self.__cor)

    @property
    def cor_fonte(self):
        return self.__cor_font
    
    @cor_fonte.setter
    def cor_fonte(self, color_hex: str):
        self.__cor_font = color_hex
        if self.__cor_font is not None:
            self.config(fg=self.__cor_font)
    
    @property
    def caption(self) -> str:
        return self.__caption
    
    @caption.setter
    def caption(self, value: str):
        """Define o caminho da imagem."""
        self.__caption = value
        self.config(text=self.__caption)

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
        self.bind('<B1-Motion>', self.on_drag)
        self.bind('<ButtonRelease-1>', self.on_button_release)
        self.bind('<Key>', self.on_key_press)

        for event, event_type in events.items():
            self.bind(event, self.__create_event_handler(event_type))

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