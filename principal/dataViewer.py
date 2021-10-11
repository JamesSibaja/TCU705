#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Plataforma para base de datos con interfaz gráfica
========================
Esta aplicación fue desarrollada como una colaboración entre la municipalidad de Acosta y el TCU-705 de 
la UCR. La aplicación consiste en una plataforma con interfaz gráfica que permite la manipulación amigable 
y segura de bases de datos.
'''

import sqlite3
import pandas as pd
#from pdf2image import convert_from_path
import shutil
import time
import webbrowser
import math
from operator import itemgetter

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image 
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior


'''
===================
Widgets secundarios
===================
Diferentes widgets que complementan la ventana principal y conforman la interfaz gráfica
'''    
#Widget que muestra los datos solicitados de la base de datos
class DataViewer(ScrollView):
    end = BooleanProperty()
    def __init__(self,index,entrada,base,table,aplicacion,pag=0):
        super(DataViewer, self).__init__()
        self.editar=False
        self.index = index
        self.totalDatos = 0
        self.table = table
        self.filtroWhere = ''
        self.filtroSelect = ''
        self.aplicacion = aplicacion
        self.calcEst = ''
        self.c = base
        for row in self.c.execute('SELECT * From '+ self.table):
            self.totalDatos += 1
        self.total = self.totalDatos
        self.totalDatos2 = self.totalDatos
        self.id = 0
        self.campo=''
        self.calculando = ''
        self.information = []
        self.select = 0
        self.listEst=[]
        self.build(entrada =entrada,imagen=True,pag=0)

    #Constructor del data viewer
    def build(self,entrada,pag,filtros=[],busqueda=[],imagen=False, general=False):
        self.scroll_y=1
        self.aplicacion.pantalla.select=False
        self.aplicacion.agregar = True
        self.contenedor=DataViewerContainer()
        self.contenedor.bind(minimum_height=self.contenedor.setter('height'))
        self.filas=[]
        PDF = (False,0)
        color = True
        cont = 0
        self.filtroSelect = "SELECT `"+ self.index +"`"
        n = 0
        for selectField in entrada:
            if (n == 0):
                self.filtroSelect += ", "
            self.filtroSelect += "`" + str(selectField) + "`"
            if (selectField == 'PDF'):
                PDF = (True,n)
            if(selectField != entrada[len(entrada)-1]):
                self.filtroSelect += ", "
            n += 1
            
        self.filtroWhere =" FROM "+ self.table
        n=0
        primero=True
        for elemento in busqueda:
            if elemento.text.split() != []:
                if primero:
                    self.filtroWhere +=" WHERE "

                for palabra in elemento.text.split():
                    if primero:
                        primero = False
                        self.filtroWhere += self.sinTilde(str(filtros[n]),str(palabra))
                        
                    else:
                        if general:
                            self.filtroWhere +="or "+self.sinTilde(str(filtros[n]),str(palabra))
                        else:
                            self.filtroWhere +="and "+self.sinTilde(str(filtros[n]),str(palabra))
            n+=1
        filtro = self.filtroSelect + self.filtroWhere + " LIMIT 50 OFFSET " + str(pag*50)
        color = False
        
        for row in self.c.execute(filtro):
            
            self.filas.append(Fila(color))
            
            columnas = 0
            index = True 
            for x in row:
                if index:
                    index = False
                    indexID = str(x)
                else:    
                    if isinstance(x,float):
                        x=int(x)
                    if PDF[0] and columnas == PDF[1]:
                        if self.editar:
                            if x == None or x == '':
                                self.filas[len(self.filas)-1].add_widget(campoBD2(True,indexID,pag=pag,editar=True,index=self.index))
                            else:
                                self.filas[len(self.filas)-1].add_widget(campoBD2(False,indexID,str(x),pag=pag,editar=True,index=self.index))
                        else:
                            if x == None or x == '':
                                self.filas[len(self.filas)-1].add_widget(campoBD2(True,indexID,pag=pag,index=self.index))
                            else:
                                self.filas[len(self.filas)-1].add_widget(campoBD2(False,indexID,str(x),pag=pag,index=self.index))
                        
                    else:
                        self.filas[len(self.filas)-1].add_widget(campoBD1(str(x),cont,indexID,entrada[columnas],on_press=self.info))
                    columnas += 1
            color = not color
                                
            cont += 1

        for row in self.filas:
            self.contenedor.add_widget(row)
            
        self.add_widget(self.contenedor)

    #Función para ignorar tildes
    def sinTilde(self,word1,word2):
        text = "REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(LOWER(`"+str(word1)+"`),'á','a'), 'é','e'),'í','i'),'ó','o'),'ú','u'),'ñ','n'),'Á','A'), 'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N') LIKE REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(LOWER('%"+str(word2)+"%'),'á','a'), 'é','e'),'í','i'),'ó','o'),'ú','u'),'ñ','n'),'Á','A'), 'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N')"
        return text
    
    def info(self,obj):
        
        self.id = obj.ID
        self.campo = obj.col
        self.filas[obj.num].dark = 0.2 - self.filas[obj.num].dark
        self.filas[obj.num].canvas.ask_update()
        if self.select != obj.num:
            self.filas[self.select].dark = 0
            self.filas[self.select].canvas.ask_update()
        self.select = obj.num
        if self.filas[obj.num].dark == 0.2:
            self.aplicacion.pantalla.select = True
            self.information = []
            for row in self.c.execute('SELECT * From '+ self.table+' WHERE `' + self.index + "` = '" + str(self.id) +"'"):
                self.information.append(row)
        else:
            self.aplicacion.pantalla.select = False
        self.aplicacion.pantalla.toolbarBuilder()

    def calcAct(self,pag=0):#Actualizar la página del calculo de estadísticas
        self.aplicacion.pantalla.select=False
        self.scroll_y=1
        self.contenedor=DataViewerContainer()
        self.contenedor.bind(minimum_height=self.contenedor.setter('height'))
        self.filas=[]
        color = False
        top = len(self.listEst)
        if top > 50*(pag+1):
            top = 50*(pag+1)
        num = 0
        for item in sorted(self.listEst,
         key=itemgetter(1),reverse=True)[50*pag:top]:
            self.filas.append(Fila(color))
            for element in item:
                self.filas[len(self.filas)-1].add_widget(campoBD1(str(element),num,on_press=self.info))
            color = not color
            num = num +1
        for row in self.filas:
            self.contenedor.add_widget(row)
        self.add_widget(self.contenedor)

    def calc(self,text,filtroAct,pag=0): #Realizar el calculo de la estadística según las opciones escogidas
        self.aplicacion.pantalla.select=False
        self.scroll_y=1
        self.calculando = text
        self.contenedor=DataViewerContainer()
        self.contenedor.bind(minimum_height=self.contenedor.setter('height'))
        self.filas=[]
        if filtroAct:
            filtro = "SELECT `"+ str(text) +"` " + self.filtroWhere
        else:
            filtro = "SELECT `"+ str(text) +"` FROM "+ self.table
        
        data = pd.read_sql_query(filtro, miConexion)
        data=pd.unique(data[str(text)])
        data2 =[]
        data3 =[]
        dataCount=0
        for palabra in data:
            if palabra != None:
                
                a,b = 'áéíóúüñÁÉÍÓÚÜÑ','aeiouunAEIOUUN'
                trans = str.maketrans(a,b)
                data2.append(" ".join(((str(palabra).upper()).translate(trans)).split()))
            dataCount+=1
            
        for palabra in list(set(data2)):
            data3.append(palabra.split())

        self.contenedor=DataViewerContainer()
        self.contenedor.bind(minimum_height=self.contenedor.setter('height'))
        self.filas=[]
 
        self.listEst=[]
        palabras=""
        self.totalDatos=len(data3)
        for diferente in data3:
            if diferente != None:
                if filtroAct:
                    filtro2 = "SELECT COUNT(`"+ str(text) +"`) "+self.filtroWhere
                else:
                    filtro2 = "SELECT COUNT(`"+ str(text) +"`) FROM "+ self.table+" WHERE "
                primero = True
                for palabra in diferente:
                    palabras += str(palabra)+" "
                    if primero:
                        primero=False
                        if filtroAct:
                            filtro2 += "and " + self.sinTilde(str(text),str(palabra)) 
                        else:
                            filtro2 += self.sinTilde(str(text),str(palabra)) 
                    else:                        
                        filtro2 += "and " + self.sinTilde(str(text),str(palabra)) 
                for x in self.c.execute(filtro2):
                    for y in x:
                        if filtroAct:
                            self.listEst.append((palabras,y,str(round((y*100) /self.totalDatos2,2))+"%")) 
                        else:
                            self.listEst.append((palabras,y,str(round((y*100) /self.total,2))+"%"))
                palabras=""
        self.calcAct(pag)

    #Función para agregar PDF
    def insertPdf(self,fileName,idNum):
        filtro = "UPDATE "+ self.table+" SET PDF = '" + str(fileName) + "' WHERE `" + self.index + "` = '" + str(idNum) +"'"
        self.c.execute(filtro)
        miConexion.commit()

    def reset(self):
       self.clear_widgets()

'''
=======================
Widgets complementarios
=======================
Clases de separadores, botones y contenedores varios
'''

class DataViewerContainer(StackLayout):
    pass

class campoBD1(ButtonBehavior,BoxLayout):
    ID = NumericProperty()
    g = StringProperty()
    col = StringProperty()
    num = NumericProperty()
    def __init__(self,texto,num,idNum=0,campo='',**kwargs):
        super(campoBD1, self).__init__(**kwargs)
        self.g = texto
        self.col = campo
        self.ID = idNum
        self.num = num

class Fila(BoxLayout):
    color = BooleanProperty()
    dark = NumericProperty()
    def __init__(self,colorCampo):
        super(Fila, self).__init__()
        self.color=colorCampo
        self.dark =0

class campoBD2(BoxLayout):
    pdf = BooleanProperty()
    edit = BooleanProperty()
    ID = NumericProperty()
    pag = NumericProperty()
    def __init__(self,pdf,idNum,path='',pag=0,editar=False,index = 'index'):
        super(campoBD2, self).__init__()
        self.pdf = pdf
        self.ID = idNum
        self.g = path
        self.pag = pag
        self.index = index
        self.edit = editar
      
    def agregarPDF(self):
        if (aplicacion.agregar):
            aplicacion.archivo = self.ID
            aplicacion.pag = self.pag
            aplicacion.SubiendoArchivo = True
            self.clear_widgets()
            self.add_widget(Label(text='Arrastrar archivo',color=(0.8,0,0)))
            aplicacion.agregar=False

    # def editar(self):
    #     aplicacion.pantalla.editPDF = True
    #     aplicacion.pantalla.toolbarBuilder()
    def delete(self):
        filtro = "UPDATE "+table+" SET PDF = '' WHERE `" + self.index + "` = '" + str(self.ID) +"'"
        c.execute(filtro)
        miConexion.commit()
        aplicacion.buildList()

    def pasar(self):
        pass

    def verPDF(self):
        path = self.g
        webbrowser.open_new(path)