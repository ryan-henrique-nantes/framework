from Components.formulario import TForm, Form_Type
from Components.labeled_edit import TLabeledEntry, LabelPosition, Align_Text

class TESte(TForm):
    def __init__(self):
        super().__init__(titulo="Teste", altura=300, largura=300, redimensionavel=False, 
                         type= Form_Type.CENTRALIZED, bg_color='#1C1C1C', fg_color='#FFFFFF')

    def on_create(self):
        self.labeled_entry1 = TLabeledEntry(self, callback_prefix='lbeteste',label_position=LabelPosition.ABOVE, 
                                            label_alignment=Align_Text.CENTER, caption="Nome:")
        self.labeled_entry1.cor_fonte = '#0000FF'
        return super().on_create()

    def on_show(self):
        self.labeled_entry1.pack(padx=10, pady=10)
        return super().on_show()

    def lbeteste_on_enter(event):
        print("lbeteste_on_enter")

    def lbeteste_on_enter_press(event):
        print("lbeteste_on_enter_press")

    def lbeteste_on_leave_focus(event):
        print("lbeteste_on_leave_focus")

    def lbeteste_on_focus(event):
        print("lbeteste_on_focus")

    def lbeteste_on_escape_press(event):
        print("lbeteste_on_escape_press")

TESte().mainloop()