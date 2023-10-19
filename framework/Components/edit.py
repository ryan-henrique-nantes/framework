from tkinter.ttk import Entry
from tkinter import END
from Frames_Enums.enums import Align_Text

class TEdit(Entry):
    """Entry customizado.
    Para usar os eventos do botão, cria a def usando o prefixo que passou no parâmetro 'callback_prefix' + '_' + nome do evento.
    Eventos disponíveis:
        on_backspace_press: Quando a tecla backspace é pressionada.
        on_button_release: Quando o botão do mouse é solto.
        on_change: Quando o texto é alterado.
        on_click: Quando o botão é clicado.
        on_drag: Quando o mouse é arrastado.
        on_drop: Quando o mouse é arrastado e solto.
        on_double_click: Quando o botão é clicado duas vezes.
        on_enter: Quando o mouse entra no botão.
        on_enter_press: Quando a tecla enter/return é pressionada.
        on_escape_press: Quando a tecla escape é pressionada.
        on_exit: Quando o mouse sai do botão.
        on_focus: Quando o botão ganha foco.
        on_key_press: Quando uma tecla é pressionada.
        on_key_release: Quando uma tecla é solta.
        on_left_click: Quando o botão é clicado com o botão esquerdo do mouse.
        on_mousewheel_click: Quando o botão é clicado com o botão do meio do mouse.
        on_tab_press: Quando a tecla tab é pressionada.
        on_unfocus: Quando o botão perde foco."""

    def __init__(self, master: any = None, align: Align_Text = Align_Text.LEFT, callback_prefix: str = '', **kwargs):
        self.callback_prefix = callback_prefix
        super().__init__(master, **kwargs)
        self.cor_fundo = kwargs.get('bg_color', '#F0F0F0')
        self.cor_fonte = kwargs.get('fg_color', '#000000')
        self.__draged = False
        self.config(justify=align.value['justify'])
        self.__bind_events()

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

    def __create_event_handler(self, method_name):
        """"'Private method.: Liga eventos a janela."""
        def handler(event=None):
            method = getattr(self, method_name, None)
            if method:
                if event:
                    method(event)
                else:
                    method()
        return handler

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
    def text(self):
        """Retorna o texto."""
        return self.get()
    
    @text.setter
    def text(self, value: str):
        """Define o texto."""
        self.delete(0, END)
        self.insert(0, value)
        
    @text.getter
    def text(self):
        return self.get()

    def clear(self):
        """Limpa o texto."""
        self.delete(0, END)

    def length(self):
        """Retorna o tamanho do texto."""
        return len(self.get())

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

    def __call_callback(self, event_type):
        """Private method.: Chama o callback."""
        method_name = f'{self.callback_prefix}_{event_type}'
        callback = getattr(self.master, method_name, None)
        if callback and callable(callback):
            callback()
