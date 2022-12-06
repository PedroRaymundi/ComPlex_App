from tkinter import *
from tkinter import filedialog
from rasterio.plot import show
from dbfread import DBF

from algoritmos.execucoes import executaChronos, executaJanus, executaROI

def janela_input_chronos(jdisplay, jinput):
    jinput_form = Frame(width=200, height=100, bg='#033D45', relief='sunken', borderwidth=0)

    jinput.place(in_=jdisplay, anchor="c", relx=.5, rely=.25)
    jinput_form.place(in_=jinput, anchor="c", relx=.5, rely=3.5)

    Label(jinput, text= "Configurações", width=10, bg='#FF9500', fg='#FDEDDF', bd = 0, font= ('Helvetica 20 bold')).grid(column=0, row=0)
    Label(jinput, text= "Chronos", width=10, bg='#FF9500', fg='#FDEDDF', bd = 0, font= ('Helvetica 20 bold')).grid(column=0, row=1)
    
    #forms do input
    dir = []
    saida = []
    def select_dir():
        nonlocal dir
        dir = filedialog.askdirectory()
    def select_saida():
        nonlocal saida
        saida = filedialog.askdirectory()

    Label(jinput_form, text= "Escolha o diretório de entrada", bg='#033D45', fg='#FDEDDF', bd = 0, font= ('Helvetica 16')).grid(column=0, row=0)
    Button(jinput_form, text="FILE", font= ('Helvetica 16'), width=5, bg='#FF9500', fg='#FDEDDF', bd = 0, command= select_dir).grid(column=1, row=0)
    
    Label(jinput_form, text= "Escolha o diretório de saída", bg='#033D45', fg='#FDEDDF', bd = 0, font= ('Helvetica 16')).grid(column=0, row=1)
    Button(jinput_form, text="FILE", font= ('Helvetica 16'), width=5, bg='#FF9500', fg='#FDEDDF', bd = 0, command= select_saida).grid(column=1, row=1)
    
    #input slider para o tamanho da janela
    past = 1
    def fix(n):
        nonlocal past
        n = int(n)
        if not n % 2:
            scale.set(n+1 if n > past else n-1)
            past = scale.get()
    
    scale = Scale(jinput_form, length= 150, bg='#FF9500', fg='#FDEDDF', bd = 0, from_=3, to_=15, command= fix, orient= HORIZONTAL)
    Label(jinput_form, text= "Escolha o tamanho da janela", bg='#033D45', fg='#FDEDDF', bd = 0, font= ('Helvetica 16')).grid(column=0, row=2)
    scale.grid(row = 2, column= 1)

    def roda_chronos(dir, njanelas):
        output = executaChronos(dir, njanelas, saida)
        show(output[0], title="Imagem He")
        show(output[1], title="Imagem He/Hmax")
        show(output[2], title="Imagem SDL")
        show(output[3], title="Imagem LMC")

    Button(jinput_form, text="iniciar chronos", bg='#FF9500', fg='#FDEDDF', bd = 0, font= ('Helvetica 16'), command= lambda: roda_chronos(dir, scale.get())).grid(row=3, columnspan= 2)




def janela_input_janus(jdisplay, jinput):
    jinput_form = Frame(width=200, height=100, bg='#033D45', relief='sunken', borderwidth=0)

    jinput.place(in_=jdisplay, anchor="c", relx=.5, rely=.25)
    jinput_form.place(in_=jinput, anchor="c", relx=.5, rely=3.5)

    #forms do input
    dir = []
    saida = []
    def select_dir():
        nonlocal dir
        dir = filedialog.askopenfilename()
    def select_saida():
        nonlocal saida
        saida = filedialog.askdirectory()

    Label(jinput, text= "Configurações", width=10, bg='#FF9500', fg='#FDEDDF', bd = 0, font= ('Helvetica 20 bold')).grid(column=0, row=0)
    Label(jinput, text= "Janus", width=10, bg='#FF9500', fg='#FDEDDF', bd = 0, font= ('Helvetica 20 bold')).grid(column=0, row=1)

    Label(jinput_form, text= "Escolha a imagem de entrada", bg='#033D45', fg='#FDEDDF', bd = 0, font= ('Helvetica 16')).grid(column=0, row=0)
    Button(jinput_form, text="FILE", font= ('Helvetica 16'), width=5, bg='#FF9500', fg='#FDEDDF', bd = 0, command= select_dir).grid(column=1, row=0)
    
    Label(jinput_form, text= "Escolha o diretório de saída", bg='#033D45', fg='#FDEDDF', bd = 0, font= ('Helvetica 16')).grid(column=0, row=1)
    Button(jinput_form, text="FILE", font= ('Helvetica 16'), width=5, bg='#FF9500', fg='#FDEDDF', bd = 0, command= select_saida).grid(column=1, row=1)
    
    #input slider para o tamanho da janela
    past = 1
    def fix(n):
        nonlocal past
        n = int(n)
        if not n % 2:
            scale.set(n+1 if n > past else n-1)
            past = scale.get()
    
    scale = Scale(jinput_form, length= 150, bg='#FF9500', fg='#FDEDDF', bd = 0, from_=3, to_=15, command= fix, orient= HORIZONTAL)
    Label(jinput_form, text= "Escolha o tamanho da janela", bg='#033D45', fg='#FDEDDF', bd = 0, font= ('Helvetica 16')).grid(column=0, row=2)
    scale.grid(row = 2, column= 1)

    #opção de output
    radioValue = IntVar() 

    rdioHe = Radiobutton(jinput_form, text='He', width=10, font= ('Helvetica 16'), bg='#FF9500', variable=radioValue, value=0) 
    rdioHmax = Radiobutton(jinput_form, text='He/Hmax', width=10, font= ('Helvetica 16'), bg='#FF9500', variable=radioValue, value=1) 
    rdioSdl = Radiobutton(jinput_form, text='SDL', width=10, font= ('Helvetica 16'), bg='#FF9500', bd = 3, variable=radioValue, value=2)
    rdioLmc = Radiobutton(jinput_form, text='LMC', width=10, font= ('Helvetica 16'), bg='#FF9500', bd = 3, variable=radioValue, value=3)

    rdioHe.grid(column=0, row=3)
    rdioHmax.grid(column=1, row=3)
    rdioSdl.grid(column=0, row=4)
    rdioLmc.grid(column=1, row=4)

    def roda_janus(dir, njanelas, opcao):
        executaJanus(dir, njanelas, opcao, saida)

    Button(jinput_form, font= ('Helvetica 16'), text="iniciar janus", bg='#FF9500', fg='#FDEDDF', bd = 0, command= lambda: roda_janus(dir, scale.get(), radioValue.get())).grid(row=5, columnspan= 2)

def menu_dropdown(shp, jinput_form):
    table = DBF(shp[:-4]+'.dbf')
    roifOptions = list(list(table.records)[0])[:]
    roif = StringVar()

    Label(jinput_form, text= "Escolha o roi field", bg='#033D45', fg='#FDEDDF', bd = 0, font= ('Helvetica 16')).grid(column=0, row=2)
    roif.set(roifOptions[0])
    dropdowRoifs = OptionMenu(jinput_form, roif, roifOptions[0], *roifOptions[1:])
    dropdowRoifs.config(font= ('Helvetica 16'), width=5, bg='#FF9500', fg='#FDEDDF', bd = 0)
    dropdowRoifs.grid(column=1, row=2)

    return roif


def janela_input_heroi(jdisplay, jinput):
    jinput_form = Frame(width=200, height=100, bg='#033D45', relief='sunken', borderwidth=0)

    jinput.place(in_=jdisplay, anchor="c", relx=.5, rely=.25)
    jinput_form.place(in_=jinput, anchor="c", relx=.5, rely=3.5)

    Label(jinput, text= "Configurações", width=10, bg='#FF9500', fg='#FDEDDF', bd = 0, font= ('Helvetica 20 bold')).grid(column=0, row=0)
    Label(jinput, text= "HeROI", width=10, bg='#FF9500', fg='#FDEDDF', bd = 0, font= ('Helvetica 20 bold')).grid(column=0, row=1)
    
    #forms do input
    imagem = []
    shp = []
    roif = StringVar()
    saida = []
    def select_imagem():
        nonlocal imagem
        imagem = filedialog.askopenfilename()
    def select_shp():
        nonlocal shp, roif
        shp = filedialog.askopenfilename()

        roif = menu_dropdown(shp, jinput_form)
    def select_saida():
        nonlocal saida
        saida = filedialog.askdirectory()

    Label(jinput_form, text= "Escolha o arquivo tif de entrada", bg='#033D45', fg='#FDEDDF', bd = 0, font= ('Helvetica 16')).grid(column=0, row=0)
    Button(jinput_form, text="FILE", font= ('Helvetica 16'), width=5, bg='#FF9500', fg='#FDEDDF', bd = 0, command= select_imagem).grid(column=1, row=0)

    Label(jinput_form, text= "Escolha o arquivo shp", bg='#033D45', fg='#FDEDDF', bd = 0, font= ('Helvetica 16')).grid(column=0, row=1)
    Button(jinput_form, text="FILE", font= ('Helvetica 16'), width=5, bg='#FF9500', fg='#FDEDDF', bd = 0, command= select_shp).grid(column=1, row=1)
    
    Label(jinput_form, text= "Escolha o diretório de saída", bg='#033D45', fg='#FDEDDF', bd = 0, font= ('Helvetica 16')).grid(column=0, row=3)
    Button(jinput_form, text="FILE", font= ('Helvetica 16'), width=5, bg='#FF9500', fg='#FDEDDF', bd = 0, command= select_saida).grid(column=1, row=3)
    
    def roda_heroi(imagem, shp, roif):
        strRoif = roif.get()
        executaROI(shp, strRoif, imagem, saida)

    Button(jinput_form, text="iniciar HeROI", bg='#FF9500', fg='#FDEDDF', bd = 0, font= ('Helvetica 16'), command= lambda: roda_heroi(imagem, shp, roif)).grid(row=4, columnspan= 2)