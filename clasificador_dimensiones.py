


from rich import print as print
import flet as ft
import pathlib

# from manejo_texto.procesar_etiquetas import Etiquetas, guardar_archivo, etiquetas2texto, separar_etiquetas

from manejo_imagenes.verificar_dimensiones import dimensiones_imagen

from sistema_archivos.buscar_extension import buscar_imagenes, listar_directorios

from constantes.constantes import Tab, Percentil, Estados, tupla_estados

from estilos.estilos_contenedores import estilos_seleccion, estilos_galeria, Estilos

from componentes.galeria_imagenes import Galeria, Contenedor, ContenedorImagen, imagen_clave,indice_clave, ContImag
# from componentes.filas_botones import FilasBotonesEtiquetas
from componentes.lista_desplegable import crear_lista_desplegable,opciones_lista_desplegable, convertir_dimensiones_opencv, extraer_numeros, tupla_resoluciones
from componentes.contenedor_etiquetado import ContenedorEtiquetado, leer_imagenes_etiquetadas
from componentes.galeria_estados import GaleriaEstados, actualizar_estilo_estado
from componentes.clasificador_estados import filtrar_dimensiones 
# from componentes.clasificador_etiquetas import filtrar_etiquetas
from componentes.dialogo_alerta import DialogoAlerta

# from vistas.etiquetador.dialogos import dialogo_dataset, dialogo_directorio, dialogo_guardado_tags
from vistas.etiquetador.dialogos import dialogo_directorio
# from vistas.etiquetador.columna_etiquetas import entrada_tags_agregar,entrada_tags_quitar
# from vistas.etiquetador.columna_etiquetas import entrada_tags_buscar
# from vistas.etiquetador.columna_etiquetas import filas_filtrado, columna_etiquetas, texto_contador_tags
# from vistas.etiquetador.columna_etiquetas import boton_reset_tags, boton_guardar_dataset, boton_reordenar_tags
# from vistas.etiquetador.columna_etiquetas import estadisticas
from vistas.etiquetador.columna_seleccion import texto_imagen, texto_ruta_data,texto_ruta_titulo,texto_tags_data,texto_tags_titulo
from vistas.etiquetador.columna_seleccion import columna_seleccion, contenedor_seleccion
from vistas.etiquetador.columna_seleccion import imagen_seleccion
from vistas.etiquetador.clasificador import clasificador_imagenes 
from vistas.etiquetador.menu_etiquetador import boton_carpeta, boton_dataset, tooltip_carpeta, ayuda_emergente
from vistas.etiquetador.menu_etiquetador import fila_controles, lista_dimensiones_desplegable, lista_estados_desplegable
from vistas.etiquetador.menu_etiquetador import actualizar_lista_dimensiones
# from vistas.etiquetador.columna_etiquetador import etiquetador_imagen, crear_botones_etiquetador




galeria_etiquetador = GaleriaEstados( estilos_galeria )


galeria_seleccion = GaleriaEstados( estilos_galeria )




def main(pagina: ft.Page):

    # estructura con data global
    # dataset = Etiquetas("") 

    # tags_teclado = Etiquetas("") 

    ############# COMPONENTES GRAFICOS ######################## 


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

    columna_seleccion.visible = False

    ############## HANDLERS ##################################


    # Funcion de apertura de directorio
    def resultado_directorio(e: ft.FilePickerResultEvent):
        """Carga las imagenes del proyecto."""
        if e.path:
            # busqueda 
            clasificador_imagenes.ruta_directorio =  e.path
            directorio = clasificador_imagenes.ruta_directorio

            ventana_emergente(pagina, f"Buscando imágenes...\nRuta: {directorio} ")
            rutas_imagen = buscar_imagenes(directorio)
        
            # lectura de imagenes del directorio
            imagenes_etiquetadas = leer_imagenes_etiquetadas(rutas_imagen)
            clasificador_imagenes.cargar_imagenes(imagenes_etiquetadas)

            clasificador_imagenes.seleccionar_estado(Estados.TODOS.value)
            clasificador_imagenes.filtrar_etiquetas()

            # asignacion de la primera imagen de la galeria 
            clave = clasificador_imagenes.clave_actual
            if len(clasificador_imagenes.seleccion)>0:         
                clave = clasificador_imagenes.seleccion[0].clave
                # etiquetador_imagen.setear_salida(clasificador_imagenes.seleccion[0]) # Previene falsas modificaciones al cambiar de carpeta
                # reporte por snackbar
                ventana_emergente(pagina, f"Directorio de imagenes abierto.\nRuta: {directorio} \nNº imágenes: {len(clasificador_imagenes.seleccion)}")
 
            else:
                clave = ""
                # reporte por snackbar
                ventana_emergente(pagina, f"Directorio de imagenes vacío.\nRuta: {directorio} ")


            clasificador_imagenes.clave_actual = clave
            # se descartan los tamaños de imagen no disponibles
            actualizar_lista_dimensiones() 
            lista_dimensiones_desplegable.update()
            # relectura del archivo dataset (puede no existir)
            # dataset.ruta = clasificador_imagenes.ruta_dataset
            # dataset.leer_archivo()
            # actualizacion de la app
            cargar_galeria_componentes()




    def cargar_galeria_componentes(  e: ft.ControlEvent | None = None ):
        """Muestra las imagenes encontradas y las asigna a los componentes de seleccion y etiquetado. Si no hay imágenes que mostra oculta y/o inhabilita componentes."""
    
        # si se encuentran imagenes se visibilizan y configuran los controles
        filtrar_dimensiones_estados()   
        # agregado de todas las etiquetas al editor
        # crear_botones_etiquetador(dataset)  

        # actualizar galeria
        actualizar_estilo_estado( clasificador_imagenes.seleccion, estilos_galeria )

        # actualizacion grafica
        actualizar_componentes()



    def filtrar_dimensiones_estados( e: ft.ControlEvent | None = None):
        """Selecciona solamente aquellas imagenes que cumplan con el tamaño y estado especificados."""

        # conversion de texto a tupla numerica de dimensiones de imagen elegida
        opcion = lista_dimensiones_desplegable.value
        dimensiones_elegidas = convertir_dimensiones_opencv(str(opcion))

        clasificador_imagenes.dimensiones_elegidas = dimensiones_elegidas

        # Filtrado en base a los estados de las imagenes
        estado = lista_estados_desplegable.value
        clasificador_imagenes.seleccionar_estado( estado )

        # reporte por snackbar 
        if len(clasificador_imagenes.todas) > 0 and estado != None:
            ventana_emergente(pagina, f"Filtrado por dimensiones y estado - {len(clasificador_imagenes.seleccion)} imagenes seleccionadas.")
        # actualizacion de las etiquetas encontradas
        estadisticas()
        # filas_filtrado.evento_click(filtrar_todas_etiquetas)
        columna_etiquetas.update()



    def ventana_emergente(pagina:ft.Page, texto: str):
        # show_snack_bar obsoleta desde la v0.23 
        pagina.show_snack_bar(
        # pagina.open(
            ft.SnackBar(ft.Text(texto), open=True, show_close_icon=True)
        )


    def actualizar_componentes( e: ft.ControlEvent | None = None):
        """Asigna la imagen actual a los componentes de seleccion y etiquetado en base a la 'clave' global.
        Si ésta no se encuentra en la galeria actual busca la primera imagen disponible y actualiza la clave.
        Tambien carga las imagenes disponibles a la galeria gráfica.
        Si la galeria queda vacia se ocultan los componentes graficos.
        """
        clave = clasificador_imagenes.clave_actual
        # actualizar galeria
        galeria_etiquetador.cargar_imagenes( clasificador_imagenes.seleccion )
        # galeria_etiquetador.eventos(click = click_imagen_galeria)
        galeria_etiquetador.update()

        if len(clasificador_imagenes.seleccion)>0:
            # busqueda imagen
            indice = indice_clave(clave, clasificador_imagenes.seleccion)
            # si la clave actual no se encuentra se toma la primera imagen disponible
            if indice == None:

                print(f"[bold magenta]Imagen '[bold yellow]{clave}' [bold magenta]no disponible en galeria")
                clave = clasificador_imagenes.seleccion[0].clave
                clasificador_imagenes.clave_actual = clave
                print(f"[bold magenta]Imagen '[bold yellow]{clave}' [bold magenta]como sustituto\n")


            # seleccion imagen
            imagen_elegida = imagen_clave(clave, clasificador_imagenes.seleccion)

            # etiquetador_imagen.setear_salida(imagen_elegida) # original
            imagen_seleccion(imagen_elegida)

            columna_seleccion.visible = True
            columna_seleccion.update()

        else:
            # ocultamiento de componentes graficos
            columna_etiquetas.visible = True
            columna_etiquetas.update()
            columna_seleccion.visible = True
            columna_seleccion.update()



    def redimensionar_controles(e: ft.ControlEvent | None):

        # redimensionado 
        filas_filtrado.altura = pagina.height - 400

        columna_etiquetas.height = pagina.height 
        columna_etiquetas.update()
        # etiquetador_imagen.update()
        fila_controles.width = pagina.width 
        fila_controles.update() 


    ###########  FUNCIONES LOCALES #################


    def apuntar_galeria(clave: str):
        """Funcion auxiliar para buscar y mostrar la imagen requerida en base a su clave ('key')."""
        galeria_etiquetador.scroll_to(key=clave, duration=500)


    ###########  ASIGNACION HANDLERS #################

    pagina.on_resized = redimensionar_controles

    lista_dimensiones_desplegable.on_change = cargar_galeria_componentes    
    lista_estados_desplegable.on_change = cargar_galeria_componentes     

    # handler para manejar dialogos de archivo y de carpeta
    dialogo_directorio   .on_result = resultado_directorio 

    # Añadido de diálogos a la página
    pagina.overlay.extend([
            dialogo_directorio, 
            # dialogo_dataset, 
            # dialogo_guardado_tags
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