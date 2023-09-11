from tkinter.ttk import Treeview
from tkinter import END
from Frames_Enums.enums import Align_Text, LabelPosition

class TTreeview(Treeview):
    """Treeview customizado.
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
        on_title_click: Quando o título é clicado, precisa de parametro para titulo da coluna
        on_unfocus: Quando o botão perde foco."""

    def __init__(self, titulos: list, tamanhos: list, master: any = None, callback_prefix: str = '', **kwargs):
        if len(titulos) != len(tamanhos):
            raise ValueError('O número de titulos deve ser igual ao número de tamanhos.')
        self.callback_prefix = callback_prefix
        super().__init__(master,columns=titulos, show="headings", **kwargs)
        self.__draged = False
        self.__criar_titulos(titulos, tamanhos)
        self.__bind_events()

    def __criar_titulos(self, titulos: list, tamanhos: list, align_titulo: Align_Text = Align_Text.CENTER, align_dados: Align_Text = Align_Text.CENTER):
        """Private method.: Cria os titulos."""
        for posicao, titulo in enumerate(titulos):
            self.heading(titulo, text=titulo, anchor=align_titulo.value['anchor'], command=lambda t=titulo: self.on_title_click(t))
            self.column(posicao, width=tamanhos[posicao], anchor=align_dados.value['anchor'])

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
    
        return self

    def set_focus(self):
        """Coloca o foco no botão."""
        self.focus_set()

    def get_selected_line(self):
        """Retorna a linha selecionada."""
        return self.selection()

    def clear(self):
        """Limpa o texto."""
        self.delete(1.0, END)

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

    def on_title_click(self, titulo: str):
        """Evento disparado quando o titulo é clicado."""
        method_name = f'{self.callback_prefix}_on_title_click'
        callback = getattr(self.master, method_name, None)
        if callback and callable(callback):
            callback(titulo)

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