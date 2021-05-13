import tkinter as tk 
from tkinter import *

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.saludo()

    def saludo(self): 
        text = Text(self)  
        text.insert(INSERT, "Bienvenido seleccione la funcion que desea realizar el dia de hoy")  
        
  
        text.pack()  
  
        text.tag_add("Write Here", "1.0", "1.4")  
        
  
        text.tag_config("Write Here", background="white", foreground="black")  
        
       
    def create_widgets(self):
        self.MBDD = tk.Button(self)
        self.MBDD["text"] = "Mis bases de datos"
        self.MBDD["command"] = self.say_hi
        self.MBDD.pack(side="right")

        self.AD= tk.Button(self)
        self.AD["text"]="Agregar Documento"
        self.AD["command"] = self.say_hi
        self.AD.pack(side="right")

        self.AU=tk.Button(self)
        self.AU["text"]="Ajustes de Usuario"
        self.AU["command"] = self.say_hi
        self.AU.pack(side="right")



        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="right")

        

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()