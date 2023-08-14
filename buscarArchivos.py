import os
class Rutas:# esta es la clase que vamos a utilizar para guardar los objetos en la lista con su ruta y nombre de archivo
    def __init__(self,Ruta="",NomArchivo=""):
        self.Ruta = Ruta
        self.NomArchivo = NomArchivo

        self.listaRutaArchivo=[]
    
    def obtener_nombre_archivo(self, ruta):
        nombre_archivo_con_extension = os.path.basename(ruta) # asignomos en una varible el nombre de la carpeta con el metodo basename (sirve tambien para archivos) que esto nos extrae la ultima parte de la ruta https://docs.python.org/3/library/os.path.html
        nombre_archivo, extension = os.path.splitext(nombre_archivo_con_extension) #aqui asignamos el en una variable el nombre de la carpeta y en otra variable el nombre de la extension con el metodo splitext() que lo que hace es separ el nombre del archivo de su extension 
        return nombre_archivo # retornamos el nombre nombre de la carpeta o nombre del archivo dependiendo de lo que le usuario quiera

    def recorrer_directorios(self,ruta):
        contenidos = os.listdir(ruta) # aqui le asignamos a una variable con este metodo una lista de string de lo que contiene la ruta ya sean carpetas o archivos
       
        for i in contenidos: # creamos un bucle donde recorremos la lista de la variable contenidos
            ruta_completa = os.path.join(ruta, i) # asignamos a una nueva variable la ruta junto con el cada elemento de la lista que cotontiene la varible contenidos mediante el bucle 
           # print("esta es la ruta completa",ruta_completa)
            if os.path.isdir(ruta_completa): # preguntamos si es una carpeta con este metodo
                nombreArchivo = self.obtener_nombre_archivo(ruta_completa) # guardamos en una variable lo que obtenemos del metodo que en este caso es el nombre de la carpeta
                self.listaRutaArchivo.append(Rutas(ruta_completa , nombreArchivo)) #guardamos en la lista un objeto de la clase con la ruta y en nombre del archivo
                self.recorrer_directorios(ruta_completa) # como la primera coincidencia es una carpeta volvemos a llamar a el metodo pero con una nueva ruta creando la recursividad 
            else: # si no es un directorio entonces recorremos esta parte
                nombreArchivo = self.obtener_nombre_archivo(ruta_completa) # guardamos en una variable lo que obtenemos del metodo obtener_nombre_archivo que le pasamos como parametro la variable de la ruta que antes creamos 
                # print(nombreArchivo)
                #self.lol = nombreArchivo # aqui voy guardando en una variable el nombre de la carpeta donde se encuentra lo que solicitamos 
                self.listaRutaArchivo.append(Rutas(ruta_completa , nombreArchivo))#guardamos en la lista un objeto de la clase con la ruta y en nombre del archivo

    def buscarArchivo(self,nombreArchivo): 
        return [objeto for objeto in self.listaRutaArchivo if objeto.NomArchivo == nombreArchivo] #esto nos retorna una lista con los objetos cuyo atributo NomArchivo sea igual al valor de la variable que le pasamos que este caso es NomArchivo
     
    def respuesta(self,lista):
        listaFinal=[] #Pendiente Vale
        if len(lista) > 0:  
            for archivo in lista: # hacemos el recorrido de la lista que tiene como 
                ruta_anterior = os.path.dirname(archivo.Ruta)# aqui usamos la funcion os.path.dirname para obtener la ruta anterior a la ruta que tenemos en el objeto archivo.Ruta 
                #self.explorador_secundario(ruta_anterior) # luego asignamos la nueva ruta a la ventana de explorador_secundario
                #print(ruta_por_nombre)
                return ruta_anterior


if __name__ == "__main__":
    print("Este módulo no debe ser ejecutado como main :)")