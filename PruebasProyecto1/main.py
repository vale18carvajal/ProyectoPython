import sys, os
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtWidgets import QWidget, QMainWindow

class ventanaArchivo(QtWidgets.QDialog):
    
    def __init__(self) -> None:
        super(ventanaArchivo,self).__init__()
        
        self.ui_path = os.path.dirname(__file__)
        uic.load_ui.loadUi ("VentanaDeArchivo.ui", self)
        
        
        self.botonBorrar = self.findChild(QtWidgets.QPushButton, "btnBorrarTexto")
        self.botonGuardar = self.findChild(QtWidgets.QPushButton, "btnGuardarArchivo")
        
        self.txtCampo = self.findChild(QtWidgets.QPlainTextEdit, "txtCampoTexto")
        self.botonBorrar.clicked.connect(self.borrar_texto)
        
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

class ventanaIncial(QMainWindow):
    def __init__(self) -> None:
        super(ventanaIncial,self).__init__()
        uic.load_ui.loadUi ("VentanaPrincipal.ui", self)
        
        self.btnAbrir_= self.findChild(QtWidgets.QPushButton, "btnAbrir")
        
        self.btnAbrir_.clicked.connect(self.abrir_ventana)
        
    def abrir_ventana(self):
        ventanaArchivo().exec()
    
        
    
        
        
if __name__ == "__main__":
    app=QtWidgets.QApplication(sys.argv)
    Form = ventanaIncial()
    Form.show()
    sys.exit(app.exec())
        
        