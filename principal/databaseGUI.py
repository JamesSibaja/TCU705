from lib import *
from dataViewer import DataViewer
SubiendoArchivo = False

'''
================
Widget principal
================
Widget asociado a la totalidad de la ventana donde se presenta la interfaz de la aplicación
'''
#Widget principal
class DatabaseGUI(BoxLayout): 
    def __init__(self,base,table,aplicacion,edit):
        super(DatabaseGUI, self).__init__()

        self.conexion = sqlite3.connect(base)
        self.base = self.conexion.cursor()
        self.aplicacion = aplicacion
        self.table = table 
        self.edit = edit 
        self.base.execute("SELECT Columns From `database` WHERE Database = '"+self.table+"'")
        self.columns = self.base.fetchall()[0][0]
        print(self.columns)
        #self.base.execute("ALTER TABLE `"+self.table+"` ADD PDF TEXT")
        self.build()
        #self.df = dfpop

    #Constructor de la ventana principal
    def build(self):
        self.clear_widgets()
        self.numPag = 0
        self.MenuMain = ToolbarShow(on_press=self.toolbarHide)
        #self.MenuMain = ToolbarTitle()
        self.tablas = False
        self.select = False
        self.infoTextBox =[]
        self.newColumnName = ''
        self.menuFiltro = False
        self.editPDF = False
        self.estadisticas = False
        self.filtroCalc = False
        self.editar = False
        self.datoCalc = ""
        self.menuTitle =0
        self.toolbar = Toolbar()
        self.contenedor = ToolbarSub() 
        self.listaFiltros =[]
        self.listaFiltros2 =[]
        self.filaTitulo = FilaTitulo()
        self.pagina = FilaPag()
        self.camposOpcion = []
        self.filtrosOpcion = []
        self.filtros = []
        self.filtros2 = []
        self.campos = []
        self.nombres = list(map(lambda x: x[0], self.base.execute("select * from `"+ self.table+"`").description))
        self.index = self.nombres[0]
        self.nombres.pop(0)
        contCampos=0
        for selectField in self.nombres:
            if contCampos < len(self.columns):
                if self.columns[contCampos]=='1':
                    self.camposOpcion.append(True)
                    self.campos.append(str(selectField))
                else:
                    self.camposOpcion.append(False)
            else:
                self.columns = self.columns + '0'
                self.camposOpcion.append(False)
            self.filtrosOpcion.append(False)
            contCampos+=1
        self.lista = DataViewer(index=self.index,entrada=self.campos,base = self.base,table = self.table,aplicacion=self.aplicacion,conexion = self.conexion,pag = self.numPag)
        self.pagina.add_widget(BoxLayout())
        self.pagina.add_widget(TitlePag(texto='Pág '+str(self.numPag+1) +' de '+str(math.ceil(self.lista.totalDatos/50))))
        self.pagina.add_widget(Button(bold=True,background_color =(0,0,0,0),text='Siguiente >',on_press=self.siguientePagina))
        self.contenedorLista = BoxLayout(padding = 10,orientation= 'vertical')
        for selectField in self.campos:
            self.filaTitulo.add_widget(TitleField(selectField))
        self.palabrasBuscadas={}
        self.nuevoFiltro = False
        self.newEst = False
        self.cambiarCampo = False
        self.pantalla = BoxLayout(orientation='horizontal')

        #Se crea la barra de Menú y barra de herramientas
        self.barraMenu = MenuBar()
        self.submitOptions = []
        self.submitOptions.append(ToolbarText(texto = 'Ver',on_press=self.volverMenu))
        if self.edit:
            self.submitOptions.append(ToolbarText(texto = 'Editar',on_press=self.editarMenu))
        else:
            self.submitOptions.append(ToolbarText2(texto = 'Editar'))
        self.submitOptions.append(ToolbarText(texto = 'Columnas',on_press=self.nuevoCampo))#
        self.submitOptions.append(ToolbarText(texto = 'Filtro',on_press=self.nuevoInicio))#
        self.submitOptions.append(ToolbarText(texto = 'Estadísticas',on_press=self.nuevoEst))#
        self.submitOptions.append(ToolbarText(texto = 'Ajustes'))
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
        # self.MenuMain.clear_widgets()
        # self.MenuMain.add_widget(ToolbarShow(on_press=self.toolbarHide))
       # self.MenuMain.add_widget(ToolbarTitleText(texto= self.table))
        
        contOpt = 0
        for option in self.submitOptions:
            if(self.menuTitle==contOpt):
                option.main = True
            contOpt = contOpt + 1

        self.barraMenu.add_widget(self.MenuMain)
        self.barraMenu.add_widget(SeparadorH())     
        contOpt = 0
        for option in self.submitOptions:
            self.barraMenu.add_widget(option)
            if not (self.menuTitle==contOpt):
                option.main = False
            contOpt = contOpt + 1        
 
    #Constructor de la barra de herramientas
    def toolbarBuilder(self):   
        self.contenedor.scroll_y=1
        self.contenedor.clear_widgets()
        self.subBoton.clear_widgets()
        self.contenedor.build()
        if self.nuevoFiltro or self.cambiarCampo or self.newEst:
            #Si se encuentra en el menú de columnas o se abre por primera vez el
            #menú de estadistica o el de filtro
            contTexto =0
            for filtro in self.filtros:
                self.palabrasBuscadas.update({self.listaFiltros[contTexto]:filtro.text})
                contTexto += 1
            self.contenedor.stack.clear_widgets()
            self.filtrosBotones = []
            contBotones =0

            if(self.cambiarCampo):
                self.contenedor.stack.add_widget(Title("Mostrar:"))                
                
            if(self.nuevoFiltro):
                self.contenedor.stack.add_widget(Title("Filtrar por:"))

            if(self.newEst):
                self.contenedor.stack.add_widget(Title("Escoger Datos:"))
                self.contenedor.stack.add_widget(Separador())

            for posibleFiltro in self.nombres:
                if(self.cambiarCampo):
                    if (self.camposOpcion[contBotones]):
                        self.newBoton= ButtonOption(texto = str(posibleFiltro),select= True, on_press=self.nuevoFinal)
                    else:
                        self.newBoton= ButtonOption(texto = str(posibleFiltro),on_press=self.nuevoFinal)
                if(self.nuevoFiltro):
                    if (self.filtrosOpcion[contBotones]):
                        self.newBoton= ButtonOption(texto = str(posibleFiltro),select= True, on_press=self.nuevoFinal)
                    else:
                        self.newBoton= ButtonOption(texto = str(posibleFiltro),on_press=self.nuevoFinal)
                if(self.newEst):
                    self.newBoton= ButtonMain(texto = str(posibleFiltro),on_press=self.newFinal)                    
                self.filtrosBotones.append(self.newBoton)
                contBotones +=1
            n=0
            for botonFiltro in self.filtrosBotones:
                self.contenedor.stack.add_widget(self.filtrosBotones[n])
                n+=1
            if(not self.newEst):
                self.contenedor.stack.add_widget(Separador2())
                self.subBoton.add_widget(ButtonAccept(texto = 'Aceptar',on_press=self.aceptarCambios))
                
        else:            
            #Si se encuentra en el menú de filtros
            if self.menuFiltro:                
                self.contenedor.stack.clear_widgets()
                self.filtros = []
                self.menuFiltro = False
                if self.estadisticas:
                    self.submit = ButtonAccept(texto = 'Usar',on_press=self.usarFiltro)
                else:
                    self.submit = ButtonAccept(texto = 'Filtrar',on_press=self.buscar)

                for filtro in self.listaFiltros:
                    if (self.palabrasBuscadas.get(filtro) != None):
                        self.filtros.append(TextInput(text=str(self.palabrasBuscadas[filtro]),size_hint_y=None,height=45))
                    else:
                        self.filtros.append(TextInput(text='',size_hint_y=None,height=45))
                n=0
                self.contenedor.stack.title = ToolbarTitle(on_press=self.volverMenu)
                self.contenedor.stack.add_widget(Separador2())
                self.contenedor.stack.add_widget(ButtonMain(texto = 'Editar Filtros',on_press=self.editarFiltros))
                self.contenedor.stack.add_widget(ButtonMain(texto = 'Limpiar Filtros',on_press=self.limpiar))
                self.contenedor.stack.add_widget(Separador2())
                for filtro in self.filtros:            
                    self.contenedor.stack.add_widget(Title(texto=self.listaFiltros[n]+':'))
                    self.contenedor.stack.add_widget(self.filtros[n])
                    n+=1
                if n > 0:
                    self.contenedor.stack.add_widget(Separador())
                    self.subBoton.add_widget(self.submit)
            else:
                #Si se encuentra en el menú de estadistica
                if self.estadisticas:
                    self.contenedor.stack.clear_widgets()
                    self.contenedor.stack.title = ToolbarTitle(on_press=self.volverMenu)
                    self.contenedor.stack.title.add_widget(ToolbarText("Estadísticas"))
                    self.contenedor.box = EstBox()
                    self.contenedor.box.add_widget(Title("Filtro"))
                    if self.filtroCalc:
                        self.contenedor.box.add_widget(BotonOpcion(text = 'Usar',background_color =(0, 0.81, 0.59, 1),on_press=self.abFiltro))
                        self.botonFiltro = BotonOpcion(background_color =(0.85,0.85,0.85),color=(0.85,0.85,0.85),disabled =False,background_disabled_normal='',text = 'Filtros',on_press=self.nuevoInicio)
                    else:
                        self.contenedor.box.add_widget(BotonOpcion(text = 'No usar',background_color =(0.8,0, 0.1, 1),on_press=self.abFiltro))
                        self.botonFiltro = BotonOpcion(background_color =(0.85,0.85,0.85),color=(0.85,0.85,0.85),disabled =True,background_disabled_normal='',text = 'Filtros',on_press=self.nuevoInicio2)
                   
                    self.contenedor.box.add_widget(self.botonFiltro)
                    self.contenedor.stack.add_widget(self.contenedor.box)
                    self.contenedor.stack.add_widget(Separador2())
                    self.contenedor.stack.add_widget(Title("Dato a calcular:"))
                    self.contenedor.stack.add_widget(BotonOpcion(text = self.datoCalc,on_press=self.editarDatos))
                    self.contenedor.stack.add_widget(Separador())
                    self.contenedor.stack.add_widget(ButtonAccept(texto = 'Calcular',on_press=self.calcular))
                    self.contenedor.stack.add_widget(Separador())
                    self.subBoton.add_widget(ButtonAccept(texto = 'Volver',on_press=self.usarFiltro))
              
                else:
                    #Si se encuentra en el menú de ver o el de editar
                    self.contenedor.stack.add_widget(Title3("Ingrese termino de busqueda"))
                    self.busqueda_gen = TextInput(text='',size_hint_y=None,height=45)
                    self.contenedor.stack.add_widget(self.busqueda_gen)
                    self.contenedor.stack.add_widget(Separador())
                    self.contenedor.stack.add_widget(ButtonAccept(texto = 'Buscar',on_press=self.buscar_gen))
                    self.contenedor.stack.add_widget(Separador2())   
                    #self.contenedor.stack.add_widget(Separador2())
                    if self.editar:
                        self.contenedor.stack.add_widget(ButtonMain(texto = 'Agregar columna',on_press=self.nuevaColumna))
                    cont = -1
                    self.infoTextBo=[]
                    if self.select:         
                        self.contenedor.stack.add_widget(Title2('Datos')) 
                        for lista in self.lista.information:
                            for text in lista:
                              
                                if cont != -1:
                                    self.contenedor.stack.add_widget(Title(texto=self.nombres[cont] + ":",bold = True))
                                    if self.editar:
                                        self.infoTextBox.append(TextInput(text=str(text),size_hint_y=None,height=70,background_color=(0.9,0.9,0.9,1)))
                                    else:
                                        self.infoTextBox.append(TextInput(text=str(text),size_hint_y=None,height=70,background_color=(0.85,0.85,0.85,0)))
                                    self.contenedor.stack.add_widget(self.infoTextBox[len(self.infoTextBox)-1])
                                   
                                    if self.editar:
                                        self.contenedor.stack.add_widget(Separador())
                                        self.contenedor.stack.add_widget(ButtonAccept(texto = 'Editar',title=self.nombres[cont],input=len(self.infoTextBox)-1,on_press=self.editarCampo))
                                cont = cont + 1
                        self.contenedor.stack.add_widget(Separador())
                        self.contenedor.stack.add_widget(Title2('')) 

        self.contenedor.add_widget(self.contenedor.stack)

    def editarCampo(self,obj): #Función que cambia las columnas que se muestran*
        filtro = "UPDATE `"+self.table+"` SET `"+ obj.title +"` = '"+ self.infoTextBox[obj.input].text +"' WHERE `" + self.index + "` = '" + str(self.lista.id) +"'"
        print(filtro)
        self.base.execute(filtro)
        self.conexion.commit()
        self.buscar()

    def volverMenu(self,obj): #Función de la opción del menu ver
        self.menuTitle=0
        self.menubarBuilder()
        self.editar = False
        self.nuevoFiltro = False
        self.menuFiltro = False
        self.cambiarCampo = False
        self.estadisticas = False
        self.nuevoFiltro = False
        self.newEst = False 
        self.lista.editar = False
        self.lista.reset()
        self.lista.build(entrada=self.campos,pag=self.numPag,filtros= self.listaFiltros,busqueda=self.filtros)
        self.toolbarBuilder()

    def editarMenu(self,obj): #Función de la opción del menu editar
        self.menuTitle=1
        self.editar = True
        self.menubarBuilder()
        self.nuevoFiltro = False
        self.menuFiltro = False
        self.cambiarCampo = False
        self.estadisticas = False
        self.nuevoFiltro = False
        self.newEst = False
        self.lista.editar = True
        self.lista.reset()
        self.lista.build(entrada=self.campos,pag=self.numPag,filtros= self.listaFiltros,busqueda=self.filtros)
        self.toolbarBuilder()

    #Habilitar la opción de usar filtro en estadistica
    def abFiltro(self,obj):
        self.filtroCalc = not self.filtroCalc
        if self.filtroCalc:
            obj.background_color =(0, 0.81, 0.59, 1)
            obj.text = "Usar"
            self.botonFiltro.disabled = False
        else:
            obj.background_color =(0.8,0, 0.1, 1)
            self.botonFiltro.disabled = True
            obj.text = "No usar"

    def editarDatos(self,obj): #Escoger dato de referencia para clacular estadisticas
        self.newEst = True
        self.toolbarBuilder()

    def editarFiltros(self,obj):  #Escoger que filtros se pueden usar
        self.nuevoFiltro = True
        self.toolbarBuilder()

    def limpiar(self,obj): #Quitar todos los filtros
        self.listaFiltros = []
        self.filtros = []
        contFiltro = 0
        for field in self.nombres:            
            self.filtrosOpcion[contFiltro]  = False
            contFiltro += 1

        self.menuFiltro = True
        self.cambiarCampo = False
        self.nuevoFiltro = False
        self.newEst = False
        
        self.toolbarBuilder()
        self.buscar()

    def newFinal(self,obj):
        self.datoCalc = obj.g
        self.cambiarCampo = False
        self.nuevoFiltro = False
        self.newEst = False
        self.estadisticas = True
        self.toolbarBuilder()

    def calcular(self,obj): #Calcular estadísticas con todas la opciones escogidas
        self.lista.reset()
        self.tablas=True
        self.numPag=0   
        self.lista.reset()    
        self.lista.calc(self.datoCalc,self.filtroCalc)
        self.pagebarBuilder(0,False)  
        
        self.filaTitulo.clear_widgets()
        self.filaTitulo.add_widget(TitleField(self.datoCalc))
        self.filaTitulo.add_widget(TitleField('Cantidad'))
        self.filaTitulo.add_widget(TitleField('Porcentaje'))

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

    def cambiarColumnas(self): #Actualiza las columnas según las opciones seleccionadas
        self.lista.reset()
        self.campos=[]
        contColum = 0
        for field in self.nombres:
            if(self.camposOpcion[contColum]):
                self.campos.append(str(field))
            contColum += 1
        self.filaTitulo.clear_widgets()
        for selectField in self.campos:
            self.filaTitulo.add_widget(TitleField(selectField.rstrip('.d')))
        self.numPag=0   
        self.lista.reset()
        self.lista.build(entrada=self.campos,filtros= self.listaFiltros,pag=self.numPag,busqueda=self.filtros) 
        self.pagebarBuilder(0,True) 
        if self.tablas:
            filtro = "SELECT COUNT(`"+self.lista.index+"`) "+ self.lista.filtroWhere
            self.base.execute(filtro)
            self.lista.totalDatos = self.base.fetchall()[0][0]
        self.tablas = False

    def buscar(self,obj=None): #Función que filtra la base
        self.lista.reset()
        self.tablas = False
        self.numPag=0
        self.lista.build(entrada=self.campos,pag=0,filtros= self.listaFiltros,busqueda=self.filtros)
        filtro = "SELECT COUNT(`"+self.lista.index+"`) "+ self.lista.filtroWhere
        self.base.execute(filtro)
        self.lista.totalDatos = self.base.fetchall()[0][0]
        self.lista.totalDatos2 = self.base.fetchall()[0][0]
        self.pagebarBuilder(0,True)

    def buscar_gen(self,obj=None): #Función que filtra la base de forma general (busca en todos los campos)
        self.listaFiltros2 = self.listaFiltros
        self.filtros2 = self.filtros
        self.listaFiltros = []
        for field in self.nombres:
            self.listaFiltros.append(str(field))
        self.lista.reset()
        self.tablas = False
        self.numPag=0
        self.filtros = []
        for elemento in self.listaFiltros:
            self.filtros.append(self.busqueda_gen)
        self.lista.build(entrada=self.campos,pag=0,filtros= self.listaFiltros,busqueda=self.filtros,general=True)
        filtro = "SELECT COUNT(`"+self.lista.index+"`) "+ self.lista.filtroWhere
        self.base.execute(filtro)
        self.lista.totalDatos = self.base.fetchall()[0][0]
        self.lista.totalDatos2 = self.base.fetchall()[0][0]
        self.pagebarBuilder(0,True)
        self.listaFiltros = self.listaFiltros2
        self.filtros = self.filtros2
                
    def nuevoInicio(self,obj):
        self.menuTitle=3
        self.menubarBuilder()
        self.newEst = False

        self.cambiarCampo = False
        self.estadisticas = False
        self.nuevoFiltro = False
      
        if len(self.listaFiltros) == 0:
            self.nuevoFiltro = True
        else:
            self.menuFiltro = True

        self.contenedor.show = False
        self.toolbar.show = False
        self.toolbarHide(obj)
        self.contenedor.stack.scroll_y=1

    def nuevoInicio2(self,obj):
        self.menuTitle=3
        self.menubarBuilder()
        self.newEst = False

        self.cambiarCampo = False
        self.nuevoFiltro = False
      
        if len(self.listaFiltros) == 0:
            self.nuevoFiltro = True
        else:
            self.menuFiltro = True

        self.contenedor.show = False
        self.toolbar.show = False
        self.toolbarHide(obj)
        self.contenedor.stack.scroll_y=1

    def nuevoEst(self,obj):
        self.menuTitle=4
        self.menubarBuilder()
        self.nuevoFiltro = False
        self.menuFiltro = False
        self.cambiarCampo = False
        self.estadisticas = False
        self.nuevoFiltro = False

        if self.datoCalc == "":
            self.newEst = True
        else:
            self.estadisticas = True
        self.contenedor.show = False
        self.toolbar.show = False
        self.toolbarHide(obj)
        self.contenedor.stack.scroll_y=1

    def nuevoFinal(self,obj):
        if (self.nuevoFiltro):
            contFiltro = 0
            for field in self.nombres:
                if (field == obj.g):
                    self.filtrosOpcion[contFiltro]  = not self.filtrosOpcion[contFiltro]
                contFiltro += 1
            self.toolbarBuilder()

        if (self.cambiarCampo):
            contTitulo = 0
            for field in self.nombres:
                if(field == obj.g):
                    self.camposOpcion[contTitulo] = not self.camposOpcion[contTitulo]
                    if self.camposOpcion[contTitulo]:
                        self.columns = self.columns[:contTitulo] + '1' + self.columns[contTitulo+1:]
                    else:
                        self.columns = self.columns[:contTitulo] + '0' + self.columns[contTitulo+1:]
                    obj.c = not obj.c
                contTitulo += 1 

    def usarFiltro(self,obj=None):       
        self.lista.reset()
        self.tablas = False
        self.numPag=0
        self.lista.reset()
        self.lista.build(entrada=self.campos,pag=0,filtros= self.listaFiltros,busqueda=self.filtros)
        self.pagebarBuilder(0,True)

        self.menuFiltro = False
       
        self.cambiarCampo = False
        self.nuevoFiltro = False
        self.newEst = False
        filtro = "SELECT COUNT(`"+self.lista.index+"`) "+ self.lista.filtroWhere
        self.base.execute(filtro)
        self.lista.totalDatos = self.base.fetchall()[0][0]
        self.lista.totalDatos2 = self.base.fetchall()[0][0]
        if self.menuTitle==4:
            self.volverMenu(obj)
        else:
            self.toolbarBuilder()
        self.menuTitle=4
        self.menubarBuilder()
            
    def aceptarCambios(self,obj):
        if(self.menuFiltro):
            self.nuevoFiltro = False
        self.menuFiltro = False
        if(self.cambiarCampo):
            self.cambiarColumnas()
        if(self.nuevoFiltro):
            self.menuFiltro = True
            contFiltro = 0
            self.listaFiltros = []
            for field in self.nombres:
                if (self.filtrosOpcion[contFiltro]):
                    self.listaFiltros.append(str(field))
                contFiltro += 1
        if self.cambiarCampo:
            print(self.columns)
            filtro = "UPDATE `database` SET `Columns` = '"+ self.columns +"' WHERE `Database` = '" + self.table +"'"
            print(filtro)
            self.base.execute(filtro)
            self.conexion.commit()
            self.volverMenu(obj)
            
        else:
            self.cambiarCampo = False
            self.nuevoFiltro = False
            self.newEst = False
            self.toolbarBuilder()

    def nuevoCampo(self,obj):
        self.menuTitle=2
        self.menubarBuilder()
        self.cambiarCampo = True
        self.nuevoFiltro = False
        self.menuFiltro = False
        self.estadisticas = False
        self.nuevoFiltro = False
        self.newEst = False 
        self.contenedor.show = False
        self.toolbar.show = False
        self.toolbarHide(obj)
        self.contenedor.stack.scroll_y=1

    def nuevaColumna(self,obj):
        self.newColumnName = TextInput(size_hint=(1, None),height=35,hint_text="Nombre de columna")
        self.documentos = ToggleButton(size_hint=(1, None),height=30,text='Campo de documento')
        botonesPop = BoxLayout(size_hint=(1, None),height=30,orientation='horizontal')
        self.pop = Popup(title='Agregar un nuevo campo a la base',
                content=BoxLayout(padding=(10,0),orientation='vertical'),
                title_align = 'center',
                title_size = '20',
                auto_dismiss=False,
                size_hint=(None, None), size=(350, 200))
        self.pop.content.add_widget(BoxLayout(size_hint=(1, None),height=10))
        self.pop.content.add_widget(self.newColumnName)
        self.pop.content.add_widget(BoxLayout(size_hint=(1, None),height=10))
        self.pop.content.add_widget(self.documentos)
        self.pop.content.add_widget(BoxLayout(size_hint=(1, 1)))
        botonesPop.add_widget(Button(text='Cancelar', background_color=(0.8,0.6,0.6),font_size= 20,on_press=self.cancelPop))
        botonesPop.add_widget(Button(text='Crear', background_color=(0.6,0.8,0.6),font_size= 20,on_press=self.nuevaColumnaCrear))
        self.pop.content.add_widget(botonesPop)
        self.pop.open()

    def cancelPop(self,obj):
        self.pop.dismiss(obj)

    def nuevaColumnaCrear(self,obj):
        strName = str(self.newColumnName.text)
        print(strName)
        content = Button(text='Aceptar', size_hint=(0.5, 0.5),font_size= 20)
        self.pop.dismiss(obj)
        if strName.strip() == '':
            pop = Popup(title='El nombre de campo no es valido',
                    content=content,
                    title_align = 'center',
                    title_size = '20',
                    auto_dismiss=False,
                    size_hint=(None, None), size=(350, 200))
            content.bind(on_press=pop.dismiss)
            pop.open()
        else:
            if self.documentos.state == 'down':
                    strName = strName + ".d"
            if strName in self.nombres:
                pop = Popup(title='Ya exite un campo con el nombre: '+str(self.newColumnName.text),
                    content=content,
                    title_align = 'center',
                    title_size = '20',
                    auto_dismiss=False,
                    size_hint=(None, None), size=(350, 200))
                content.bind(on_press=pop.dismiss)
                pop.open()
            else:        
                self.nombres.append(strName)
                self.camposOpcion.append(False)
                self.base.execute("ALTER TABLE `"+self.table+"` ADD `"+strName+"` TEXT")

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

class OcultarBarra(FloatLayout):
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
    def __init__(self,texto,bold=False,filtro = True):
        super(Title, self).__init__()
        self.g = texto
        self.bold = bold

class Title3(BoxLayout):
    g = StringProperty()
    bold = BooleanProperty()
    def __init__(self,texto,bold=False,filtro = True):
        super(Title3, self).__init__()
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
    def __init__(self,texto,r=16,**kwargs):
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

class ToolbarText2(ButtonBehavior,BoxLayout):
    g = StringProperty()
    main = BooleanProperty()
    r = NumericProperty()
    def __init__(self,texto,main=False,r=16,**kwargs):
        super(ToolbarText2, self).__init__(**kwargs)
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

class ToolbarContaner(StackLayout):
    pass

class ToolbarShow(ButtonBehavior,Image,BoxLayout):
     def __init__(self,**kwargs):
        super(ToolbarShow, self).__init__(**kwargs)