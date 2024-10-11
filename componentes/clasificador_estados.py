
# from estilos.estilos_contenedores import  estilos_seleccion, estilos_galeria, Estilos

# from manejo_imagenes.verificar_dimensiones import dimensiones_imagen

from constantes.constantes import Tab, Percentil, Estados

from componentes.galeria_imagenes import Galeria, ContenedorImagen, ContImag
# from componentes.contenedor_etiquetado import ContenedorEtiquetado
from componentes.contenedor_estados import ContenedorEstados
# from componentes.galeria_estados import actualizar_estilo_estado


# Clases


class ClasificadorEstados:
    """Clase pensada para gestionar las listas de imágenes de forma centralizada y ordenada."""
    def __init__(self):
        self.todas          : list = [ContenedorEstados]
        self.seleccion      : list = [ContenedorEstados]
        self.guardadas      : list = [ContenedorEstados]
        self.modificadas    : list = [ContenedorEstados]
        self.no_alteradas   : list = [ContenedorEstados]
        self.defectuosas    : list = [ContenedorEstados]

        # clave de la imagen actualmente seleccionada
        self.clave_actual: str= ""
        self.ruta_directorio : str = ""
        self.ruta_dataset : str = ""
        # self.ruta_descarte : str = "descartados"

        self.estado: str|None = None
        self.dimensiones_elegidas :tuple[int, int, int]|None = None


    def cargar_imagenes(self, imagenes: list[ContenedorEstados],  agregado=False):
        """Este metodo carga imagenes de tipo ft.Image o derivadas creadas externamente"""
        if agregado:
            # modo agregado
            self.todas.extend(lista)
        else:
            # modo reinicio
            self.todas = imagenes


    # def verificar_imagenes(self):
    def verificar_imagenes(self, dimensiones: tuple[int, int, int]|None=None):
        """Marca como defectuosas aquellas imágenes que no cumplan con los requisitos."""
        # marcado de imagenes defectuosas según las dimensiones requeridas 
        if dimensiones!=None:
            self.dimensiones_elegidas = dimensiones
            
        for imagen in self.todas:
            imagen.verificar_imagen(self.dimensiones_elegidas)


    def filtrar_estados(self, estado: str | None):
        """Devuelve solamente los contenedores internos con el estado de etiquetado pedido."""
        return filtrar_estados(self.todas, estado )


    def filtrar_dimensiones(self,     
        # lista_imagenes: list[ContenedorEtiquetado], 
        lista_imagenes: list[ContenedorEstados], 
        dimensiones: tuple[int, int, int] | None = None):
        """Devuelve solamente los contenedores de imagen con el ancho y altura correctos.
        Si las dimensiones de entrada son 'None' devuelve todos los conteedores de entrada. 
        """
        return filtrar_dimensiones(self.todas, dimensiones)


    def clasificar_estados(self):
        """Reparte las imagenes de la estructura en base a sus banderines de estado."""
        # actualizacion de posibles imagenes defectuosas
        self.verificar_imagenes()
        # creacion de listas internas
        self.guardadas    = self.filtrar_estados(Estados.GUARDADO  .value)
        self.modificadas  = self.filtrar_estados(Estados.MODIFICADO.value)
        self.no_alteradas = self.filtrar_estados(Estados.NO_ALTERADO.value)
        self.defectuosas  = self.filtrar_estados(Estados.DEFECTUOSO .value)


    def seleccionar_estado(self, estado:None|str=None)->list:
        """Selecciona las imágenes de una de las categorías internas. Actualiza las listas antes de asignar"""
        self.clasificar_estados()           # FIX

        if estado == None:
            # guardado de estado elegido
            estado = self.estado 
        else:
            # lectura desde estado previo
            self.estado  = estado

        if estado == Estados.MODIFICADO.value:
            self.seleccion = self.modificadas
        elif estado == Estados.GUARDADO.value:
            self.seleccion = self.guardadas
        elif estado == Estados.NO_ALTERADO.value:
            self.seleccion = self.no_alteradas
        elif estado == Estados.DEFECTUOSO.value:
            self.seleccion = self.defectuosas
        elif estado == Estados.TODOS.value:
            self.seleccion = self.todas

        elif estado == None:
            self.seleccion = self.todas

        return self.seleccion



# Funciones


def filtrar_dimensiones(
    lista_imagenes: list[ContenedorEstados], 
    dimensiones: tuple[int, int, int] | None = None
    # )->list[ContenedorEtiquetado]:
    )->list[ContenedorEstados]:
    """Devuelve solamente los contenedores de imagen con el ancho y altura correctos.
    Si las dimensiones de entrada son 'None' devuelve todos los contenedores de entrada. 
    """
    imagenes_filtradas = []

    if dimensiones != None:
        # imagenes con dimensiones correctas
        objeto_resultado = filter(lambda imagen: imagen.dimensiones == dimensiones, lista_imagenes)
        imagenes_filtradas = list(objeto_resultado)
        return imagenes_filtradas

    else:
        # caso sin dimensiones especificas
        return lista_imagenes


    
def filtrar_estados(
    lista_imagenes: list[ContenedorEstados], 
    estado: str | None ,
    )->list[ContenedorEstados]:
    """Devuelve solamente los contenedores con el estado de etiquetado pedido."""
    # imagen : ContenedorEtiquetado
    imagen : ContenedorEstados
    imagenes_filtradas = []
    # imagenes guardadas (sin cambios)
    if estado == Estados.GUARDADO.value:
        objeto_resultado = filter(lambda imagen: imagen.guardada and not imagen.modificada, lista_imagenes)
        return list(objeto_resultado)

    # imagenes tags modificados (todas)
    elif estado == Estados.MODIFICADO.value:
        objeto_resultado = filter(lambda imagen: imagen.modificada, lista_imagenes)
        return list(objeto_resultado)

    # no etiquetadas ni guardadas
    elif estado == Estados.NO_ALTERADO.value:
        objeto_resultado = filter(lambda imagen: not imagen.modificada and not imagen.guardada, lista_imagenes)
        return list(objeto_resultado)

    # defectuosas por uno u otro motivo
    elif estado == Estados.DEFECTUOSO.value:
        objeto_resultado = filter(lambda imagen: imagen.defectuosa, lista_imagenes)
        return list(objeto_resultado)

    else:
        # no filtrado
        return lista_imagenes
