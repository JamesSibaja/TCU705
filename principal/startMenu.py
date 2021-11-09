from kivy.uix.behaviors import focus
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image 
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.uix.behaviors import ToggleButtonBehavior

from contrasenas import passw_manager
import re


#Widget principal
class StartMenu(BoxLayout): 
    def __init__(self,upApp):
        super(StartMenu, self).__init__()

        self.upApp = upApp

        #Aquí se define el menú inicial
        self.menu = MenuInicial(self.upApp)

        self.add_widget(self.menu)


# Clase que contiene el menu de inicio (pagina principal de la aplicacion)
class MenuInicial(FloatLayout):
    def __init__(self, upApp):
        super().__init__()

        self.upApp = upApp

        self.build()

        self.contrasenas_manager = passw_manager('base') # Se conecta al controlador de contrasenas por medio de un objeto diferente

    def build(self, *args):

        # self.add_widget(Label(text="Nombre de usuario", size_hint=(.4, .05), pos_hint={'x':.15, 'y':.7}))
        self.user = TextInput(size_hint=(.4, .05), pos_hint={'x':.3, 'y':.6}, multiline=False, write_tab= False, hint_text="Nombre de usuario")
        self.add_widget(self.user)

        # self.add_widget(Label(text="Contraseña", size_hint=(.4, .05), pos_hint={'x':.15, 'y':.5}))
        self.password = TextInput(hint_text="Contraseña",password=True, size_hint=(.4, .05),  pos_hint={'x':.3, 'y':.5}, multiline=False, write_tab= False, on_text_validate=self.loggin)
        self.add_widget(self.password)

        self.submit = Button(text='Iniciar Sesión', size_hint=(.3, .1), pos_hint={'x':.35, 'y':.35},on_press=self.loggin)
        self.add_widget(self.submit)

        self.register = Button(text='Registrarse', size_hint=(.3, .1), pos_hint={'x':.35, 'y':.25},on_press=self.btn_register)
        self.add_widget(self.register)

        # Comandos empleados para la funcionalidad Focus, pasar entre inputs con el "TAB"
        self.user.focus_next =self.password
        self.password.focus_next = self.user





    def loggin(self,obj):
        if self.contrasenas_manager.comparar(self.user.text, self.password.text):
            #print(self.contrasenas_manager.get_data(self.user.text)[0])
            self.upApp.build(userID=self.contrasenas_manager.get_data(self.user.text)[0])
        else:
                self.Fallo_UC()


    # En caso de haber un error en el usurio o contraseña se despliega un PopUp informando del error
    def Fallo_UC(self):
        content = Button(text='Aceptar', size_hint=(0.5, 0.5),font_size= 20)
        pop = Popup(title='Usuario y/o contraseña incorrecto(s), intente de nuevo',
                content=content,
                title_align = 'center',
                title_size = '20',
                auto_dismiss=False,
                size_hint=(None, None), size=(350, 200))

        content.bind(on_press=pop.dismiss)
        
        self.user.text = ""
        self.password.text = ""

        pop.open()

    # Metodo del boton de registro
    def btn_register(self, obj):
        self.clear_widgets()
        self.pag_register = RegisterWindow(self)
        self.add_widget(self.pag_register)


# Clase que contiene la pagina de registro
class RegisterWindow(FloatLayout, FocusBehavior):
    def __init__(self, init_page):
        super().__init__()

        self.init_page = init_page
        self.contrasenas_manager = passw_manager('base') # Se conecta al controlador de contrasenas por medio de un objeto diferente
        

        # self.add_widget(Label(text="Nombre de usuario", size_hint=(.4, .05), pos_hint={'x':.15, 'y':.7}))
        self.nombre = TextInput(size_hint=(.4, .05), pos_hint={'x':.3, 'y':.8}, multiline=False, write_tab= False, hint_text="Nombre")
        self.add_widget(self.nombre)

        self.apellido = TextInput(size_hint=(.4, .05), pos_hint={'x':.3, 'y':.7}, multiline=False, write_tab= False, hint_text="Apellido")
        self.add_widget(self.apellido)

        self.email = TextInput(size_hint=(.4, .05), pos_hint={'x':.3, 'y':.6}, multiline=False, write_tab= False, hint_text="Correo")
        self.add_widget(self.email)

        self.user = TextInput(size_hint=(.4, .05), pos_hint={'x':.3, 'y':.5}, multiline=False, write_tab= False, hint_text="Nombre de usuario")
        self.add_widget(self.user)

        
        # self.add_widget(Label(text="Contraseña", size_hint=(.4, .05), pos_hint={'x':.15, 'y':.5}))
        self.password = TextInput(password=True, size_hint=(.35, .05),  pos_hint={'x':.3, 'y':.4}, multiline=False, write_tab= False, hint_text="Contraseña")
        self.add_widget(self.password)

        self.selector_pass1 = BTN_Ojito( size_hint=(.05, .05), pos_hint={'x':.65, 'y':.4}, on_press=self.ver_passwords)
        self.add_widget(self.selector_pass1)

        # self.add_widget(Label(text="Repetir Contraseña", size_hint=(.4, .05), pos_hint={'x':.15, 'y':.4}))
        self.password2 = TextInput(password=True, size_hint=(.35, .05),  pos_hint={'x':.3, 'y':.3}, multiline=False, 
                                    on_text_validate=self.btn_registrarse, write_tab= False, hint_text="Repetir Contraseña")
        self.add_widget(self.password2)

        self.selector_pass2 = BTN_Ojito(size_hint=(.05, .05), pos_hint={'x':.65, 'y':.3}, on_press=self.ver_passwords)
        self.add_widget(self.selector_pass2)

        self.submit = Button(text='Registrarse', size_hint=(.3, .1), pos_hint={'x':.35, 'y':.15},on_press=self.btn_registrarse)
        self.add_widget(self.submit)

        self.btn_return = Button(size_hint=(0.1,0.1), pos_hint={'x':.01, 'y':.9},background_normal = './imagenes/arrow.png', on_press=self.return_callback)
        self.add_widget(self.btn_return)

        # self.btn_test = button_rtnr()
        # self.add_widget(self.btn_test)

        self.user.focus_next = self.password
        self.password.focus_next = self.password2
        self.password2.focus_next = self.user

    # Metodo que se devuelve a la pagina de menu inicial
    def return_callback(self,obj=None):
        self.clear_widgets()
        # Limpia el fundo
        with self.canvas:
            Color(1,1,1)
            Rectangle(size=self.size, pos=self.pos)

        self.init_page.build(obj)
    
    def ver_passwords(self, obj):
        if (obj == self.selector_pass1):
            if (self.password.password == True):
                self.password.password=False
                self.selector_pass1.source='./imagenes/ojito.png'
            else:
                self.password.password = True
                self.selector_pass1.source='./imagenes/no_ojito.png'
                ## Cambiar el ojito


        if (obj == self.selector_pass2):
            if (self.password2.password == True):
                self.password2.password=False
                self.selector_pass2.source='./imagenes/ojito.png'
            else:
                self.password2.password = True
                self.selector_pass2.source='./imagenes/no_ojito.png'


    # Metodo que realiza la operacion del registro de usuario y contraseña en la base de datos
    def btn_registrarse(self,obj):
        if (self.user.text == ""):
            self.Fallo_UC()
        
        else:
            if(self.password.text == self.password2.text):

                if (re.findall("^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[.,@#$%^&+=]).*$", self.password.text)):
                    
                    
                    if(re.findall("^(?![-._])(?!.*[_.-]{2})[\w.-]{5,30}(?<![-._])$", self.user.text) and self.contrasenas_manager.save_new(self.user.text, self.password.text, self.nombre.text, self.apellido.text, self.email.text)):
                    # if(re.findall("^(?![-._])(?!.*[_.-]{2})[\w.-]{5,30}(?<![-._])$", self.user.text) and self.contrasenas_manager.save_new(self.user.text, self.password.text)):
                        self.return_callback()

                    else:
                        self.Fallo_UC()
                        self.user.text=""
                        self.password.text=""
                        self.password2.text=""
                    
                else:
                    self.Fallo_longitud()
                    self.user.text=""
                    self.password.text=""
                    self.password2.text=""
            else:
                self.Fallo_passw_igual()
                self.password.text=""
                self.password2.text=""

            

    # En caso de haber un error en el usurio o contraseña se despliega un PopUp informando del error
    def Fallo_UC(self):
        content = Button(text='Aceptar', size_hint=(0.5, 0.5),font_size= 20)
        pop = Popup(title='El nombre de usuario no se encuentra disponible, o no es válido',
                content=content,
                title_align = 'center',
                title_size = '20',
                auto_dismiss=False,
                size_hint=(None, None), size=(350, 200))

        content.bind(on_press=pop.dismiss)
        
        self.user.text = ""
        self.password.text = ""

        pop.open()
    
    # En caso de no cumplir con una contraseña de mas de 8 caracteres, se despliega un PopUp informando del error
    def Fallo_longitud(self):
        content = Button(text='Aceptar', size_hint=(0.5, 0.5),font_size= 20)
        pop = Popup(title='La contraseña debe tener mayúsculas, minúsculas, números y símbolos especiales',
                content=content,
                title_align = 'center',
                title_size = '20',
                auto_dismiss=False,
                size_hint=(None, None), size=(350, 200))

        content.bind(on_press=pop.dismiss)
        
        self.user.text = ""
        self.password.text = ""

        pop.open()

    # En caso de no cumplir con una contraseñas iguales, se despliega un PopUp informando del error
    def Fallo_passw_igual(self):
        content = Button(text='Aceptar', size_hint=(0.5, 0.5),font_size= 20)
        pop = Popup(title='Las contraseñas no coinciden',
                content=content,
                title_align = 'center',
                title_size = '20',
                auto_dismiss=False,
                size_hint=(None, None), size=(350, 200))

        content.bind(on_press=pop.dismiss)

        pop.open()



'''
=======================
Widgets complementarios
=======================
'''

class BTN_Ojito(ToggleButtonBehavior,Image,BoxLayout):
    def __init__(self,**kwargs):
        super(BTN_Ojito, self).__init__(**kwargs)