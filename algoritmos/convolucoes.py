import numpy as np

from numba import prange

#Convolução Numba para o Janus
def convolucaoNumba (E, ImArray, rows, cols, janela, opcao):
    """
    Execução do algoritmo para o Janus

    Parameters
    ----------
    E : numpy array
        transformação do array formado pelo raster da imagem original
        em um array numpy
    ImArray : array
        leitura do raster da imagem original como array formado de floats
    rows : int
        tamanho do eixo y do raster da imagem
    cols : int
        tamanho do eixo x do raster da imagem
    janela : int
        tamanho do kernel escolhido pelo usuário
    opcao : int 
        opção de métrica escolhida pelo usuário
        He = 0, H2/Hmax = 1, SDL = 2, LMC = 3

    Returns
    -------
    numpy array
        a imagem da região com a métrica escolhida
    """

    for row in prange(rows):
        for col in prange(cols):
            #marcação do kernel/janela
            Lx=max(0,col-janela)
            Ux=min(cols,col+janela+1)
            Ly=max(0,row-janela)
            Uy=min(rows,row+janela+1)
            mascara=ImArray[Ly:Uy,Lx:Ux].flatten()
            He=0.0
            lenVet=mascara.size
            Lista=list(set(mascara))
            if len(Lista)==1 and Lista.count(0)==1:
                E[row,col]=0
            else:
                #Cálculo do He
                prob=[(mascara[mascara==i]).size/(lenVet*1.0) for i in Lista]
                He = np.sum([(-1.0*p*np.log2(p)) for p in prob if p>0])
                if opcao==0:
                    E[row,col]=He
                #Cálculo de N
                N=len(Lista)*1.0
                if N == 1:
                    C=0
                else:
                    Hmax=np.log2(N)
                    C=He/Hmax
                #He/Hmax
                if opcao==1:
                    E[row,col]=C
                #SDL
                if opcao==2:
                    SDL=(1-C)*C
                    E[row,col]=SDL
                #LMC
                if opcao==3:
                    D = 0.0
                    D = np.sum([((p-(1/N))**2) for p in prob])
                    LMC=D*C
                    E[row,col]=LMC
    return E

#Convolução Cube para o Chronos
def convolucaoCube (listArray, rows, cols, imagens, janela):
    """
    Execução do algoritmo para o Chronos

    Parameters
    ----------
    listArray : array
        array do raster das imagens
    rows : int
        tamanho do eixo y do raster da imagem
    cols : int
        tamanho do eixo x do raster da imagem
    imagens : int
        quantidade de imagens em listArray
    janela : int
        tamanho do kernel (janela) escolhido pelo usuário

    Returns
    -------
    numpy array
        a imagem da região com a métrica escolhida
    """

    arrayHe = np.empty((rows,cols), dtype=float)
    arrayHemax = np.empty((rows,cols), dtype=float)
    arraySDL = np.empty((rows,cols), dtype=float)
    arrayLMC = np.empty((rows,cols), dtype=float)
    for row in range(rows):
        for col in range(cols):
            #excessão de tamanho de janela = 1
            if janela==1:
                mascara=[]
                for imagem in range(imagens):
                    mascara.append(listArray[imagem][row][col])
            else:
                #Definição dos valores com base no tamanho da janela
                Lx=max(0,col-janela)
                Ux=min(cols,col+janela+1)
                Ly=max(0,row-janela)
                Uy=min(rows,row+janela+1)
                #Agrupamento de todas as imagens recebidas para uma mesma máscara
                mascara=[]
                mascara1 = []
                for imagem in range(imagens):
                    imArray = listArray[imagem]
                    mascara1 = list( imArray[Ly:Uy,Lx:Ux].flatten())
                    mascara = mascara + mascara1 #soma das máscaras + máscara da imagem da iteração atual
                    mascara1=[]
            He=0.0
            lenVet=len(mascara)
            Lista=list(set(mascara))
            #Exceção de comprimento = 1
            if len(Lista)==1 and Lista.count(0)==1:
                arrayHe[row,col]=0
                arrayHemax[row,col]=0
                arraySDL[row,col]=0
                arrayLMC[row,col]=0
            else:
                #Cálculo do He
                prob=[(mascara.count(i))/(lenVet*1.0) for i in Lista]
                He = np.sum([(-1.0*p*np.log2(p)) for p in prob if p>0])
                arrayHe[row,col]=He
                #Cálculo do N
                N=len(Lista)*1.0
                if N == 1:
                    C=0
                #Cálculo do Hmax
                else:
                    Hmax=np.log2(N)
                    C=He/Hmax
                arrayHemax[row,col]=C
                #Cálculo do SDL
                SDL=(1-C)*C
                arraySDL[row,col]=SDL
                #Cálculo do LMC
                D = 0.0
                D = np.sum([((p-(1/N))**2) for p in prob])
                LMC=D*C
                arrayLMC[row,col]=LMC
    return (arrayHe, arrayHemax, arraySDL, arrayLMC)