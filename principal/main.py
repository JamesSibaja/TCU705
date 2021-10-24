#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Plataforma para base de datos con interfaz gráfica
========================
Esta aplicación fue desarrollada como una colaboración entre la municipalidad de Acosta y el TCU-705 de 
la UCR. La aplicación consiste en una plataforma con interfaz gráfica que permite la manipulación amigable 
y segura de bases de datos.
'''

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
            self.pantalla.window.lista.insertPdf(doc = self.doc,fileName=self.nombreArchivo,idNum=self.archivo)
            self.pantalla.window.lista.reset()
            self.pantalla.window.lista.build(entrada=self.pantalla.window.campos,pag=self.pag,filtros= self.pantalla.window.listaFiltros,busqueda=self.pantalla.window.filtros)
        if self.subiendoBase:
            table = self.nombreArchivo
            self.subiendoBase = False
            xls = pd.ExcelFile(file_path.decode("utf-8")) #Se carga el documento de excel
            miConexion = sqlite3.connect('base')
            df = pd.read_excel(file_path.decode("utf-8")) #Se lee el documento de excel  
            df.to_sql(name = table, con = miConexion, if_exists = 'replace', index = True) #Se pasa el documento de excel a sql
            c = miConexion.cursor()
            #c.execute('ALTER TABLE '+table+' ADD PDF TEXT')
            c.execute("INSERT INTO database (Database) VALUES ('"+self.nombreArchivo+"') ")
            miConexion.commit()
            for x in c.execute("SELECT ID FROM database WHERE `Database` = '"+self.nombreArchivo+"'"):
                for y in x:
                    self.pantalla.window.baseLink(y)
            c.close
            miConexion.close
            #self.pantalla.window.lista.reset()

    def buildList(self):
        self.pantalla.window.lista.reset()
        self.pantalla.window.lista.build(entrada=self.pantalla.window.campos,pag=self.pag,filtros= self.pantalla.window.listaFiltros,busqueda=self.pantalla.window.filtros)
    

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
        self.build(0)

    #Constructor de la ventana principal
    def build(self,currentWindow=1,table= 'database',userID=1,edit = True):
        self.clear_widgets()
        if currentWindow == 0:
            self.window = StartMenu(self)
        elif currentWindow == 1:
            self.window = DatabaseMenu(self,base='base',aplicacion = aplicacion,userID=userID)
        else:
            self.window = DatabaseGUI(base='base',table=table,aplicacion = aplicacion,edit=edit)
        self.add_widget(self.window)

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