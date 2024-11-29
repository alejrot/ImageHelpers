import flet as ft
import re
from componentes.etiquetador_botones import FilasBotonesEtiquetas
from componentes.botones import BotonBiestable

from vistas.etiquetador.dialogos import dialogo_dataset, dialogo_directorio, dialogo_guardado_tags
from manejo_texto.procesar_etiquetas import Etiquetas

from constantes.constantes import Tab, Percentil, Estados, tupla_estados

from vistas.etiquetador.clasificador import clasificador_imagenes

from constantes.colores import LISTA_COLORES_ACTIVO, LISTA_COLORES_PASIVO

from vistas.etiquetador.columna_galeria import galeria_etiquetador



lista_imagenes = clasificador_imagenes


# Entradas de texto
entrada_tags_buscar = ft.TextField(
    label="Buscar coincidencias",
    # on_change=textbox_changed,
    # on_submit=agregar_tags_seleccion,
    height=60,
    width=400
)


entrada_tags_agregar = ft.TextField(
    label="Agregar tags a las imágenes - pulsar 'ENTER' para confirmar",
    # on_change=textbox_changed,
    # on_submit=agregar_tags_seleccion,
    height=60,
    width=400
)

entrada_tags_quitar = ft.TextField(
    label="Quitar tags a las imágenes - pulsar 'ENTER' para confirmar",
    # on_change=textbox_changed,
    # on_submit=quitar_tags_seleccion,
    height=60,
    width=400
)

filas_filtrado = FilasBotonesEtiquetas()
# filas_filtrado.altura = pagina.height - 200
# filas_filtrado.altura = pagina.height - 330     #FIX



filas_filtrado.lista_colores_activo = LISTA_COLORES_ACTIVO

filas_filtrado.lista_colores_pasivo = LISTA_COLORES_PASIVO


boton_reordenar_tags = BotonBiestable(
    texto_false="Orden por percentiles",
    color_false=ft.colors.GREEN_ACCENT_700,
    color_true=ft.colors.GREEN_800,
    texto_true="Orden alfabético",
    color_texto=ft.colors.WHITE,
    )


boton_guardar_dataset = ft.ElevatedButton(
    # text = f"Guardar como dataset",
    text = f"Guardar tags",
    bgcolor = ft.colors.AMBER_800,
    icon=ft.icons.SAVE,
    color = ft.colors.WHITE,
    ## manejador
    on_click=lambda _: dialogo_guardado_tags.save_file(
        dialog_title = "Guardar archivo de dataset (formato .txt)",
        allowed_extensions=["txt"],
        ),
    tooltip="Guarda en archivo de texto las etiquetas encontradas. Si el archivo ya existe lo sobreescribe.",
    )

boton_reset_tags = ft.ElevatedButton(
    text = f"Deseleccionar",
    bgcolor = ft.colors.BLUE_800,
    color = ft.colors.WHITE,
    icon=ft.icons.UNDO_ROUNDED, 
    tooltip="Reinicia la selección de etiquetas encontradas."
    )

texto_contador_tags= ft.Text(
    "Tags encontados:",
    size=15,
    weight=ft.FontWeight.BOLD,
    text_align=ft.TextAlign.START,
    )

columna_etiquetas = ft.Column(
    controls=[    
        ft.Row(
            [ texto_contador_tags],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),  
        ft.Row(
            # [boton_reset_tags, 
            [boton_reordenar_tags,
            boton_reset_tags, 
            boton_guardar_dataset],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),  
        ft.Divider(height=7, thickness=1) ,
        entrada_tags_buscar,
        ft.Divider(height=7, thickness=1) ,
        filas_filtrado,
        ft.Divider(height=7, thickness=1) ,
        entrada_tags_agregar, #FIX
        entrada_tags_quitar,
    ],
    # visible=False,      # FIX
    visible=True,
    expand=1,
    # scroll=ft.ScrollMode.HIDDEN, 
    scroll=ft.ScrollMode.AUTO, 
    # height=pagina.height - 330     #FIX
    )



def contar_etiquetas_repetidas( etiquetados:Etiquetas, secuencia:str, inversa=False, conteo_salida=True )->list:
    """
    Devuelve una lista con todas las etiquetas detectadas  en la lista de entrada.
    La lista se ordena en base al nímero de repeticiones de cada etiqueta.
    Puede indicarse el número de repeticiones a la salida de manera opcional. 
    """
    # busqueda y conteo de etiquetas
    conteo_etiquetas = dict()

    for etiquetado in etiquetados:  
        for tag in etiquetado.tags:
            retorno = re.search(secuencia, tag, re.I) 
            if retorno !=None:
                conteo_etiquetas[tag] = 1 if tag not in conteo_etiquetas else conteo_etiquetas[tag]+1


    # etiquetas ordenadas de más repetidas a menos usadas
    conteo_etiquetas = dict(sorted(conteo_etiquetas.items(), key=lambda item:item[1], reverse=inversa))
    lista_tags = list(conteo_etiquetas.keys()) 

    if conteo_salida==False:
        return lista_tags

    else:
        # etiquetas con numero de repeticiones agregado
        return list(map(lambda tag: f"{tag}  ({conteo_etiquetas[tag]})",  lista_tags))


def etiquetas_orden_alfabetico(lista_tags: list, inverso=False)->Etiquetas:
    """
    Se ordenan todos los tags de entrada ordenados en orden alfabético.
    No se distinguen letras mayúsculas de minúsculas.
    El resultado se devuelve en un objeto de tipo 'Etiquetas'.
    """
    etiquetas = Etiquetas()
    letras = []
    # se hace una lista ordenada con el primer caracter de todas las etiquetas
    set_letras = set()
    for tag in lista_tags:
        set_letras.add(tag[0].lower())
    letras = list(set_letras)
    letras.sort(reverse=inverso)

    # se reparten las etiquetas en grupos en abse al primer caracter detectado 
    for tag in lista_tags:
        n = letras.index(tag[0].lower())    
        etiquetas.agregar_tags([tag], n)

    return etiquetas



def etiquetas_orden_percentiles(lista_tags: list, inverso=False)->Etiquetas:
    """
    Se ordenan todos los tags de entrada ordenados en base a percentiles del 20%.
    El resultado se devuelve en un objeto de tipo 'Etiquetas'.
    (La lista de entrada debe estar ordenada).
    """
    etiquetas = Etiquetas()
    tags_grupo = []
    nro_tags = len(lista_tags) 

    # número de tags para cada percentil
    umbral_1 = int(nro_tags * Percentil.UMBRAL_1.value)
    umbral_2 = int(nro_tags * Percentil.UMBRAL_2.value)
    umbral_3 = int(nro_tags * Percentil.UMBRAL_3.value)
    umbral_4 = int(nro_tags * Percentil.UMBRAL_4.value)
    umbral_5 = int(nro_tags * Percentil.UMBRAL_5.value)

    # reparto entre percentiles
    etiquetas.agregar_tags(lista_tags[       0:umbral_1])
    etiquetas.agregar_tags(lista_tags[umbral_1:umbral_2])
    etiquetas.agregar_tags(lista_tags[umbral_2:umbral_3])
    etiquetas.agregar_tags(lista_tags[umbral_3:umbral_4])
    etiquetas.agregar_tags(lista_tags[umbral_4:umbral_5])

    return etiquetas


def estadisticas()->dict:
    """Detecta todas las etiquetas usadas en las imagenes y cuenta cuantas repeticiones tiene cada una.
    Crea tambien los botones de filtrado correspondientes a cada una."""


    # lectura de patron de busqueda
    secuencia = entrada_tags_buscar.value
    # descarte de espacios en blanco
    secuencia = secuencia.strip()

    # imagenes = lista_imagenes.seleccion
    imagenes = galeria_etiquetador.imagenes_mostradas

    lista_tags = contar_etiquetas_repetidas(imagenes, secuencia)

    nro_tags = len(lista_tags)
    texto_contador_tags.value = f"Etiquetas encontadas: {nro_tags}"
    boton_reset_tags.text = f"Deseleccionar tags"


    # if boton_reordenar_tags.valor == True:
    if boton_reordenar_tags.estado == True:
        # reparto en grupos y coloreo de botones en base al orden alfabetico
        etiquetas_marcadas = etiquetas_orden_alfabetico(lista_tags)

    else:
        # reparto en grupos y coloreo de botones en base a percentiles del 20%
        etiquetas_marcadas = etiquetas_orden_percentiles(lista_tags, True)


    filas_filtrado.leer_dataset(etiquetas_marcadas, False)
    filas_filtrado.agregar_tags([], True)
    # filas_filtrado.evento_click(filtrar_todas_etiquetas)

    # columna_etiquetas.update()

    # return conteo_etiquetas




# Demo
if __name__=="__main__":

    def main(pagina: ft.Page):
        pagina.add(columna_etiquetas)

        # Añadido de diálogos a la página
        pagina.overlay.extend([
                dialogo_directorio, dialogo_dataset, dialogo_guardado_tags
            ])

        pagina.update()


    ft.app(target=main)       