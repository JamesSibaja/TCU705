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
        self.lista = ListaBase(['Nombre','Telefono','Carrera'])  
        self.listaFiltros =[]
        self.palabrasBuscadas=[]
        self.nuevoFiltro = False
        self.barraTareas()
        self.add_widget(self.contenedor)
        self.add_widget(self.lista)

    def barraTareas(self):
        self.contenedor.clear_widgets()
        self.filtros = []
        if self.nuevoFiltro:
            self.filtrosBotones = []
            for posibleFiltro in df:
                self.filtrosBotones.append(Button(text = str(posibleFiltro),size_hint=(0.9, 0.05),on_press=self.nuevoFinal))
            n=0
            for botonFiltro in self.filtrosBotones:
                self.contenedor.add_widget(self.filtrosBotones[n])
                n+=1
            self.nuevoFiltro = False
        else:
            if self.palabrasBuscadas != []:
                for filtro in self.palabrasBuscadas:
                    self.filtros.append(TextInput(text=str(filtro),size_hint=(0.6, 0.05)))           
            else:
                for filtro in self.listaFiltros:
                    self.filtros.append(TextInput(text=str(filtro),size_hint=(0.6, 0.05)))

            n=0
            for filtro in self.filtros:
                self.contenedor.add_widget(tituloFiltro(self.listaFiltros[n]))
                self.contenedor.add_widget(self.filtros[n])
                n+=1
            self.submit = Button(text = 'Buscar',size_hint=(1, 0.05),on_press=self.buscar)
            self.submit2 = Button(text = 'Nuevo Filtro',size_hint=(1, 0.05),on_press=self.nuevoInicio)
            self.contenedor.add_widget(self.submit)
            self.contenedor.add_widget(self.submit2)

    def buscar(self,obj):
        self.lista.reset()
        self.palabrasBuscadas=[]
        for filtro in self.filtros:
            self.palabrasBuscadas.append(filtro.text)
        self.lista.build(entrada=['Nombre', 'Telefono','Carrera'],filtros= self.listaFiltros,busqueda=self.filtros)

    def nuevoInicio(self,obj):
        #self.listaFiltros.append(self.textoDos.text)
        self.nuevoFiltro = True
        self.barraTareas()

    def nuevoFinal(self,obj):
        self.listaFiltros.append(obj.text)
        self.palabrasBuscadas.append('')
        self.barraTareas()


def on_enter(instance, value):
    print('User pressed enter in', instance)

class ListaBase(BoxLayout):
    def __init__(self,entrada):
        super(ListaBase, self).__init__()
        self.build(entrada =entrada)

    def build(self,entrada,filtros=['Nombre'],busqueda=['']):
        for row in entrada:
            self.add_widget(MyWidget(entrada=row,filtros=filtros,busqueda=busqueda))

    def reset(self):
       self.clear_widgets()

class MyWidget(BoxLayout):
    
    def __init__(self,entrada,filtros,busqueda):
        super(MyWidget, self).__init__()
        color = True
        cont = 0
        self.add_widget(campoTitulo(entrada))
        filtro = "SELECT "+str(entrada)+" FROM CV"
        n=0
        if busqueda != ['']:
            filtro +=" WHERE "+filtros[n]+" LIKE '% %'"
        for elemento in busqueda:
            if elemento != '':
                for palabra in elemento.text.split():
                    filtro += "and "+filtros[n]+" LIKE '%" + str(palabra)+"%'"
                n+=1
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

class tituloFiltro(BoxLayout):
    g = StringProperty()
    def __init__(self,texto):
        super(tituloFiltro, self).__init__()
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
