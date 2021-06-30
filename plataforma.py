import sqlite3
import pandas as pd	



class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.entrythingy = tk.Entry()
        self.entrythingy.pack()

        # Create the application variable.
        self.contents = tk.StringVar()
        # Set it to some value.
        self.contents.set("this is a variable")
        # Tell the entry widget to watch this variable.
        self.entrythingy["textvariable"] = self.contents

        # Define a callback for when the user hits return.
        # It prints the current value of the variable.
        self.entrythingy.bind('<Key-Return>',
                             self.print_contents)

    def print_contents(self, event):
        print("Hi. The current entry content is:",
              self.contents.get())



def read_from_db(entrada):
    
    cont = 0
    text = ''
    #print(data)
    for row in c.execute('SELECT Nombre, Sexo FROM CV'):
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
    

    root = tk.Tk()
    myapp = App(root)
    myapp.mainloop()

    c.close
    miConexion.close
