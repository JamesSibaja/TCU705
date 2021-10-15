from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image 
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from contrasenas import passw_manager

# from kivy.config import Config
# Config.set('kivy', 'keyboard_mode', 'system')
# Builder.load_file('designMenu.kv')

#Widget principal
class StartMenu(BoxLayout): 
    def __init__(self,upApp):
        super(StartMenu, self).__init__()

        self.upApp = upApp

        #Aquí se define el menú inicial
        self.menu = MenuInicial()
        #self.menu.add_widget( startButton)

        self.menu.add_widget(Label(text="Nombre de usuario", size_hint=(.4, .05), pos_hint={'x':.15, 'y':.7}))

        self.user = TextInput(size_hint=(.4, .05), pos_hint={'x':.5, 'y':.7})
        self.menu.add_widget(self.user)

        self.menu.add_widget(Label(text="Contraseña", size_hint=(.4, .05), pos_hint={'x':.15, 'y':.5}))
        self.password = TextInput(password=True, size_hint=(.4, .05),  pos_hint={'x':.5, 'y':.5})
        self.menu.add_widget(self.password)

        self.submit = Button(text='Iniciar Seción', size_hint=(.3, .1), pos_hint={'x':.15, 'y':.2},on_press=self.loggin)
        self.menu.add_widget(self.submit)

        self.menu.add_widget( Button(text='Registrarse', size_hint=(.3, .1),
                pos_hint={'x':.55, 'y':.2},on_press=self.loggin))
        # self.menu.add_widget(Image(source='imagenes/logo.png', size_hint=(1, .6),
        #         pos_hint={'x':0, 'y':0.35}))
        #self.up = up
        self.add_widget(self.menu)

        self.contrasenas_manager = passw_manager("pass.db")

    # def build(self,obj):
    #     self.up.build()

    def loggin(self,obj):
        if self.contrasenas_manager.comparar(self.user.text, self.password.text):
                self.upApp.build(obj)
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




class MenuInicial(FloatLayout):
    pass 