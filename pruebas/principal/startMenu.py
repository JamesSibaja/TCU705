from lib import *

#Widget principal
class StartMenu(BoxLayout): 
    def __init__(self,upApp):
        super(StartMenu, self).__init__()
        self.upApp = upApp
        #Aquí se define el menú inicial
        self.menu = MenuInicial()
        #self.menu.add_widget( startButton)
        self.menu.add_widget(TextInput(text='Nombre', size_hint=(.7, .1),
                                        pos_hint={'x':.15, 'y':.7}))
        self.menu.add_widget(TextInput(text='Contraseña', size_hint=(.7, .1),
                                        pos_hint={'x':.15, 'y':.5}))
        self.menu.add_widget( Button(text='Mis proyectos', size_hint=(.3, .1),
                                        pos_hint={'x':.15, 'y':.2},on_press=self.my_project))
        self.menu.add_widget( Button(text='Nuevo proyecto', size_hint=(.3, .1),
                                        pos_hint={'x':.55, 'y':.2},on_press=self.my_project))
        # self.menu.add_widget(Image(source='imagenes/logo.png', size_hint=(1, .6),
        #         pos_hint={'x':0, 'y':0.35}))
        #self.up = up
        self.add_widget(self.menu)
    
    def my_project(self,obj):
        self.upApp.build(1)
    # def build(self,obj):
    #     self.up.build()

class MenuInicial(FloatLayout):
    pass 