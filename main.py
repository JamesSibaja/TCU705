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
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout

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
        self.contenedor = StackLayout(size_hint=(0.3, 1)) 
        self.lista = ListaBase(['Nombre', 'Telefono','Carrera'])  
        self.listaFiltros =['Nombre', 'Telefono','Carrera']    
        self.filtros = [] 
        self.barraTareas()
        self.add_widget(self.contenedor)
        self.add_widget(self.lista)

    def barraTareas(self):
        self.contenedor.clear_widgets()
        for filtro in self.listaFiltros:
            self.filtros.append(TextInput(text=str(filtro),size_hint=(1, 0.05)))
        n=0
        for filtro in self.listaFiltros:
            self.contenedor.add_widget(self.filtros[n])
            n+=1

        self.textoDos = TextInput(text='Filtro',size_hint=(1, 0.05))
        self.submit = Button(text = 'Buscar',size_hint=(1, 0.05),on_press=self.buscar)
        self.submit2 = Button(text = 'Nuevo Filtro',size_hint=(1, 0.05),on_press=self.nuevo)
        self.contenedor.add_widget(self.submit)
        self.contenedor.add_widget(self.textoDos)
        self.contenedor.add_widget(self.submit2)

    def buscar(self,obj):
        self.lista.reset()
        self.lista.build(entrada=['Nombre', 'Telefono','Carrera'],busqueda=self.filtros[0].text.split())

    def nuevo(self,obj):
        self.listaFiltros.append(self.textoDos.text.split())
        self.barraTareas()


def on_enter(instance, value):
    print('User pressed enter in', instance)

class ListaBase(BoxLayout):
    def __init__(self,entrada):
        super(ListaBase, self).__init__()
        self.build(entrada)

    def build(self,entrada,busqueda=['']):
        for row in entrada:
            self.add_widget(MyWidget(entrada=row,busqueda=busqueda))

    def reset(self):
       self.clear_widgets()

class MyWidget(BoxLayout):
    
    def __init__(self,entrada,busqueda):
        super(MyWidget, self).__init__()
        color = True
        cont = 0
        self.add_widget(campoTitulo(entrada))
        filtro = "SELECT "+str(entrada)+" FROM CV WHERE Nombre LIKE '%" + ''+"%'"
        filtro2 = "SELECT COUNT(*) FROM CV WHERE Nombre LIKE '%" + ''+"%'"
        for elemento in busqueda:
            filtro += "and Nombre LIKE '%" + str(elemento)+"%'"
        for row in c.execute(filtro):
            for x in row:
                if color:
                    
                    self.add_widget(campoBD1(str(x)))
                    color = False
                    
                else:
                    self.add_widget(campoBD2(str(x)))
                    color = True
                
            cont += 1
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

    df.to_sql(name = table, con = miConexion, if_exists = 'replace', index = False)
    

    myApp().run()

    c.close
    miConexion.close
