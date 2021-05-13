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

Builder.load_file('design.kv')


def read_from_db(entrada):
    c.execute('SELECT * FROM CV')
    cont = 0
    text = ''
    data = c.fetchall()
    #print(data)
    for row in data:
        cont+=1
        text += str(row)
        if cont == entrada:
            break
    return text


class MyWidget(BoxLayout):
    
    def __init__(self,entrada):
        super(MyWidget, self).__init__()
        for x in range(0,entrada):
            self.add_widget(campoBD())

class campoBD(BoxLayout):
    g = StringProperty()
    def __init__(self):
        super(campoBD, self).__init__()
        self.g = read_from_db(1)


class myApp(App):
    title = 'Plataforma'
    def build(self):
        return MyWidget(4)
    def on_pause(self):
        return True
    def on_resume(self): #¿Para que sirve esta función?
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
