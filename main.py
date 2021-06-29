import sqlite3
import pandas as pd	
from kivy.uix.label import Label
import math

# config
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'system')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
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
from kivy.uix.anchorlayout import AnchorLayout
import shutil
import time

import webbrowser


#from PIL import Image

# pages = convert_from_path('Programa.pdf', 500) 
# cont = 0
# for page in pages:
#     page.save('out'+ str(cont) +'.png', 'PNG')
#     cont +=1
# from kivymd.uix.textfield import MDTextField

Builder.load_file('design.kv')
SubiendoArchivo = False
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

class MenuInicial(FloatLayout):
    # def __init__(self):
    #     super(MenuInicial, self).__init__()
    pass 
   

class Cuadro(BoxLayout):
    pass

class Pantalla(BoxLayout):
    def __init__(self):
        super(Pantalla, self).__init__()
        self.menu = MenuInicial()
        self.menu.add_widget( Button(text='Mis Proyectos', size_hint=(.3, .1),
                pos_hint={'x':.15, 'y':.2},on_press=self.build))
        self.menu.add_widget( Button(text='Nuevo proyecto', size_hint=(.3, .1),
                pos_hint={'x':.55, 'y':.2},on_press=self.build))
        self.menu.add_widget(Image(source='logo.png', size_hint=(1, .6),
                pos_hint={'x':0, 'y':0.35}))
        self.add_widget(self.menu)
       # picture = Picture(source='out.png')
       # self.add_widget(picture)
        # img = Zoom()
        # self.add_widget(img)

    def build(self,obj):
        self.clear_widgets()
        self.divisor=Divisor()
        self.contenedorBarra = BoxLayout(size_hint=(0.25,1),orientation= 'vertical')
        self.numPag = 0
        self.contenedor = Barra()  
        self.listaFiltros =[]
        self.filaTitulo = Fila2()
        self.pagina = Fila2()
        self.camposOpcion = []
        self.filtrosOpcion = []
        self.filtros = []
        self.campos = []
        self.nombres = list(map(lambda x: x[0], c.execute('select * from CV').description))
        contCampos=0
        for selectField in self.nombres:
            print(selectField)
            if(contCampos<3):
                self.camposOpcion.append(True)
                self.campos.append(str(selectField))
            else:
                self.camposOpcion.append(False)
            self.filtrosOpcion.append(False)
            contCampos+=1
        self.lista = MyWidget(entrada=self.campos,pag = self.numPag)
        self.pagina.add_widget(tituloFiltro(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50)),filtro=False))
        #self.pagina.add_widget(BoxLayout(text='Siguiente',on_press=self.nuevaPagina()))
        self.pagina.add_widget(Button(text='Siguiente >',on_press=self.siguientePagina))
        self.contenedorLista = BoxLayout(orientation= 'vertical')
        for selectField in self.campos:
            self.filaTitulo.add_widget(campoTitulo(selectField))
            
        
        #self.principal=ScrollView(do_scroll_y= True,size_hint=(1, None), size=(Window.width, Window.height))
        self.palabrasBuscadas={}
        self.nuevoFiltro = False
        self.cambiarCampo = False
        #self.contenedor
        self.contenedor.bind(minimum_height=self.contenedor.setter('height'))
        self.divisor.add_widget(self.contenedor)
        self.contenedorBarra.add_widget(self.divisor)
        self.add_widget(self.contenedorBarra)

        #self.divisor.contenedor=Barra2(size_hint_y= None)

        self.contenedorLista.add_widget(self.filaTitulo)
        self.contenedorLista.add_widget(self.lista)
        self.contenedorLista.add_widget(self.pagina)
        self.add_widget(self.contenedorLista)

        self.barraTareas()
        #self.add_widget(self.principal)

    def siguientePagina(self,obj):
        self.lista.reset()
        # self.palabrasBuscadas=[]
        # for filtro in self.filtros:
        #     self.palabrasBuscadas.append(filtro.text)
        self.numPag +=1
        self.lista.build(entrada=self.campos,pag=self.numPag,filtros= self.listaFiltros,busqueda=self.filtros)
        self.pagina.clear_widgets()
        if(self.numPag>0):
            self.pagina.add_widget(Button(text='< Anterior',on_press=self.anteriorPagina))
        self.pagina.add_widget(tituloFiltro(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50)),filtro=False))
        if(self.numPag + 1 < math.ceil(self.lista.totalDatos/50)):
            self.pagina.add_widget(Button(text='Siguiente >',on_press=self.siguientePagina))

    def anteriorPagina(self,obj):
        self.lista.reset()
        # self.palabrasBuscadas=[]
        # for filtro in self.filtros:
        #     self.palabrasBuscadas.append(filtro.text)
        self.numPag = self.numPag-1
        if(self.numPag<math.ceil(self.lista.totalDatos/50)):
            self.lista.build(entrada=self.campos,pag=self.numPag,filtros= self.listaFiltros,busqueda=self.filtros)
        
        self.pagina.clear_widgets()
        if(self.numPag>0):
            self.pagina.add_widget(Button(text='< Anterior',on_press=self.anteriorPagina))
        self.pagina.add_widget(tituloFiltro(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50)),filtro=False))
        if(self.numPag + 1 < math.ceil(self.lista.totalDatos/50)):
            self.pagina.add_widget(Button(text='Siguiente >',on_press=self.siguientePagina))
       

    def barraTareas(self):
        #self.palabrasBuscadas=[]
        
        #print(self.palabrasBuscadas)
        
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
                
                #self.newBoton.bind(text_size=self.newBoton.setter('height'))
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
            self.submit = BotonOpcion(text = 'Buscar',background_color =(0.3, 0.59, 0.1,1),on_press=self.buscar)
            self.submit2 = BotonOpcion(text = 'Filtros',background_color =(0, 0.59, 0.81,1),on_press=self.nuevoInicio)
            self.submit3 = BotonOpcion(text = 'Columnas',background_color =(0, 0.59, 0.81,1),on_press=self.nuevoCampo)
            
            self.contenedor.add_widget(self.submit3)
            self.contenedor.add_widget(self.submit2)
            # print('----------------')
            # print(self.palabrasBuscadas)
            # # if self.palabrasBuscadas != []:
            # #     for filtro in self.palabrasBuscadas:
            # #         self.filtros.append(TextInput(text='str(filtro)',size_hint=(0.6, 0.05)))           
            # # else:
            
            # print('-----------------------------')
            # print(self.palabrasBuscadas)
            # print(self.listaFiltros)
            # print('-----------------------------')
            print('lista filtro:')
            print(self.listaFiltros)
            print('diccionario palabra buscada')
            print(self.palabrasBuscadas)
            for filtro in self.listaFiltros:
                if (self.palabrasBuscadas.get(filtro) != None):
                    self.filtros.append(TextInput(text=str(self.palabrasBuscadas[filtro]),size_hint=(0.6, 0.05)))
                else:
                    self.filtros.append(TextInput(text='',size_hint=(0.6, 0.05)))
                #contTexto +=1
            n=0
            self.contenedor.add_widget(Separador2())
            
            for filtro in self.filtros:
                
                self.contenedor.add_widget(tituloFiltro(texto=self.listaFiltros[n]))
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
            self.filaTitulo.add_widget(campoTitulo(selectField))
        self.lista.build(entrada=self.campos,filtros= self.listaFiltros,pag=self.numPag,busqueda=self.filtros)       

    def buscar(self,obj):
        self.lista.reset()
        
        self.numPag = 0
        self.lista.build(entrada=self.campos,pag=0,filtros= self.listaFiltros,busqueda=self.filtros)
        self.pagina.clear_widgets()
        if(self.numPag>0):
            self.pagina.add_widget(Button(text='< Anterior',on_press=self.anteriorPagina))
        
        self.pagina.add_widget(tituloFiltro(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50)),filtro=False))
        if(self.numPag + 1 < math.ceil(self.lista.totalDatos/50)):
                self.pagina.add_widget(Button(text='Siguiente >',on_press=self.siguientePagina))
                
    def nuevoInicio(self,obj):
        #self.listaFiltros.append(self.textoDos.text)
        # self.palabrasBuscadas=[]
        # for filtro in self.filtros:
        #     self.palabrasBuscadas.append(filtro.text)
        self.nuevoFiltro = True
        self.barraTareas()

    def nuevoFinal(self,obj):
        if (self.nuevoFiltro):
            contFiltro = 0
            for field in self.nombres:
                if (field == obj.text):
                    self.filtrosOpcion[contFiltro]  = not self.filtrosOpcion[contFiltro]
                contFiltro += 1
            #self.palabrasBuscadas.append('')
            self.barraTareas()

        if (self.cambiarCampo):
            contTitulo = 0
            for field in self.nombres:
                if(field == obj.text):
                    self.camposOpcion[contTitulo] = not self.camposOpcion[contTitulo]
                contTitulo += 1 

            self.barraTareas()
            
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
            self.barraTareas()

    def nuevoCampo(self,obj):
        self.cambiarCampo = True
        print(Window.size[0])
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

# class ListaBase(BoxLayout):
#     def __init__(self,entrada):
#         super(ListaBase, self).__init__()
#         self.build(entrada =entrada,imagen=True)

#     def build(self,entrada,filtros=[],busqueda=[],imagen=False):
#         # for row in entrada:
#         #     self.add_widget(MyWidget(entrada=row,filtros=filtros,busqueda=busqueda))
#         # self.add_widget(MyWidget(entrada=entrada[0],endRow=True,filtros=filtros,busqueda=busqueda))
#         self.add_widget(MyWidget(entrada=entrada,filtros=filtros,busqueda=busqueda))
#     def reset(self):
#        self.clear_widgets()

class MyWidget(ScrollView):
    end = BooleanProperty()
    def __init__(self,entrada,pag=0):
        super(MyWidget, self).__init__()
        self.build(entrada =entrada,imagen=True,pag=0)


    def build(self,entrada,pag,filtros=[],busqueda=[],imagen=False):


        self.contenedor=Barra2()
        self.contenedor.bind(minimum_height=self.contenedor.setter('height'))
        self.filas=[]
        PDF = (False,0)
        color = True
        cont = 0
        cont2 = 0
        
        filtro = "SELECT "
        n = 0
        for selectField in entrada:
            filtro += "`" + str(selectField) + "`"
            if (selectField == 'PDF'):
                PDF = (True,n)
            if(selectField != entrada[len(entrada)-1]):
                filtro += ", "
            n += 1
        filtro += " "

        filtro +=" FROM CV"
        n=0
        primero=True
        for elemento in busqueda:
            if elemento.text.split() != []:
                if primero:
                    filtro +=" WHERE "

                for palabra in elemento.text.split():
                   # palabra2 = normalize(palabra)
                    if primero:
                        primero = False
                        filtro +="`" + str(filtros[n])+"` COLLATE NOACCENTS LIKE '%" + str(palabra)+"%'"
                        
                    else:
                        filtro +="and `"+str(filtros[n])+"` LIKE '%" + str(palabra)+"%'"
            n+=1
        color = False
        
        stop = False
        for row in c.execute(filtro):
            if((cont2 == pag*50 or cont2 > pag*50) and not stop):
                self.filas.append(Fila())
                columnas = 0
                for x in row:
                    if PDF[0] and columnas == PDF[1]:
                        if x == None:
                            self.filas[len(self.filas)-1].add_widget(campoBD2(color,True,cont))
                        else:
                            self.filas[len(self.filas)-1].add_widget(campoBD2(color,False,cont,str(x)))
                    else:
                        self.filas[len(self.filas)-1].add_widget(campoBD1(str(x),color))
                    columnas += 1
                color = not color
                                    
                cont += 1
                if cont == 50:
                    stop = True
            else:
                pass
            cont2 += 1
            
        self.totalDatos = cont2
        for row in self.filas:
            self.contenedor.add_widget(row)
            
        self.add_widget(self.contenedor)

    def insertPdf(self,fileName,idNum,pag,filtros=[],busqueda=[],imagen=False):
        cont = 0
        cont2 = 0
        
        filtro = "SELECT * FROM CV"
        n=0
        primero=True
        for elemento in busqueda:
            if elemento.text.split() != []:
                if primero:
                    filtro +=" WHERE "

                for palabra in elemento.text.split():
                    #palabra2 = normalize(palabra)
                    if primero:
                        primero = False
                        filtro +="`" + str(filtros[n])+"` COLLATE NOACCENTS LIKE '%" + str(palabra)+"%'"
                        
                    else:
                        filtro +="and `"+str(filtros[n])+"` LIKE '%" + str(palabra)+"%'"
            n+=1
       
        palabras = []
        stop = False
        for row in c.execute(filtro):
            if((cont2 == pag*50 or cont2 > pag*50) and not stop):
                if cont == idNum:
                    for x in row:
                        print('//////////////'+str(x))
                        palabras.append(str(x))            
                cont += 1
                if cont == 50:
                    stop = True
            else:
                pass
            cont2 += 1
        n=0
        primero=True
        filtro = "UPDATE CV SET PDF = '" + str(fileName) + "' WHERE "
        print(list(map(lambda x: x[0], c.execute('select * from CV').description)))
        print(palabras)
        for nombre in list(map(lambda x: x[0], c.execute('select * from CV').description)):

            if primero:
                primero = False
                if(str(palabras[n])!='None'):
                    filtro +="`" + str(nombre)+"` = '" + str(palabras[n])+"' "

            else:
                if(str(palabras[n])!='None'):
                    filtro +=" and `"+str(nombre)+"` = '" + str(palabras[n])+"' "
            n+=1
        print(filtro)
        c.execute(filtro)
        #c.execute("UPDATE CV SET PDF = '2018' WHERE `Nombre` lIKE '%maría%' ")
        miConexion.commit()

    def reset(self):
       self.clear_widgets()


class campoTitulo(BoxLayout):
    g = StringProperty()
    def __init__(self,texto):
        super(campoTitulo, self).__init__()
        self.g = texto

class tituloFiltro(BoxLayout):
    g = StringProperty()
    filtro = BooleanProperty()
    def __init__(self,texto,filtro = True):
        super(tituloFiltro, self).__init__()
        self.g = texto
        self.filtro =filtro

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

class campoBD2(BoxLayout):
    color = BooleanProperty()
    pdf = BooleanProperty()
    ID = NumericProperty()
    # g = StringProperty()
    def __init__(self,colorCampo,pdf,idNum,path=''):
        super(campoBD2, self).__init__()
        self.pdf = pdf
        self.color = colorCampo
        self.ID = idNum
        self.g = path
      
    def agregarPDF(self):
        if (aplicacion.agregar):
            aplicacion.archivo = self.ID
            aplicacion.SubiendoArchivo = True
            #self.remove_widget(self.ids.boton)
            self.clear_widgets()
            self.add_widget(Label(text='Arrastrar archivo',color=(0.8,0,0)))
            aplicacion.agregar=False
        print('listo')

    def verPDF(self):
        path = self.g
        webbrowser.open_new(path)




class myApp(App):
    title = 'Plataforma'

    def build(self):
        Window.bind(on_dropfile=self._on_file_drop)
        self.SubiendoArchivo = False
        self.pantalla = Pantalla()
        #self.principal = Principal()
        self.archivo = ''
        self.nombreArchivo=''
        self.agregar=True
        return self.pantalla
        #return self.principal

    def _on_file_drop(self, window, file_path):
        print(self.SubiendoArchivo)
        if self.SubiendoArchivo:
            #pathFile = file_path
            self.agregar=True
            self.nombreArchivo = "./pdf/" + str(time.time()) + ".pdf"
            self.SubiendoArchivo = False
            shutil.copy(file_path,self.nombreArchivo)
            # self.pantalla.lista.reset()
            self.pantalla.lista.insertPdf(fileName=self.nombreArchivo,idNum=self.archivo,pag=0,filtros= self.pantalla.listaFiltros,busqueda=self.pantalla.filtros)
            self.pantalla.lista.reset()
            self.pantalla.lista.build(entrada=self.pantalla.campos,pag=0,filtros= self.pantalla.listaFiltros,busqueda=self.pantalla.filtros)
            print(file_path)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

# def normalize(s):
#     replacements = (
#         ("á", "a"),
#         ("é", "e"),
#         ("í", "i"),
#         ("ó", "o"),
#         ("ú", "u"),
#     )
#     for a, b in replacements:
#         s = s.replace(a, b).replace(a.upper(), b.upper())
#     return s
    

if __name__ == '__main__':

    table = "CV"
    path = "./cv_acosta.xlsx"

    xls = pd.ExcelFile(path)
    miConexion = sqlite3.connect('base')
    
    df = pd.read_excel(path)
    
    df.to_sql(name = table, con = miConexion, if_exists = 'replace', index = False)

    c = miConexion.cursor()
    c.execute('ALTER TABLE CV ADD PDF TEXT')
    pathFile = ''
    
    SubiendoArchivo = False
    aplicacion = myApp()
    aplicacion.run()

    c.close
    miConexion.close
