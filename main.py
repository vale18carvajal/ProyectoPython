import sys
import typing
import os

from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QFileSystemModel
class ventanaArchivo(QtWidgets.QDialog):
    
    def __init__(self,textoArchivo="") -> None:
        super(ventanaArchivo,self).__init__()
        
        self.ui_path = os.path.dirname(__file__)
        uic.load_ui.loadUi ("VentanaArchivo.ui", self)
        
        
        self.botonBorrar = self.findChild(QtWidgets.QPushButton, "btnBorrarTexto")
        self.botonGuardar = self.findChild(QtWidgets.QPushButton, "btnGuardarArchivo")
        
        self.txtCampo = self.findChild(QtWidgets.QPlainTextEdit, "txtCampoTexto")
        self.botonBorrar.clicked.connect(self.borrar_texto)
        
        self.txtCampo.setPlainText(textoArchivo)
        self.botonGuardar.clicked.connect(self.guardarArchivo)
        
        
    def guardarArchivo(self):
        try:
            fichero=open(os.path.join(self.ui_path, "Archivo.txt"),'a')
            txt = self.txtCampo.toPlainText() + "\r"
            fichero.write(txt)
            fichero.close()
        except OSError:
                print("Error al abrir archivo")
        
    def borrar_texto(self):
        self.txtCampo.clear()

class ExploradorDeArchivos(QtWidgets.QDialog):
    def __init__(self) -> None:
        super(ExploradorDeArchivos,self).__init__()
        uic.load_ui.loadUi("UI_Explorador.ui", self)
        self.ruta= os.path.dirname(__file__) + '\\Raiz' #Creamos una ruta raiz que queremos mostrar en nuestra aplicación
        self.explorador_rapido()
        self.explorador_secundario()
        self.arbol.clicked.connect(self.actualizar_explorador_secundario)
        self.arbol2.doubleClicked.connect(self.abrir_directorio)
        self.texto = None
        
        self.btnFolder= self.findChild(QtWidgets.QPushButton, "btnCrearCarpeta")
        self.btnFolder.clicked.connect(self.abrir_ventana)
        self.btnReini = self.findChild(QtWidgets.QPushButton,"btnReiniciar")
        self.btnReini.clicked.connect(self.reiciar_vista)
        #self.btnFolder= self.findChild(QtWidgets.QPushButton, "btnCrearArchivo")
        #self.btnFolder.clicked.connect(self.abrir_ventana)
        
        
        
     
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
        
    def actualizar_explorador_secundario(self, index):
        ruta_nueva= self.modelo2.filePath(index)
        self.explorador_secundario(ruta_nueva)
        
    def reiciar_vista(self):
        self.explorador_rapido(self.ruta)
    
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
        except UnboundLocalError: #Erro al abrir una carpeta como si duera archivo
            pass
        except BaseException:
            archivo.close()          
    
    def filtro(self, model, tipo):#Con este método filtramos solo archivos .txt aparezcan
        filtro = [tipo]#Tipo de archivo con extensión .txt que deseamos mostrar, en formato lista
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
            
    def crear_archivo(self,ruta_actual,nombre):
        try:
            self.newPath= os.path.join(ruta_actual, nombre)
            open()
        except FileExistsError: #Se reconoce una excepeción el nombre de la carpeta ya existe
            self.mensaje_error_directorio()      
            
    def mensaje_error_directorio(self):
        mensaje = QtWidgets.QMessageBox(self)
        mensaje.setWindowTitle("Error")
        mensaje.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        mensaje.setText("Nombre de carpeta ya existe")
        mensaje.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mensaje.exec()

    def abrir_ventana(self):
        #NuevoDirectorio().exec() #Método para abrir ventana para estabelecer nombre al nuevo directorio
        nuevo_directorio_dialog = NuevoDirectorio(self)
        nuevo_directorio_dialog.exec()
        
class NuevoDirectorio(QtWidgets.QDialog):
    def __init__(self,parent=None) -> None:
        super(NuevoDirectorio,self).__init__(parent)
        uic.load_ui.loadUi("NuevoDirectorio.ui", self)
        self.cajaTexto = self.findChild(QtWidgets.QLineEdit, "txtNombreDir")
        self.btnCancelar = self.findChild(QtWidgets.QPushButton, "btnCancelar")
        self.btnSiguiente = self.findChild(QtWidgets.QPushButton, "btnSiguiente")
        
        
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
                explorador.crear_directorio(explorador.txtDir.text(), nombre)
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

class NuevoArchivo(QtWidgets.QDialog):
    def __init__(self,parent=None) -> None:
        super(NuevoDirectorio,self).__init__(parent)
        uic.load_ui.loadUi("NuevoDirectorio.ui", self)
        self.cajaTexto = self.findChild(QtWidgets.QLineEdit, "txtNombreDir")
        self.btnCancelar = self.findChild(QtWidgets.QPushButton, "btnCancelar")
        self.btnSiguiente = self.findChild(QtWidgets.QPushButton, "btnSiguiente")
        
        
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
                explorador.crear_archivo(explorador.txtDir.text(), nombre)
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
    
    