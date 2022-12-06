from tkinter import *
from gui.janela_lateral import *

#
#proporções da janela
janela=Tk()

janela.title('ComPlex')
janela.geometry("{0}x{1}+0+0".format(950, 500))

#conteúdo principal
jdisplay = Frame(janela, bg='#001C2E', width=500, height=500)
jdisplay.pack(expand=True, fill='both', side='right')

#sidebar
janela_lateral(janela, jdisplay)

janela.mainloop()