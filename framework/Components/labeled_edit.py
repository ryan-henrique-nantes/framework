"""Componente LabeledEdit, que é um label com um edit junto"""
import tkinter as tk
import sys
sys.path.append('utils')
from Frames_Enums.enums import Align_Text, LabelPosition

class TLabeledEntry(tk.Frame):
    """Componente Label com Edit, callback_prefix sendo o prefixo que vai usar no inicio
    de cada evento dele que for chamar, que deve ser seguido de _(nome do evento), ex:
    _on_change, label_position sendo aonde quer definir a posição do label em relação ao edit: 
    Above sendo acima, Bellow sendo abaixo, Left sendo a Esquerda e Right a direita, label_alignment
    sendo o alinhado do texto do edit junto do label, caption sendo o texto do label, também possui
    bg_color sendo a cor do fundo e fg_color sendo a cor da fonte.
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
    def __init__(self, master, callback_prefix: str ='', label_position: LabelPosition = 
                 LabelPosition.ABOVE, label_alignment: Align_Text = Align_Text.CENTER, 
                 caption="", **kwargs):
        super().__init__(master)
        self.callback_prefix = callback_prefix
        self.__draged = False
        self.label_position = label_position
        self.label_alignment = label_alignment
        self.label = tk.Label(self)
        self.entry = tk.Entry(self)
        self.cor_fundo = kwargs.get('bg_color', '#F0F0F0')
        self.cor_fonte = kwargs.get('fg_color', '#000000')
        self.caption = caption
        self.entry_width = kwargs.get('width', 20)
        self.__position_widgets(label_position.value).__align_label(label_alignment, label_position)
        self.__bind_events()


    @property
    def cor_fundo(self):
        """Property da cor de fundo"""
        return self.__cor

    @cor_fundo.setter
    def cor_fundo(self, color_hex: str):
        """Define a cor do fundo"""
        self.__cor = color_hex
        if self.__cor is not None:
            self.config(bg=self.__cor)
            self.entry.config(bg=self.__cor)
            self.label.config(bg=self.__cor)

    @property
    def cor_fonte(self):
        """Property da cor da fonte"""
        return self.__cor_font
    
    @cor_fonte.setter
    def cor_fonte(self, color_hex: str):
        """Define a cor da fonte"""
        self.__cor_font = color_hex
        if self.__cor_font is not None:
            self.entry.config(fg=self.__cor_font)
            self.label.config(fg=self.__cor_font)

    @property
    def entry_width(self):
        """Property da largura do campo de entrada."""
        return self.entry['width']

    @entry_width.setter
    def entry_width(self, value: int):
        """Define a largura do campo de entrada."""
        self.entry.config(width=value)

    @property
    def caption(self) -> str:
        """Retorna o texto do label."""
        return self.label['text']
    
    @caption.setter
    def caption(self, value: str):
        """Define o texto do label."""
        self.label.config(text=value)
        
    @property
    def text(self) -> str:
        """Retorna o texto do campo de entrada."""
        return self.entry.get()
    
    @text.setter
    def text(self, value: str):
        """Define o texto do campo de entrada."""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
        
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