
from manejo_texto.procesar_etiquetas import Etiquetas

from componentes.contenedor_estados import ContenedorEstados
from componentes.galeria_imagenes import   EstiloContenedor

from estilos.estilos_contenedores import  estilos_galeria, Estilos


class ContenedorEtiquetado( Etiquetas, ContenedorEstados):
    """Clase usada para manejar imágenes etiquetables."""
    def __init__(
        self, 
        ruta: str, 
        ancho:int=768, 
        alto:int=768, 
        redondeo:int=0 , 
        estilos: dict[str, EstiloContenedor] = estilos_galeria,
        ):
        Etiquetas.__init__(self, ruta)
        ContenedorEstados.__init__(self,ruta, ancho, alto, redondeo)

 
    # Implementacion de metodos requeridos
    def verificar_guardado(self):
        """Comprueba si las etiquetas actuales son las mismas que las guardadas en archivo de texto"""
        # verificacion guardado
        tags_archivo  = self.tags_archivo 
        self.__guardada = False if len(tags_archivo)==0 else True
        # verificacion modificaciones de etiquetado
        tags_imagen =  self.tags
        self.__modificada = True if set(tags_imagen) != set(tags_archivo) else False 


    def buscar_etiqueta(self, etiqueta: str):
        """Este método busca la etiqueta en la imagen y si la encuentra devuelve 'True'."""
        return True if etiqueta in self.tags else False
            

    def guardar_archivo(self)->bool:
        """
        Escribe/rescribe el archivo de etiquetas si éstas no coinciden con las guardadas en la estructura. 
        Si 'tags' es 'None' se usan las etiquetas almacenadas en el objeto imagen.
        """
        guardado_exitoso = False
        self.verificar_guardado()
        if self.modificada:
            guardado_exitoso = self.guardar(self.tags)
            self.__guardada = guardado_exitoso
        return guardado_exitoso


    #  REPETIDOS PERO NECESARIOS 
    @property
    def modificada(self)->bool:
        return self.__modificada 

    @property
    def guardada(self)->bool:
        return self.__guardada 






def leer_imagenes_etiquetadas(rutas_imagen: list[str], ancho=1024, alto=1024, redondeo=0, nro_inicial=0):
    """Esta funcion crea lee imagenes desde archivo y crea una lista de objetos ft.Container modificados.
    También asigna una clave ('key') a cada una.
    """
    contenedores = [] 

    for i in range(nro_inicial, nro_inicial + len(rutas_imagen)):
        contenedor = ContenedorEtiquetado(rutas_imagen[i], ancho, alto, redondeo)
        contenedor.clave = f"imag_{i}"
        contenedores.append(contenedor)

    return contenedores




