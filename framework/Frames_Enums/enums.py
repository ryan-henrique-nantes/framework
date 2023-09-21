from enum import Enum
import tkinter as tk

class Align_Text(Enum):
    LEFT = {'justify': "left",
            'anchor': tk.W}
    CENTER = {'justify': "center",
              'anchor': tk.CENTER}
    RIGHT = {'justify': "right",
             'anchor': tk.E}


class LabelPosition(Enum):
    ABOVE = {'entry_row': 1, 'label_row': 0,
             'entry_column': 0, 'label_column': 0,
             'index': 0, 'weigth':1}
    BELOW = {'entry_row': 0, 'label_row': 1,
                'entry_column': 0, 'label_column': 0,
                'index': 1, 'weigth':1}
    LEFT = {'entry_row': 0, 'label_row': 0,
            'entry_column': 1, 'label_column': 0,
            'index': 1, 'weigth':1}
    RIGHT = {'entry_row': 0, 'label_row': 0,
                'entry_column': 0, 'label_column': 1,
                'index': 0, 'weigth':1}

class Form_Type(Enum):
    CENTRALIZED = 1
    FULL_SCREEN = 2