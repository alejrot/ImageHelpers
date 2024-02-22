import tempfile
import pathlib


def crear_directorio_temporal(
    prefijo: str, 
    ruta_relativa: tempfile.TemporaryDirectory | None = None):
    """Esta funcion crea una carpeta temporal con nombre. 
    Opcionalmente se puede indicar una carpeta para alojarla (ésta debe ser preexistente).
    """
    eliminar = False
    if ruta_relativa == None:
        directorio_temporal = tempfile.TemporaryDirectory(
        prefix = prefijo,
        delete = eliminar,
        ) 
        return directorio_temporal

    else: 
        directorio_temporal = tempfile.TemporaryDirectory(
        prefix = prefijo,
        dir = ruta_relativa.name,
        delete = eliminar,
        ) 
        return directorio_temporal


def crear_archivo_temporal(
    ruta_archivo: str, 
    directorio_virtual: tempfile.TemporaryDirectory | None = None):
    """Esta funcion crea un archivo temporal con nombre. 
    Opcionalmente se puede indicar un subdirectorio para alojar el archivo (éste debe ser preexistente)
    """
    # Crear un archivo temporal con nombre 

    eliminar = False    # eliminacion habilitada
    
    # configuracion recomendada Windows (en POSIX no molesta)
    # eliminar = True     # eliminacion habilitada
    eliminar_al_cerrar = False  # permite reapertua

    # prevencion de carga de ruta absoluta
    nombre_archivo = pathlib.Path(ruta_archivo).name
    # extension del archivo temporal
    extension = pathlib.Path(nombre_archivo ).suffix 
    # nombre archivo temporal (prefijo)
    nombre = pathlib.Path(str(nombre_archivo) ).with_suffix('')
    nombre = str(nombre)

    # print("ARCH", extension, nombre)

    if directorio_virtual == None:
        archivo_temporal = tempfile.NamedTemporaryFile( 
                prefix = nombre,    # parte del nombre de archivo
                suffix = extension,    # extensión añadida de archivo
                delete = eliminar,
                delete_on_close= eliminar_al_cerrar,
                )
    else:
        archivo_temporal = tempfile.NamedTemporaryFile( 
                prefix = nombre,    # parte del nombre de archivo
                suffix = extension,    # extensión añadida de archivo
                dir = directorio_virtual.name,
                delete = eliminar,
                delete_on_close= eliminar_al_cerrar,
                )
    # # apertura archivo en modo lectura binaria
    archivo_disco = open(ruta_archivo, "rb")
    data = archivo_disco.read()

    # Asignacion de data al archivo
    archivo_temporal.write( data )
    archivo_temporal.seek(0)

    # retorno del descriptor del archivo temporal
    return archivo_temporal


def eliminar_archivo(ruta: str):
    archivo = pathlib.Path(ruta)
    try:
        archivo.unlink()  
        return True
    except OSError as e:
        print(f"Error:{ e.strerror}")
        return False


def eliminar_directorio(ruta: str):
    directorio = pathlib.Path(ruta)
    try:
        directorio.rmdir()  
        return True
    except OSError as e:
        print(f"Error:{ e.strerror}")
        return False



if __name__=="__main__":


    import sys
    import cv2 as cv


    ruta = sys.argv[1]

    carpeta_temporal = crear_directorio_temporal(
        "imagenes_temporales"
    ) 
    subcarpeta_temporal = crear_directorio_temporal(
        "subcarpeta", carpeta_temporal
    ) 


    # archivo: dentro de un subdirectorio
    archivo_temporal = crear_archivo_temporal(
        ruta, 
        subcarpeta_temporal
        )


    # archivo 2: sin subdirectorio
    ruta2 = ruta
    archivo_temporal2 = crear_archivo_temporal(ruta2)

    print('carpeta de archivos temporales',tempfile.gettempdir()) # carpeta por defecto
    print('carpeta temporal creada: ',subcarpeta_temporal.name)
    print("ruta archivo temporal: ", archivo_temporal.name)
    print("ruta archivo temporal (sin subdirectorios): ", archivo_temporal2.name)


    img = cv.imread(archivo_temporal.name)

    if img is None:
        sys.exit("No se pudo leer la imagen.")

    cv.imshow("Ventana grafica", img)
    k = cv.waitKey(0)


    # eliminar archivos creados
    eliminar_archivo(archivo_temporal.name)
    eliminar_archivo(archivo_temporal2.name)
    
    # eliminar directorios creados
    eliminar_directorio(subcarpeta_temporal.name)
    eliminar_directorio(   carpeta_temporal.name)





