from Components.formulario import TForm, Form_Type
from Components.labeled_edit import TLabeledEntry, LabelPosition, Align_Text

class TESte(TForm):
    def __init__(self, titulo: str, largura: int, altura: int, redimensionavel: bool = False, type: Form_Type = Form_Type.CENTRALIZED):
        super().__init__(titulo, largura, altura, redimensionavel, type)

    def on_create(self, event):
        self.labeled_entry1 = TLabeledEntry(self, callback_prefix='lbeteste',label_position=LabelPosition.ABOVE, label_alignment=Align_Text.CENTER, label_text="Nome:")
        return super().on_create(event)

    def on_show(self, event):
        self.labeled_entry1.pack(padx=10, pady=10)
        return super().on_show(event)

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

TESte("Teste", 300, 300, False, Form_Type.FULL_SCREEN).mainloop()