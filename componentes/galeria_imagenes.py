# Ejecutar demo como:
# py -m componentes.galeria_imagenes
from functools import partial
from typing import TypeVar
import flet as ft
import pathlib

from estilos.estilos_contenedores import EstiloContenedor

from componentes.contenedores import Imagen, Contenedor, ContenedorImagen
from componentes.contenedores import Cont, ContImag 

class Galeria(ft.Row):
    """Clase 'Galeria' compuesta creada para manejar fácilmente multiples contenedores de imagenes. 
    Es subclase del objeto 'fila' (ft.Row) de FLET
    """
    def __init__(self):
        super().__init__(
            expand = True,
            wrap = True, # version galería (si es 'False' las imagenes van en linea)
            scroll=ft.ScrollMode.ALWAYS,
            spacing=0,              # espaciado horizontal extra
            run_spacing=0,        # espaciado vertical extra
            )
        self.numero = 0


    def estilo(self, estilo: EstiloContenedor ): 
        """Asigna un mismo estilo visual a todos los contenedores de la galeria."""
        for contenedor in self.controls:
            contenedor.estilo(estilo)


    # def leer_imagenes(self, rutas_imagen: list[str], ancho=256, alto=256, redondeo=0,  cuadricula=True):
    #     """Crea los contenedores vacios para la galeria y les carga las imagenes"""
    #     self.wrap = cuadricula # version galería (si es 'False' las imagenes van en linea)
    #     self.numero = len(rutas_imagen)
    #     self.controls = leer_imagenes( rutas_imagen, ancho, alto, redondeo) 

    def imagen_clave(self, clave: str)->ContImag:
        """Devuelve el contenedor de la primera imagen con la clave seleccionada. Se presupone que dicha clave existe."""
        return imagen_clave(clave, self.controls)


    def indice_clave(self, clave: str)->int|None:
        """Devuelve el indice de la primera imagen con la clave seleccionada. Si dicha clave no se encuentra se devuelve 'None'"""
        return indice_clave(clave, self.controls)


    def cargar_imagenes(self, imagenes: list[ContImag],  cuadricula=True):
        """Este metodo carga imagenes de tipo ft.Image creadas externamente"""
        self.wrap = cuadricula # version galería (si es 'False' las imagenes van en linea)
        self.numero = len(imagenes)
        self.controls = imagenes 


    def eventos(self, click = None, hover = None, longpress = None ):
        """Este metodo asigna handlers para todos los componentes de la galeria"""
        for contenedor in self.controls:
            contenedor.eventos(click, hover, longpress)

    @property
    def alto(self):
        return self.height

    @alto.setter
    def alto(self, valor):
        self.height = valor

    @property
    def ancho(self):
        """Lee el ancho maximo de galeria"""
        return self.width

    @ancho.setter
    def ancho(self, valor):
        """Establece el ancho maximo de galeria"""
        self.width = valor
  


def rutas_imagenes_picsum(numero: int, dim = 200 ):
    """Funcion auxiliar: busca imagenes online en Picsum.
    Permite elegir el número y tamaño de las imagenes.
    """
    rutas_imagenes = []
    for i in range(numero):
        ruta = f"https://picsum.photos/{dim}/{dim}?{i}"
        rutas_imagenes.append(ruta)
    return rutas_imagenes


def leer_imagenes(rutas_imagen: list[str], ancho=256, alto=256, redondeo=0,  cuadricula=True):
    """Esta funcion crea contenedores con imagenes internas incluidas.
    También asigna una clave ('key') a cada una.
    """
    contenedores = [] 
    for i in range( len(rutas_imagen)):
        contenedor = ContenedorImagen(rutas_imagen[i], ancho, alto, redondeo)
        # contenedor.content.key = str(i)
        contenedor.content.key = f"imag_{i}"
        contenedores.append(contenedor)
    return contenedores


def clave_imagen_correcta(key, x: ContImag):
    """Compara la clave interna del contenedor de imagen con la clave indicada"""
    return True if key == x.clave else False


def imagen_clave(clave: str, imagenes: list[ContImag])->ContImag:
    """Devuelve el contenedor de la primera imagen con la clave seleccionada. Se presupone que dicha clave existe."""
    key_imagen = lambda x: clave_imagen_correcta(clave, x)
    objeto_filtrado = filter(key_imagen ,imagenes)
    imagenes_clave = list(objeto_filtrado)
    return imagenes_clave[0]


def indice_clave(clave: str, imagenes: list[ContImag])->int|None:
    """Devuelve el indice de la primera imagen con la clave seleccionada. Si dicha clave no se encuentra se devuelve 'None'"""
    key_imagen = lambda x: clave_imagen_correcta(clave, x)
    objeto_filtrado = filter(key_imagen ,imagenes)
    imagenes_clave = list(objeto_filtrado)
    if len(imagenes_clave) > 0:
        return imagenes.index(imagenes_clave[0])
    else:
        return None


def nombre_imagen_correcto(nombre: str, contenedor: ContImag ):
    """Verifica que el nombre de archivo sea el correcto"""
    return nombre == pathlib.Path(contenedor.ruta_imagen).name


def imagen_nombre(nombre: str, imagenes: list[ContImag]):
    """Devuelve el contenedor de imagen con el nombre de archivo"""
    name_imagen = lambda x: nombre_imagen_correcto(nombre, x)
    objeto_filtrado = filter(name_imagen, imagenes)
    return list(objeto_filtrado)[0]


# demo
if __name__ == "__main__":

    def pagina_galeria(page: ft.Page):
        
        # parametros de ejemplo
        numero_imagenes =  15
        rutas_imagenes = rutas_imagenes_picsum(numero_imagenes, 256 )

        # estilos para contenedores 
        estilo_defecto = EstiloContenedor(
            width = 300,
            height = 300,
            border_radius = 50, 
            bgcolor = ft.colors.BLUE_400,
            border=ft.border.all(20, ft.colors.INDIGO_100),
            )

        estilo_click = EstiloContenedor(
            width = 300,
            height = 300,
            border_radius = 5,
            bgcolor = ft.colors.RED_900,
            border = ft.border.all(20, ft.colors.PURPLE_900),
            )   

        estilo_hover = EstiloContenedor(
            width = 300,
            height = 300,
            border_radius = 50, 
            bgcolor = ft.colors.AMBER_400,
            border=ft.border.all(20, ft.colors.ORANGE_600),
            )


        # Funciones para los eventos del mouse que producirán un cambio de estilo del contenedor afectado
        def funcion_click(e: ft.ControlEvent):
            cont = e.control 
            cont.estilo(estilo_click)
            print("click: ", cont.content.key)
            cont.update()

        def funcion_hover(e: ft.ControlEvent):
            cont = e.control 
            cont.estilo(estilo_hover)
            cont.update()

        def funcion_longpress(e: ft.ControlEvent): 
            cont = e.control        
            cont.estilo(estilo_defecto)
            cont.update()

        # Maquetado
        # componente galeria de contenedores con imágenes
        galeria = Galeria()
        page.add(galeria)

        # galeria.leer_imagenes(rutas_imagenes, redondeo = 30)
        imagenes = leer_imagenes(rutas_imagenes, redondeo = 30)
        galeria.cargar_imagenes(imagenes)
        galeria.estilo(estilo_defecto)
        galeria.eventos(
            click = funcion_click,
            hover = funcion_hover,
            longpress = funcion_longpress
            )

        def scroll_to_key(clave, e):
            # galeria.scroll_to(key=str(n), duration=1000)
            galeria.scroll_to(key=clave, duration=1000)
            print(f"Imagen con clave: {clave}")

        m = 0 
        clave = f"imag_{m}" 
        boton_inicio = ft.ElevatedButton(  
            text="Inicio",    
            bgcolor=ft.colors.RED_800, 
            color=ft.colors.WHITE,
            on_click=partial(scroll_to_key, clave)
            )

        m = int((numero_imagenes-1)/2)  
        clave = f"imag_{m}" 
        boton_medio = ft.ElevatedButton(
            text="Medio",    
            bgcolor=ft.colors.AMBER_800, 
            color=ft.colors.WHITE, 
            on_click=partial(scroll_to_key, clave)
            )

        m = numero_imagenes - 1 
        clave = f"imag_{m}" 
        boton_fin = ft.ElevatedButton(   
            text="Fin",    
            bgcolor=ft.colors.GREEN_800, 
            color=ft.colors.WHITE,
            on_click=partial(scroll_to_key, clave)
            )

        page.add(ft.Row([boton_inicio, boton_medio, boton_fin]))

        # dimensiones componente
        # galeria.ancho = 1400      # ancho maximo
        # galeria.alto = 600
        galeria.update()

        # Elementos generales de la pagina
        page.title = "Galería Imágenes"
        page.window_width  = 1500
        page.window_height =  800
        page.theme_mode = ft.ThemeMode.LIGHT
        # page.theme_mode = ft.ThemeMode.DARK

        page.padding = 10
        page.update()


    # creacion de ventana
    ft.app(target = pagina_galeria)
