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
        self.ruta= os.path.dirname(__file__) + '\\Raiz'
        #self.inicializarElementos()

    #def inicializarElementos(self): #Método para inicializar los widgets
        #Creamos una variable Modelo en la cual vamos a instanciar la clase QFileSystemModel que
        #proporcional un modelo de datos para archvios locales
        #self.ruta= 'c:\\Users\\valer\\OneDrive\\Documentos\\CISCO IT ESSENTIALS'
        self.modelo = QFileSystemModel()
        #Creamos una variable de ruta para guardar la ruta raíz que queremos mostrar en la ventana
        
        #Seteamos la ruta raiz para mostrar en el QTreeView
        self.modelo.setRootPath(self.ruta)
        
        
        
        
        #Incializamos una variable de tipo QTreeView que se encuentra en al archivo .ui
        self.arbol = self.findChild(QtWidgets.QTreeView, "treeArbol")
        #SetModel() es un método heredado de la clase "QAbstractItemModel Class" que proporciona una clase
        #abstracta para las clases de modelos de elemetnos. Como QTreeview es un elemento que requiere
        #items, podemos manipular su modelo de intem con la función setModel()
        self.arbol.setModel(self.modelo)
        #Con setRootIndex() se establece el elemento de ruta raiz: https://doc.qt.io/qt-6/qabstractitemview.html#setRootIndex
        #Con el método index() de la clase QFileSystemModel retornar el item del modelo con la ruta establecida como ruta raíz
        self.arbol.setRootIndex(self.modelo.index(self.ruta))
        self.filtro()#

        self.arbol.doubleClicked.connect(self.abrir_archivo)
        self.texto = None
        
        self.btnFolder= self.findChild(QtWidgets.QPushButton, "btnCrearCarpeta")
        self.btnFolder.clicked.connect(self.abrir_ventana)
        
    def abrir_archivo(self,index):
        
        try:
           
            archivo = open(self.modelo.filePath(index), 'r')
            texto= archivo.read()
            archivo.close()
            ventanaArchivo(texto).exec()

        except OSError:
            print("El archivo no se pudo abrir \n", OSError.strerror) #Mandamos un mensaje en consola e imprimimos el detalle del error
            #archivo.close()
        except UnboundLocalError:
            pass
        except BaseException:
            archivo.close()
            
    
    def filtro(self):
        filtro = ["*.txt"]#
        self.modelo.setNameFilters(filtro)#
        self.modelo.setNameFilterDisables(False)#
    
    def crear_directorio(self):#Este método es para crear una nueva carpeta
        try:
            self.newPath= os.path.join(self.ruta, "Carpeta") #Establecemos la ruta de la carpeta más el nombre de la misma en una variabel str
            self.folder = os.makedirs(self.newPath) #Creamos la carpeta con el método mkdirs() del módulo os con su número de modelo
        except FileExistsError: #Se reconoce una excepeción el nombre de la carpeta ya existe
            self.mensaje_error_directorio()
            

    def mensaje_error_directorio(self):
        mensaje = QtWidgets.QMessageBox(self)
        mensaje.setWindowTitle("Error")
        mensaje.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        mensaje.setText("Nombre de carpeta existente")
        mensaje.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mensaje.exec()

    def abrir_ventana(self):
        NuevoDirectorio().exec()

class NuevoDirectorio(QtWidgets.QDialog):
    def __init__(self) -> None:
        super(NuevoDirectorio,self).__init__()
        uic.load_ui.loadUi("NuevoDirectorio.ui", self)
        self.cajaTexto = self.findChild(QtWidgets.QLineEdit, "txtNombreDir")
        self.btnCancelar = self.findChild(QtWidgets.QPushButton, "btnCancelar")
        self.btnSiguiente = self.findChild(QtWidgets.QPushButton, "btnSiguiente")
        
        self.btnSiguiente.clicked.connect(self.generarNombre)
        
    def generarNombre(self):
        nombre = self.cajaTexto.text()
        if ((nombre !="") or not(nombre.isspace)):
            ExploradorDeArchivos.crear_directorio()
        
            NuevoDirectorio.close()
               
def main():
    app = QApplication(sys.argv)
    Form = ExploradorDeArchivos()
    Form.show()
    sys.exit(app.exec())
        
if __name__ == "__main__":
    main()        
    
    