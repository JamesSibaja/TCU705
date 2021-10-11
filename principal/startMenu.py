from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image 
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.textinput import TextInput

# from kivy.config import Config
# Config.set('kivy', 'keyboard_mode', 'system')
# Builder.load_file('designMenu.kv')

#Widget principal
class StartMenu(BoxLayout): 
    def __init__(self,upApp):
        super(StartMenu, self).__init__()
        #Aquí se define el menú inicial
        self.menu = MenuInicial()
        #self.menu.add_widget( startButton)
        self.menu.add_widget(TextInput(text='Nombre', size_hint=(.7, .1),
                pos_hint={'x':.15, 'y':.7}))
        self.menu.add_widget(TextInput(text='Contraseña', size_hint=(.7, .1),
                pos_hint={'x':.15, 'y':.5}))
        self.menu.add_widget( Button(text='Mis proyectos', size_hint=(.3, .1),
                pos_hint={'x':.15, 'y':.2},on_press=upApp.build))
        self.menu.add_widget( Button(text='Nuevo proyecto', size_hint=(.3, .1),
                pos_hint={'x':.55, 'y':.2},on_press=upApp.build))
        # self.menu.add_widget(Image(source='imagenes/logo.png', size_hint=(1, .6),
        #         pos_hint={'x':0, 'y':0.35}))
        #self.up = up
        self.add_widget(self.menu)

    # def build(self,obj):
    #     self.up.build()

class MenuInicial(FloatLayout):
    pass 