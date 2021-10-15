import sqlite3
from hashlib import sha256


class passw_manager:
    def __init__(self, base_datos):
        self.base = base_datos

        self.data = sqlite3.connect(self.base)

        c = self.data.cursor()

        #get the count of tables with the name
        c.execute('''CREATE TABLE IF NOT EXISTS passwords
             (user BLOB, pass BLOB)''')


        self.data.commit()
        self.data.close()

    def comparar(self, usuario, password):
        self.data = sqlite3.connect(self.base)

        c = self.data.cursor()

        c.execute('''SELECT * FROM passwords;''')

        rows = c.fetchall()

        for r in rows:
            if r[0] == sha256(usuario.encode()).hexdigest() and r[1] == sha256(password.encode()).hexdigest():
                self.data.commit()
                self.data.close()
                return True
        
        self.data.commit()
        self.data.close()
        return False

        
        

    def save_new(self, usuario, password):
        self.data = sqlite3.connect(self.base)

        c = self.data.cursor()

        c.execute('''SELECT * FROM passwords;''')

        rows = c.fetchall()

        usuario_ya_añadido = False
        for r in rows:
            if r[0] == sha256(usuario.encode()).hexdigest():
                usuario_ya_añadido = True
                break

        if (not usuario_ya_añadido):
            c.execute('''INSERT INTO passwords
                VALUES(?,?)''', (sha256(usuario.encode()).hexdigest(), sha256(password.encode()).hexdigest()))

            self.data.commit()
            self.data.close()
            return True
        else:
            return False

