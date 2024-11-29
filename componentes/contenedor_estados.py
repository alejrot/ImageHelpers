
from abc import ABC, abstractclassmethod

from constantes.constantes import Tab, Percentil, Estados
from estilos.estilos_contenedores import  estilos_seleccion, estilos_galeria, Estilos, EstiloContenedor
from manejo_imagenes.verificar_dimensiones import dimensiones_imagen
from componentes.galeria_imagenes import Galeria, ContenedorImagen, EstiloContenedor, ContImag
from componentes.contenedores import ContenedorImagen
from sistema_archivos.rutas import ruta_relativa_usuario


# Clase plantilla para crear contenedores de imagenes con estados
class ContenedorEstados(ABC, ContenedorImagen):
    """Clase plantilla para manejar imagenes con estados de guardado, modificación, etc."""
    #  Inicializacion
    def __init__(
        self, 
        ruta: str, 
        ancho:int=768, 
        alto:int=768, 
        redondeo:int=0 , 
        estilos: dict[str, EstiloContenedor] = estilos_galeria,
        ):
        ContenedorImagen.__init__(self,ruta, ancho, alto, redondeo)
        self.ruta_origen = ruta            # CUIDADO: la imagen interna TAMBIEN tiene un parametro 'ruta'
        self.__modificada = False
        self.__guardada = False
        self.__defectuosa = False
        self.__dimensiones: tuple[int, ...]|None
        self.leer_dimensiones()
        self.verificar_imagen()   
        self.verificar_guardado()
        self.estilos = estilos
        self.tooltip = ruta_relativa_usuario(ruta)


    # clases a rediseñar
    def verificar_guardado(self):
        pass


    # clases prediseñadas 

    def estilo_estado(self):

        if self.defectuosa :     
            estilo = self.estilos[Estilos.ERRONEO.value]     
        elif self.modificada :
            estilo = self.estilos[Estilos.MODIFICADO.value]
        elif self.guardada :
            estilo = self.estilos[Estilos.GUARDADO.value]
        else: 
            estilo = self.estilos[Estilos.DEFAULT.value]
        self.estilo( estilo )


    def leer_dimensiones(self):
        """Este método lee altura, base y numero de canales de la imagen"""
        dim = dimensiones_imagen(self.ruta_origen)  
        self.__dimensiones = dim if dim!=None else None 
        return self.__dimensiones

    @property
    def dimensiones(self):
        return self.__dimensiones


    def verificar_imagen(self, dimensiones: tuple[int, int, int] | None=None)->bool|None:
        """Este método verifica dimensiones de archivo.
        Devuelve 'True' si las dimensiones coinciden.
        """
        if dimensiones == None:
            self.__defectuosa = False
            return None
        if self.__dimensiones != dimensiones:
            self.__defectuosa = True
            return False
        else:
            self.__defectuosa = False
            return True


    @property
    def defectuosa(self)->bool:
        return self.__defectuosa

    @property
    def guardada(self)->bool:
        return self.__guardada 

    @property
    def modificada(self)->bool:
        return self.__modificada 

