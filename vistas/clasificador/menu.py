import flet as ft

from componentes.contenedor_estados import ContenedorEstados
from componentes.lista_desplegable import crear_lista_desplegable,opciones_lista_desplegable, convertir_dimensiones_opencv, extraer_numeros, tupla_resoluciones
from componentes.etiquetador_botones import BotonBiestable

from constantes.constantes import Tab, Percentil, Estados, tupla_estados

from vistas.clasificador.dialogos import dialogo_directorio_origen, dialogo_directorio_destino



ancho_botones = 200
altura_botones = 40

texto_ayuda = """
Bordes de imagen:
  Cada color de borde da informacion sobre el estado del etiquetado o de las dimensiones de cada imagen.
  Opciones:
  - Celeste: no etiquetado
  - Verde: tags guardados
  - Amarillo: tags agregados o modificados
  - Rojo: dimensiones incorrectas
"""


ayuda_emergente = ft.Tooltip(
    message=texto_ayuda,
    content=ft.Text("Ayuda extra",size=18, width=100),        # FIX
    padding=20,
    border_radius=10,
    text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
)

# listas desplegable para elegir opciones de imagen 
lista_dimensiones_desplegable = crear_lista_desplegable(tupla_resoluciones, ancho=120)
lista_estados_desplegable = crear_lista_desplegable(tupla_estados, ancho=120)


# Botones apertura de ventana emergente
boton_carpeta_origen = ft.ElevatedButton(
    text = "Carpeta origen",
    # icon=ft.icons.FOLDER_OPEN,
    icon=ft.icons.FOLDER_OPEN,
    bgcolor = ft.colors.BLUE_900,   
    color= ft.colors.WHITE,
    height = altura_botones,
    width  = ancho_botones,
    ## manejador
    on_click=lambda _: dialogo_directorio_origen.get_directory_path(
        dialog_title="Elegir carpeta con todas las imágenes"
    ),
    tooltip="Elegir carpeta con todas las imágenes",
)


boton_carpeta_destino = ft.ElevatedButton(
    text = "Carpeta destino",
    icon=ft.icons.FOLDER_OPEN,
    ## manejador: leer sólo directorios
    on_click=lambda _: dialogo_directorio_destino.get_directory_path(
        dialog_title="Elegir carpeta para mover la seleccion",
        ),
    tooltip = "Elegir carpeta para mover la seleccion",
    disabled = True,       
    height = altura_botones,
    width  = ancho_botones,
    bgcolor=ft.colors.RED_900,
    color = ft.colors.WHITE,
)



# textos
texto_dimensiones = ft.Text("Dimensiones\nimagen:")
texto_estados = ft.Text("Estado\netiquetado:")


# componentes repartidos en segmentos horizontales
fila_controles_apertura = ft.Row(
    [boton_carpeta_origen, boton_carpeta_destino],
    # [tooltip_carpeta, boton_dataset],     # TOOLTIP problematico
    width = 500,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    wrap = True
    )
fila_controles_dimensiones = ft.Row(
    # [texto_dimensiones, lista_dimensiones_desplegable, boton_filtrar_dimensiones],
    [texto_dimensiones, lista_dimensiones_desplegable],
    # width = 400,
    width = 300,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    wrap = False
    )

fila_controles_etiquetas = ft.Row(
    # [texto_estados, lista_estados_desplegable, boton_filtrar_etiquetas],    
    [texto_estados, lista_estados_desplegable],
    # width = 400,
    width = 300,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    wrap = False
    )


# Fila de botones para abrir carpetas y leer archivos
fila_controles = ft.Row([
    fila_controles_apertura,
    fila_controles_dimensiones,
    fila_controles_etiquetas,
    ayuda_emergente,
    ],
    wrap=True,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )


# funciones

def actualizar_lista_dimensiones(lista_imagenes: list[ContenedorEstados]):
    """Reduce la lista de dimensiones seleccionables en base al tamaño detectado de las imagenes de galeria."""
    # acceso a elementos globales
    # lista_resoluciones = [] 
    lista_resoluciones = [tupla_resoluciones[0]] # opcion "No filtrar" agregada
    set_dimensiones = set()

    # conjunto de dimensiones encontradas en imagenes
    objeto = map(lambda img: img.dimensiones, lista_imagenes)
    set_dimensiones = set(objeto)

    for resolucion in tupla_resoluciones:
        resolucion_conv = convertir_dimensiones_opencv(str(resolucion))
        if resolucion_conv in set_dimensiones:
            lista_resoluciones.append(resolucion)


    opciones_lista_desplegable(lista_dimensiones_desplegable, tuple(lista_resoluciones))
