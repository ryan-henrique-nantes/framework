from tkinter import Text, END

class TMemo(Text):
    """Text customizado.
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

    def __init__(self, master: any = None, callback_prefix: str = '', **kwargs):
        self.callback_prefix = callback_prefix
        super().__init__(master, **kwargs)
        self.__draged = False
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

    def clear(self):
        """Limpa o texto."""
        self.delete(1.0, END)

    def add(self, text):
        """Adiciona texto."""
        self.insert(END, text)

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
