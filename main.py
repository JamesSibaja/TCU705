import sqlite3
import pandas as pd	
from kivy.uix.label import Label

# config
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'system')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from pdf2image import convert_from_path
from kivy.uix.textinput import TextInput

pages = convert_from_path('Programa.pdf', 500)
cont = 0
for page in pages:
    page.save('out'+ str(cont) +'.png', 'PNG')
    cont +=1
#from kivymd.uix.textfield import MDTextField

Builder.load_file('design.kv')

class Pantalla(BoxLayout):
    def __init__(self):
        super(Pantalla, self).__init__()
        self.add_widget(Barra())
        self.add_widget(ListaBase(['Nombre', 'Telefono','Carrera']))

class Barra(BoxLayout):
    def __init__(self):
        super(Barra, self).__init__()
        #self.username = MDTextField(text="hola")
        self.add_widget(TextInput(text='Hello world'))

class ListaBase(BoxLayout):
    def __init__(self,entrada):
        super(ListaBase, self).__init__()
        for row in entrada:
            self.add_widget(MyWidget(row))

class MyWidget(BoxLayout):
    
    def __init__(self,entrada):
        super(MyWidget, self).__init__()
        color = True
        cont = 0
        texto = ''
        self.add_widget(campoTitulo(entrada))
        for row in c.execute("SELECT %s FROM CV" %entrada):
            for x in row:
                texto += x 
                if color:
                    
                    self.add_widget(campoBD1(texto))
                    color = False
                    
                else:
                    self.add_widget(campoBD2(texto))
                    color = True
                
            cont += 1
            texto = ''
            if cont == 15:
                break

class campoTitulo(BoxLayout):
    g = StringProperty()
    def __init__(self,texto):
        super(campoTitulo, self).__init__()
        self.g = texto

class campoBD1(BoxLayout):
    g = StringProperty()
    def __init__(self,texto):
        super(campoBD1, self).__init__()
        self.g = texto

class campoBD2(BoxLayout):
    g = StringProperty()
    def __init__(self,texto):
        super(campoBD2, self).__init__()
        self.g = texto


class myApp(App):
    title = 'Plataforma'
    def build(self):
        return Pantalla()
    def on_pause(self):
        return True
    def on_resume(self):
        pass

if __name__ == '__main__':

    table = "CV"
    path = "./cv_acosta.xlsx"

    xls = pd.ExcelFile(path)
    miConexion = sqlite3.connect('base')
    c = miConexion.cursor()
    df = pd.read_excel(path)

    df.to_sql(name = table, con = miConexion, if_exists = 'append', index = False)
    

    myApp().run()

    c.close
    miConexion.close
