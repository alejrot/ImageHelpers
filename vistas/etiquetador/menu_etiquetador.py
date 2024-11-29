import flet as ft

from componentes.lista_desplegable import crear_lista_desplegable,opciones_lista_desplegable, convertir_dimensiones_opencv, extraer_numeros, tupla_resoluciones
from componentes.etiquetador_botones import BotonBiestable

from constantes.constantes import Tab, Percentil, Estados, tupla_estados

from vistas.etiquetador.dialogos import dialogo_dataset, dialogo_directorio, dialogo_guardado_tags

from vistas.etiquetador.clasificador import clasificador_imagenes

lista_imagenes = clasificador_imagenes


texto_ayuda = """
Bordes de imagen:
  Cada color de borde da informacion sobre el estado del etiquetado o de las dimensiones de cada imagen.
  Opciones:
  - Celeste: no etiquetado
  - Verde: tags guardados
  - Amarillo: tags agregados o modificados
  - Rojo: dimensiones incorrectas

Teclado: 
Permite cambiar rápidamente la imagen seleccionada. 
Teclas rápidas:
- Home:  primera imagen;
- RePag | A : imagen anterior;
- AvPag | D : imagen siguiente;
- End:   última imagen.
- Space : restaurar etiquetas (imagen actual)
-  W    : guardar etiquetas   (imagen actual)
- Flechas : navegar por el menú
- ENTER   : abrir ventanas y listas 
- Escape  : salir de ventanas emergentes, deseleccionar opciones
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
boton_carpeta = ft.ElevatedButton(
    text = "Abrir imágenes",
    # icon=ft.icons.FOLDER_OPEN,
    icon=ft.icons.FOLDER,
    bgcolor=ft.colors.RED,
    color= ft.colors.WHITE,
    ## manejador
    on_click=lambda _: dialogo_directorio.get_directory_path(
        dialog_title="Elegir carpeta con todas las imágenes"
    ),
    tooltip="Abre la carpeta con todas las imágenes a etiquetar.",
)

# Tooltip obsoleto desde la V0.24

tooltip_carpeta = ft.Tooltip(
    message="Abre la carpeta con todas las imágenes a etiquetar.",
    # content=ft.Text("Ayuda extra",size=18, width=100),
    content=[boton_carpeta],                                      # FIX
    padding=20,
    border_radius=10,
    text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
)


boton_dataset = ft.ElevatedButton(
    text = "Abrir dataset",
    icon=ft.icons.FILE_OPEN,
    bgcolor=ft.colors.BLUE,
    color= ft.colors.WHITE,
    ## manejador
    on_click=lambda _: dialogo_dataset.pick_files(
        dialog_title= "Elegir archivo de dataset (formato .txt)",
        allowed_extensions=["txt"],
        allow_multiple=False,
    ),
    tooltip="Elige el archivo TXT con las etiquetas a agregar.\nCada renglón se interpreta como un 'grupo' de tags."
)




boton_filtrar_dimensiones = BotonBiestable("Filtrar", ft.colors.BROWN_100, ft.colors.BROWN_800)
boton_filtrar_dimensiones.color = ft.colors.WHITE
boton_filtrar_dimensiones.tooltip = "Selecciona las imágenes que cumplan con las dimensiones indicadas."

# boton_filtrar_etiquetas = BotonBiestable("Panel filtrado", ft.colors.PURPLE_100, ft.colors.PURPLE_800)
# boton_filtrar_etiquetas.color = ft.colors.WHITE
# boton_filtrar_etiquetas.tooltip = "Abre el panel de filtrado con todas las etiquetas detectadas.\nRequiere que haya al menos una imagen cargada."



# textos
texto_dimensiones = ft.Text("Dimensiones\nimagen:")
texto_estados = ft.Text("Estado\netiquetado:")


# componentes repartidos en segmentos horizontales
fila_controles_apertura = ft.Row(
    [boton_carpeta, boton_dataset],
    # [tooltip_carpeta, boton_dataset],     # TOOLTIP problematico
    width = 350,
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
    # fila_controles_dimensiones,
    fila_controles_etiquetas,
    ayuda_emergente,
    ],
    wrap=True,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )


# funciones

def actualizar_lista_dimensiones():
    """Reduce la lista de dimensiones seleccionables en base al tamaño detectado de las imagenes de galeria."""
    # acceso a elementos globales

    lista_resoluciones = [tupla_resoluciones[0]] # opcion "No filtrar" agregada
    set_dimensiones = set()

    for imagen in lista_imagenes.seleccion:
        dimensiones = imagen.dimensiones
        set_dimensiones.add(dimensiones)

    for resolucion in tupla_resoluciones:
        resolucion_conv = convertir_dimensiones_opencv(str(resolucion))
        if resolucion_conv in set_dimensiones:
            lista_resoluciones.append(resolucion)

    opciones_lista_desplegable(lista_dimensiones_desplegable, tuple(lista_resoluciones))
    # lista_dimensiones_desplegable.update()