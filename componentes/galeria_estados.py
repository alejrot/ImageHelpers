
from componentes.galeria_imagenes import Galeria, ContenedorImagen, EstiloContenedor, ContImag
from componentes.contenedor_estados import ContenedorEstados
from constantes.constantes import Estados


def nada( e ):
    pass





# REDEFINICION  de componente
class GaleriaEstados(Galeria):
    """Clase usada para manejar galerías de imágenes con estados.
    Acepta objetos de la clase ContenedorEstados y sus derivados."""
    def __init__(self, estilos: dict):
        super().__init__()
        self.estilos = estilos
        # lista auxiliar para seleccionar contenedores internos a mostrar
        self.__claves_mostradas :list|None = None

    def cargar_imagenes(self, 
        imagenes: list[ContImag ], 
        cuadricula=True):
        """Lee objetos de imagen Flet del tipo ContenedorImagen previamente creados."""
        super().cargar_imagenes(imagenes, cuadricula)
        self.imagenes = imagenes
        # self.actualizar_estilos( )  
        self.estilo_estados( )  



    def estilo_estados(self):
        actualizar_estilo_estado( self.imagenes, self.estilos)    



    @property
    def claves_mostradas(self)->list|None:
        """Devuelve una lista con las claves de las imágenes mostradas.
        Si todas son visibles se retorna 'None'.
        """
        return self.__claves_mostradas


    @claves_mostradas.setter
    def claves_mostradas(self, claves: list|None)->None:

        if claves==None:
            # se hacen visibles todas las imagenes
            for contenedor in self.controls:
                contenedor.visible = True
        else:
            # se visibilizan solo los contenedores listados
            for contenedor in self.controls:
                contenedor.visible = True if contenedor.clave in claves else False
                    
        self.__claves_mostradas = claves


    @property
    def imagenes_mostradas(self):
        """Devuelve todos los contenedores de imagenes visibles"""
        if self.__claves_mostradas == None:
            return self.controls
        else:
            mostrados = []
            for contenedor in self.controls:
                if contenedor.visible:
                    mostrados.append(contenedor)

            return mostrados 


    # @property
    def claves_estado(self, estado: str)->list|None:
        """Devuelve una lista con las claves de las imágenes con el estado pedido.
        Si no se elige ningun estado válido se devuelve 'None'.
        """
        # print(f"imagenes totales: {len(self.controls)} ")
        # print(f"estado elegido: {estado} ")

        lista_claves = []
        if estado == Estados.GUARDADO.value:
            for contenedor in self.controls:
                if contenedor.guardada:
                    lista_claves.append(contenedor.clave)
            return lista_claves
        elif estado == Estados.MODIFICADO.value:
            for contenedor in self.controls:
                if contenedor.modificada:
                    lista_claves.append(contenedor.clave)
            return lista_claves
        elif estado == Estados.DEFECTUOSO.value:
            for contenedor in self.controls:
                if contenedor.defectuosa:
                    lista_claves.append(contenedor.clave)
            return lista_claves
        elif estado == Estados.NO_ALTERADO.value:
            for contenedor in self.controls:
                if  not contenedor.modificada and not contenedor.guardada:
                    lista_claves.append(contenedor.clave)
            return lista_claves
        else:
            return None


def actualizar_estilo_estado( contenedores: list[ContenedorEstados], estilos : dict ):
    """Cambia colores y espesor de bordes de imagen según los flags de estado internos."""
    objeto = map(lambda c : c.estilo_estado(), contenedores)
    contenedores = list(objeto)

