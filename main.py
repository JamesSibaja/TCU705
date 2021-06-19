import sqlite3
import pandas as pd	
from kivy.uix.label import Label

# config
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'system')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from pdf2image import convert_from_path
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.scatterlayout import ScatterLayout
from kivy.core.window import Window
from kivy.graphics.transformation import Matrix
from kivy.uix.image import Image 
from kivy.effects.scroll import ScrollEffect

#from PIL import Image

pages = convert_from_path('Programa.pdf', 500)
cont = 0
for page in pages:
    page.save('out'+ str(cont) +'.png', 'PNG')
    cont +=1
#from kivymd.uix.textfield import MDTextField

Builder.load_file('design.kv')
# print('-------------------------------------')
# img=Image.open('out.png')
# img.show()
# print(img)
# print('-------------------------------------')
class Picture(Scatter):
    source = StringProperty(None)

class Barra(StackLayout):
    pass

class Barra2(StackLayout):
    pass

class Pantalla(BoxLayout):
    def __init__(self):
        super(Pantalla, self).__init__()
       # picture = Picture(source='out.png')
       # self.add_widget(picture)
        # img = Zoom()
        # self.add_widget(img)
        self.divisor=Divisor()
        self.contenedor = Barra()  
        self.listaFiltros =[]
        self.lista = MyWidget(['Nombre','Telefono','Carrera']) 
        #self.principal=ScrollView(do_scroll_y= True,size_hint=(1, None), size=(Window.width, Window.height))
        self.palabrasBuscadas=[]
        self.nuevoFiltro = False
        self.barraTareas()
        self.divisor.add_widget(self.contenedor)
        
        self.add_widget(self.divisor)
        self.add_widget(self.lista)
        #self.add_widget(self.principal)

    def barraTareas(self):
        self.contenedor.clear_widgets()
        self.filtros = []
        if self.nuevoFiltro:
            self.filtrosBotones = []
            for posibleFiltro in df:
                self.filtrosBotones.append(Button(text = str(posibleFiltro),background_color =(0, 0.59, 0.81, 1), size_hint=(1, 0.05),on_press=self.nuevoFinal))
            n=0
            for botonFiltro in self.filtrosBotones:
                self.contenedor.add_widget(self.filtrosBotones[n])
                n+=1
            self.nuevoFiltro = False
        else:
            self.submit = Button(text = 'Buscar',background_color =(0, 0.81, 0.59, 1),size_hint=(1, 0.05),on_press=self.buscar)
            self.submit2 = Button(text = 'Nuevo Filtro',background_color =(0, 0.81, 0.59, 1),size_hint=(1, 0.05),on_press=self.nuevoInicio)
            self.contenedor.add_widget(self.submit)
            self.contenedor.add_widget(self.submit2)
            if self.palabrasBuscadas != []:
                for filtro in self.palabrasBuscadas:
                    self.filtros.append(TextInput(text=str(filtro),size_hint=(0.6, 0.05)))           
            else:
                for filtro in self.listaFiltros:
                    self.filtros.append(TextInput(text=str(filtro),size_hint=(0.6, 0.05)))

            n=0
            self.contenedor.add_widget(Separador())
            for filtro in self.filtros:
                
                self.contenedor.add_widget(tituloFiltro(self.listaFiltros[n]))
                self.contenedor.add_widget(self.filtros[n])
                n+=1
           
            

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

class Picture(Image):
    pass

class Page(PageLayout):
    def __init__(self):
        super(Page, self).__init__()
        self.lista = ListaBase(['Nombre','Telefono','Carrera']) 
        self.lista2 = ListaBase(['Nombre','Telefono','Carrera']) 
        self.lista3 = ListaBase(['Nombre','Telefono','Carrera']) 
        self.add_widget(self.lista) 
        self.add_widget(self.lista2) 
        self.add_widget(self.lista3) 

class ListaBase(BoxLayout):
    def __init__(self,entrada):
        super(ListaBase, self).__init__()
        self.build(entrada =entrada,imagen=True)

    def build(self,entrada,filtros=[],busqueda=[],imagen=False):
        # for row in entrada:
        #     self.add_widget(MyWidget(entrada=row,filtros=filtros,busqueda=busqueda))
        # self.add_widget(MyWidget(entrada=entrada[0],endRow=True,filtros=filtros,busqueda=busqueda))
        self.add_widget(MyWidget(entrada=entrada,filtros=filtros,busqueda=busqueda))
    def reset(self):
       self.clear_widgets()

class Zoom(ScatterLayout):

    def on_touch_down(self, touch):
        x, y = touch.x, touch.y
        self.prev_x = touch.x
        self.prev_y = touch.y
        self.add_widget(Image(source='out.png'))

        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                print('down')
                ## zoom in
                if self.scale < 10:
                    self.scale = self.scale * 1.1

            elif touch.button == 'scrollup':
                print('up')  ## zoom out
                if self.scale > 1:
                    self.scale = self.scale * 0.9

        # if the touch isn't on the widget we do nothing
        if not self.do_collide_after_children:
            if not self.collide_point(x, y):
                return False

        if 'multitouch_sim' in touch.profile:
            touch.multitouch_sim = True
        # grab the touch so we get all it later move events for sure
        self._bring_to_front(touch)
        touch.grab(self)
        self._touches.append(touch)
        self._last_touch_pos[touch] = touch.pos

        return True

class MyWidget(ScrollView):
    end = BooleanProperty()
    def __init__(self,entrada):
        super(MyWidget, self).__init__()
        self.build(entrada =entrada,imagen=True)

    def build(self,entrada,filtros=[],busqueda=[],imagen=False):
        #self.principal=ScrollView(effect_cls= ScrollEffect,do_scroll_y= True,size_hint=(1, 1))
        #self.end = endRow
        self.contenedor=Barra2(size_hint_y= None)
        self.contenedor.bind(minimum_height=self.contenedor.setter('height'))
        self.filas=[]
        color = True
        cont = 0
        # if(endRow):
        #     self.contenedor.add_widget(campoTitulo(''))
        # else:
        #     self.contenedor.add_widget(campoTitulo(entrada))
        # filtro = "SELECT "+str(entrada)+" FROM CV"
        filtro = "SELECT "
        self.filas.append(Fila())
        for selectField in entrada:
            self.filas[len(self.filas)-1].add_widget(campoTitulo(selectField))
            filtro +=str(selectField )
            if(selectField != entrada[len(entrada)-1]):
                filtro += ", "
        filtro += " "

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
                        filtro +=filtros[n]+" LIKE '%" + str(palabra)+"%'"
                    else:
                        filtro +="and "+filtros[n]+" LIKE '%" + str(palabra)+"%'"
            n+=1
        color = False
        print(filtro)
        for row in c.execute(filtro):
            self.filas.append(Fila())
            for x in row:
                # if(endRow):
                #     campo = campoBD2(color)
                #     self.filas[len(self.filas)-1].add_widget(campo)
                # else:
                #     self.filas[len(self.filas)-1].add_widget(campoBD1(str(x),color))
                self.filas[len(self.filas)-1].add_widget(campoBD1(str(x),color))
            color = not color
                                   
            cont += 1
            if cont == 50:
                break
        for row in self.filas:
            self.contenedor.add_widget(row)
        # for i in range(50):
        #     self.contenedor.add_widget(Button(size_hint_y= None))
        self.add_widget(self.contenedor)
        # self.add_widget(self.principal)

    def reset(self):
       self.clear_widgets()

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

class Separador(BoxLayout):
    pass

class Divisor(BoxLayout):
    pass

class Fila(BoxLayout):
    pass

class campoBD1(BoxLayout):
    g = StringProperty()
    color = BooleanProperty()
    def __init__(self,texto,colorCampo):
        super(campoBD1, self).__init__()
        self.g = texto
        self.color=colorCampo

class campoBD2(BoxLayout):
    color = BooleanProperty()
    def __init__(self,colorCampo):
        super(campoBD2, self).__init__()
        self.color=colorCampo

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
