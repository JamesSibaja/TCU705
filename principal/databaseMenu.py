from lib import *
from dataViewer import DataViewer
from contrasenas import passw_manager
SubiendoArchivo = False

'''
================
Widget principal
================
Widget asociado a la totalidad de la ventana donde se presenta la interfaz de la aplicación
'''
#Widget principal 
class DatabaseMenu(BoxLayout): 
    def __init__(self,upApp,base,aplicacion,userID,**kwargs):
        super(DatabaseMenu, self).__init__(**kwargs)
        self.baseName = base
        self.conexion = sqlite3.connect(self.baseName)
        self.base = self.conexion.cursor()
        self.userID = userID
        self.aplicacion = aplicacion
        self.table = 'myDatabases'   
        self.upApp = upApp
        #get the count of tables with the name 
        self.base.execute('''CREATE TABLE IF NOT EXISTS database(
                            ID INTEGER primary key autoincrement,
                            Nombre varchar(255) NOT NULL,
                            Columns varchar(255) NOT NULL
                        ) ''')

        # self.base.execute('''CREATE TABLE IF NOT EXISTS users(
        #                     ID INTEGER primary key autoincrement,
        #                     UserName varchar(255) NOT NULL
        #                 ) ''') passwords

        self.base.execute('''CREATE TABLE IF NOT EXISTS usersxdatabase(
                            ID INTEGER primary key autoincrement,
                            UserID INTEGER NOT NULL,
                            DatabaseID INTEGER NOT NULL,
                            Permiso varchar(255) NOT NULL,
                            FOREIGN KEY (UserID) REFERENCES passwords(ID),
                            FOREIGN KEY (DatabaseID) REFERENCES database(ID)
                        ) ''')
        
        # self.base.execute('''INSERT INTO users (UserName)
        #                      VALUES ('Luis') ''')

        # self.base.execute('''INSERT INTO users (UserName)
        #                      VALUES ('James') ''')

        # self.base.execute('''INSERT INTO users (UserName)
        #                      VALUES ('Erick') ''')

        self.conexion.commit()
        self.df = ['Nombre'] #Mejorar ya que esta linea prodia no ser necesaria
        self.build()
        

    #Constructor de la ventana principal bus
    def build(self):
        self.base.close()
        self.conexion.close()
        self.conexion = sqlite3.connect(self.baseName)
        self.base = self.conexion.cursor()
        self.base.execute("CREATE TEMPORARY TABLE myDatabases AS SELECT database.ID, database.Nombre, usersxdatabase.Permiso FROM database INNER JOIN usersxdatabase ON usersxdatabase.DatabaseID = database.ID WHERE usersxdatabase.UserID = "+str(self.userID))
        self.conexion.commit()
        self.clear_widgets()
        self.numPag = 0
        self.exit = Exit(on_press=self.salir)
        self.selectBase = ''
        self.MenuMain = ToolbarTitle()
        self.editarPerfil = False
        self.nuevaBase = False
        self.tablas = False
        self.select = False

        self.search = Search(on_press=self.buscarpop)
        self.res = Res(on_press=self.reset)
        self.infoTextBox =[]
        self.success = False
        self.editar = False
        self.selectEdit = False
        self.selectDatabase = True
        self.datoCalc = ""
        self.menuTitle =0
        self.toolbar = Toolbar()
        self.contenedor = ToolbarSub() 
        self.base.execute("select username from passwords where ID = "+ str(self.userID))
        self.nameTitle = self.base.fetchall()[0][0]

        self.colaboradores =[self.nameTitle]
        self.colaboradoresID =[self.userID]
        self.compartirID =[]
        self.filaTitulo = FilaTitulo()
        self.pagina = FilaPag()
        self.listaFiltros =[]
        self.listaFiltros2 =[]
        self.camposOpcion = []
        self.filtrosOpcion = []
        self.filtros = []
        self.filtros2 = []
        self.campos = []
        self.nombres = list(map(lambda x: x[0], self.base.execute('select * from '+ self.table).description))
        self.index = self.nombres[0]
        self.nombres.pop(0)
        contCampos=0
        for selectField in self.nombres:
            if selectField !='Columns':
                self.camposOpcion.append(True)
                self.campos.append(str(selectField))
            else:
                self.camposOpcion.append(False)
            self.filtrosOpcion.append(False)
            contCampos+=1
        self.lista = DataViewer(upapp=self,index=self.index,entrada=self.campos,base = self.base,table = self.table,aplicacion=self.aplicacion,conexion = self.conexion,pag = self.numPag)
        self.pagina.add_widget(BoxLayout())
        self.pagina.add_widget(TitlePag(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50))))
        self.pagebarBuilder(0,True)
        #self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='Siguiente >',on_press=self.siguientePagina))
        self.contenedorLista = BoxLayout(padding = 10,orientation= 'vertical')
        for selectField in self.campos:
            self.filaTitulo.add_widget(TitleField(selectField))
        self.palabrasBuscadas={}
        self.pantalla = BoxLayout(orientation='horizontal')

        #Se crea la barra de Menú y barra de herramientas
        self.barraMenu = MenuBar()
        self.submitOptions = []
        self.submitOptions.append(ToolbarText(texto = 'Bases de Datos',on_press=self.openBase))
        self.submitOptions.append(ToolbarText(texto = 'Nueva Base',on_press=self.newBase))
        self.submitOptions.append(ToolbarText(texto = 'Perfil',on_press=self.perfil))
        # self.submitOptions.append(ToolbarText(texto = 'Filtro',on_press=self.nuevoInicio))#
        # self.submitOptions.append(ToolbarText(texto = 'Estadísticas',on_press=self.nuevoEst))#
        # self.submitOptions.append(ToolbarText(texto = 'Ajustes'))
        self.menubarBuilder()
        self.toolbar.add_widget(self.contenedor)
        self.subBoton = BoxLayout(size_hint=(1,None),height=50,padding= (15,5,15,10))
        self.toolbar.add_widget(self.subBoton)
        self.pantalla.add_widget(self.toolbar)
        self.contenedorLista.add_widget(self.filaTitulo)
        self.contenedorLista.add_widget(self.lista)
        self.contenedorLista.add_widget(self.pagina)
        self.pantalla.add_widget(self.contenedorLista)
        self.add_widget(self.barraMenu)
        self.add_widget(self.pantalla)
        self.add_widget(PiePagina(self.nameTitle))
        self.permisoEditar = ToggleButton(text="Permiso para editar",size_hint_y=None,height=25)
        
        self.toolbarBuilder()

    #Función que esconde la barra de herramientas
    def toolbarHide(self,obj): 
        self.contenedor.show = not self.contenedor.show
        self.toolbar.show = not self.toolbar.show
        if self.contenedor.show:
            self.toolbarBuilder()
        else:
            self.contenedor.clear_widgets()
            self.subBoton.clear_widgets()
            
    #Constructor de la barra de herramientas
    def menubarBuilder(self):
        self.barraMenu.clear_widgets()
        #self.MenuMain.clear_widgets()
        # self.MenuMain.add_widget(ToolbarShow(on_press=self.toolbarHide))
        # self.MenuMain.add_widget(ToolbarTitleText(texto= self.nameTitle))
        contOpt = 0
        for option in self.submitOptions:
            if(self.menuTitle==contOpt):
                option.main = True
            else:
                option.main = False
            contOpt = contOpt + 1

        #self.barraMenu.add_widget(self.MenuMain)
        self.barraMenu.add_widget(ToolbarShow(on_press=self.toolbarHide))

        
        self.barraMenu.add_widget(SeparadorH())     
        contOpt = 0
        for option in self.submitOptions:
            self.barraMenu.add_widget(option)
            # if not (self.menuTitle==contOpt):
            #     option.main = False
            # contOpt = contOpt + 1    
         
        self.barraMenu.add_widget(SeparadorH())  
        self.barraMenu.add_widget(self.res)
        self.barraMenu.add_widget(self.search)
        self.barraMenu.add_widget(self.exit)  
       # self.barraMenu.add_widget(ToolbarTitleText(texto= self.nameTitle)) 
 
    #Constructor de la barra de herramientas
    def toolbarBuilder(self):   
        self.contenedor.scroll_y=1
        self.contenedor.clear_widgets()
        self.subBoton.clear_widgets()
        self.contenedor.build()
        self.contenedorLista.clear_widgets()
               
        #Si se encuentra en el menú de filtros
        #if self.nuevaBase:
        if self.menuTitle==1:
            self.contenedorLista.add_widget(NewDocument(self.aplicacion))
            self.contenedor.stack.add_widget(Title3("Agregar colaborador"))
            self.newUser = TextInput(text='',size_hint_y=None,height=45)
            self.permisoEditar = ToggleButton(text="Permiso para editar",size_hint_y=None,height=25)
            self.contenedor.stack.add_widget(self.newUser)
            self.contenedor.stack.add_widget(Separador())
            self.contenedor.stack.add_widget(self.permisoEditar) 
            self.contenedor.stack.add_widget(Separador())
            self.contenedor.stack.add_widget(ButtonAccept(texto = 'Verificar',on_press=self.addUser))
            self.contenedor.stack.add_widget(Separador2()) 
            
            primero = True
            for user in self.colaboradores: 
                if not primero:
                    self.contenedor.stack.add_widget(Title2(user))
                primero = False

        else:
            
            #if self.selectDatabase:
            if self.menuTitle==0:
                self.createLista()
                cont = -1
                self.infoTextBo=[]
                if self.select:
                    self.contenedor.stack.add_widget(Title2('Datos')) 
                    for lista in self.lista.information:
                        for text in lista:
                            
                            if cont != -1:
                                self.contenedor.stack.add_widget(Title(texto=self.nombres[cont] + ":",bold = True))
                                if self.nombres[cont] == 'Nombre':
                                    self.selectBase = str(text)
                                if self.nombres[cont] == 'Permiso':
                                    if text == 'Editar':
                                        self.selectEdit = True
                                    else:
                                        self.selectEdit = False
                                if self.editar:
                                    self.infoTextBox.append(TextInput(text=str(text),size_hint_y=None,height=70,background_color=(0.9,0.9,0.9,1)))
                                else:
                                    self.infoTextBox.append(TextInput(text=str(text),size_hint_y=None,height=70,background_color=(0.85,0.85,0.85,0)))
                                self.contenedor.stack.add_widget(self.infoTextBox[len(self.infoTextBox)-1])
                                
                                if self.editar:
                                    self.contenedor.stack.add_widget(Separador())
                                    self.contenedor.stack.add_widget(ButtonAccept(texto = 'Editar',title=self.nombres[cont],input=len(self.infoTextBox)-1,on_press=self.editarCampo))
                            cont = cont + 1
                    self.contenedor.stack.add_widget(Title2('')) 
                    if self.toolbar.show:
                        self.subBoton.add_widget(ButtonAccept(texto = 'Abrir',on_press=self.open))
                else:
                    #self.cuadroTexto = BoxLayout(size_hint_y= None,height=300)
                    #self.cuadroTexto.add_widget(Label(text='Ningún elemento seleccionado, haga click sobre algún elemento de la lista', halign='center', valign='top', color=  (0.7,0.45,0,1),text_size=self.cuadroTexto.size)) 
                    self.contenedor.stack.add_widget(Title('Ningún elemento seleccionado, haga click sobre algún elemento de la lista',size_hint_y= None,height=300)) 
                    #self.contenedor.stack.add_widget(self.cuadroTexto) 
            else:
                if self.menuTitle==2:
                    self.contenedorLista.add_widget(NewDocument2(self.nameTitle))
                    self.contenedor.stack.add_widget(ButtonMain(texto = 'Ver perfil'))
                    self.contenedor.stack.add_widget(ButtonMain(texto = 'Editar Perfil'))
                    self.contenedor.stack.add_widget(Separador())
                    self.contenedor.stack.add_widget(Title("Ajustes"))
                    self.contenedor.stack.add_widget(ButtonMain(texto = 'Idioma'))
                    self.contenedor.stack.add_widget(ButtonMain(texto = 'Tamaño de Letra'))
                    self.contenedor.stack.add_widget(ButtonMain(texto = 'Tamaño de Página'))
                    self.contenedor.stack.add_widget(ButtonMain(texto = 'Tema'))
                    self.contenedor.stack.add_widget(ButtonMain(texto = 'Accesibilidad'))
                
        self.contenedor.add_widget(self.contenedor.stack)

    def addUser(self,obj):
        self.success = False
        incluido = False
        ID = 0
        for r in self.base.execute('''SELECT ID, UserName FROM passwords'''):
            if r[1] == self.newUser.text:
                self.success = True  
                ID = r[0] 
                for user in self.colaboradores: 
                    if user == self.newUser.text:
                        incluido = True
                        self.success = False
        if not self.success:
            content = Button(text='Aceptar', size_hint=(0.5, 0.5),font_size= 20)
            if incluido:
                pop = Popup(title='El nombre de usuario ya está incluido',
                        content=content,
                        title_align = 'center',
                        title_size = '20',
                        auto_dismiss=False,
                        size_hint=(None, None), size=(350, 200))
            else:
                pop = Popup(title='El nombre de usuario no se encuentra disponible',
                        content=content,
                        title_align = 'center',
                        title_size = '20',
                        auto_dismiss=False,
                        size_hint=(None, None), size=(350, 200))

            content.bind(on_press=pop.dismiss)
            pop.open()
        else:
            self.colaboradores.append(self.newUser.text)
            if self.permisoEditar.state == 'down':                
                self.colaboradoresID.append(ID)
            else:
                self.compartirID.append(ID)
        self.toolbarBuilder()


    def open(self,obj):
        self.upApp.build(2,table= self.selectBase,edit= self.selectEdit)

    def createLista(self):
        self.contenedorLista.add_widget(self.filaTitulo)
        self.contenedorLista.add_widget(self.lista)
        self.contenedorLista.add_widget(self.pagina)

    def editarCampo(self,obj): #Función que cambia las columnas que se muestran*
        filtro = "UPDATE "+self.table+" SET `"+ obj.title +"` = '"+ self.infoTextBox[obj.input].text +"' WHERE `" + self.index + "` = '" + str(self.lista.id) +"'"
        self.base.execute(filtro)
        self.conexion.commit()
        self.buscar()

    def baseLink(self,baseID):
        for user in self.colaboradoresID:
            self.base.execute("INSERT INTO usersxdatabase (UserID,DatabaseID,Permiso) VALUES ("+str(user)+","+str(baseID)+",'Editar') ")
            self.conexion.commit()

        for user in self.compartirID:
            self.base.execute("INSERT INTO usersxdatabase (UserID,DatabaseID,Permiso) VALUES ("+str(user)+","+str(baseID)+",'Ver') ")
            self.conexion.commit()

        self.build()

    def openBase(self,obj): #Función de la opción del menu ver
        self.menuTitle=0
        self.menubarBuilder()
        self.selectDatabase = True
        self.nuevaBase = False
        # self.toolbar.show = False
        # self.toolbarHide(obj)
        self.toolbarBuilder()
        self.contenedor.stack.scroll_y=1
        

    def newBase(self,obj): #Función de la opción del menu editar
        self.menuTitle=1
        self.menubarBuilder()
        self.selectDatabase = False
        self.nuevaBase = True
        self.colaboradores =[self.nameTitle]
        self.colaboradoresID =[self.userID]
        self.lista.reset()
        self.lista.build(entrada=self.campos,pag=self.numPag,filtros= self.listaFiltros,busqueda=self.filtros)
        #self.toolbar.show = False
        #self.toolbarHide(obj)

        self.toolbarBuilder() 
        self.contenedor.stack.scroll_y=1

    def siguientePagina(self,obj): #Siguiente página para caso general
        self.lista.reset()
        self.lista.build(entrada=self.campos,pag=self.numPag+1,filtros= self.listaFiltros,busqueda=self.filtros)
        self.pagebarBuilder(1,True)
        
    def anteriorPagina(self,obj): #Página anterior para caso general
        self.lista.reset()
        self.lista.build(entrada=self.campos,pag=self.numPag-1,filtros= self.listaFiltros,busqueda=self.filtros)
        self.pagebarBuilder(-1,True)

    def sigPag(self,obj):   #Siguiente página para lista de estadísticas
        self.lista.reset()    
        self.lista.calcAct(pag=self.numPag+1)
        self.pagebarBuilder(1,False)

    def antPag(self,obj): #Página anterior para lista de estadísticas
        self.lista.reset()     
        self.lista.calcAct(pag=self.numPag-1)
        self.pagebarBuilder(-1,False)

    def pagebarBuilder(self,dif,goc): #Contructor de la barra de página
        self.numPag=self.numPag + dif 
        self.pagina.clear_widgets()

        if(self.numPag>0):
            if (goc):
                self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='< Anterior',on_press=self.anteriorPagina))
            else:
                self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='< Anterior',on_press=self.antPag))
        else:
            self.pagina.add_widget(BoxLayout())
       
        self.pagina.add_widget(TitlePag(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50))))
        if(self.numPag + 1 < math.ceil(self.lista.totalDatos/50)):
            if (goc):
                self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='Siguiente >',on_press=self.siguientePagina))
            else:
                self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='Siguiente >',on_press=self.sigPag))
        else:
            self.pagina.add_widget(BoxLayout())

    def buscar(self,obj=None): #Función que filtra la base
        self.lista.reset()
        self.tablas = False
        self.numPag=0
        self.lista.build(entrada=self.campos,pag=0,filtros= self.listaFiltros,busqueda=self.filtros)
        filtro = "SELECT COUNT(`"+self.lista.index+"`) "+ self.lista.filtroWhere
        for x in self.base.execute(filtro):
                    for y in x:
                        self.lista.totalDatos=y
                        self.lista.totalDatos2=y
        self.pagebarBuilder(0,True)

    def buscar_gen(self,obj=None): #Función que filtra la base de forma general (busca en todos los campos)
        self.listaFiltros2 = self.listaFiltros
        self.filtros2 = self.filtros
        self.listaFiltros = []
        for field in self.df:
            self.listaFiltros.append(str(field))
        self.lista.reset()
        self.tablas = False
        self.numPag=0
        self.filtros = []
        for elemento in self.listaFiltros:
            self.filtros.append(self.busqueda_gen)
        self.lista.build(entrada=self.campos,pag=0,filtros= self.listaFiltros,busqueda=self.filtros,general=True)
        filtro = "SELECT COUNT(`"+self.lista.index+"`) "+ self.lista.filtroWhere
        for x in self.base.execute(filtro):
                    for y in x:
                        self.lista.totalDatos=y
                        self.lista.totalDatos2=y
        self.pagebarBuilder(0,True)
        self.listaFiltros = self.listaFiltros2
        self.filtros = self.filtros2
        self.pop.dismiss(obj)
                
    def perfil(self,obj):
        self.menuTitle=2
        self.menubarBuilder()        
        self.selectDatabase = False
        self.nuevaBase = False
        # self.toolbar.show = False 
        # self.toolbarHide(obj)
        self.toolbarBuilder()
        self.contenedor.stack.scroll_y=1
       

    def buscarpop(self,obj):

        self.busqueda_gen = TextInput(hint_text='Ingrese termino de busqueda',size_hint_y=None,height=60)
        botonesPop = BoxLayout(size_hint=(1, None),height=30,orientation='horizontal')
        self.pop = Popup(title='Busqueda rápida',
                content=BoxLayout(padding=(10,0),orientation='vertical'),
                title_align = 'center',
                title_size = '20',
                auto_dismiss=False,
                size_hint=(None, None), size=(350, 185))
        self.pop.content.add_widget(self.busqueda_gen)
        self.pop.content.add_widget(BoxLayout(size_hint=(1, None),height=15))
        botonesPop.add_widget(Button(text='Cancelar', font_size= 20,on_press=self.cancelPop))
        botonesPop.add_widget(Button(text='Buscar', background_color=(0.6,0.6,0.8),font_size= 20,on_press=self.buscar_gen))
        self.pop.content.add_widget(botonesPop)
        self.pop.open()  

    def salir(self,obj):
        botonesPop = BoxLayout(size_hint=(1, None),height=30,orientation='horizontal')
        self.pop = Popup(title='Cerrar sesión',
                content=BoxLayout(padding=(10,0),orientation='vertical'),
                title_align = 'center',
                title_size = '20',
                auto_dismiss=False,
                size_hint=(None, None), size=(350, 125))
        botonesPop.add_widget(Button(text='Continuar', font_size= 20,on_press=self.cancelPop))
        botonesPop.add_widget(Button(text='Cerrar', font_size= 20,on_press=self.cerrarSesion))
        self.pop.content.add_widget(botonesPop)
        self.pop.open()

    def cancelPop(self,obj):
        self.pop.dismiss(obj)

    def cerrarSesion(self,obj):
        self.pop.dismiss(obj)
        self.upApp.build(0)

    def error(self):
        botonesPop = BoxLayout(size_hint=(1, None),height=30,orientation='horizontal')
        self.pop = Popup(title='No se pudo crear la base, intentelo de nuevo usando un archivo con extensión xlsx',
                content=BoxLayout(padding=(10,0),orientation='vertical'),
                title_align = 'center',
                title_size = '20',
                auto_dismiss=False,
                size_hint=(None, None), size=(350, 160))
        botonesPop.add_widget(Button(text='Aceptar', font_size= 20,on_press=self.cancelPop))
        self.pop.content.add_widget(botonesPop)
        self.pop.open()

    def reset(self,obj):
        self.build()

def on_enter(instance, value):
    print('User pressed enter in', instance)

'''
=======================
Widgets complementarios
=======================
Clases separadores, botones y contenedores varios
'''

class BotonOpcion(Button):
    pass

class BotonOpcion2(Button):
    pass

class ButtonOption(ButtonBehavior,BoxLayout):
    g = StringProperty()
    c = BooleanProperty()
    def __init__(self,texto,select=False,**kwargs):
        super(ButtonOption, self).__init__(**kwargs)
        self.g = texto
        self.c = select

class ButtonMain(ButtonBehavior,BoxLayout):
    g = StringProperty()
    c = BooleanProperty()
    def __init__(self,texto,select=False,**kwargs):
        super(ButtonMain, self).__init__(**kwargs)
        self.g = texto
        self.c = select

class ButtonMain2(ButtonBehavior,BoxLayout):
    g = StringProperty()
    c = BooleanProperty()
    def __init__(self,texto,select=False,**kwargs):
        super(ButtonMain2, self).__init__(**kwargs)
        self.g = texto
        self.c = select

class ButtonAccept(ButtonBehavior,BoxLayout):
    g = StringProperty()
    def __init__(self,texto,title = '',input=0,**kwargs):
        super(ButtonAccept, self).__init__(**kwargs)
        self.g = texto
        self.input = input
        self.title = title
class ColorBox(BoxLayout):
    r = NumericProperty()
    g = NumericProperty()
    b = NumericProperty()
    def __init__(self,r=0,g=0,b=0):
        super(ColorBox, self).__init__()
        self.r = r
        self.g = g
        self.b = b

class Cuadro(BoxLayout):
    pass
class Color(BoxLayout):
    g = StringProperty()
    color = BooleanProperty()
    def __init__(self,texto,color=True):
        super(Color, self).__init__()
        self.g = texto
        self.color = color

class Divisor(BoxLayout):
    pass

class EstBox(BoxLayout):
    pass

class Exit(ButtonBehavior,Image,BoxLayout):
    def __init__(self,**kwargs):
        super(Exit, self).__init__(**kwargs)
        pass

class FilaPag(BoxLayout):
    r = NumericProperty()
    def __init__(self,r=20):
        super(FilaPag, self).__init__()
        self.r = r

class FilaTitulo(BoxLayout):
    r = NumericProperty()
    def __init__(self,r=20):
        super(FilaTitulo, self).__init__()
        self.r = r

class Fila3(BoxLayout):
    pass

class Info(BoxLayout):
    g = StringProperty()
    def __init__(self,texto):
        super(Info, self).__init__()
        self.g = texto

class MenuBar(BoxLayout):
    pass

class NewDocument(FloatLayout):
    doc = BooleanProperty()
    def __init__(self,aplicacion):
        super(NewDocument, self).__init__()
        self.aplicacion = aplicacion
        self.doc = False
        self.name = TextInput(size_hint=(.6, .05), pos_hint={'x':.2, 'y':.475})
        self.add_widget(Label(text='Nombre de la nueva base',color=(0.2,0.2,0.1),size_hint=(.6, .05), pos_hint={'x':.2, 'y':.55}))
        self.add_widget(self.name)
        self.add_widget(Button(text='Aceptar', size_hint=(.6, .05), pos_hint={'x':.2, 'y':.4},on_press=self.insertarBase))

    def insertarBase(self,obj):
        self.clear_widgets()
        self.doc = True
        self.aplicacion.subiendoBase = True
        self.aplicacion.nombreArchivo = self.name.text
        self.add_widget(Label(text='Arrastre un documento',color=(0.75,0.35,0.35),size_hint=(.6, .05), pos_hint={'x':.2, 'y':.475}))

class NewDocument2(FloatLayout):
    doc = BooleanProperty()
    def __init__(self,user):
        super(NewDocument2, self).__init__()
        self.contrasenas_manager = passw_manager('base')
        #self.name = TextInput(size_hint=(.6, .05), pos_hint={'x':.2, 'y':.475})
        
        self.add_widget(Label(text='Usuario:',halign='left',color=(0.2,0.2,0.1),size_hint=(.3, .1), pos_hint={'x':.1, 'y':.8},font_size=17,bold = True))
        self.add_widget(Label(text=self.contrasenas_manager.get_data(user)[1],halign='left',color=(0.2,0.2,0.1),size_hint=(.6, .1), pos_hint={'x':.3, 'y':.8},font_size=17))
        self.add_widget(Label(text='Nombre:',halign='left',color=(0.2,0.2,0.1),size_hint=(.3, .1), pos_hint={'x':.1, 'y':.65},font_size=17,bold = True))
        self.add_widget(Label(text=self.contrasenas_manager.get_data(user)[3],halign='left',color=(0.2,0.2,0.1),size_hint=(.6, .1), pos_hint={'x':.3, 'y':.65},font_size=17))
        self.add_widget(Label(text='Apellido:',halign='left',color=(0.2,0.2,0.1),size_hint=(.3, .1), pos_hint={'x':.1, 'y':.50},font_size=17,bold = True))
        self.add_widget(Label(text=self.contrasenas_manager.get_data(user)[4],halign='left',color=(0.2,0.2,0.1),size_hint=(.6, .1), pos_hint={'x':.3, 'y':.50},font_size=17))
        self.add_widget(Label(text='Correo:',halign='left',color=(0.2,0.2,0.1),size_hint=(.3, .1), pos_hint={'x':.1, 'y':.35},font_size=17,bold = True))
        self.add_widget(Label(text=self.contrasenas_manager.get_data(user)[5],halign='left',color=(0.2,0.2,0.1),size_hint=(.6, .1), pos_hint={'x':.3, 'y':.35},font_size=17))
    
    #     self.add_widget(self.name)
    #     self.add_widget(Button(text='Aceptar', size_hint=(.6, .05), pos_hint={'x':.2, 'y':.4},on_press=self.insertarBase))

    # def insertarBase(self,obj):
    #     self.clear_widgets()
    #     self.doc = True
    #     self.aplicacion.subiendoBase = True
    #     self.aplicacion.nombreArchivo = self.name.text
    #     self.add_widget(Label(text='Arrastre un documento',color=(0.75,0.35,0.35),size_hint=(.6, .05), pos_hint={'x':.2, 'y':.475}))
        

class OcultarBarra(FloatLayout):
    pass

class PiePagina(BoxLayout):
    g = StringProperty()
    def __init__(self,texto):
        super(PiePagina, self).__init__()
        self.g = texto

class Res(ButtonBehavior,Image,BoxLayout):
    def __init__(self,**kwargs):
        super(Res, self).__init__(**kwargs)
        pass

class Search(ButtonBehavior,Image,BoxLayout):
    def __init__(self,**kwargs):
        super(Search, self).__init__(**kwargs)
        pass

class Separador2(BoxLayout):
    pass

class SeparadorH(BoxLayout):
    pass

class Separador(BoxLayout):
    pass

#Widget que define los cuadros con los titulos de columna de las bases de datos
class TitleField(BoxLayout):
    g = StringProperty()
    def __init__(self,texto):
        super(TitleField, self).__init__()
        self.g = texto

#Widget que define los cuadros con los titulos de los filtros
class TitleFilter(BoxLayout):
    g = StringProperty()
    filtro = BooleanProperty()
    def __init__(self,texto,filtro = True):
        super(TitleFilter, self).__init__()
        self.g = texto
        self.filtro =filtro

class Title(BoxLayout):
    g = StringProperty()
    bold = BooleanProperty()
    def __init__(self,texto,bold=False,filtro = True,**kwargs):
        super(Title, self).__init__(**kwargs)
        self.g = texto
        self.bold = bold

class Title3(BoxLayout):
    g = StringProperty()
    bold = BooleanProperty()
    def __init__(self,texto,bold=False,filtro = True,**kwargs):
        super(Title3, self).__init__(**kwargs)
        self.g = texto
        self.bold = bold

class Title2(BoxLayout):
    g = StringProperty()
    def __init__(self,texto,**kwargs):
        super(Title2, self).__init__(**kwargs)
        self.g = texto

class TitlePag(BoxLayout):
    g = StringProperty()
    def __init__(self,texto):
        super(TitlePag, self).__init__()
        self.g = texto

class ToolbarTitle(BoxLayout):
    pass

class ToolbarTitleText(BoxLayout):
    g = StringProperty()
    r = NumericProperty()
    def __init__(self,texto,r=20,**kwargs):
        super(ToolbarTitleText, self).__init__(**kwargs)
        self.g = texto
        self.r = r

class ToolbarText(ButtonBehavior,BoxLayout):
    g = StringProperty()
    main = BooleanProperty()
    r = NumericProperty()
    def __init__(self,texto,main=False,r=16,**kwargs):
        super(ToolbarText, self).__init__(**kwargs)
        self.g = texto
        self.main = main
        self.r = r

class Toolbar(BoxLayout):
    show = BooleanProperty()
    def __init__(self):
        super(Toolbar, self).__init__()
        self.show=True

class ToolbarSub(ScrollView):
    show = BooleanProperty()
    def __init__(self):
        super(ToolbarSub, self).__init__()
        self.show=True
        self.build()

    def build(self):
        self.stack=ToolbarContaner()
        self.stack.bind(minimum_height=self.stack.setter('height'))
        #self.add_widget(self.stack)

class ToolbarContaner(StackLayout):
    pass

class ToolbarShow(ButtonBehavior,Image,BoxLayout):
     def __init__(self,**kwargs):
        super(ToolbarShow, self).__init__(**kwargs)