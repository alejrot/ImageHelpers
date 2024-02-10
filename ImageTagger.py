from rich import print as print
import flet as ft

import re

from manejo_texto.procesar_etiquetas import Etiquetas 

from componentes.galeria_imagenes import Galeria, Contenedor, Contenedor_Imagen, Estilo_Contenedor
from componentes.menu_navegacion import  MenuNavegacion
from componentes.etiquetador_botones import EtiquetadorBotones

from sistema_archivos.buscar_extension import buscar_imagenes


def nada( e ):
    pass


class Contenedor_Etiquetado( Etiquetas, Contenedor_Imagen):
    def __init__(self, ruta, ancho=768, alto=768, redondeo=0):
        Etiquetas.__init__(self, ruta)
        Contenedor_Imagen.__init__(self,ruta, ancho, alto, redondeo)
        self.__etiquetada = False
        self.__guardada = False
        self.__defectuosa = False
        self.verificar_imagen()
        self.verificar_etiquetado()
        self.verificar_guardado(None)


    def verificar_imagen(self):
        """NO IMPLEMENTADA AUN - Este metodo verificará extension y dimensiones de archivo"""
        self.__defectuosa = False

    @property
    def defectuosa(self):
        return self.__defectuosa

    def verificar_etiquetado(self):
        """Verifica si hay etiquetas en la imagen, ya sea guardadas o sin guardar """
        self.__etiquetada = True if len(self.tags) > 0 else False


    @property
    def etiquetada(self):
        return self.__etiquetada 


    def verificar_guardado(self , tags: list[str] | None):
        """Comprueba si las etiquetas actuales son las mismas que las guardas en archivo de texto"""
        archivado = Etiquetas(self.ruta)
        # etiquetado = self.verificar_etiquetado()
        if tags == None:
            guardado = True if set(self.tags) == set(archivado.tags) else False   # si los tags son iguales da True; en caso contrario da False
        else:    
            guardado = True if set(tags) == set(archivado.tags) else False   # si los tags son iguales da True; en caso contrario da False
        # se lee cuantas etiquetas hay en archivo
        etiquetado = True if len(archivado.tags) > 0 else False
        self.__guardada = guardado  and etiquetado     # se descartan no etiquetados
        # print(etiquetado, guardado, self.__guardada)


    @property
    def guardada(self):
        return self.__guardada 

    @guardada.setter
    def guardada(self, valor: bool):
        self.__guardada = valor


class MenuEtiquetado( MenuNavegacion):
    def __init__(self, estilos: dict):
        super().__init__()
        self.estilos = estilos
        self.alto  = 800
        self.ancho = 600
        

    def cargar_imagen(self):
        """"Este metodo carga la imagen y cambia el estilo del contenedor segun el estado del etiquetado"""
        super().cargar_imagen()
        indice = self.indice
        contenedor_imagen = self.imagenes[indice]
        # seleccion de estilo segun jerarquia
        actualizar_estilo_estado( [contenedor_imagen], self.estilos)


    def cargar_imagenes(self, imagenes: list[Contenedor]):
        super().cargar_imagenes(imagenes)
        actualizar_estilo_estado( imagenes, self.estilos)


class GaleriaEtiquetado( Galeria):
    def __init__(self, estilos: dict):
        super().__init__()
        self.estilos = estilos

    def leer_imagenes(self, rutas_imagen: list[str], ancho=256, alto=256, redondeo=0,  cuadricula=True):
        self.wrap = cuadricula # version galería (si es 'False' las imagenes van en linea)
        
        contenedores = leer_imagenes_etiquetadas(rutas_imagen, ancho, alto, redondeo)
        self.numero = len(contenedores)
        self.controls = contenedores

        actualizar_estilo_estado( contenedores, self.estilos)


    def cargar_imagenes(self, 
        imagenes: list[Contenedor_Etiquetado | Contenedor_Imagen], 
        cuadricula=True):
        super().cargar_imagenes(imagenes, cuadricula)
        actualizar_estilo_estado( imagenes, self.estilos)  # FIX


def actualizar_estilo_estado(
    contenedores: list[Contenedor_Etiquetado], estilos : dict ):
    for contenedor in contenedores:
        if contenedor.defectuosa :
            estilo = estilos["erroneo"]     
        elif contenedor.guardada :
            estilo = estilos["guardado"]
        elif contenedor.etiquetada :
            estilo = estilos["modificado"]
        else: 
            estilo = estilos["predefinido"]

        contenedor.estilo( estilo )


def leer_imagenes_etiquetadas(rutas_imagen: list[str], ancho=1024, alto=1024, redondeo=0):
    """Esta funcion crea lee imagenes desde archivo y crea una lista de objetos ft.Image.
    También asigna una clave ('key') a cada una.
    """
    contenedores = [] 
    for i in range( len(rutas_imagen)):
        contenedor = Contenedor_Etiquetado(rutas_imagen[i], ancho, alto, redondeo)
        # contenedor.content.key = str(i)
        contenedor.content.key = f"imag_{i}"
        contenedores.append(contenedor)
    return contenedores


# estilos para contenedores 
estilo_galeria_defecto = Estilo_Contenedor(
    width = 256, 
    height = 256,
    border_radius = 10, 
    bgcolor = ft.colors.BLUE_100,
    border=ft.border.all(5, ft.colors.INDIGO_100)
    )

estilo_galeria_modificado = Estilo_Contenedor(
    width = 256, 
    height = 256,
    border_radius = 10, 
    bgcolor = ft.colors.YELLOW_600,
    border=ft.border.all(5, ft.colors.AMBER_600)
    )

estilo_galeria_guardado = Estilo_Contenedor(
    width = 256, 
    height = 256,
    border_radius = 10, 
    bgcolor = ft.colors.LIME_800,
    border=ft.border.all(5, ft.colors.GREEN_800)
    )

estilo_galeria_erroneo = Estilo_Contenedor(
    width = 256, 
    height = 256,
    border_radius = 10, 
    bgcolor = ft.colors.RED_800,
    border=ft.border.all(5, ft.colors.BROWN_800)
    )

estilos_galeria = {
    "predefinido" : estilo_galeria_defecto,
    "modificado" : estilo_galeria_modificado,
    "guardado" : estilo_galeria_guardado,
    "erroneo" : estilo_galeria_erroneo
    }


# estilos para el contenedor 
estilo_menu_defecto = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.BLUE_100,
    border=ft.border.all(10, ft.colors.INDIGO_100)
    )

estilo_menu_modificado = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.YELLOW_600,
    border=ft.border.all(10, ft.colors.AMBER_600)
    )

estilo_menu_guardado = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.LIME_800,
    border=ft.border.all(10, ft.colors.GREEN_800)
    )

estilo_menu_erroneo = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.RED_800,
    border=ft.border.all(10, ft.colors.BROWN_800)
    )

estilos_seleccion = {
    "predefinido" : estilo_menu_defecto,
    "modificado" : estilo_menu_modificado,
    "guardado" : estilo_menu_guardado,
    "erroneo" : estilo_menu_erroneo
    }


def main(pagina: ft.Page):

    ###########  FUNCIONES LOCALES #################

    # Creacion de imagenes con su propio contenedor por duplicado con distintas resoluciones
    # (Compartir una misma imagen en distintos contenedores funciona mal)
    def cargar_imagenes(rutas: list[str]):
        # Imagenes - objetos ft.Image con etiquetas leidas desde archivo TXT
        etiquetadas = []
        etiquetadas = leer_imagenes_etiquetadas(
            rutas,
            ancho=768,
            alto=768, 
            redondeo=30
            )
        # replica de imagenes para la galeria - menor resolucion
        galeria = []
        galeria = leer_imagenes_etiquetadas(
            rutas,
            ancho=256,
            alto=256, 
            redondeo=10
            )
        return [etiquetadas, galeria]

    ############# COMPONENTES ######################## 

    # Botones apertura de ventana emergente
    boton_carpeta = ft.ElevatedButton(
        text = "Abrir carpeta",
        icon=ft.icons.FOLDER_OPEN,
        bgcolor=ft.colors.RED,
        color= ft.colors.WHITE,
        ## manejador
        on_click=lambda _: dialogo_directorio.get_directory_path(
            dialog_title="Elegir carpeta con todas las imágenes"
        ),
    )

    boton_dataset = ft.ElevatedButton(
        text = "Abrir dataset",
        icon=ft.icons.FILE_OPEN,
        bgcolor=ft.colors.BLUE,
        color= ft.colors.WHITE,
        ## manejador
        on_click=lambda _: dialogo_dataset.pick_files(
            dialog_title= "Elegir archivo TXT con todas las etiquetas",
            allowed_extensions=["txt"],
            allow_multiple=False,
        )
    )
    
    # Componentes gráficos
    etiquetador_imagen = EtiquetadorBotones()
    galeria = GaleriaEtiquetado( estilos_galeria )
    menu_seleccion = MenuEtiquetado( estilos_seleccion)

    #############  MAQUETADO ############################

    # Fila de botones para abrir carpetas y leer archivos
    pagina.add(ft.Row([
        boton_carpeta,
        boton_dataset
        ]))

    #pestaña de galeria
    tab_galeria = ft.Tab(
        text="Galeria",
        content=galeria,
        )

    # pestaña de etiquetado y navegacion de imagenes
    altura_tab_etiquetado = 800
    fila_etiquetado_navegacion = ft.Row(
        controls = [ 
            menu_seleccion ,
            ft.VerticalDivider(),
            etiquetador_imagen
            ], 
        spacing = 10, 
        height = altura_tab_etiquetado
    ) 
    tab_etiquetado = ft.Tab(
        text="Etiquetado",
        content=fila_etiquetado_navegacion,
    )

    # organizacion en pestañas
    pestanias = ft.Tabs(
        selected_index=0,
        animation_duration=500,
        tabs=[
            tab_galeria   ,
            tab_etiquetado
        ],
        expand=1,
        # disabled=True,        # deshabilita controles internos, no las pestañas en si
    )

    # Añadido componentes (todos juntos)
    pagina.add(pestanias)

    ############## HANDLERS ##################################

    def etiquetas_a_imagen(indice: int):
        global imagenes_etiquetadas
        global imagenes_galeria
        # Se transfieren los botones de la botonera a las imagenes 
        etiquetas_botones = etiquetador_imagen.leer_botones()
        imagenes_galeria[indice].tags = etiquetas_botones
        imagenes_etiquetadas[indice].tags = etiquetas_botones
        # etiquetador_imagen.update()
        return etiquetas_botones


    def etiquetas_a_botones(indice: int):
        global imagenes_etiquetadas
        # Se transfieren los botones de la imagen  a la botonera 
        # etiquetas_botones = etiquetador_imagen.leer_botones()
        etiquetas_imagen = imagenes_etiquetadas[indice].tags 

        # actualizacion grafica
        etiquetador_imagen.asignar_etiquetas(etiquetas_imagen)
        return etiquetas_imagen


    def actualizar_bordes( e: ft.ControlEvent ):

        # acceso a elementos globales
        global imagenes_etiquetadas
        global imagenes_galeria

        indice = menu_seleccion.indice

        # Se transfieren los botones de la botonera a las imagenes 
        etiquetas_botones = etiquetas_a_imagen(indice)
        # indice = menu_seleccion.indice
        # etiquetas_botones = etiquetador_imagen.leer_botones()
        # imagenes_galeria[indice].tags = etiquetas_botones
        # imagenes_etiquetadas[indice].tags = etiquetas_botones

        # actualizacion bordes galeria
        imagenes_galeria[indice].verificar_etiquetado()
        imagenes_galeria[indice].verificar_imagen()
        imagenes_galeria[indice].verificar_guardado(etiquetas_botones)
        imagenes_galeria[indice].update()

        # actualizacion bordes selector
        imagenes_etiquetadas[indice].verificar_etiquetado()
        imagenes_etiquetadas[indice].verificar_imagen()
        imagenes_etiquetadas[indice].verificar_guardado(etiquetas_botones) 
        imagenes_etiquetadas[indice].update()

        menu_seleccion.cargar_imagen()
        menu_seleccion.update()

        galeria.cargar_imagenes( imagenes_galeria )
        galeria.update()
        

    # Funcion de apertura de directorio
    def resultado_directorio(e: ft.FilePickerResultEvent):
        if e.path:

            # acceso a elementos globales
            global imagenes_etiquetadas
            global imagenes_galeria
            # busqueda 
            directorio = e.path
            rutas_imagen = buscar_imagenes(directorio)
            # Carga de imagenes del directorio
            imagenes_etiquetadas, imagenes_galeria = cargar_imagenes(rutas_imagen)

            # Objeto galeria
            galeria.cargar_imagenes( imagenes_galeria )
            galeria.eventos(click = click_imagen_galeria)
            galeria.update()

            # Objeto seleccion imagen
            menu_seleccion.cargar_imagenes(imagenes_etiquetadas)
            menu_seleccion.indice = 0
            menu_seleccion.cargar_imagen()
            menu_seleccion.eventos(
                click=click_imagen_seleccion,
                funcion_botones = lambda _ : click_botones_seleccion(_)
                )
            # actualizacion del etiquetador --> habilita los controles y etiquetas
            etiquetador_imagen.setear_salida(imagenes_etiquetadas[0])
            etiquetador_imagen.update()

            # actualizacion del selector de imagenes --> habilita los controles
            menu_seleccion.alto  = altura_tab_etiquetado
            menu_seleccion.ancho = 600
            menu_seleccion.expand = True
            menu_seleccion.habilitado = True
            menu_seleccion.update()

            # reporte por consola
            print("[bold red]Carga imagenes")
            print("[bold red]Nº imagenes etiquetadas : ", len(imagenes_etiquetadas))
            print("[bold red]Nº imagenes galeria     : ", len(imagenes_galeria))
        else:
            return


    # Funcion de apertura de archivo con etiquetas (dataset)
    def resultado_dataset(e: ft.FilePickerResultEvent):
        if e.files:

            ruta = e.files[0]                   # SOLO UN ARCHIVO DE LISTA ( FIX )
            archivo_dataset = ruta.path

            # Objeto etiquetador
            dataset = Etiquetas(archivo_dataset) 
            etiquetador_imagen.leer_dataset( dataset )

            # se asegura que los botones esten deshabilitados hasta abrir galeria
            etiquetador_imagen.habilitado = True if menu_seleccion.habilitado else False
            etiquetador_imagen.update() 

            etiquetador_imagen.alto  = altura_tab_etiquetado
            etiquetador_imagen.ancho = 500
            etiquetador_imagen.expand = True
            etiquetador_imagen.update()

            # Eventos de los botones
            # etiquetador_imagen.evento_click(funcion_etiqueta, funcion_grupos, funcion_comando)
            etiquetador_imagen.evento_click(
                actualizar_bordes,
                actualizar_bordes,
                actualizar_bordes
                )
            print("[bold cyan]Carga dataset")
            print("[bold cyan]Nombre archivo: ", archivo_dataset)

        else:
            return

    # Clase para manejar dialogos de archivo y de carpeta
    dialogo_directorio   = ft.FilePicker(on_result = resultado_directorio )
    dialogo_dataset      = ft.FilePicker(on_result = resultado_dataset)

    # Añadido de diálogos a la página
    pagina.overlay.extend([
            dialogo_directorio, dialogo_dataset
        ])


    def apuntar_galeria(clave):
        """Funcion auxiliar para buscar y mostrar la imagen requerida en base a su numero ('key')."""
        galeria.scroll_to(key=clave, duration=1000)


    def clave_imagen_correcta(key, x: Contenedor_Etiquetado):
        return True if key == x.content.key else False


    # Eventos galeria
    def click_imagen_galeria(e: ft.ControlEvent):
        """Esta imagen permite elegir una imagen desde la galeria y pasarla al selector de imagenes al tiempo que carga las etiquetas de archivo."""
        contenedor = e.control
        clave = contenedor.content.key

        global imagenes_etiquetadas
        global imagenes_galeria

        # actualizacion de imagen seleccionada y etiquetado
        key_imagen = lambda x: clave_imagen_correcta(clave, x)
        objeto_filtrado = filter(key_imagen ,imagenes_etiquetadas)
        imagen_seleccionada = list(objeto_filtrado)[0]

        # etiquetador_imagen.setear_salida(imagenes_etiquetadas[i])
        etiquetador_imagen.setear_salida(imagen_seleccionada)
        patron = r"[0-9]+" 
        retorno = re.search(patron, clave)
        indice_str = retorno.group()
        indice = int(indice_str)
        menu_seleccion.indice = indice
        # carga de etiquetas a los botones
        etiquetas_a_botones(indice)
        #cambio de pestaña
        pestanias.selected_index = 1
        # actualizacion grafica
        pagina.update()


    # Funcion para el click sobre la imagen seleccionada
    def click_imagen_seleccion( e: ft.ControlEvent):
        """Esta funcion regresa a la galería de imagenes cerca de la imagen seleccionada."""

        global imagenes_etiquetadas
        # global imagenes_galeria

        #regreso a la galeria
        indice = menu_seleccion.indice
        clave = imagenes_etiquetadas[indice].content.key
        apuntar_galeria( clave)   

        # carga de etiquetas a los botones
        etiquetas_a_botones(indice)

        #cambio de pestaña
        pestanias.selected_index=0
        pagina.update()


    def click_botones_seleccion( indice: int ):
        """ Esta funcion controla el cambio de imagen en el selector"""
        # (el cambio de imagen está integrado al componente)
        # actualizacion etiquetas
        global imagenes_etiquetadas
        global imagenes_galeria

        etiquetador_imagen.setear_salida(imagenes_etiquetadas[indice])
        # carga de etiquetas a los botones
        etiquetas_a_botones(indice)
        # actualizacion pagina
        tab_etiquetado.update()


    # manejador del teclado
    def desplazamiento_teclado(e: ft.KeyboardEvent):
        """Permite el desplazamiento rapido de imagenes con teclas del teclado predefinidas"""
        tecla = e.key   
        # Avance y retroseso de imagenes en seleccion y galeria
        incremento = 0
        if tecla == "Arrow Left" or tecla == "A":
            incremento = - 1     # retroceso
        elif tecla == "Arrow Right" or tecla == "D":
            incremento = 1      # avance
        # cambio de imagen seleccion
        menu_seleccion.cambiar_indice(incremento, 1 )


    # propiedad de pagina: handler del teclado elegido
    pagina.on_keyboard_event = desplazamiento_teclado

    def cambio_pestanias(e):
        indice = menu_seleccion.indice
        clave = imagenes_etiquetadas[indice].content.key
        if pestanias.selected_index == 0:
            apuntar_galeria(clave)

    pestanias.on_change = cambio_pestanias


    ############## CONFIGURACIONES GRAFICAS ################     
     
    galeria.ancho = 1200

    menu_seleccion.alto  = altura_tab_etiquetado
    # menu_seleccion.ancho = 600
    menu_seleccion.expand = True
    menu_seleccion.habilitado = False

    etiquetador_imagen.alto  = altura_tab_etiquetado
    etiquetador_imagen.ancho = 500
    etiquetador_imagen.expand = True
    etiquetador_imagen.habilitado = False

    # Propiedades pagina 
    pagina.title = "Etiquetador Imágenes"
    pagina.window_width  = 1500
    pagina.window_height = 900
    pagina.window_maximizable = True
    pagina.window_minimizable = True
    pagina.window_maximized   = False
    pagina.update()
    


if __name__ == "__main__":
    ft.app(target=main)