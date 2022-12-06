#(ou usar "python -m pip install...")
#pip install -U pip
#pip install wheel
#pip install rasterio
#pip install matplotlib
#pip install numba
#pip install pandas
#pip install dbfread

#precisa baixar a wheel antes, serve para o import do osgeo
#python -m pip install GDAL-3.4.3-cp310-cp310-win_amd64.whl

import os
import rasterio
import pandas as pd
from rasterio.plot import show
from osgeo import gdal, ogr
from algoritmos.convolucoes import *

def executaChronos(dir, njanelas, saida):
    #receber os arquivos das imagens colocando em raster_paths
    raster_paths = []
    for rootdir, dirs, files in os.walk(dir):
        for single_file in files:
            if single_file.endswith('.tif'):
                inpt_raster = os.path.join(rootdir, single_file)
                raster_paths.append(inpt_raster)

    #colocar os arrays do raster das imagens em uma lista
    listRasterArrays = []
    for path in raster_paths:
        Im=gdal.Open(path)
        banda_img=Im.GetRasterBand(1)
        listRasterArrays.append(banda_img.ReadAsArray())

    #Chronos
    output=convolucaoCube(listRasterArrays, Im.RasterYSize, Im.RasterXSize, len(listRasterArrays), njanelas)

    #salvando se o dir de saísa não estiver vazio
    if saida:
        with rasterio.open(raster_paths[0]) as src:
                ras_meta = src.profile
                ras_meta['dtype']='float32'

                outHe = rasterio.open(saida+"\Imagem_He.tif", 'w', **ras_meta)
                outHe.write(output[0], 1)
                outHe.close()

                outHeMax = rasterio.open(saida+"\Imagem_HeMax.tif", 'w', **ras_meta)
                outHeMax.write(output[1], 1)
                outHeMax.close()

                outSDL = rasterio.open(saida+"\Imagem_SDL.tif", 'w', **ras_meta)
                outSDL.write(output[2], 1)
                outSDL.close()

                outLMC = rasterio.open(saida+"\Imagem_LMC.tif", 'w', **ras_meta)
                outLMC.write(output[3], 1)
                outLMC.close()

    return(output)

def executaJanus(imagem, janela, opcao, saida):
    Im=gdal.Open(imagem)
    cols=Im.RasterXSize
    rows=Im.RasterYSize
    NrBandas = Im.RasterCount

    for band in range(NrBandas):
        band +=1
        banda_img=Im.GetRasterBand(band)
        ImArray=banda_img.ReadAsArray().astype(np.float)
        EE=np.array(ImArray)
        #Janus
        ES=convolucaoNumba(EE, ImArray, rows, cols, janela, opcao)

        #saida
        #Escolha do nome na apresentação para o usuário
        nome = "\Imagem_"
        if opcao == 0:
            nome += "He.tif"
        elif opcao == 1:
            nome += 'HeMax.tif'
        elif opcao == 2:
            nome += 'SDL.tif'
        elif opcao == 3:
            nome += 'LMC.tif'

        #salvando
        if saida:        
            with rasterio.open(imagem) as src:
                ras_meta = src.profile
                ras_meta['dtype']='float32'

                print(saida)
                print(saida+nome+'\n')
                out = rasterio.open(saida+nome, 'w', **ras_meta)
                out.write(ES, 1)
                out.close()

        #apresentação
        titulo = "Imagem " + nome[8:-4]
        show(ES, title= titulo)
        del(EE)
        del(ES)
        del(ImArray)
    del(Im)


#Executa HeROI
def Complexidade(Vetor):
     lenVet=Vetor.size
     Lista=list(set(Vetor))
     prob=[np.size(Vetor[Vetor==i])/(lenVet*1.0) for i in Lista]
     #Cálculo de N
     N=len(prob)*1.0
     #Cálculo de He
     He=np.sum([p*np.log2(1/p) for p in prob])
     D=np.sum([(p-(1/N))**2 for p in prob])
     #Cálculo de Hmax
     Hmax=np.log2(N)
     #Cálculo de He/Hmax
     C=He/Hmax
     #Cálculo do LMC
     LMC=D*C
     #Cálculo do SDL
     SDL=(1-C)*C
     return He,Hmax,C,SDL,LMC,N

def bbox_to_pixel_offsets(gt, bbox):
     originX = gt[0]
     originY = gt[3]
     pixel_width = gt[1]
     pixel_height = gt[5]
     x1 = int((bbox[0] - originX) / pixel_width)
     x2 = int((bbox[1] - originX) / pixel_width) + 1
     y1 = int((bbox[3] - originY) / pixel_height)
     y2 = int((bbox[2] - originY) / pixel_height) + 1
     xsize = x2 - x1
     ysize = y2 - y1
     return (x1, y1, xsize, ysize)

def zonal_stats(vector_path, raster_path, banda, nodata_value=None, global_src_extent=False):
    rds = gdal.Open(raster_path)
    assert(rds)
    rb = rds.GetRasterBand(banda)
    rgt = rds.GetGeoTransform()
    if nodata_value:
        nodata_value = float(nodata_value)
        rb.SetNoDataValue(nodata_value)
    vds = ogr.Open(vector_path)
    assert(vds)
    vlyr = vds.GetLayer(0)
    if global_src_extent:
        src_offset = bbox_to_pixel_offsets(rgt, vlyr.GetExtent())
        src_array = rb.ReadAsArray(*src_offset)
        new_gt = ((rgt[0] + (src_offset[0] * rgt[1])), rgt[1], 0.0, (rgt[3] + (src_offset[1] * rgt[5])), 0.0, rgt[5] )
    mem_drv = ogr.GetDriverByName('Memory')
    driver = gdal.GetDriverByName('MEM')
    stats = []
    ArrayMasked=[]
    feat = vlyr.GetNextFeature()
    cont=0
    while feat is not None:
        if not global_src_extent:
            src_offset = bbox_to_pixel_offsets(rgt, feat.geometry().GetEnvelope())
            src_array = rb.ReadAsArray(*src_offset)
            new_gt = ((rgt[0] + (src_offset[0] * rgt[1])), rgt[1], 0.0, (rgt[3] + (src_offset[1] * rgt[5])), 0.0, rgt[5])
            mem_ds = mem_drv.CreateDataSource('out')
        mem_layer = mem_ds.CreateLayer('poly', None, ogr.wkbPolygon)
        mem_layer.CreateFeature(feat.Clone())
        rvds = driver.Create('', src_offset[2], src_offset[3], 1, gdal.GDT_Byte)
        rvds.SetGeoTransform(new_gt)
        gdal.RasterizeLayer(rvds, [1], mem_layer, burn_values=[1])
        rv_array = rvds.ReadAsArray()
        masked = np.ma.MaskedArray( src_array, mask=np.logical_or(src_array == nodata_value, np.logical_not(rv_array) ) )
        ArrayMasked.append(masked)
        feature_stats = {'min': float(masked.min()),'mean': float(masked.mean()),'max': float(masked.max()),'std': float(masked.std()),'sum': float(masked.sum()),'count': int(masked.count()),'fid': int(feat.GetFID())}
        stats.append(feature_stats)
        rvds = None
        mem_ds = None
        feat = vlyr.GetNextFeature()
        cont=cont+1
    return stats, ArrayMasked, cont

def executaROI(roi_shp, roiField, imagem, saida):
    mField = roiField
    #abre o  shp e pega o número de campos da classe escolhida
    SHP = ogr.Open(roi_shp)
    layer = SHP.GetLayer()
    FeatureCount=layer.GetFeatureCount()
    im = gdal.Open(imagem)

    NrBandas = im.RasterCount
    #primeira linha do csv de saída
    colNames=['Banda','Regiao','He','Hmax','He/Hmax','SDL','LMC','DNCount','N','DNmax','DNmin','DNmean','DNstd']
    df_Results  = pd.DataFrame(columns = colNames)
    for band in range(NrBandas):
            band +=1
            stats = zonal_stats(roi_shp, imagem, band)
            x = stats[1]
            #iteração por cada campo/classe (o selecionado pelo usuário presente no shp da imagem para o cálculo de sua complexidade
            #ex:
            #classe = região | campos da classe = Veg Nativa, Urbano, Agua, Pastagem
            for iter in range(FeatureCount):
                Class=layer.GetFeature(iter).GetField(mField)
                y=x[iter].flatten()
                #HeROI
                Comp=Complexidade(y.compressed())
                EstDescritivas=stats[0][iter]
                #dataframe dos resultados
                df_Results.loc[len(df_Results)] = [band,Class,Comp[0],Comp[1],Comp[2],Comp[3],Comp[4], EstDescritivas['count'],Comp[5],EstDescritivas['max'],EstDescritivas['min'],EstDescritivas['mean'],EstDescritivas['std']]

    #salvando o csv
    df_Results.to_csv(saida+'/heroi.csv', encoding='utf-8', index=False)
    pass
