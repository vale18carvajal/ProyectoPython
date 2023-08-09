import sys
import typing
import os

from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QFileSystemModel
#Clase para la ventana de edición de archivo
class ventanaArchivo(QtWidgets.QDialog):
    
    def __init__(self,textoArchivo="") -> None:
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
        
        #Establecer el texto inicial del campo de edición
        self.txtCampo.setPlainText(textoArchivo)
        
        
    def guardarArchivo(self):
        try:
            #Abrir el archivo en modo append y escribir el contenido en el campo de texto
            fichero=open(os.path.join(self.ui_path, "Archivo.txt"),'a')
            txt = self.txtCampo.toPlainText() + "\r"
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
        
        #Flag para inidicar si se está crando un archivo //
        self.creating_file= False
        
        #Conectar botones a funciones
        self.btnFolder= self.findChild(QtWidgets.QPushButton, "btnCrearCarpeta")
        self.btnFolder.clicked.connect(self.abrir_ventana)
        self.btnFolder= self.findChild(QtWidgets.QPushButton, "btnCrearArchivo")
        self.btnFolder.clicked.connect(self.abrir_ventana_archivo)
        self.btnReini = self.findChild(QtWidgets.QPushButton,"btnReiniciar")
        self.btnReini.clicked.connect(self.reiniciar_vista)
        
        
        
        
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
    
    #Función para actualizar el explorador secundario al hacer click en una carpeta    
    def actualizar_explorador_secundario(self, index):
        ruta_nueva= self.modelo2.filePath(index)
        self.explorador_secundario(ruta_nueva)
     
    #Función que reinicia la vista a la ruta raíz | Llama al explorador secundario con la ruta raíz    
    def reiniciar_vista(self):
        self.explorador_secundario(self.ruta)
    
    #Función para abrir un archivo o un directorio en la ventana de edición
    def abrir_directorio(self,index):
        
        try:
            ruta_nueva = self.modelo2.filePath(index)
            if os.path.isfile(ruta_nueva):
                archivo = open(self.modelo2.filePath(index), 'r')#Agarrro la ruta del directorio que le di doble click
                texto= archivo.read()
                archivo.close()
                ventanaArchivo(texto).exec()
            else:
                self.explorador_secundario(ruta_nueva)

        except OSError:
            print("El archivo no se pudo abrir \n", OSError.strerror) #Mandamos un mensaje en consola e imprimimos el detalle del error
            #archivo.close()
        except UnboundLocalError: #Error al abrir una carpeta como si duera archivo
            pass
        except BaseException:
            archivo.close()          
    
    #Función para filtrar los archivos que se muestran en el explorador (solo carpetas en el árbol1 y archivos txt en árbol2)
    def filtro(self, model, tipo):
        filtro = [tipo]#Tipo de directorio
        model.setNameFilters(filtro)#Añadimos el fltro recibido como lista
        model.setNameFilterDisables(False)#Activamos el filro
    
    def crear_directorio(self,ruta_actual,nombre):#Este método es para crear una nueva carpeta
        try:
           
            self.newPath= os.path.join(ruta_actual, nombre) #Establecemos la ruta de la carpeta más el nombre de la misma en una variabel str
            #print("cuadro: " ,self.txtDir.text())
            #print("path: " ,self.modelo2.rootPath())
            os.makedirs(self.newPath) #Creamos la carpeta con el método mkdirs() del módulo os con su número de modelo
            #self.explorador_secundario(self.newPath)
        except FileExistsError: #Se reconoce una excepeción el nombre de la carpeta ya existe
            self.mensaje_error_directorio()
  
    #Funcion para crear un elemento (archivo o carpeta) //
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
            self.mensaje_error_directorio
        #inicializa y devuelve una nueva instancia deQFileSystemModel. Después de crear un nuevo archivo o directorio, puede llamar a este
        #método para recrear el modelo y configurarlo como el modelo para su QTreeView
    
    #Función para crear un mensaje de error al crear un directorio duplicado        
    def mensaje_error_directorio(self):
        mensaje = QtWidgets.QMessageBox(self)
        mensaje.setWindowTitle("Error")
        mensaje.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        mensaje.setText("Nombre de carpeta ya existe")
        mensaje.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mensaje.exec()

    def abrir_ventana(self):
        self.creating_file = False #//
        nuevo_directorio_dialog = NuevoDirectorio(self, self.creating_file) #//
        nuevo_directorio_dialog.exec()
    
    #Funcion para abrir la ventana de creación de archivo //
    def abrir_ventana_archivo(self):
        self.creating_file = True
        nuevo_directorio_dialog = NuevoDirectorio(self)
        nuevo_directorio_dialog.exec()
        
#Clase para la ventana de creación de carpeta/archivo        
class NuevoDirectorio(QtWidgets.QDialog):
    def __init__(self,parent=None, creating_file = False) -> None: #//
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
            #ExploradorDeArchivos
            #crear = ExploradorDeArchivos()
            #crear.crear_directorio(nombre)
            #self.close()
            
            if isinstance(self.parent(), ExploradorDeArchivos):  # Check if the parent is of the right class
                explorador = self.parent()
                explorador.crear_elemento(explorador.txtDir.text(), nombre)
                self.close()

        except AssertionError:
            self.mensaje_error_al_crear()
            
    def mensaje_error_al_crear(self):
        mensaje = QtWidgets.QMessageBox(self)
        mensaje.setWindowTitle("Error")
        mensaje.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        mensaje.setText("Nombre no válido")
        mensaje.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mensaje.exec()        
           
def main():
    app = QApplication(sys.argv)
    Form = ExploradorDeArchivos()
    Form.show()
    sys.exit(app.exec())
        
if __name__ == "__main__":
    main()        
    
    