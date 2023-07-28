import sys
import typing
import os

from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QFileSystemModel


class ExploradorDeArchivos(QtWidgets.QDialog):
    def __init__(self) -> None:
        super(ExploradorDeArchivos,self).__init__()
        uic.load_ui.loadUi("UI_Explorador.ui", self)
        self.ruta= os.path.dirname(__file__)
        #self.inicializarElementos()
    
    #def inicializarElementos(self): #Método para inicializar los widgets
        #Creamos una variable Modelo en la cual vamos a instanciar la clase QFileSystemModel que
        #proporcional un modelo de datos para archvios locales
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

        self.btnFolder= self.findChild(QtWidgets.QPushButton, "btnCrearCarpeta")
        self.btnFolder.clicked.connect(self.crear_directorio)
    #El siguiente método es para crear una nueva carpeta 
    def crear_directorio(self):
        try:
            self.newPath= os.path.join(self.ruta, "Carpetita") #Establecemos la ruta de la carpeta más el nombre de la misma en una variabel str
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
            
def main():
    app = QApplication(sys.argv)
    Form = ExploradorDeArchivos()
    Form.show()
    sys.exit(app.exec())
        
if __name__ == "__main__":
    main()        
    
    