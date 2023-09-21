from tkinter import ttk
from PIL import Image, ImageTk

class TImage(ttk.Label):
    def __init__(self, master: any = None, imagem: str = '', **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.imagem = imagem
    
    @property
    def imagem(self) -> str:
        """Retorna o caminho da imagem."""
        return self.__imagem
    
    @imagem.setter
    def imagem(self, value: str):
        """Define o caminho da imagem."""
        self.__imagem = value
        
    @imagem.getter
    def imagem(self) -> str:
        return self.__imagem

    def mostrar_imagem(self):
        # Criar e renderizar o grafo
        imagem_caminho = self.__imagem

        # Carregar a imagem usando Pillow
        img = Image.open(imagem_caminho)
        photo = ImageTk.PhotoImage(img)

        # Exibir a imagem em um label tkinter
        self.config(image=photo)
        self.image = photo