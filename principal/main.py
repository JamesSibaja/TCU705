#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Plataforma para base de datos con interfaz gráfica
========================
Esta aplicación fue desarrollada como una colaboración entre la municipalidad de Acosta y el TCU-705 de 
la UCR. La aplicación consiste en una plataforma con interfaz gráfica que permite la manipulación amigable 
y segura de bases de datos.
'''

from kivy.config import Config
Config.set('graphics', 'minimum_width', '800')
Config.set('graphics', 'minimum_height', '600')

from lib import *
from startMenu import StartMenu
from databaseGUI import DatabaseGUI
from databaseMenu import DatabaseMenu

# config
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'system')
Builder.load_file('design.kv')

SubiendoArchivo = False

'''
====================
Aplicación principal
====================
Clase que define la aplicación principal
'''
class DatabaseGUIApp(App): #Aplicación principal    
    def __init__(self):
        super(DatabaseGUIApp, self).__init__()
        title = 'Plataforma'

    def build(self):
        Window.bind(on_dropfile=self._on_file_drop)
        self.SubiendoArchivo = False
        self.subiendoBase = False
        self.pantalla = MainWindow()
        self.archivo = ''
        self.nombreArchivo=''
        self.doc = ''
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
            #print(self.pag)
            self.pantalla.baseWidget.lista.insertPdf(doc = self.doc,fileName=self.nombreArchivo,idNum=self.archivo)
            self.pantalla.baseWidget.lista.reset()
            self.pantalla.baseWidget.lista.build(entrada=self.pantalla.baseWidget.campos,pag=self.pag,filtros= self.pantalla.baseWidget.listaFiltros,busqueda=self.pantalla.baseWidget.filtros)
        if self.subiendoBase:
            try:
                table = self.nombreArchivo
                
                xls = pd.ExcelFile(file_path.decode("utf-8")) #Se carga el documento de excel
                miConexion = sqlite3.connect('base')
                df = pd.read_excel(file_path.decode("utf-8")) #Se lee el documento de excel  
                df.to_sql(name = table, con = miConexion, if_exists = 'replace', index = True) #Se pasa el documento de excel a sql
                c = miConexion.cursor()
                #c.execute('ALTER TABLE '+table+' ADD PDF TEXT')
                c.execute("INSERT INTO database (Nombre,columns) VALUES ('"+self.nombreArchivo+"','111') ")
                miConexion.commit()
                for x in c.execute("SELECT ID FROM database WHERE `Nombre` = '"+self.nombreArchivo+"'"):
                    for y in x:
                        self.pantalla.menuWidget.baseLink(y)
                c.close
                miConexion.close
                self.subiendoBase = False
            except:
                self.pantalla.error()
            #self.pantalla.window.lista.reset()

    # def buildList(self):
    #     self.pantalla.baseWidget.build()
    #     '''
    #     Arreglar est linea
    #     '''
    #     self.pantalla.baseWidget.lista.build(entrada=self.pantalla.baseWidget.campos,pag=self.pag,filtros= self.pantalla.baseWidget.listaFiltros,busqueda=self.pantalla.baseWidget.filtros)
    

    def on_pause(self):
        return True

    def on_resume(self):
        pass

'''
================
Widget principal
================
Widget asociado a la totalidad de la ventana donde se presenta la interfaz de la aplicación
'''

class MainWindow(BoxLayout): 
    def __init__(self):
        super(MainWindow, self).__init__()
        self.sm = ScreenManager()
        self.add_widget(self.sm)
        # for i in range(1,3):
        #     screen = Screen(name='Title%d' % i)
        #     sm.add_widget(screen)
        self.log = Screen(name='log')
        self.sm.add_widget(self.log)
        self.menu = Screen(name='menu')
        self.sm.add_widget(self.menu)
        self.base = Screen(name='base')
        self.sm.add_widget(self.base)

        self.build(0)

        
        # for i in range(4):
        #     screen = Screen(name='Title %d' % i)
        #     self.sm.add_widget(screen)
            
        # self.sm.current = 'Title 2'

    #Constructor de la ventana principal
    def build(self,currentWindow=1,table= 'database',userID=1,edit = True):
        #self.clear_widgets()
        if currentWindow == 0:
            self.menu.clear_widgets()
            self.base.clear_widgets()
            self.log.clear_widgets()
            self.logWidget=StartMenu(upApp=self)
            self.log.add_widget(self.logWidget)
            self.sm.current = 'log'
        elif currentWindow == 1: 
            self.userID = userID
            self.menuWidget = DatabaseMenu(upApp=self,base='base',aplicacion = aplicacion,userID=userID)
            self.menu.add_widget(self.menuWidget)
            self.sm.current = 'menu'
        elif currentWindow == 2:
            self.edit = edit
            self.table = table
            self.baseWidget = DatabaseGUI(upApp=self,base='base',table=table,aplicacion = aplicacion,edit=edit)
            self.base.add_widget(self.baseWidget)
            self.sm.current = 'base'
        else:
            self.sm.current = 'menu'

    def error(self):
        self.menuWidget.error()
        

'''
=================
Función principal
=================
Crea la base de datos y crea el objeto aplicación a partir de clase  DatabaseGUIApp
'''

if __name__ == '__main__': #Función principal

    # table = "BaseCV"
    # path = "./cv_acosta.xlsx"
    # xls = pd.ExcelFile(path) #Se carga el documento de excel
    # miConexion = sqlite3.connect('base')
    # df = pd.read_excel(path) #Se lee el documento de excel  
    # df.to_sql(name = table, con = miConexion, if_exists = 'replace', index = True) #Se pasa el documento de excel a sql
    # for x in df:
    #     print(x)
    # c = miConexion.cursor()
    # c.execute('ALTER TABLE '+table+' ADD PDF TEXT')
    # pathFile = ''
    # SubiendoArchivo = False
    aplicacion = DatabaseGUIApp() #Se crea un objeto con la aplicación
    aplicacion.run() #Se ejecuta la aplicación
    # c.close
    # miConexion.close