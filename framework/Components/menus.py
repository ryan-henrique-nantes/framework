from tkinter import Menu, Menubutton

class TMenu(Menu):
    """Menu customizado.
    Métodos:
        add_sub_menu: Adiciona um submenu ao menu, recebe um label e um menu.
        add_lista: Adiciona uma lista de opções ao menu, recebe um label principal, uma lista de labels e uma lista de comandos.
    """

    def __init__(self, master, iscontext: bool=False, tearoff: int=0, type: str='normal'):
        super().__init__(master, tearoff=tearoff, type=type)
        if iscontext:
            master.bind("<Button-3>", self._show_context_menu)

    def add_sub_menu(self, label: str, menu: Menu):
        """Adiciona um submenu ao menu."""
        self.add_cascade(label=label, menu=menu)

    def add_lista(self, label: str, labels: list, commands: list):
        """Adiciona uma lista de opções ao menu."""
        opcoes = TMenu(self,  tearoff=0, type='normal')
        for posicao, texto in enumerate(labels):
            opcoes.add_command(label=texto, command=commands[posicao])
        self.add_sub_menu(label, opcoes)

    def _show_context_menu(self, event):
        self.post(event.x_root, event.y_root)

class TMenuButton(Menubutton):
    """MenuBotão customizado.
    Para usar os eventos do botão, cria a def usando o prefixo que passou no parâmetro 'callback_prefix' + '_' + nome do evento.
    Eventos disponíveis:
        on_backspace_press: Quando a tecla backspace é pressionada.
        on_button_release: Quando o botão do mouse é solto.
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

    def __init__(self, text:str, relief: str ='raised', master: any = None, callback_prefix: str = '', **kwargs):
        self.callback_prefix = callback_prefix
        super().__init__(master, text=text, relief= relief, **kwargs)
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

    def add_sub_menu(self, label: str, menu: Menu):
        """Adiciona um submenu ao menu."""
        self[label] =menu   

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