
from copy import deepcopy 

from rich import print as print
import flet as ft
import pathlib

from manejo_imagenes.verificar_dimensiones import dimensiones_imagen

from sistema_archivos.buscar_extension import buscar_imagenes, listar_directorios
from sistema_archivos.rutas import ruta_relativa_usuario

from constantes.constantes import Tab, Percentil, Estados, tupla_estados

from estilos.estilos_contenedores import estilos_seleccion, estilos_galeria, Estilos

from componentes.lista_desplegable import crear_lista_desplegable,opciones_lista_desplegable, convertir_dimensiones_opencv, extraer_numeros, tupla_resoluciones
from componentes.contenedor_etiquetado import ContenedorEtiquetado, leer_imagenes_etiquetadas
from componentes.galeria_estados import GaleriaEstados, actualizar_estilo_estado
from componentes.clasificador_estados import filtrar_dimensiones 
from componentes.dialogo_alerta import DialogoAlerta

from vistas.clasificador.dialogos import dialogo_directorio_origen, dialogo_directorio_destino
from vistas.clasificador.menu import boton_carpeta_origen, boton_carpeta_destino, ayuda_emergente
from vistas.clasificador.menu import fila_controles, lista_dimensiones_desplegable, lista_estados_desplegable
from vistas.clasificador.menu import actualizar_lista_dimensiones


galeria_etiquetador = GaleriaEstados( estilos_galeria )
galeria_seleccion = GaleriaEstados( estilos_galeria )

imagenes_etiquetadas = []
imagenes_seleccionadas = []


def main(pagina: ft.Page):


    #############  MAQUETADO ############################

    galeria_etiquetador.expand = 1
    galeria_seleccion.expand = 1


    altura_galerias = 800

    fila_galerias = ft.Row(
        [galeria_etiquetador, ft.VerticalDivider(), galeria_seleccion],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        vertical_alignment=ft.CrossAxisAlignment.START,
        wrap = False,
        expand=True,
        height = altura_galerias,
        )

    pagina.add(fila_controles)  
    pagina.add(ft.Divider(height=7, thickness=1))


    pagina.add(fila_galerias)

    # columna_seleccion.visible = False

    ############## HANDLERS ##################################


    # Funcion de apertura de directorio
    def resultado_directorio_origen(e: ft.FilePickerResultEvent):
        """Carga las imagenes del proyecto."""
        global imagenes_etiquetadas
        if e.path:
            # busqueda 
            directorio = e.path
            ventana_emergente(pagina, f"Buscando imágenes...\nRuta: {directorio} ")
            rutas_imagen = buscar_imagenes(directorio)
        
            # lectura de imagenes del directorio
            imagenes_etiquetadas = leer_imagenes_etiquetadas(rutas_imagen)

            if len(imagenes_etiquetadas)>0:         
                # reporte por snackbar
                ventana_emergente(pagina, f"Directorio de imagenes abierto.\nRuta: {directorio} \nNº imágenes: {len(imagenes_etiquetadas)}")
                # habilitacion de boton destino
                boton_carpeta_destino.disabled = False
                boton_carpeta_destino.update()
            else:
                # reporte por snackbar
                ventana_emergente(pagina, f"Directorio de imagenes vacío.\nRuta: {directorio} ")
                # deshabilitacion de boton destino
                boton_carpeta_destino.disabled = True
                boton_carpeta_destino.update()

            # ruta de carpeta en el tooltip de boton
            boton_carpeta_origen.tooltip = ruta_relativa_usuario(directorio)
            boton_carpeta_origen.update()

            # se descartan los tamaños de imagen no disponibles
            actualizar_lista_dimensiones(imagenes_etiquetadas) 
            lista_dimensiones_desplegable.update()
            
            # actualizacion de la app
            cargar_galeria_componentes()
            # actualizar_estilo_estado( imagenes_etiquetadas, estilos_galeria )


    def resultado_directorio_destino(e: ft.FilePickerResultEvent):
        """Carga las imagenes del proyecto."""

        return      # FIX


        global imagenes_etiquetadas
        if e.path:
            # busqueda 
            directorio = e.path
            ventana_emergente(pagina, f"Buscando imágenes...\nRuta: {directorio} ")
            rutas_imagen = buscar_imagenes(directorio)
        
            # lectura de imagenes del directorio
            imagenes_etiquetadas = leer_imagenes_etiquetadas(rutas_imagen)

            # if len(imagenes_etiquetadas)>0:         
            #     # reporte por snackbar
            #     ventana_emergente(pagina, f"Directorio de imagenes abierto.\nRuta: {directorio} \nNº imágenes: {len(imagenes_etiquetadas)}")
            #     # habilitacion de boton destino
            #     boton_carpeta_destino.disabled = False
            #     boton_carpeta_destino.update()
            # else:
            #     # reporte por snackbar
            #     ventana_emergente(pagina, f"Directorio de imagenes vacío.\nRuta: {directorio} ")
            #     # deshabilitacion de boton destino
            #     boton_carpeta_destino.disabled = True
            #     boton_carpeta_destino.update()

            # ruta de carpeta en el tooltip de boton
            boton_carpeta_origen.tooltip = ruta_relativa_usuario(directorio)
            boton_carpeta_origen.update()

            # se descartan los tamaños de imagen no disponibles
            actualizar_lista_dimensiones(imagenes_etiquetadas) 
            lista_dimensiones_desplegable.update()
            
            # actualizacion de la app
            # cargar_galeria_componentes()



    def cargar_galeria_componentes(  e: ft.ControlEvent | None = None ):
        """Muestra las imagenes encontradas y las asigna a los componentes de seleccion y etiquetado. Si no hay imágenes que mostra oculta y/o inhabilita componentes."""
    
        # conversion de texto a tupla numerica de dimensiones de imagen elegida
        opcion = lista_dimensiones_desplegable.value
        dimensiones = convertir_dimensiones_opencv(str(opcion))

        # print(dimensiones)

        global imagenes_etiquetadas, imagenes_seleccionadas 

        seleccion = filtrar_dimensiones(imagenes_etiquetadas, dimensiones)   

        # FIX 
        # imagenes_seleccionadas = deepcopy(seleccion)        # MAL
        imagenes_seleccionadas = seleccion.copy()
        # imagenes_seleccionadas = list(seleccion)

        # print(len(imagenes_seleccionadas))

        galeria_etiquetador.cargar_imagenes( imagenes_etiquetadas   )       
        galeria_seleccion  .cargar_imagenes( imagenes_seleccionadas )        

        # actualizar_estilo_estado( imagenes_seleccionadas, estilos_galeria )
        galeria_etiquetador.update()
        galeria_seleccion.update()


        actualizar_estilo_estado( imagenes_etiquetadas, estilos_galeria )
        actualizar_estilo_estado( imagenes_seleccionadas, estilos_galeria )



    def ventana_emergente(pagina:ft.Page, texto: str):
        # show_snack_bar obsoleta desde la v0.23 
        pagina.show_snack_bar(
        # pagina.open(
            ft.SnackBar(ft.Text(texto), open=True, show_close_icon=True)
        )


    def redimensionar_controles(e: ft.ControlEvent | None):

        # redimensionado 
        filas_filtrado.altura = pagina.height - 400

        columna_etiquetas.height = pagina.height 
        columna_etiquetas.update()
        # etiquetador_imagen.update()
        fila_controles.width = pagina.width 
        fila_controles.update() 


    ###########  ASIGNACION HANDLERS #################

    pagina.on_resized = redimensionar_controles

    lista_dimensiones_desplegable.on_change = cargar_galeria_componentes    
    lista_estados_desplegable.on_change = cargar_galeria_componentes     

    # handler para manejar dialogos de archivo y de carpeta
    dialogo_directorio_origen.on_result = resultado_directorio_origen 
    dialogo_directorio_destino.on_result = resultado_directorio_destino 

    # Añadido de diálogos a la página
    pagina.overlay.extend([
            dialogo_directorio_origen, 
            dialogo_directorio_destino, 
        ])


    ############## CONFIGURACIONES GRAFICAS ################     
     
    ancho_pagina = 1400

    galeria_etiquetador.ancho = ancho_pagina 
    fila_controles.width = ancho_pagina 

    # Propiedades pagina 
    pagina.title = "Clasificador Imágenes"
    pagina.window_width  = ancho_pagina
    pagina.window_min_width  = 1024
    pagina.window_height = 900
    # pagina.theme_mode = ft.ThemeMode.DARK
    pagina.theme_mode = ft.ThemeMode.LIGHT
    pagina.window_maximizable = True
    pagina.window_minimizable = True
    pagina.window_maximized   = False
    pagina.update()
    


if __name__ == "__main__":
    ft.app(target=main)