import pymysql
from hashlib import sha256

# class database:
#     def __init__(self) -> None:
#         try:
#             self.connection = pymysql.connect(
#                 host = 'localhost',
#                 user='TCU',
#                 password='1234',
#                 db='users'
#             )
#             self.cursor = self.connection.cursor()
#         except:
#             print("Hubo un error")

#     def creat_table(self):
#         command = '''CREATE TABLE IF NOT EXISTS passwords
#              (user BLOB, pass BLOB)'''
#         self.cursor.execute(command)
#         self.connection.commit()

#     def save_new(self):
#         pass

# data = database()
# data.creat_table()

class passw_manager:
    def __init__(self):

        self.data = pymysql.connect(
                host = 'localhost',
                user='TCU',
                password='1234',
                db='users'
            )

        c = self.data.cursor()

        #get the count of tables with the name
        c.execute('''CREATE TABLE IF NOT EXISTS passwords
             (username varchar(255) NOT NULL, pass BLOB NOT NULL, nombre TEXT NOT NULL, apellido TEXT NOT NULL, correo TEXT NOT NULL)''')


        self.data.commit()
        self.data.close()

    def comparar(self, usuario, password):
        self.data = pymysql.connect(
                host = 'localhost',
                user='TCU',
                password='1234',
                db='users'
            )

        c = self.data.cursor()
        
        comando = '''SELECT * 
                    FROM passwords 
                    WHERE (username = {})'''.format(usuario)

        c.execute(comando)

        rows = c.fetchall()

        for r in rows:
            if r[0] == usuario and r[1] == sha256(password.encode()).hexdigest():
                self.data.commit()
                self.data.close()
                return True
        
        self.data.commit()
        self.data.close()
        # return False

        
        

    def save_new(self, username, password, nombre="", apellido="", correo=""):
        self.data = pymysql.connect(
                host = 'localhost',
                user='TCU',
                password='1234',
                db='users'
            )

        c = self.data.cursor()

        # c.execute('''INSERT INTO passwords
        #         VALUES(?,?)''', (sha256(usuario.encode()).hexdigest(), sha256(password.encode()).hexdigest()))

        comando = '''SELECT * 
                    FROM passwords 
                    WHERE (username = {})'''.format(username)
        try:
            c.execute(comando)
        except:
            print("Hubo un error, con el comando: ")
            print(comando)

        rows = c.fetchall()

        if (len(rows)>0):
            self.data.commit()
            self.data.close()
            return False
        else:
            comando = '''INSERT INTO passwords
                    VALUES({},{},{},{},{})'''.format(username, sha256(password.encode()).hexdigest(), nombre, apellido, correo)
            
            try:
                c.execute(comando)
            except:
                print('hubo un error con el comando:')
                print(comando)
            self.data.commit()
            self.data.close()
            return True

    #######  Metodos que devuelven un valor de la tabla ##########

    ## Metodo que devuelve los datos del usuario, execpto la contraseña
    def get_data(self, username):
        self.data = pymysql.connect(
                host = 'localhost',
                user='TCU',
                password='1234',
                db='users'
            )
        c = self.data.cursor()
        
        comando = '''SELECT * FROM passwords 
                    WHERE username={}'''.format(username)
        c.execute(comando)

        user = c.fetchall()
        
        self.data.commit()
        self.data.close()
        return user[0][2:]


    #######  Metodos de edicion del registro de un usuario ##########
    

    ## Metodo que realiza la edicion del nombre del usuario.
    def editname(self, username, name):
        self.data = pymysql.connect(
                host = 'localhost',
                user='TCU',
                password='1234',
                db='users'
            )
        c = self.data.cursor()
        try:
            comando='''UPDATE passwords
                        SET nombre = {} 
                        WHERE username = {}'''.format(name, username)
            c.execute(comando)

        except:
            self.data.commit()
            self.data.close()  
            return False
        self.data.commit()
        self.data.close()
        return True


    ## Metodo que realiza la edicion del apellido
    def editapellido(self, username, lastname):
        self.data = pymysql.connect(
                host = 'localhost',
                user='TCU',
                password='1234',
                db='users'
            )
        c = self.data.cursor()


    ## Metodo que realiza la actualizacon del username
    def editusername(self, username, newusername):
        self.data = pymysql.connect(
                host = 'localhost',
                user='TCU',
                password='1234',
                db='users'
            )
        c = self.data.cursor()

    ## Metodo que actualiza la contraseña del usuario
    def editpassword(self, username, password):
        self.data = pymysql.connect(
                host = 'localhost',
                user='TCU',
                password='1234',
                db='users'
            )
        c = self.data.cursor()


data=passw_manager()
data.save_new("erick.sancho",'12345','Erick', 'Sancho')
data.get_data()