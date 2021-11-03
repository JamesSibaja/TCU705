import sqlite3
from hashlib import sha256


class passw_manager:
    def __init__(self, base_datos):
        self.base = base_datos

        self.data = sqlite3.connect(self.base)

        c = self.data.cursor()

        #get the count of tables with the name
        c.execute('''CREATE TABLE IF NOT EXISTS passwords
             (username varchar(255) NOT NULL, pass BLOB NOT NULL, nombre TEXT NOT NULL, apellido TEXT NOT NULL, correo TEXT NOT NULL)''')


        self.data.commit()
        self.data.close()

    def comparar(self, username, password):
        self.data = sqlite3.connect(self.base)

        c = self.data.cursor()

        c.execute('''SELECT * 
                    FROM passwords 
                    WHERE (username = ?)''', (username,))

        rows = c.fetchall()

        for r in rows:
            if r[0] == username and r[1] == sha256(password.encode()).hexdigest():
                self.data.commit()
                self.data.close()
                return True
        
        self.data.commit()
        self.data.close()
        # return False

        
        

    def save_new(self, username, password, nombre="", apellido="", correo=""):
        self.data = sqlite3.connect(self.base)

        c = self.data.cursor()

        # c.execute('''INSERT INTO passwords
        #         VALUES(?,?)''', (sha256(usuario.encode()).hexdigest(), sha256(password.encode()).hexdigest()))

        c.execute('''SELECT * 
                    FROM passwords 
                    WHERE (username = ?)''', (username,))

        rows = c.fetchall()

        if (len(rows)>0):
            self.data.commit()
            self.data.close()
            return False
        else:

            c.execute('''INSERT INTO passwords
                    VALUES(?,?,?,?,?)''', (username, sha256(password.encode()).hexdigest(), nombre, apellido, correo))

            self.data.commit()
            self.data.close()
            return True

    #######  Metodos que devuelven un valor de la tabla ##########

    ## Metodo que devuelve los datos del usuario, execpto la contraseña
    def get_data(self, username):
        self.data = sqlite3.connect(self.base)
        c = self.data.cursor()

        c.execute('''SELECT * FROM passwords 
                    WHERE username=?''', (username,))

        user = c.fetchall()
        
        self.data.commit()
        self.data.close()
        return user[0][2:]


    #######  Metodos de edicion del registro de un usuario ##########
    

    ## Metodo que realiza la edicion del nombre del usuario.
    def editname(self, username, name):
        self.data = sqlite3.connect(self.base)
        c = self.data.cursor()
        try:
            c.execute('''UPDATE passwords
                        SET nombre = ? 
                        WHERE username = ?''', (name, username))

        except:
            self.data.commit()
            self.data.close()  
            return False
        self.data.commit()
        self.data.close()
        return True


    ## Metodo que realiza la edicion del apellido
    def editapellido(self, username, lastname):
        self.data = sqlite3.connect(self.base)
        c = self.data.cursor()


    ## Metodo que realiza la actualizacon del username
    def editusername(self, username, newusername):
        self.data = sqlite3.connect(self.base)
        c = self.data.cursor()

    ## Metodo que actualiza la contraseña del usuario
    def editpassword(self, username, password):
        self.data = sqlite3.connect(self.base)
        c = self.data.cursor()

