from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode
from PyQt6 import QtCore, QtWidgets, uic, QtGui

class cifrado_archivos():
    def __init__(self) -> None:
        super(cifrado_archivos,self).__init__()

        #Varibles del encriptado de archivos
        self.FIRMA = b"ENCRIPTADO"

    #Función para crear llave de encriptado
    def crear_llave (self,archivo,contrasena): #no agregar
        clave = contrasena
        clave = clave.encode()
        sal = b"una_salt_aleatoria"
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=sal, iterations=100000, backend=default_backend())
        clave = urlsafe_b64encode(kdf.derive(clave))
        self.encriptar_archivo(archivo, clave)
    
    #Función para cargar llave de desencriptado
    def cargar_llave (self,archivo,contrasena): #no agregar
        clave = contrasena
        clave = clave.encode()
        sal = b"una_salt_aleatoria"
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=sal, iterations=100000, backend=default_backend())
        clave = urlsafe_b64encode(kdf.derive(clave))
        self.desencriptar_archivo(archivo, clave)
    
    #Función de encriptado
    def encriptar_archivo(self,archivo,clave): #aqui le pasamos dos argumentos el primero es el archivo de texto que queremos encriptar y el segundo es la clave generada
        if self.verificar_encriptado(archivo):# aqui perguntamos si el archivo esta encriptado, si le está mandamos un mensaje de alerta y si no ejecutamos el metodo
            mensaje = QtWidgets.QMessageBox()
            mensaje.setWindowTitle("Error")
            #mensaje.setWindowIcon()
            mensaje.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mensaje.setText("Lo sentimos el archivo ya esta encriptado")
            mensaje.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mensaje.exec() 
        else:
            f = Fernet(clave) # aqui creamos un objeto de tipo fernet que le pasamos la llave, sin esto no se puede encriptar
            with open(archivo, "rb") as file: #aqui abrimos el archivo en modo lectura # despues lo asignamos en una varible para utilizarlo
                file_data = file.read() # aqui asignamos en una variable los datos que tiene
        
            datos_encriptados = f.encrypt(file_data) # aqui asignamos a una variable los datos a  encriptar del archivo con el metodo encrypt( esto encripta los datos que le pasemos como parametro) 
        
            with open(archivo,"wb") as file: #aqui guardamos nuevamente los archivos pero con los datos ya encriptados, esto se hace abriendo el archivo en modo escritura binaria # se le asigna a una variable para poder utilizarlo
                file.write(self.FIRMA +  datos_encriptados)# lo almacenamos con el metodo write y luego le agragamos una firma al principio del archivo encriptado para mas adelante poder saber si esta o no encriotado
            mensaje = QtWidgets.QMessageBox()
            mensaje.setIcon(QtWidgets.QMessageBox.Icon.Information)
            mensaje.setWindowTitle("Aviso")
            mensaje.setText("Contraseña creada")
            mensaje.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mensaje.exec()    
    
    #Función de decifrado  
    def desencriptar_archivo(self,archivo,clave):
        if self.verificar_encriptado(archivo):# aqui perguntamos si el archivo esta desencriptado, si lo está mandamos un mensaje de alerta y si no ejecutamos el metodo
            try:
                f = Fernet(clave) # aqui creamos un objeto de tipo fernet que le pasamos la llave, sin esto no se puede desencriptar
                with open(archivo, "rb") as file: #aqui abrimos el archivo en modo lectura binaria # despues lo asignamos en una varible para utilizarlo
                    datos_encriptados = file.read() # aqui asignamos en una variable los datos que tiene 
                    dato_encriptado = datos_encriptados[len(self.FIRMA):] #aqui usamos el metodo len junto con el de rebanado para que me tomo la longitud despues del  la firma guardando en una nueva variable solo lo que contiene el archivo
                    datos = f.decrypt(dato_encriptado)# aqui asignamos a una variable los datos a desencriptar del archivo con el metodo encrypt( esto encripta los datos que le pasemos como parametro) 
        
                with open(archivo,"wb") as file: #aqui abrimos el archivo en modo lectura
                    file.write(datos)# lo almacenamos con el metodo write
                mensaje = QtWidgets.QMessageBox()
                mensaje.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mensaje.setWindowTitle("Aviso")
                mensaje.setText("Contraseña válida")
                mensaje.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mensaje.exec()
            except:
                mensaje = QtWidgets.QMessageBox()
                mensaje.setWindowTitle("Error")
                mensaje.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mensaje.setText("Contraseña inválida")
                mensaje.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mensaje.exec()
        else:
            mensaje = QtWidgets.QMessageBox()
            mensaje.setWindowTitle("Error")
            mensaje.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mensaje.setText("Lo sentimos el archivo no esta encriptado")
            mensaje.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mensaje.exec()
            
    #Fución para confirmar si un archivo se encuentra encriptado o no
    def verificar_encriptado(self,ruta_archivo): # este metodo toma la ruta como argumento y verifica si tiene la firma al principio 
        with open(ruta_archivo, "rb") as f: # Verifica si el archivo tiene la firma al principio leyendo los primeros bytes del archivo
            firma = f.read(len(self.FIRMA))
        return firma == self.FIRMA # aqui lo compara con la firma y si son iguales devueve true de lo contrario devuelve false
       

if __name__ == "__main__":
    print("Este módulo no debe ser ejecutado como main :)")