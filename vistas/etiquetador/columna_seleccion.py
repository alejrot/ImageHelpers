import pathlib
import flet as ft


from componentes.galeria_imagenes import  ContenedorImagen
from estilos.estilos_contenedores import estilos_seleccion, estilos_galeria, Estilos

from componentes.contenedor_etiquetado import ContenedorEtiquetado

# from vistas.etiquetador.clasificador import clasificador_imagenes
from vistas.etiquetador.columna_galeria import galeria_etiquetador

from manejo_texto.procesar_etiquetas import etiquetas2texto

from sistema_archivos.rutas import ruta_relativa_usuario



texto_imagen= ft.Text(
    "(Titulo)",
    size=20,
    # height=30, 
    weight=ft.FontWeight.BOLD,
    text_align=ft.TextAlign.CENTER,
    )
texto_ruta_titulo = ft.Text(
    "(ruta))",
    weight=ft.FontWeight.BOLD,
    text_align=ft.TextAlign.CENTER,
    )
texto_ruta_data = ft.Text(
    "(ruta_completa))",
    weight=ft.FontWeight.NORMAL,
    text_align=ft.TextAlign.CENTER,
    )
texto_tags_titulo = ft.Text(
    "(nro tags)",
    weight=ft.FontWeight.BOLD,
    text_align=ft.TextAlign.CENTER,
    )
texto_tags_data = ft.Text(
    "(tags)",
    weight=ft.FontWeight.NORMAL,
    text_align=ft.TextAlign.CENTER,
    )


# contenedor visualizador de la imagen actual
contenedor_seleccion = ContenedorImagen("",512,512)
contenedor_seleccion.estilo(estilos_seleccion[Estilos.DEFAULT.value])
# contenedor_seleccion.estilo(estilos_seleccion[Estilos.ACTUAL.value])          # FIX
contenedor_seleccion.bgcolor = ft.colors.LIGHT_BLUE



columna_seleccion = ft.Column(
    [
        texto_imagen, 
        contenedor_seleccion, 
        texto_ruta_titulo, 
        texto_ruta_data, 
        texto_tags_titulo,
        texto_tags_data,
    ],
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    expand=True,
    # expand=1,
    visible=True,
    )



def imagen_seleccion(imagen: ContenedorEtiquetado):
    """Actualiza imagen y estilo de bordes del selector de imagen"""
    contenedor_seleccion.ruta_imagen = imagen.ruta

    if imagen.defectuosa :   
        estilo = Estilos.ERRONEO.value  
    elif imagen.modificada :  
        estilo = Estilos.MODIFICADO.value  
    elif imagen.guardada :
        estilo = Estilos.GUARDADO.value  
    else: 
        estilo = Estilos.DEFAULT.value  

    contenedor_seleccion.estilo(estilos_seleccion[estilo]) 
    contenedor_seleccion.update()


    #textos informativos
    # ruta = pathlib.Path(imagen.ruta)
    # nombre = ruta.name
    nombre = pathlib.Path(imagen.ruta).name
    ruta = ruta_relativa_usuario(imagen.ruta)
    # indice = lista_imagenes.seleccion.index(imagen)
    # indice = clasificador_imagenes.seleccion.index(imagen)
    tags = imagen.tags
    # n = len(lista_imagenes.seleccion)
    # n = len(clasificador_imagenes.seleccion)
    n = len(galeria_etiquetador.imagenes_mostradas)
    # texto_imagen.value = f"{indice+1}/{n} - '{nombre}'"
    texto_imagen.visible = True 
    texto_imagen.update()
    texto_ruta_titulo.value = f"Ruta archivo:"
    texto_ruta_titulo.visible = True
    texto_ruta_titulo.update()
    texto_ruta_data.value = f"{ruta}"
    texto_ruta_data.visible = True
    texto_ruta_data.update()
    texto_tags_titulo.value = f"Tags imagen ({len(tags)}):"
    texto_tags_titulo.visible = True
    texto_tags_titulo.update()
    texto_tags_data.value = f"{etiquetas2texto(tags)}"
    texto_tags_data.visible = True
    texto_tags_data.update()





# Demo
if __name__=="__main__":

    def main(pagina: ft.Page):
        pagina.add(columna_seleccion)


        pagina.update()


    ft.app(target=main)       