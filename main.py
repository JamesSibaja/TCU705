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
from pdf2image import convert_from_path
import shutil
import time
import webbrowser
import math

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

# config
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'system')
Builder.load_file('design.kv')

SubiendoArchivo = False

'''
================
Widget principal
================
Widget asociado a la totalidad de la ventana donde se presenta la interfaz de la aplicación
'''
#Widget principal
class DatabaseGUI(BoxLayout): 
    def __init__(self):
        super(DatabaseGUI, self).__init__()
        #Aquí se define el menú inicial
        self.menu = MenuInicial()
        self.menu.add_widget( Button(text='Mis proyectos', size_hint=(.3, .1),
                pos_hint={'x':.15, 'y':.2},on_press=self.build))
        self.menu.add_widget( Button(text='Nuevo proyecto', size_hint=(.3, .1),
                pos_hint={'x':.55, 'y':.2},on_press=self.build))
        self.menu.add_widget(Image(source='logo.png', size_hint=(1, .6),
                pos_hint={'x':0, 'y':0.35}))
        self.add_widget(self.menu)

    #Constructor de la ventana principal
    def build(self,obj):
        self.clear_widgets()
        #self.divisor=BoxLayout()
        #self.contenedorBarra = BoxLayout(size_hint=(0.25,1),orientation= 'vertical')
        self.numPag = 0
        self.contenedor = Toolbar()   
        self.listaFiltros =[]
        self.filaTitulo = Fila2()
        self.pagina = Fila2()
        self.camposOpcion = []
        self.filtrosOpcion = []
        self.filtros = []
        self.campos = []
        self.nombres = list(map(lambda x: x[0], c.execute('select * from CV').description))
        index = self.nombres[0]
        self.nombres.pop(0)
        contCampos=0
        for selectField in self.nombres:
            if(contCampos < 3 ):
                self.camposOpcion.append(True)
                self.campos.append(str(selectField))
            else:
                self.camposOpcion.append(False)
            self.filtrosOpcion.append(False)
            contCampos+=1
        self.lista = DataViewer(index=index,entrada=self.campos,pag = self.numPag)
        self.pagina.add_widget(TitleFilter(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50)),filtro=False))
        self.pagina.add_widget(Button(text='Siguiente >',on_press=self.siguientePagina))
        self.contenedorLista = BoxLayout(orientation= 'vertical')
        for selectField in self.campos:
            self.filaTitulo.add_widget(TitleField(selectField))
        self.palabrasBuscadas={}
        self.nuevoFiltro = False
        self.cambiarCampo = False
        self.contenedor.bind(minimum_height=self.contenedor.setter('height'))
        #self.divisor.add_widget(self.contenedor)
        #self.contenedorBarra.add_widget(self.divisor)
        #self.add_widget(self.contenedorBarra)
        self.add_widget(self.contenedor)
        self.add_widget(ToolbarShow(on_press=self.toolbarHide))
        self.contenedorLista.add_widget(self.filaTitulo)
        self.contenedorLista.add_widget(self.lista)
        self.contenedorLista.add_widget(self.pagina)
        self.add_widget(self.contenedorLista)
        self.toolbarBuilder()

    def siguientePagina(self,obj):
        self.lista.reset()
        self.numPag +=1
        self.lista.build(entrada=self.campos,pag=self.numPag,filtros= self.listaFiltros,busqueda=self.filtros)
        self.pagina.clear_widgets()
        if(self.numPag>0):
            self.pagina.add_widget(Button(text='< Anterior',on_press=self.anteriorPagina))
        self.pagina.add_widget(TitleFilter(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50)),filtro=False))
        if(self.numPag + 1 < math.ceil(self.lista.totalDatos/50)):
            self.pagina.add_widget(Button(text='Siguiente >',on_press=self.siguientePagina))

    def anteriorPagina(self,obj):
        self.lista.reset()
        self.numPag = self.numPag-1
        if(self.numPag<math.ceil(self.lista.totalDatos/50)):
            self.lista.build(entrada=self.campos,pag=self.numPag,filtros= self.listaFiltros,busqueda=self.filtros)
        
        self.pagina.clear_widgets()
        if(self.numPag>0):
            self.pagina.add_widget(Button(text='< Anterior',on_press=self.anteriorPagina))
        self.pagina.add_widget(TitleFilter(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50)),filtro=False))
        if(self.numPag + 1 < math.ceil(self.lista.totalDatos/50)):
            self.pagina.add_widget(Button(text='Siguiente >',on_press=self.siguientePagina))

    def toolbarHide(self,obj): 
        self.contenedor.show = not self.contenedor.show
        if self.contenedor.show:
            self.toolbarBuilder()
        else:
            self.contenedor.clear_widgets()
            

    #Constructor de la barra de herramientas
    def toolbarBuilder(self):   
        if self.nuevoFiltro or self.cambiarCampo:
            contTexto =0
            for filtro in self.filtros:
                self.palabrasBuscadas.update({self.listaFiltros[contTexto]:filtro.text})
                contTexto += 1
            self.contenedor.clear_widgets()
            self.filtrosBotones = []
            contBotones =0
            for posibleFiltro in self.nombres:
                if(self.cambiarCampo):
                    self.newBoton= BotonOpcion(text = str(posibleFiltro),background_color =(0, 0.81, 0.59, 0.8) if self.camposOpcion[contBotones] else (0.8,0, 0.1, 1), size_hint=(1, 0.05),on_press=self.nuevoFinal)
                if(self.nuevoFiltro):
                    self.newBoton= BotonOpcion(text = str(posibleFiltro),background_color =(0, 0.81, 0.59, 0.8) if self.filtrosOpcion[contBotones] else (0.8,0, 0.1, 1), size_hint=(1, 0.05),on_press=self.nuevoFinal)
                self.filtrosBotones.append(self.newBoton)
                contBotones +=1
            n=0
            for botonFiltro in self.filtrosBotones:
                self.contenedor.add_widget(self.filtrosBotones[n])
                n+=1
            self.contenedor.add_widget(BotonOpcion(border= (10,10,10,10),text = 'Aceptar',background_color =(0, 0.59, 0.81,1),on_press=self.aceptarCambios))

        else:
            self.contenedor.clear_widgets()
            self.filtros = []
            self.submit = BotonOpcion(text = 'Aplicar Filtros',background_color =(0.3, 0.59, 0.1,1),on_press=self.buscar)
            self.submit2 = BotonOpcion(text = 'Filtros',background_color =(0, 0.59, 0.81,1),on_press=self.nuevoInicio)
            self.submit3 = BotonOpcion(text = 'Columnas',background_color =(0, 0.59, 0.81,1),on_press=self.nuevoCampo)
            
            self.contenedor.add_widget(self.submit3)
            self.contenedor.add_widget(self.submit2)
            for filtro in self.listaFiltros:
                if (self.palabrasBuscadas.get(filtro) != None):
                    self.filtros.append(TextInput(text=str(self.palabrasBuscadas[filtro]),size_hint=(1, 0.05)))
                else:
                    self.filtros.append(TextInput(text='',size_hint=(1, 0.05)))
            n=0
            self.contenedor.add_widget(Separador2())
            
            for filtro in self.filtros:            
                self.contenedor.add_widget(TitleFilter(texto=self.listaFiltros[n]+':'))
                self.contenedor.add_widget(self.filtros[n])
                n+=1
            if n > 0:
                self.contenedor.add_widget(Separador())
                self.contenedor.add_widget(self.submit)
           
    def cambiarColumnas(self):
        self.lista.reset()
        self.campos=[]
        contColum = 0
        for field in self.nombres:
            if(self.camposOpcion[contColum]):
                self.campos.append(str(field))
            contColum += 1
        self.filaTitulo.clear_widgets()
        for selectField in self.campos:
            self.filaTitulo.add_widget(TitleField(selectField))
        self.lista.build(entrada=self.campos,filtros= self.listaFiltros,pag=self.numPag,busqueda=self.filtros)       

    def buscar(self,obj):
        self.lista.reset()
        
        self.numPag = 0
        self.lista.build(entrada=self.campos,pag=0,filtros= self.listaFiltros,busqueda=self.filtros)
        self.pagina.clear_widgets()
        if(self.numPag>0):
            self.pagina.add_widget(Button(text='< Anterior',on_press=self.anteriorPagina))
       
        self.pagina.add_widget(TitleFilter(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50)),filtro=False))
        if(self.numPag + 1 < math.ceil(self.lista.totalDatos/50)):
                self.pagina.add_widget(Button(text='Siguiente >',on_press=self.siguientePagina))
                
    def nuevoInicio(self,obj):
        self.nuevoFiltro = True
        self.toolbarBuilder()

    def nuevoFinal(self,obj):
        if (self.nuevoFiltro):
            contFiltro = 0
            for field in self.nombres:
                if (field == obj.text):
                    self.filtrosOpcion[contFiltro]  = not self.filtrosOpcion[contFiltro]
                contFiltro += 1
            self.toolbarBuilder()

        if (self.cambiarCampo):
            contTitulo = 0
            for field in self.nombres:
                if(field == obj.text):
                    self.camposOpcion[contTitulo] = not self.camposOpcion[contTitulo]
                contTitulo += 1 

            self.toolbarBuilder()
            
    def aceptarCambios(self,obj):
            if(self.cambiarCampo):
                self.cambiarColumnas()
            if(self.nuevoFiltro):
                contFiltro = 0
                self.listaFiltros = []
                for field in df:
                    if (self.filtrosOpcion[contFiltro]):
                        self.listaFiltros.append(str(field))
                    contFiltro += 1
            self.cambiarCampo = False
            self.nuevoFiltro = False
            self.toolbarBuilder()

    def nuevoCampo(self,obj):
        self.cambiarCampo = True
        self.toolbarBuilder()

def on_enter(instance, value):
    print('User pressed enter in', instance)

'''
===================
Widgets secundarios
===================
Diferentes widgets que complementan la ventana principal y conforman la interfaz gráfica
'''    
#Widget que muestra los datos solicitados de la base de datos
class DataViewer(ScrollView):
    end = BooleanProperty()
    def __init__(self,index,entrada,pag=0):
        super(DataViewer, self).__init__()
        self.index = index
        self.totalDatos = 0
        for row in c.execute('SELECT * From CV'):
            self.totalDatos += 1
        self.build(entrada =entrada,imagen=True,pag=0)

    def build(self,entrada,pag,filtros=[],busqueda=[],imagen=False):
        aplicacion.agregar = True
        self.contenedor=DataViewerContainer()
        self.contenedor.bind(minimum_height=self.contenedor.setter('height'))
        self.filas=[]
        PDF = (False,0)
        color = True
        cont = 0
        
        filtro = "SELECT `"+ self.index +"`"
        n = 0
        for selectField in entrada:
            if (n == 0):
                filtro += ", "
            filtro += "`" + str(selectField) + "`"
            if (selectField == 'PDF'):
                PDF = (True,n)
            if(selectField != entrada[len(entrada)-1]):
                filtro += ", "
            n += 1
            
        filtro +=" FROM CV"
        n=0
        primero=True
        for elemento in busqueda:
            if elemento.text.split() != []:
                if primero:
                    filtro +=" WHERE "

                for palabra in elemento.text.split():
                    if primero:
                        primero = False
                        filtro +="`" + str(filtros[n])+"` COLLATE NOACCENTS LIKE '%" + str(palabra)+"%'"
                        
                    else:
                        filtro +="and `"+str(filtros[n])+"` LIKE '%" + str(palabra)+"%'"
            n+=1
        filtro += " LIMIT 50 OFFSET " + str(pag*50)
        color = False
        data = pd.read_sql_query(filtro, miConexion)
        data2=pd.unique(data[str(entrada[0])])
        for diferente in data2:
            filtro2 = "SELECT COUNT(`"+ str(entrada[0]) +"`) FROM CV WHERE `" + str(entrada[0]) + "` = '"+str(diferente)+"'"
            for x in c.execute(filtro2):
                for y in x:
                    print(y)
        for row in c.execute(filtro):
            
            self.filas.append(Fila())
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
                        if x == None:
                            self.filas[len(self.filas)-1].add_widget(campoBD2(color,True,indexID,pag=pag))
                        else:
                            self.filas[len(self.filas)-1].add_widget(campoBD2(color,False,indexID,str(x),pag=pag))
                    else:
                        self.filas[len(self.filas)-1].add_widget(campoBD1(str(x),color))
                    columnas += 1
            color = not color
                                
            cont += 1

        for row in self.filas:
            self.contenedor.add_widget(row)
            
        self.add_widget(self.contenedor)

    def insertPdf(self,fileName,idNum,pag,filtros=[],busqueda=[],imagen=False):
        cont = 0
        cont2 = 0
        
        #filtro = "SELECT * FROM CV LIMIT 50 OFFSET " + str(pag*50) + " WHERE " + self.index + " = " + str(idNum)
        # n=0
        # primero=True
        # for elemento in busqueda:
        #     if elemento.text.split() != []:
        #         if primero:
        #             filtro +=" WHERE " + self.index + " LIKE " + str(idNum)

        #         for palabra in elemento.text.split():
        #             if primero:
        #                 primero = False
        #                 filtro +="`" + str(filtros[n])+"` COLLATE NOACCENTS LIKE '%" + str(palabra)+"%'"
                        
        #             else:
        #                 filtro +="and `"+str(filtros[n])+"` LIKE '%" + str(palabra)+"%'"
        #     n+=1
       
        # palabras = []
        # for row in c.execute(filtro):
            
        #     if cont == idNum:
        #         for x in row:
        #             palabras.append(str(x))            
        #     cont += 1
        # n=0
        # primero=True
        filtro = "UPDATE CV SET PDF = '" + str(fileName) + "' WHERE `" + self.index + "` = '" + str(idNum) +"'"
        # for nombre in list(map(lambda x: x[0], c.execute('select * from CV').description)):

        #     if primero:
        #         primero = False
        #         if(str(palabras[n])!='None'):
        #             filtro +="`" + str(nombre)+"` = '" + str(palabras[n])+"' "

        #     else:
        #         if(str(palabras[n])!='None'):
        #             filtro +=" and `"+str(nombre)+"` = '" + str(palabras[n])+"' "
        #     n+=1
        print(filtro)
        c.execute(filtro)
        miConexion.commit()

    def reset(self):
       self.clear_widgets()

#Widget que define los cuadros con los titulos de columna de las bases de datos
class TitleField(BoxLayout):
    g = StringProperty()
    def __init__(self,texto):
        super(TitleField, self).__init__()
        self.g = texto

#Widget que define los cuadros con los titulos de los filtros
class TitleFilter(BoxLayout):
    g = StringProperty()
    filtro = BooleanProperty()
    def __init__(self,texto,filtro = True):
        super(TitleFilter, self).__init__()
        self.g = texto
        self.filtro =filtro

#Separadores y contenedores varios
class Separador2(BoxLayout):
    pass

class Separador(ScrollView):
    pass

class Divisor(BoxLayout):
    pass

class Fila(BoxLayout):
    pass

class Fila2(BoxLayout):
    pass

class Fila3(BoxLayout):
    pass

class BotonOpcion(Button):
    pass

class BotonOpcion2(Button):
    pass

class campoBD1(BoxLayout):
    g = StringProperty()
    color = BooleanProperty()
    def __init__(self,texto,colorCampo):
        super(campoBD1, self).__init__()
        self.g = texto
        self.color=colorCampo

class OcultarBarra(FloatLayout):
    pass

class campoBD2(BoxLayout):
    color = BooleanProperty()
    pdf = BooleanProperty()
    ID = NumericProperty()
    pag = NumericProperty()
    def __init__(self,colorCampo,pdf,idNum,path='',pag=0):
        super(campoBD2, self).__init__()
        self.pdf = pdf
        self.color = colorCampo
        self.ID = idNum
        self.g = path
        self.pag = pag
      
    def agregarPDF(self):
        if (aplicacion.agregar):
            aplicacion.archivo = self.ID
            aplicacion.pag = self.pag
            aplicacion.SubiendoArchivo = True
            self.clear_widgets()
            self.add_widget(Label(text='Arrastrar archivo',color=(0.8,0,0)))
            aplicacion.agregar=False

    def verPDF(self):
        path = self.g
        webbrowser.open_new(path)

class Toolbar(ButtonBehavior,StackLayout):
    show = BooleanProperty()
    def __init__(self):
        super(Toolbar, self).__init__()
        self.show=True

class ToolbarShow(ButtonBehavior,BoxLayout):
     def __init__(self,**kwargs):
        super(ToolbarShow, self).__init__(**kwargs)

class DataViewerContainer(StackLayout):
    pass

class MenuInicial(FloatLayout):
    pass    

class Cuadro(BoxLayout):
    pass

'''
====================
Aplicación principal
====================
Clase que define la aplicación principal
'''
class DatabaseGUIApp(App): #Aplicación principal
    title = 'Plataforma'

    def build(self):
        Window.bind(on_dropfile=self._on_file_drop)
        self.SubiendoArchivo = False
        self.pantalla = DatabaseGUI()
        self.archivo = ''
        self.nombreArchivo=''
        self.agregar=True
        self.pag = 0
        return self.pantalla

    #Función que se ejecuta al arrastrar un archivo a la ventana
    def _on_file_drop(self, window, file_path):
        if self.SubiendoArchivo:
            self.agregar=True
            self.nombreArchivo = "./pdf/" + str(time.time()) + ".pdf"
            self.SubiendoArchivo = False
            shutil.copy(file_path,self.nombreArchivo)
            print(self.pag)
            self.pantalla.lista.insertPdf(fileName=self.nombreArchivo,idNum=self.archivo,pag=self.pag,filtros= self.pantalla.listaFiltros,busqueda=self.pantalla.filtros)
            self.pantalla.lista.reset()
            self.pantalla.lista.build(entrada=self.pantalla.campos,pag=self.pag,filtros= self.pantalla.listaFiltros,busqueda=self.pantalla.filtros)

    def on_pause(self):
        return True

    def on_resume(self):
        pass


'''
=================
Función principal
=================
Crea la base de datos y crea el objeto aplicación a partir de clase  DatabaseGUIApp
'''


if __name__ == '__main__': #Función principal

    table = "CV"
    path = "./cv_acosta.xlsx"
    xls = pd.ExcelFile(path) #Se carga el documento de excel
    miConexion = sqlite3.connect('base')    
    df = pd.read_excel(path) #Se lee el documento de excel  
    df.to_sql(name = table, con = miConexion, if_exists = 'replace', index = True) #Se pasa el documento de excel a sql
    c = miConexion.cursor()
    c.execute('ALTER TABLE CV ADD PDF TEXT')
    pathFile = ''    
    SubiendoArchivo = False
    aplicacion = DatabaseGUIApp() #Se crea un objeto con la aplicación
    aplicacion.run() #Se ejecuta la aplicación
    c.close
    miConexion.close