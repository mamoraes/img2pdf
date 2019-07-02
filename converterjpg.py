# -- coding: utf-8 --'
from fpdf import FPDF
from PIL import Image
import os # I added this and the code at the end
import easygui

from datetime import datetime
from os.path import getmtime

def gerarJPG(listaImagens,dirImagens='', dirDestino=''):
    if not listaImagens:
        return

    if not dirDestino:
        dirDestino = dirImagens
    n=1
    for pagina in listaImagens:
        diretorio, nome_arq = os.path.split(pagina)
        nome, extensao = nome_arq.split('.')
        novoarq = str(n).zfill(3)+'-'+str(nome)
        n += 1
        #novoarq =  dir + datetime.fromtimestamp(getmtime(dir+arq)).strftime('%Y%m%d%H%M') +'-'+ arq
        #datamodificacao = getmtime(os.path.join(dirImagens,arq))
        #print(datamodificacao)
        #novoarq = str(datetime.fromtimestamp(datamodificacao.strftime('%Y%m%d%H%M%S')))
        #novoarq = str(datetime.now().strftime('%Y%m%d%H%M%S%f')) + '-' + arq
        # novoarq = arq
        novoarq = str(os.path.join(diretorio,novoarq)+'.png')
        print(novoarq)
        arq= pagina #os.path.join(dirImagens,arq)
        imagem = Image.open(arq)
        imagem.save(novoarq)
    '''imagem.mode = 'I'
    print(destiny+arq)
    imagem.point(lambda i: i * (1. / 256)).convert('L').save(destiny+arq+'.png')'''

def gui_pasta(pasta):
    # GUI para obter a pastas escolhida pelo usuário
    nomepasta = easygui.diropenbox(
        default=pasta,
        msg =u"Selecione a pasta com as imagens",
        title ="Gera PDF a partir de imagens em uma pasta"
    )
    if not nomepasta:
        exit(1)
    return nomepasta

def gerarPDF(nomePDF, listaImagens, dirImagens='', dirDestino=''):
    if not listaImagens:
        return
    if not dirDestino:
        dirDestino = dirImagens

    capa = Image.open(os.path.join(dirImagens,str(listaImagens[0])))
    width, height = capa.size

    pdf = FPDF(unit="pt", format=[width, height])

    i=0
    for imagem in listaImagens:
        i+=1
        pdf.add_page()
        pdf.image(os.path.join(dirImagens, str(imagem)), 0, 0)
    #pdf.close()
    print('Gravando',i, 'imagens')
    arqdestino = os.path.join(dirDestino, nomePDF + ".pdf")
    pdf.output(arqdestino, "F")
    print('Arquivo gerado em ',arqdestino)


def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles    

def gerarListaArqData(diretorio):
#    os.chdir(diretorio)
    arqs = list(filter(os.path.isfile, os.listdir(diretorio)))
    arqs = [os.path.join(diretorio,f) for f in os.listdir(subdiretorio) if os.path.isfile(os.path.join(diretorio,f))]
#   arqs = [os.path.join(diretorio, arq) for arq in arqs] # add path to each file
    arqs.sort(key=lambda x: os.path.getmtime(x))
    return arqs

def getSubdiretorios(diretorio):
    p = [d for d in os.listdir(diretorio) if os.path.isdir(os.path.join(diretorio,d))]
    return p

#caminho = '/home/pais/Imagens'
#caminho = 'd:\\img'
easygui.msgbox(msg='Gera um arquivo PDF a partir de imagens (jpg e png)) em uma pasta')
caminho = gui_pasta('d:\\img')
for pasta in getSubdiretorios(caminho):
    subdiretorio = os.path.join(caminho,pasta)
    if not os.path.isdir(subdiretorio): 
        continue
    
    l = gerarListaArqData(subdiretorio)    
    x = [f for f in l if f.endswith(".tif")]
    #x = gerarListaArqData(subdiretorio)    
    gerarJPG(x, subdiretorio, caminho)
    
    x = [f for f in os.listdir(subdiretorio) if (f.endswith(".png") or f.endswith(".jpg"))]
    y = len(x)
    gerarPDF(nomePDF=pasta, listaImagens=x, dirImagens=subdiretorio, dirDestino=caminho)
