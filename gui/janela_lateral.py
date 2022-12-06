from tkinter import *
from gui.janela_input import *
import tkinter.font as font


#eventos causados pelos mouses nos botões
def mouse_entraBtn(e):
    e.widget['background'] = '#CC7700'

def mouse_saiBtn(e):
    e.widget['background'] = '#FF9500'    

#sidebar
def janela_lateral(janela, jdisplay):
    jlateral = Frame(janela, bg='#FF9F19', relief='sunken', borderwidth=0)
    jlateral.pack(expand=False, fill='both', side='left', anchor='nw')
    jlateral.grid_propagate(False)

    
    jinput = Frame(width=100, height=100, bg='#FF9500', relief='sunken', borderwidth=0)
    def clica_Chronos(e):
        nonlocal jinput
        jinput.destroy()
        jinput = Frame(width=100, height=100, bg='#FF9500', relief='sunken', borderwidth=0)
        Label(jinput, text= "Configurações", bg='#FF9500', fg='#FDEDDF', bd = 0, font= ('Helvetica 20 bold')).grid(column=0, row=0)
        janela_input_chronos(jdisplay, jinput)

    def clica_Janus(e):
        nonlocal jinput
        jinput.destroy()
        jinput = Frame(width=100, height=100, bg='#FF9500', relief='sunken', borderwidth=0)
        Label(jinput, text= "Configurações", bg='#FF9500', fg='#FDEDDF', bd = 0, font= ('Helvetica 20 bold')).grid(column=0, row=0)
        janela_input_janus(jdisplay, jinput)

    def clica_heroi(e):
        nonlocal jinput
        jinput.destroy()
        jinput = Frame(width=100, height=100, bg='#FF9500', relief='sunken', borderwidth=0)
        Label(jinput, text= "Configurações", bg='#FF9500', fg='#FDEDDF', bd = 0, font= ('Helvetica 20 bold')).grid(column=0, row=0)
        janela_input_heroi(jdisplay, jinput)
    
    #fonte para os botões
    f = font.Font(size=20)
    #cria os botões
    btnChronos = Button(jlateral, text='Chronos', width = 15, bg='#FF9500', fg='#FDEDDF', bd = 0)
    btnChronos.bind("<Enter>", mouse_entraBtn)
    btnChronos.bind("<Leave>", mouse_saiBtn)
    btnChronos.bind("<Button>", clica_Chronos)

    btnHeroi = Button(jlateral, text='HeROI', width = 15, bg='#FF9500', fg='#FDEDDF', bd = 0)
    btnHeroi.bind("<Enter>", mouse_entraBtn)
    btnHeroi.bind("<Leave>", mouse_saiBtn)
    btnHeroi.bind("<Button>", clica_heroi)

    btnJanus = Button(jlateral, text='Janus', width = 15, bg='#FF9500', fg='#FDEDDF', bd = 0)
    btnJanus.bind("<Enter>", mouse_entraBtn)
    btnJanus.bind("<Leave>", mouse_saiBtn)
    btnJanus.bind("<Button>", clica_Janus)

    #fontes
    btnChronos['font'] = f
    btnHeroi['font'] = f
    btnJanus['font'] = f
    
    #Fixa os botões na jenala  
    btnChronos.pack(side = 'top')
    btnHeroi.pack(side = 'top')
    btnJanus.pack(side = 'top')