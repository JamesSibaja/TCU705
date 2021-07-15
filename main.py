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
        self.tablas = False
        self.menuFiltro = False
        self.estadisticas = False
        self.filtroCalc = False
        self.datoCalc = ""
        self.contenedor = Toolbar() 
        #self.contenedorStack= ToolbarContaner()  
        self.listaFiltros =[]
        self.filaTitulo = FilaTitulo()
        self.pagina = FilaPag()
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
        self.pagina.add_widget(BoxLayout())
        self.pagina.add_widget(TitlePag(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50))))
        self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='Siguiente >',on_press=self.siguientePagina))
        self.contenedorLista = BoxLayout(padding = 10,orientation= 'vertical')
        for selectField in self.campos:
            self.filaTitulo.add_widget(TitleField(selectField))
        self.palabrasBuscadas={}
        self.nuevoFiltro = False
        self.newEst = False
        self.cambiarCampo = False
        
        #self.divisor.add_widget(self.contenedor)
        
        #self.add_widget(self.contenedorBarra)
        self.add_widget(self.contenedor)
        #self.contenedor.add_widget(self.contenedorStack)
        #self.contenedorStack.bind(minimum_height=self.contenedor.setter('height'))
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
            self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='< Anterior',on_press=self.anteriorPagina))
        else:
            self.pagina.add_widget(BoxLayout())
        self.pagina.add_widget(TitlePag(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50))))
        if(self.numPag + 1 < math.ceil(self.lista.totalDatos/50)):
            self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='Siguiente >',on_press=self.siguientePagina))
        else:
            self.pagina.add_widget(BoxLayout())

    def anteriorPagina(self,obj):
        self.lista.reset()
        self.numPag = self.numPag-1
        if(self.numPag<math.ceil(self.lista.totalDatos/50)):
            self.lista.build(entrada=self.campos,pag=self.numPag,filtros= self.listaFiltros,busqueda=self.filtros)
        
        self.pagina.clear_widgets()
        if(self.numPag>0):
            self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='< Anterior',on_press=self.anteriorPagina))
        else:
            self.pagina.add_widget(BoxLayout())
        self.pagina.add_widget(TitlePag(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50))))
        if(self.numPag + 1 < math.ceil(self.lista.totalDatos/50)):
            self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='Siguiente >',on_press=self.siguientePagina))
        else:
            self.pagina.add_widget(BoxLayout())

    def toolbarHide(self,obj): 
        self.contenedor.show = not self.contenedor.show
        if self.contenedor.show:
            self.toolbarBuilder()
        else:
            self.contenedor.clear_widgets()
            

    #Constructor de la barra de herramientas
    def toolbarBuilder(self):   
        self.contenedor.scroll_y=1
        self.contenedor.clear_widgets()
        self.contenedor.build()
        if self.nuevoFiltro or self.cambiarCampo or self.newEst:
            print(self.nuevoFiltro)
            print(self.cambiarCampo)
            print(self.newEst)
            contTexto =0
            for filtro in self.filtros:
                self.palabrasBuscadas.update({self.listaFiltros[contTexto]:filtro.text})
                contTexto += 1
            self.contenedor.stack.clear_widgets()
            self.filtrosBotones = []
            contBotones =0

            if(self.cambiarCampo):
                self.contenedor.stack.title = ToolbarTitle(on_press=self.volverMenu)
                self.contenedor.stack.title.add_widget(ToolbarText("<",size=0.2))
                self.contenedor.stack.title.add_widget(ToolbarText("Columnas"))
                self.contenedor.stack.add_widget(self.contenedor.stack.title)
                self.contenedor.stack.add_widget(Separador())
                self.contenedor.stack.add_widget(Title("Mostrar:"))
                # self.contenedor.stack.add_widget(Color(">Ocultar",True))
                # self.contenedor.stack.add_widget(Color(">Mostrar",False))
                
                
            if(self.nuevoFiltro):
                self.contenedor.stack.title = ToolbarTitle(on_press=self.volverMenu)
                self.contenedor.stack.title.add_widget(ToolbarText("<",size=0.2))
                self.contenedor.stack.title.add_widget(ToolbarText("Filtros"))
                self.contenedor.stack.add_widget(self.contenedor.stack.title)
                self.contenedor.stack.add_widget(Separador())
                self.contenedor.stack.add_widget(Title("Filtrar por:"))
                # self.contenedor.stack.add_widget(Color(">No incluir",True))
                # self.contenedor.stack.add_widget(Color(">Incluir",False))
                

            if(self.newEst):
                self.contenedor.stack.title = ToolbarTitle(on_press=self.volverMenu)
                self.contenedor.stack.title.add_widget(ToolbarText("<",size=0.2))
                self.contenedor.stack.title.add_widget(ToolbarText("Datos"))
                self.contenedor.stack.add_widget(Separador())
                self.contenedor.stack.add_widget(self.contenedor.stack.title)
                self.contenedor.stack.add_widget(Title("Escoger Datos:"))
                self.contenedor.stack.add_widget(Separador())
            for posibleFiltro in self.nombres:
                if(self.cambiarCampo):
                    #self.newBoton= BotonOpcion(text = str(posibleFiltro),background_color =(0, 0.81, 0.59, 0.8) if self.camposOpcion[contBotones] else (0.8,0, 0.1, 1), size_hint=(1, 0.05),on_press=self.nuevoFinal)
                    if (self.camposOpcion[contBotones]):
                        self.newBoton= ButtonOption(texto = str(posibleFiltro),select= True, on_press=self.nuevoFinal)
                    else:
                        self.newBoton= ButtonOption(texto = str(posibleFiltro),on_press=self.nuevoFinal)
                if(self.nuevoFiltro):
                    if (self.filtrosOpcion[contBotones]):
                        self.newBoton= ButtonOption(texto = str(posibleFiltro),select= True, on_press=self.nuevoFinal)
                    else:
                        self.newBoton= ButtonOption(texto = str(posibleFiltro),on_press=self.nuevoFinal)
                if(self.newEst):
                    # if (self.camposOpcion[contBotones]):
                    #     self.newBoton= ButtonOption(texto = str(posibleFiltro),select= True, on_press=self.newFinal)
                    # else:
                    self.newBoton= ButtonMain(texto = str(posibleFiltro),on_press=self.newFinal)                    
                self.filtrosBotones.append(self.newBoton)
                contBotones +=1
            n=0
            for botonFiltro in self.filtrosBotones:
                self.contenedor.stack.add_widget(self.filtrosBotones[n])
                n+=1
            if(not self.newEst):
            #     self.contenedor.stack.add_widget(BotonOpcion(border= (10,10,10,10),text = 'Volver',background_color =(0.8,0, 0.1, 1),on_press=self.aceptarCambios))
            # else:
                self.contenedor.stack.add_widget(Separador2())
                self.contenedor.stack.add_widget(ButtonAccept(texto = 'Aceptar',on_press=self.aceptarCambios))
                #self.contenedor.stack.add_widget(BotonOpcion(border= (10,10,10,10),text = 'Aceptar',background_color =(0, 0.59, 0.81,1),on_press=self.aceptarCambios))
            
            #self.menuFiltro = False

            #self.nuevoFiltro = True
        else:
            
            if self.menuFiltro:
                
                self.contenedor.stack.clear_widgets()
                self.filtros = []
                self.menuFiltro = False
                if self.estadisticas:
                    self.submit = ButtonAccept(texto = 'Usar',on_press=self.usarFiltro)
                else:
                    self.submit = ButtonAccept(texto = 'Filtrar',on_press=self.buscar)

                for filtro in self.listaFiltros:
                    if (self.palabrasBuscadas.get(filtro) != None):
                        self.filtros.append(TextInput(text=str(self.palabrasBuscadas[filtro]),size_hint_y=None,height=45))
                    else:
                        self.filtros.append(TextInput(text='',size_hint_y=None,height=45))
                n=0
                self.contenedor.stack.title = ToolbarTitle(on_press=self.volverMenu)
                self.contenedor.stack.title.add_widget(ToolbarText("<",size=0.2))
                self.contenedor.stack.title.add_widget(ToolbarText("Filtros"))
                self.contenedor.stack.add_widget(self.contenedor.stack.title)
                self.contenedor.stack.add_widget(Separador2())
                self.contenedor.stack.add_widget(ButtonMain(texto = 'Editar Filtros',on_press=self.editarFiltros))
                self.contenedor.stack.add_widget(ButtonMain(texto = 'Limpiar Filtros',on_press=self.limpiar))
                #self.contenedor.stack.add_widget(self.submit)
                #self.contenedor.stack.add_widget(ButtonMain(texto = 'Volver',background_color =(0.8,0, 0.1, 1),on_press=self.aceptarCambios))
                self.contenedor.stack.add_widget(Separador2())
                for filtro in self.filtros:            
                    self.contenedor.stack.add_widget(TitleFilter(texto=self.listaFiltros[n]+':'))
                    self.contenedor.stack.add_widget(self.filtros[n])
                    n+=1
                if n > 0:
                    self.contenedor.stack.add_widget(Separador())
                    self.contenedor.stack.add_widget(self.submit)
            else:
                if self.estadisticas:
                    self.contenedor.stack.clear_widgets()
                    self.contenedor.stack.title = ToolbarTitle(on_press=self.volverMenu)
                    self.contenedor.stack.title.add_widget(ToolbarText("<",size=0.2))
                    self.contenedor.stack.title.add_widget(ToolbarText("Estadísticas"))
                    self.contenedor.stack.add_widget(self.contenedor.stack.title)
                   # self.contenedor.stack.add_widget(Title("Estadísticas"))

                    #self.contenedor.stack.add_widget(Separador2())
                    self.contenedor.stack.add_widget(Separador2())
                    self.contenedor.box = EstBox()
                    self.contenedor.box.add_widget(Title("Filtro"))
                    if self.filtroCalc:
                        self.contenedor.box.add_widget(BotonOpcion(text = 'Usar',background_color =(0, 0.81, 0.59, 1),on_press=self.abFiltro))
                        self.botonFiltro = BotonOpcion(disabled =False,text = 'Filtros',on_press=self.nuevoInicio)
                    else:
                        self.contenedor.box.add_widget(BotonOpcion(text = 'No usar',background_color =(0.8,0, 0.1, 1),on_press=self.abFiltro))
                        self.botonFiltro = BotonOpcion(disabled =True,text = 'Filtros',on_press=self.nuevoInicio)
                    
                    self.contenedor.box.add_widget(self.botonFiltro)
                    self.contenedor.stack.add_widget(self.contenedor.box)
                    self.contenedor.stack.add_widget(Separador2())
                    self.contenedor.stack.add_widget(Title("Dato a calcular:"))
                    self.contenedor.stack.add_widget(BotonOpcion(text = self.datoCalc,on_press=self.editarDatos))
                    self.contenedor.stack.add_widget(Separador())
                    self.contenedor.stack.add_widget(ButtonAccept(texto = 'Calcular',on_press=self.calcular))
                    self.contenedor.stack.add_widget(Separador2())
                    #self.contenedor.stack.add_widget(BotonOpcion(border= (10,10,10,10),text = 'Volver',background_color =(0.8,0, 0.1, 1),on_press=self.volverMenu))
                    #self.contenedor.stack.add_widget(Separador2())
              
                else:
                    self.contenedor.stack.clear_widgets()
                    self.filtros = []
                    self.contenedor.stack.title = ToolbarTitle(on_press=self.volverMenu)
                    self.contenedor.stack.title.add_widget(ToolbarText("x",size=0.2))
                    self.contenedor.stack.title.add_widget(ToolbarText("Menú"))
                    self.contenedor.stack.add_widget(self.contenedor.stack.title)
                    self.contenedor.stack.add_widget(Separador())
                    self.submit2 =ButtonMain(texto = 'Filtro',on_press=self.nuevoInicio)
                    self.submit3 = ButtonMain(texto = 'Columnas',on_press=self.nuevoCampo)
                    self.submit4 = ButtonMain(texto = 'Estadísticas',on_press=self.nuevoEst)
                    #self.submit2 = BotonOpcion(text = 'Filtros',background_color =(0, 0.59, 0.81,1),on_press=self.nuevoInicio)
                    # self.submit3 = BotonOpcion(text = 'Columnas',background_color =(0, 0.59, 0.81,1),on_press=self.nuevoCampo)
                    # self.submit4 = BotonOpcion(text = 'Estadísticas',background_color =(0, 0.59, 0.81,1),on_press=self.nuevoEst)
                    
                    self.contenedor.stack.add_widget(self.submit3)
                    self.contenedor.stack.add_widget(self.submit2)
                    self.contenedor.stack.add_widget(self.submit4)
                    self.contenedor.stack.add_widget(ButtonMain(texto = 'Ajustes'))

                    self.contenedor.stack.add_widget(Separador2())
                    #self.contenedor.stack.add_widget(BotonOpcion(text = 'Salir',background_color =(0.8,0, 0.1, 1)))
            
                    
        self.contenedor.add_widget(self.contenedor.stack)

    def volverMenu(self,obj):
        self.nuevoFiltro = False
        self.menuFiltro = False
        self.cambiarCampo = False
        self.estadisticas = False
        self.nuevoFiltro = False
        self.newEst = False        
        self.toolbarBuilder()

    def abFiltro(self,obj):
        self.filtroCalc = not self.filtroCalc
        if self.filtroCalc:
            obj.background_color =(0, 0.81, 0.59, 1)
            obj.text = "Usar"
            self.botonFiltro.disabled = False
        else:
            obj.background_color =(0.8,0, 0.1, 1)
            self.botonFiltro.disabled = True
            obj.text = "No usar"

    def editarDatos(self,obj):
        self.newEst = True
        self.toolbarBuilder()

    def editarFiltros(self,obj):
        self.nuevoFiltro = True
        self.toolbarBuilder()

    def limpiar(self,obj):
        self.listaFiltros = []
        self.filtros = []
        contFiltro = 0
        for field in self.nombres:            
            self.filtrosOpcion[contFiltro]  = False
            
            contFiltro += 1

        self.menuFiltro = True
        self.cambiarCampo = False
        self.nuevoFiltro = False
        self.newEst = False
        
        self.toolbarBuilder()
        self.buscar()

    def newFinal(self,obj):
        self.datoCalc = obj.g
        self.cambiarCampo = False
        self.nuevoFiltro = False
        self.newEst = False
        self.estadisticas = True
        self.toolbarBuilder()

    def calcular(self,obj):
        self.lista.reset()
        self.tablas=True
        self.lista.calc(self.datoCalc,self.filtroCalc)
        self.numPag=0
        self.filaTitulo.clear_widgets()
        self.filaTitulo.add_widget(TitleField(self.datoCalc))
        self.filaTitulo.add_widget(TitleField('Cantidad'))
        self.filaTitulo.add_widget(TitleField('Porcentaje'))
    
        self.pagina.clear_widgets()

        if(self.numPag>0):
            self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='< Anterior',on_press=self.antPag))
        else:
            self.pagina.add_widget(BoxLayout())
       
        self.pagina.add_widget(TitlePag(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50))))
        if(self.numPag + 1 < math.ceil(self.lista.totalDatos/50)):
                self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='Siguiente >',on_press=self.sigPag))
        else:
            self.pagina.add_widget(BoxLayout())

        
        # self.cambiarCampo = False
        # self.nuevoFiltro = False
        # self.newEst = False
        # self.estadisticas = True
        # self.toolbarBuilder()

    def sigPag(self,obj):
        self.numPag=self.numPag + 1
        self.lista.reset()
        self.lista.calcAct(pag=self.numPag)
        self.pagina.clear_widgets()

        if(self.numPag>0):
            self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='< Anterior',on_press=self.antPag))
        else:
            self.pagina.add_widget(BoxLayout())
       
        self.pagina.add_widget(TitlePag(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50))))
        if(self.numPag + 1 < math.ceil(self.lista.totalDatos/50)):
                self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='Siguiente >',on_press=self.sigPag))
        else:
            self.pagina.add_widget(BoxLayout())

    def antPag(self,obj):
        self.numPag=self.numPag - 1 
        self.lista.reset()
        self.lista.calcAct(pag=self.numPag) 
        self.pagina.clear_widgets()

        if(self.numPag>0):
            self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='< Anterior',on_press=self.antPag))
        else:
            self.pagina.add_widget(BoxLayout())
       
        self.pagina.add_widget(TitlePag(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50))))
        if(self.numPag + 1 < math.ceil(self.lista.totalDatos/50)):
                self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='Siguiente >',on_press=self.sigPag))
        else:
            self.pagina.add_widget(BoxLayout())  

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
        if self.tablas:
            filtro = "SELECT COUNT(`"+self.lista.index+"`) "+ self.lista.filtroWhere
            for x in c.execute(filtro):
                        for y in x:
                            self.lista.totalDatos=y
            self.numPag=0
            self.pagina.clear_widgets()
            if(self.numPag>0):
                self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='< Anterior',on_press=self.anteriorPagina))
            else:
                self.pagina.add_widget(BoxLayout())
            self.pagina.add_widget(TitlePag(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50))))
            if(self.numPag + 1 < math.ceil(self.lista.totalDatos/50)):
                self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='Siguiente >',on_press=self.siguientePagina))
            else:
                self.pagina.add_widget(BoxLayout())
        self.tablas = False

    def buscar(self,obj=None):
        self.lista.reset()
        self.tablas = False
        self.numPag = 0
        self.lista.build(entrada=self.campos,pag=0,filtros= self.listaFiltros,busqueda=self.filtros)
        self.pagina.clear_widgets()
        filtro = "SELECT COUNT(`"+self.lista.index+"`) "+ self.lista.filtroWhere
        #print(filtro)
        for x in c.execute(filtro):
                    for y in x:
                        self.lista.totalDatos=y
                        self.lista.totalDatos2=y
        if(self.numPag>0):
            self.pagina.add_widget(Button(bold=True,background=(0,0,0,0),text='< Anterior',on_press=self.anteriorPagina))
        else:
            self.pagina.add_widget(BoxLayout())
       
        self.pagina.add_widget(TitlePag(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50))))
        if(self.numPag + 1 < math.ceil(self.lista.totalDatos/50)):
                self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='Siguiente >',on_press=self.siguientePagina))
        else:
            self.pagina.add_widget(BoxLayout())
                
    def nuevoInicio(self,obj):
        self.newEst = False
      
        if len(self.listaFiltros) == 0:
            self.nuevoFiltro = True
        else:
            self.menuFiltro = True
        self.toolbarBuilder()

    def nuevoEst(self,obj):
        if self.datoCalc == "":
            self.newEst = True
        else:
            self.estadisticas = True
        self.toolbarBuilder()

    def nuevoFinal(self,obj):
        if (self.nuevoFiltro):
            contFiltro = 0
            for field in self.nombres:
                if (field == obj.g):
                    self.filtrosOpcion[contFiltro]  = not self.filtrosOpcion[contFiltro]
                contFiltro += 1
            self.toolbarBuilder()

        if (self.cambiarCampo):
            contTitulo = 0
            for field in self.nombres:
                if(field == obj.g):
                    self.camposOpcion[contTitulo] = not self.camposOpcion[contTitulo]
                    obj.c = not obj.c
                contTitulo += 1 

            #self.toolbarBuilder()

    def usarFiltro(self,obj=None):
        self.lista.reset()
        self.tablas = False
        self.numPag = 0
        self.lista.build(entrada=self.campos,pag=0,filtros= self.listaFiltros,busqueda=self.filtros)
     
        self.menuFiltro = False
       
        self.cambiarCampo = False
        self.nuevoFiltro = False
        self.newEst = False
        
        self.pagina.clear_widgets()
        filtro = "SELECT COUNT(`"+self.lista.index+"`) "+ self.lista.filtroWhere
        #print(filtro)
        for x in c.execute(filtro):
                    for y in x:
                        self.lista.totalDatos=y
                        self.lista.totalDatos2=y
        if(self.numPag>0):
            self.pagina.add_widget(Button(bold=True,background=(0,0,0,0),text='< Anterior',on_press=self.anteriorPagina))
        else:
            self.pagina.add_widget(BoxLayout())
       
        self.pagina.add_widget(TitlePag(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50))))
        if(self.numPag + 1 < math.ceil(self.lista.totalDatos/50)):
                self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='Siguiente >',on_press=self.siguientePagina))
        else:
            self.pagina.add_widget(BoxLayout())
        
        self.toolbarBuilder()
            
    def aceptarCambios(self,obj):
        # print(self.nuevoFiltro)
        # print(self.menuFiltro)
        if(self.menuFiltro):
            self.nuevoFiltro = False
        self.menuFiltro = False
        if(self.cambiarCampo):
            self.cambiarColumnas()
        if(self.nuevoFiltro):
            self.menuFiltro = True
            #self.estadisticas = False
            contFiltro = 0
            self.listaFiltros = []
            for field in df:
                if (self.filtrosOpcion[contFiltro]):
                    self.listaFiltros.append(str(field))
                contFiltro += 1
        self.cambiarCampo = False
        self.nuevoFiltro = False
        self.newEst = False
        
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
        self.filtroWhere = ''
        self.filtroSelect = ''
        self.calcEst = ''
        for row in c.execute('SELECT * From CV'):
            self.totalDatos += 1
        self.total = self.totalDatos
        self.totalDatos2 = self.totalDatos
        self.calculando = ''
        self.listEst=[]
        self.build(entrada =entrada,imagen=True,pag=0)

    def build(self,entrada,pag,filtros=[],busqueda=[],imagen=False):
        self.scroll_y=1
        aplicacion.agregar = True
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
            
        self.filtroWhere =" FROM CV"
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
                        self.filtroWhere +="and "+self.sinTilde(str(filtros[n]),str(palabra))
            n+=1
        filtro = self.filtroSelect + self.filtroWhere + " LIMIT 50 OFFSET " + str(pag*50)
        color = False
        #print(filtro)
        for row in c.execute(filtro):
            
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
                        if x == None:
                            self.filas[len(self.filas)-1].add_widget(campoBD2(True,indexID,pag=pag))
                        else:
                            self.filas[len(self.filas)-1].add_widget(campoBD2(False,indexID,str(x),pag=pag))
                    else:
                        self.filas[len(self.filas)-1].add_widget(campoBD1(str(x)))
                    columnas += 1
            color = not color
                                
            cont += 1

        for row in self.filas:
            self.contenedor.add_widget(row)
            
        self.add_widget(self.contenedor)

    def sinTilde(self,word1,word2):
        text = "REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(LOWER(`"+str(word1)+"`),'á','a'), 'é','e'),'í','i'),'ó','o'),'ú','u'),'ñ','n'),'Á','A'), 'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N') LIKE REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(LOWER('%"+str(word2)+"%'),'á','a'), 'é','e'),'í','i'),'ó','o'),'ú','u'),'ñ','n'),'Á','A'), 'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N')"
        return text
    def calcAct(self,pag=0):

        self.contenedor=DataViewerContainer()
        self.contenedor.bind(minimum_height=self.contenedor.setter('height'))
        self.filas=[]
        color = False
        top = len(self.listEst)
        if top > 50*(pag+1):
            top = 50*(pag+1)
        #print(sorted(self.listEst, key=itemgetter(1),reverse=True))
        for item in sorted(self.listEst,
         key=itemgetter(1),reverse=True)[50*pag:top]:
            self.filas.append(Fila(color))
            for element in item:
                self.filas[len(self.filas)-1].add_widget(campoBD1(str(element)))
            color = not color

        for row in self.filas:
            self.contenedor.add_widget(row)

        #self.add_widget(Info(self.calcEst))
        self.add_widget(self.contenedor)
        #self.calcEst = ''

    def calc(self,text,filtroAct,pag=0):
        self.calculando = text
        self.contenedor=DataViewerContainer()
        self.contenedor.bind(minimum_height=self.contenedor.setter('height'))
        self.filas=[]
        if filtroAct:
            filtro = "SELECT `"+ str(text) +"` " + self.filtroWhere
        else:
            filtro = "SELECT `"+ str(text) +"` FROM CV"
        
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
        #filtro = "SELECT `"+ str(text) +"` FROM CV"
 
        self.listEst=[]
        palabras=""
        #self.totalDatos2 = self.totalDatos
        self.totalDatos=len(data3)
        for diferente in data3:
            if diferente != None:
                if filtroAct:
                    filtro2 = "SELECT COUNT(`"+ str(text) +"`) "+self.filtroWhere
                else:
                    filtro2 = "SELECT COUNT(`"+ str(text) +"`) FROM CV WHERE "
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
                print("--------------------------------------------")
                print(self.filtroWhere)
                print("--------------------------------------------")
                print(filtro2)
                for x in c.execute(filtro2):
                    for y in x:
                        if filtroAct:
                            self.listEst.append((palabras,y,str(round((y*100) /self.totalDatos2,2))+"%")) 
                        else:
                            self.listEst.append((palabras,y,str(round((y*100) /self.total,2))+"%"))
                palabras=""
                        #self.calcEst +=": "+ str(y) + " (" + str(round((y*100) /self.total,2))+"%)"
                #self.calcEst +="\n"
       
        self.calcAct(pag)


  

    def insertPdf(self,fileName,idNum,pag,filtros=[],busqueda=[],imagen=False):
        filtro = "UPDATE CV SET PDF = '" + str(fileName) + "' WHERE `" + self.index + "` = '" + str(idNum) +"'"
        #print(filtro)
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

class Title(BoxLayout):
    g = StringProperty()
    def __init__(self,texto,filtro = True):
        super(Title, self).__init__()
        self.g = texto

class Color(BoxLayout):
    g = StringProperty()
    color = BooleanProperty()
    def __init__(self,texto,color=True):
        super(Color, self).__init__()
        self.g = texto
        self.color = color

class TitlePag(BoxLayout):
    g = StringProperty()
    def __init__(self,texto):
        super(TitlePag, self).__init__()
        self.g = texto

#Separadores y contenedores varios
class Separador2(BoxLayout):
    pass

class ButtonOption(ButtonBehavior,BoxLayout):
    g = StringProperty()
    c = BooleanProperty()
    def __init__(self,texto,select=False,**kwargs):
        super(ButtonOption, self).__init__(**kwargs)
        self.g = texto
        self.c = select

class ButtonMain(ButtonBehavior,BoxLayout):
    g = StringProperty()
    c = BooleanProperty()
    def __init__(self,texto,select=False,**kwargs):
        super(ButtonMain, self).__init__(**kwargs)
        self.g = texto
        self.c = select

class ButtonAccept(ButtonBehavior,BoxLayout):
    g = StringProperty()
   # c = BooleanProperty()
    def __init__(self,texto,**kwargs):
        super(ButtonAccept, self).__init__(**kwargs)
        self.g = texto
 #       self.c = select

class Separador(ScrollView):
    pass

class Divisor(BoxLayout):
    pass

class Fila(BoxLayout):
    color = BooleanProperty()
    def __init__(self,colorCampo):
        super(Fila, self).__init__()
        self.color=colorCampo

class EstBox(BoxLayout):
    pass

class FilaPag(BoxLayout):
    r = NumericProperty()
    def __init__(self,r=20):
        super(FilaPag, self).__init__()
        self.r = r

class FilaTitulo(BoxLayout):
    r = NumericProperty()
    def __init__(self,r=20):
        super(FilaTitulo, self).__init__()
        self.r = r

class ToolbarTitle(ButtonBehavior,BoxLayout):
    r = NumericProperty()
    #g = StringProperty()
    def __init__(self,r=16,**kwargs):
        super(ToolbarTitle, self).__init__(**kwargs)
        self.r = r
      #  self.g = texto

class ToolbarText(BoxLayout):
    g = StringProperty()
    s = NumericProperty()
    def __init__(self,texto,size = 1):
        super(ToolbarText, self).__init__()
        self.g = texto
        self.s = size

class Fila3(BoxLayout):
    pass

class BotonOpcion(Button):
    pass

class BotonOpcion2(Button):
    pass

class Info(BoxLayout):
    g = StringProperty()
    def __init__(self,texto):
        super(Info, self).__init__()
        self.g = texto

class campoBD1(BoxLayout):
    g = StringProperty()
    def __init__(self,texto):
        super(campoBD1, self).__init__()
        self.g = texto

class OcultarBarra(FloatLayout):
    pass

class ColorBox(BoxLayout):
    r = NumericProperty()
    g = NumericProperty()
    b = NumericProperty()
    def __init__(self,r=0,g=0,b=0):
        super(ColorBox, self).__init__()
        self.r = r
        self.g = g
        self.b = b

class campoBD2(BoxLayout):
    pdf = BooleanProperty()
    ID = NumericProperty()
    pag = NumericProperty()
    def __init__(self,pdf,idNum,path='',pag=0):
        super(campoBD2, self).__init__()
        self.pdf = pdf
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

class Toolbar(ScrollView):
    show = BooleanProperty()
    def __init__(self):
        super(Toolbar, self).__init__()
        self.show=True
        self.build()

    def build(self):
        self.stack=ToolbarContaner()
        self.stack.bind(minimum_height=self.stack.setter('height'))
        

class ToolbarContaner(StackLayout):
    pass

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