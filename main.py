import sys
import typing
import os,shutil

from PyQt6 import QtCore, QtWidgets, uic, QtGui
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QFileSystemModel

import encriptado as crypt
import buscarArchivos as buscar

#Clase para la ventana de edición de archivo
class ventanaArchivo(QtWidgets.QDialog):
    
    def __init__(self,ruta, textoArchivo="") -> None:
        super(ventanaArchivo,self).__init__()
        
        #Cargar la interfaz de usuario desde un archivo .ui
        self.ui_path = os.path.dirname(__file__)
        uic.load_ui.loadUi ("VentanaArchivo.ui", self)
        
        #Obtener referencias a los Widgets
        self.botonBorrar = self.findChild(QtWidgets.QPushButton, "btnBorrarTexto")
        self.botonGuardar = self.findChild(QtWidgets.QPushButton, "btnGuardarArchivo")
        self.txtCampo = self.findChild(QtWidgets.QPlainTextEdit, "txtCampoTexto")
        
        #Conectar funciones a botones
        self.botonBorrar.clicked.connect(self.borrar_texto)
        self.botonGuardar.clicked.connect(self.guardarArchivo)
        
        #Ruta de archivo a editar
        self.rutaArchivo = ruta
        
        #Establecer el texto inicial del campo de edición
        self.txtCampo.setPlainText(textoArchivo)
        
    def guardarArchivo(self):
        try:
            #Abrir el archivo en modo write para sobreescribir en él si hay cambios nuevos
            fichero=open(self.rutaArchivo,'w')
            txt = self.txtCampo.toPlainText() #+ "\r"
            fichero.write(txt)
            fichero.close()
        except OSError:
                print("Error al abrir archivo")
        
    def borrar_texto(self):
        self.txtCampo.clear()

#Clase para la ventana de explorador de archivos
class ExploradorDeArchivos(QtWidgets.QDialog):
    def __init__(self) -> None:
        super(ExploradorDeArchivos,self).__init__()
        uic.load_ui.loadUi("UI_Explorador.ui", self)
        #Creamos una ruta raiz que queremos mostrar en nuestra aplicación
        self.ruta= os.path.dirname(__file__) + '\\Raiz'
        
        #Configuración inical del explorador 
        self.explorador_rapido()
        self.explorador_secundario()
        self.arbol.clicked.connect(self.actualizar_explorador_secundario)
        self.arbol2.doubleClicked.connect(self.abrir_directorio)
        self.texto = None
        
        #Flag para inidicar si se está creando un archivo //
        self.creating_file= False
        
        #Conectar botones a funciones
        self.btnFolder= self.findChild(QtWidgets.QPushButton, "btnCrearCarpeta")
        self.btnFolder.clicked.connect(self.abrir_ventana)
        self.btnFolder= self.findChild(QtWidgets.QPushButton, "btnCrearArchivo")
        self.btnFolder.clicked.connect(self.abrir_ventana_archivo)
        self.btnReini = self.findChild(QtWidgets.QPushButton,"btnReiniciar")
        self.btnReini.clicked.connect(self.reiniciar_vista)
        self.btnBuscar = self.findChild(QtWidgets.QPushButton,"btnBuscar")
        self.btnBuscar.clicked.connect(self.encontrar)
        self.txtBuscar = self.findChild(QtWidgets.QLineEdit,"txtBusqueda")

        #Varibles del encriptado de archivos
        self.FIRMA = b"ENCRIPTADO" # AGREGAR ESTO
        
        self.arbol2.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu) #Establecer señal de click derecho
        self.arbol2.customContextMenuRequested.connect(self.verificar_menu_directorio) #Mostrar el menu con click derecho
        #self.arbol.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu) #Establecer señal de click derecho
        #self.arbol.customContextMenuRequested.connect(self.mostrar_menu) #Mostrar el menu con click derecho

        
        
    #Función para configurar el explorador rápido (árbol izquierdo)
    def explorador_rapido(self):
        #Creamos una variable Modelo en la cual vamos a instanciar la clase QFileSystemModel que
        #proporcional un modelo de datos para archvios locales
        modelo1 = QFileSystemModel()
        #Creamos una variable de ruta para guardar la ruta raíz que queremos mostrar en la ventana
        
        #Establecemos la ruta raiz para mostrar en el QTreeView
        modelo1.setRootPath(self.ruta)
        
        self.arbol = self.findChild(QtWidgets.QTreeView, "arbol2")
        self.arbol.setModel(modelo1)
        self.arbol.setRootIndex(modelo1.index(self.ruta))
        self.arbol.hideColumn(1)
        self.arbol.hideColumn(2)
        self.arbol.hideColumn(3)
        self.filtro(modelo1,"")
    
    #Función para configurar el explorador secundario (árbol derecho)     
    def explorador_secundario(self, ruta_2 = os.path.dirname(__file__) + '\\Raiz'):
        #Creamos una variable Modelo en la cual vamos a instanciar la clase QFileSystemModel que
        #proporcional un modelo de datos para archvios locales
        self.modelo2 = QFileSystemModel()
        #Creamos una variable de ruta para guardar la ruta raíz que queremos mostrar en la ventana
        
        #Establecemos la ruta raiz para mostrar en el QTreeView
        self.modelo2.setRootPath(ruta_2)
        
        #Incializamos una variable de tipo QTreeView que se encuentra en al archivo .ui
        self.arbol2 = self.findChild(QtWidgets.QTreeView, "treeArbol")
        
        #SetModel() es un método heredado de la clase "QAbstractItemModel Class" que proporciona una clase
        #abstracta para las clases de modelos de elemetnos. Como QTreeview es un elemento que requiere
        #items, podemos manipular su modelo de intem con la función setModel()
        self.arbol2.setModel(self.modelo2)
        self.arbol2.setColumnWidth(0, 250) #Expando la columna de nombre de archivos/directorios
        #Con setRootIndex() se establece el elemento de ruta raiz: https://doc.qt.io/qt-6/qabstractitemview.html#setRootIndex
        #Con el método index() de la clase QFileSystemModel retornar el item del modelo con la ruta establecida como ruta raíz
        self.arbol2.setRootIndex(self.modelo2.index(ruta_2))
        #Cuadro de texto con directorio
        self.txtDir = self.findChild(QtWidgets.QLineEdit, "txtDirectorio")
        self.txtDir.setText(ruta_2) #Inicialmente se mostrará la ruta raiz en la pantalla
        self.filtro(self.modelo2,"*.txt")#
        
        #self.arbol2.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu) #Establecer señal de click derecho
        #self.arbol2.customContextMenuRequested.connect(self.mostrar_menu) #Mostrar el menu con click derecho

    #Función para actualizar el explorador secundario al hacer click en una carpeta    
    def actualizar_explorador_secundario(self, index):
        ruta_nueva= self.modelo2.filePath(index)
        self.explorador_secundario(ruta_nueva)

    #Función que reinicia la vista a la ruta raíz | Llama al explorador secundario con la ruta raíz    
    def reiniciar_vista(self):
        self.explorador_secundario(self.ruta)
        self.txtBuscar.setText("")
    
    #Función para abrir un archivo o un directorio en la ventana de edición
    def abrir_directorio(self,index):
        
        try:
            ruta = self.modelo2.filePath(index)
            if os.path.isfile(ruta):
                archivo = open(ruta, 'r')#Agarrro la ruta del directorio que le di doble click
                texto= archivo.read()
                archivo.close()
                ventanaArchivo(ruta,texto).exec()
            else:
                self.explorador_secundario(ruta)

        except OSError:
            print("El archivo no se pudo abrir \n", OSError.strerror) #Mandamos un mensaje en consola e imprimimos el detalle del error
            #archivo.close()
        except UnboundLocalError: #Error al abrir una carpeta como si duera archivo
            pass
        except BaseException:
            archivo.close()   
    
    def encontrar(self): # AGREGAR ESTO 
        txt = self.txtBuscar.text() #aqui asignamos en una variable la palabra que pase el usuario para buscar
        mod= buscar.Rutas()
        mod.recorrer_directorios(self.ruta) # llamamos al metodo y le pasamos la ruta con la que va a interactuar
        lista = mod.buscarArchivo(txt)
        encontrado=mod.respuesta(lista)
        if encontrado != None: #Si lo buscado no existe, no quiero que se actualice la ventana
            self.explorador_secundario(encontrado)
        else: 
            self.txtBuscar.setText("")
               
    #Función para mostrar tipo de menú
    def verificar_menu_directorio(self,point): #esto es una prueba
        index = self.arbol2.indexAt(point)
        selected_path = str(self.arbol2.model().filePath(index))
        if os.path.isfile(selected_path):
            self.mostrar_menu_archivo(point) 
        elif os.path.isdir(selected_path):
            self.mostrar_menu_general(point)
        else:
            self.mostrar_menu_general(point)
            
    #Función para mostrar el menú emergente general
    def mostrar_menu_general(self, point): # esta es la funcion que maneja el menú contextual
        try: 
            index = self.arbol2.indexAt(point)
            selected_path = str(self.arbol2.model().filePath(index)) #Seleccionamos la ruta de la elección
            
            #Dirección del mouse y del menú
            pos_raton = QtGui.QCursor.pos() #  aqui obtenemos la posicion globlal del raton gracias al modulo QCursor de la libreria QtGui para poder aujustarla segun sea necesario
            pos_menu  = QtCore.QPoint(pos_raton.x() + 10,pos_raton.y() + 0) #aqui ajustamos la posicion del menu 10 pixeles a la derecha del raton que en este caso seria X y 0 pexeles hacia abajo
            
            menu_vista = QtWidgets.QMenu(self) # aqui se crea un una variable el objeto QMenu
            accion_1 = menu_vista.addAction("Crear Carpeta")  # aquí se van agregando en una variable las acciones deseadas del menu para posteriormente utilizarlas con los metodos que queramos
            accion_2 = menu_vista.addAction("Crear Archivo")
            accion_3 = menu_vista.addAction("Borrar")
   
            #Metodos a acceder según la acción
            accion_1.triggered.connect(self.abrir_ventana) # aqui se conectan las acciones a las funciones correspondientes llamando a los metodos que les asignamos 
            accion_2.triggered.connect(self.abrir_ventana_archivo)
            accion_3.triggered.connect(lambda: self.borrar_directorio(selected_path)) 

            menu_vista.exec(pos_menu)
            menu_vista.close() # Una vez elegida la opción cerramos el menú
        except BaseException:
          print("Error de señal")
    
    #Función para mostrar menú al seleccionar archivo
    def mostrar_menu_archivo(self,point): #esto es una prueba
        index = self.arbol2.indexAt(point)
        selected_path = str(self.arbol2.model().filePath(index))
        pos_raton = QtGui.QCursor.pos() #  aqui obtenemos la posicion globlal del raton gracias al modulo QCursor de la libreria QtGui para poder aujustarla segun sea necesario
        pos_menu  = QtCore.QPoint(pos_raton.x() + 10,pos_raton.y() + 0) #aqui ajustamos la posicion del menu contextual 10 pixeles a la derecha del raton que en este caso seria X y 0 pexeles hacia abajo del raton que en este caso seria y
        menu_vista = QtWidgets.QMenu() # aqui se crea un una variable el objeto QMenu
        accion_1 = menu_vista.addAction("encriptar")  # aquí se van agregando en una variable las acciones deseadas del menu para posteriormente utilizarlas con los metodos que queramos            accion_2 = menu_vista.addAction("Crear Archivo")
        accion_2 = menu_vista.addAction("desencriptar")
        accion_3 = menu_vista.addAction("Borrar")
        accion_1.triggered.connect(lambda : self.ventana_contrasena(selected_path,True))
        accion_2.triggered.connect(lambda : self.ventana_contrasena(selected_path))
        accion_3.triggered.connect(lambda : self.borrar_directorio(selected_path))
       
        menu_vista.exec(pos_menu)
        menu_vista.close() # Una vez elegida la opción cerramos el menú
    
    #Función para abrir clase/ventana para escribir y generar contraseña
    def ventana_contrasena(self,ruta,cifrando = False):    
        nuevo = contrasena(ruta,cifrando)
        nuevo.exec()

    #Función para borrar archivos o carpetas
    def borrar_directorio(self,ruta):
        try:
            if os.path.isfile(ruta):
                os.remove(ruta)
            elif os.path.isdir(ruta):
                shutil.rmtree(ruta)
        except OSError:
            print("Error al borrar el directorio \n", OSError.strerror) #Mandamos un mensaje en consola e imprimimos el detalle del error
            #archivo.close()
        except UnboundLocalError: #Error al abrir una carpeta como si duera archivo
            print("ERROR1")
            
    #Función para filtrar los archivos que se muestran en el explorador (solo carpetas en el árbol1 y archivos txt en árbol2)
    def filtro(self, model, tipo):
        filtro = [tipo]#Tipo de directorio
        model.setNameFilters(filtro)#Añadimos el fltro recibido como lista
        model.setNameFilterDisables(False)#Activamos el filro
    
    #Funcion para crear un elemento (archivo o carpeta)
    def crear_elemento(self, ruta_actual, nombre):
        try:
            nueva_ruta = os.path.join(ruta_actual, nombre)
            if self.creating_file:
                open(nueva_ruta + ".txt", "a").close() #Crear e inmediatamente cerrar el archivo
            else:
                os.makedirs(nueva_ruta)
                self.modelo2.setRootPath(ruta_actual)
                self.explorador_secundario(ruta_actual)
        except FileExistsError:
            #crear un mensaje de error al crear un directorio duplicado
            mensaje = QtWidgets.QMessageBox(self)
            mensaje.setWindowTitle("Error")
            mensaje.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mensaje.setText("Nombre de carpeta ya existe")
            mensaje.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mensaje.exec()
        #inicializa y devuelve una nueva instancia deQFileSystemModel. Después de crear un nuevo archivo o directorio, puede llamar a este
        #método para recrear el modelo y configurarlo como el modelo para su QTreeView
          
    #Funcion para abrir la ventana de creación de carpeta
    def abrir_ventana(self):
        self.creating_file = False 
        nuevo_directorio_dialog = NuevoDirectorio(self, self.creating_file) 
        nuevo_directorio_dialog.exec()
    
    #Funcion para abrir la ventana de creación de archivo
    def abrir_ventana_archivo(self):
        self.creating_file = True
        nuevo_directorio_dialog = NuevoDirectorio(self)
        nuevo_directorio_dialog.exec()
        
#Clase para la ventana de creación de carpeta/archivo        
class NuevoDirectorio(QtWidgets.QDialog):
    def __init__(self,parent=None, creating_file = False) -> None:
        super(NuevoDirectorio,self).__init__(parent)
        uic.load_ui.loadUi("NuevoDirectorio.ui", self)
        self.cajaTexto = self.findChild(QtWidgets.QLineEdit, "txtNombreDir")
        self.btnCancelar = self.findChild(QtWidgets.QPushButton, "btnCancelar")
        self.btnSiguiente = self.findChild(QtWidgets.QPushButton, "btnSiguiente")
        
        self_creating_file = creating_file
        
        self.btnSiguiente.clicked.connect(self.generarNombre)
        
        
    def generarNombre(self):
        nombre = self.cajaTexto.text()
        try:
            assert nombre != ""
            assert nombre.find(" ") != 0
            if isinstance(self.parent(), ExploradorDeArchivos):  #Chequeamos si la instancia es de la clase correcta
                explorador = self.parent()
                explorador.crear_elemento(explorador.txtDir.text(), nombre)
                self.close()

        except AssertionError:
            self.mensaje_error_al_crear()
            
    def mensaje_error_al_crear(self):
        mensaje = QtWidgets.QMessageBox(self)
        mensaje.setWindowTitle("Error")
        #mensaje.setWindowIcon()
        mensaje.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        mensaje.setText("Nombre no válido")
        mensaje.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mensaje.exec()        

#Clase para la ventana de escribir contraseña
class contrasena(QtWidgets.QDialog): # AGREGAR ESTO
    def __init__(self, ruta, cifrando = False) -> None:
        super(contrasena,self).__init__()
        self.ui_path = os.path.dirname(__file__)
        uic.load_ui.loadUi ("VentanaContraseña.ui", self)
        
        #Inicialización de Widgets de ventanas 
        self.cajaTexto = self.findChild(QtWidgets.QLineEdit, "txtBusqueda")        
        self.btnCancelar = self.findChild(QtWidgets.QPushButton, "btnCancelar")
        self.btnCrear = self.findChild(QtWidgets.QPushButton, "btnBuscar")
        
        #Establecer función a botones
        self.btnCrear.clicked.connect(self.generar_contrasena)
        
        #Convertir parámetros a variables de clase
        self.ruta = ruta
        self.cifrando = cifrando
     
    def generar_contrasena(self):
        contrasena = self.cajaTexto.text()
        if self.cifrando:      
            #explorador = ExploradorDeArchivos()
            #explorador.crear_llave(self.ruta, contrasena)
            cifrado= crypt.cifrado_archivos()
            cifrado.crear_llave(self.ruta,contrasena)
            self.close()
        else:
             #explorador = ExploradorDeArchivos()
             #explorador.cargar_llave(self.ruta,contrasena)
            cifrado= crypt.cifrado_archivos()
            cifrado.cargar_llave(self.ruta,contrasena)
            self.close()
             
           
           
def main():
    app = QApplication(sys.argv)
    Form = ExploradorDeArchivos()
    Form.show()
    sys.exit(app.exec())
        
if __name__ == "__main__":
    main()        
    
    