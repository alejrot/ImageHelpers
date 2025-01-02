from rich import print as print
import flet as ft
from manejo_texto.procesar_etiquetas import  Etiquetas, separar_etiquetas
from componentes.botones import BotonBiestable, BotonGrupo
from componentes.filas_botones import FilasBotonesEtiquetas


def nada( e ):
    pass


class EtiquetadorBotones(ft.Column):
    def __init__(self):
        """Inicializa un componente etiquuetador, agregando a los botones de etiquetas los botones de guardado, descarte de cambios, etc """
        # banderines de control y de maquetado
        self.__altura_filas = 40
        self.__habilitado = False
        self.__dataset_seteado = False
        self.__salida_seteada = False
        self.__filas_botones = FilasBotonesEtiquetas()   # componente interno --> composicion
        # campos de entrada de texto
        self.__entrada_texto = ft.TextField(
            label="Agregar nuevos tags al etiquetador - pulsar 'ENTER' para confirmar",
            on_change=None,
            on_submit=self.agregar_tags_texto,
            focused_border_color=ft.colors.BLUE_700,
            height=60,
            width=500,
            )
        # botones de comando
        self.__boton_guardar = ft.ElevatedButton(
            text="guardar cambios",
            width = 200,
            bgcolor= ft.colors.RED_900,
            color= ft.colors.WHITE,
            on_click= self.guardar_etiquetas
            )
        self.__boton_todos = ft.ElevatedButton(
            text="todas",
            width = 200,
            bgcolor= ft.colors.INDIGO_400,
            color= ft.colors.WHITE,
            on_click= self.todas_etiquetas
            )
        self.__boton_nada = ft.ElevatedButton(
            text="ninguna",
            width = 200,
            bgcolor= ft.colors.INDIGO_400,
            color= ft.colors.WHITE,
            on_click= self.ninguna_etiqueta
            )
        self.__boton_descartar = ft.ElevatedButton(
            text="descartar cambios",
            width = 200,
            bgcolor= ft.colors.GREEN_800,
            color= ft.colors.WHITE,
            on_click= self.restablecer_etiquetas
            )
        super().__init__(
            controls = [],
            wrap=False,
            # spacing=10,       # espaciado horizontal 
            # run_spacing=50,     # espaciado vertical entre filas
            )
        self.__divisor = ft.Divider(height = 10)
        self.__f1 =ft.Row(
            controls= [ self.__boton_todos, self.__boton_nada ],
            wrap = True,    
            alignment = ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 50,
            height = self.__altura_filas,
            width = 600,
            )
        self.__f2 = ft.Row(
            controls= [ self.__boton_descartar, self.__boton_guardar],
            wrap = True,
            alignment = ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 50,
            height = self.__altura_filas,
            width = 600,
            )  
        self.__fila_texto = ft.Row(
            controls= [ self.__entrada_texto],
            wrap = True,
            alignment = ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 50,
            height = self.__entrada_texto.height + 10,
            width = 600,
            )  
        self.controls=[
            self.__fila_texto, 
            self.__filas_botones,
            self.__divisor, 
            self.__f1, 
            self.__f2,
            ]
        self.click_botones = nada
        self.alignment = ft.MainAxisAlignment.START


    def todas_etiquetas(self, e):
        """Activa todas las etiquetas del dataset"""
        for boton in self.__filas_botones.botones_etiquetas:
            boton.estado = True
        # funcionalidad externa al etiquetador
        self.click_botones(e)


    def ninguna_etiqueta(self, e):
        """Descarta todas las etiquetas del dataset"""
        for boton in self.__filas_botones.botones_etiquetas:
            boton.estado = False
        # funcionalidad externa al etiquetador
        self.click_botones(e)


    def restablecer_etiquetas(self, e):
        """Actualiza los botones de etiquetas a sus valores guardados en archivo"""
        # reestablecimiento de diccionario interno (sin relectura de archivo)
        datos_archivo = self.__filas_botones.etiquetas.datos_archivo
        self.__filas_botones.etiquetas.datos = datos_archivo
        # actualizacion grafica
        self.__filas_botones.actualizar_botones()
        # funcionalidad externa al etiquetador
        self.click_botones(e)


    def guardar_etiquetas(self, e):
        """Guarda todas las etiquetas seleccionadas en el archivo de texto asignado al componente. Se filtran las etiquetas repetidas."""
        # lectura de botones activos (elementos repetidos flitrados)
        tags_botones = self.__filas_botones.leer_botones()
        # lectura de datos originales de archivo
        tags_archivo = self.__filas_botones.etiquetas.tags_archivo
        # se intenta el guardado sólo si se detectan cambios de etiquetado 
        if set(tags_botones) != set(tags_archivo): 
            # guardado de etiquetas( relectura archivo intrinseca)
            self.__filas_botones.etiquetas.guardar(tags_botones)
        # funcionalidad externa al etiquetador
        self.click_botones(e)
        # actualizacion grafica y salida
        self.update()


    @property
    def base(self):
        """Devuelve el ancho total del componente grafico"""
        return self.width

    @base.setter
    def base(self, valor):
        """Define el ancho total del componente grafico"""
        self.width = valor
        # self.__f1.width = valor
        # self.__f2.width = valor
        self.__filas_botones.width = valor

    @property
    def altura(self):
        """Devuelve la altura total del componente grafico"""
        return self.height

    @altura.setter
    def altura(self, valor):
        """Define la altura total del componente grafico"""
        self.height = valor
        resta = self.__altura_filas * 3 
        resta = resta + int(self.__divisor.height) *3
        self.__filas_botones.height = valor - resta


    def leer_dataset(self, etiquetas: Etiquetas, botones_grupo_visibles=True):
        """Lee las etiquetas del dataset y actualiza etiquetas de salida si corresponde.
        Permite dejar los botones de grupo ocultos."""
        self.__filas_botones.leer_dataset( etiquetas, botones_grupo_visibles )
        self.__dataset_seteado = True
        self.habilitado = True if self.__salida_seteada else False
        # actualiza aspecto grafico para prevenir errores
        if self.__salida_seteada : 
            self.restablecer_etiquetas( "e")


    def agregar_linea_dataset(self, tags: list[str], boton_grupo_visible=True):
        """Agrega etiquetas al dataset y a si corresponde.
        Permite dejar el boton de grupo ocultos."""
        n = len(self.__filas_botones.botones_grupo) 
        colores = len(self.__filas_botones.lista_colores_activo)
        self.__filas_botones.agregar_linea_dataset(
            lista_tags = tags,
            indice_grupo = n,
            indice_color = (n % colores),
            boton_grupo_visible=boton_grupo_visible
            )

    @property
    def entrada_texto(self):
        """AUXILIAR - QUIZA SEA ELIMINADO MAS ADELANTE"""
        return self.__entrada_texto     # FIX


    def guardar_dataset(self, etiquetas: Etiquetas, sobreescribir=False):
        """Añade o sobreescribe las etiquetas del archivo de dataset"""
        guardado_exitoso = self.__filas_botones.guardar_dataset(etiquetas, sobreescribir)
        return guardado_exitoso


    def setear_salida(self, etiquetas: Etiquetas):
        """Elige el archivo de salida de etiquetas y establece qué botones se activan """
        self.__filas_botones.setear_salida( etiquetas )
        self.__salida_seteada = True
        self.habilitado = True if self.__dataset_seteado else False
            

    def agregar_tags(self, tags: list[str],  sobreescribir:bool=False):
        """Ingresa las etiquetas desde una lista y actualiza los botones."""
        self.__filas_botones.agregar_tags(tags, sobreescribir)
        self.habilitado = True if self.__dataset_seteado else False
        self.actualizar_botones()


    @property
    def dataset_seteado(self):
        """Indica si se eligio el archivo del dataset con todas las etiquetas"""
        return self.__dataset_seteado

    @property
    def salida_seteada(self):
        """Indica si se eligio el archivo de salida para las etiquetas"""
        return self.__salida_seteada

    @property
    def habilitado(self):
        """Indica si los controles están habilitados o no"""
        return self.__habilitado

    @habilitado.setter
    def habilitado(self, booleano):
        """Habilita / deshabilita manualmente los controles del etiquetador"""
        if booleano: 
            self.__boton_descartar.disabled = False
            self.__boton_nada     .disabled = False
            self.__boton_todos    .disabled = False
            self.__boton_guardar  .disabled = False
            self.__filas_botones.deshabilitar_botones(False)
            # flag de estado
            self.__habilitado = True
        else: 
            self.__boton_descartar.disabled = True
            self.__boton_nada     .disabled = True
            self.__boton_todos    .disabled = True
            self.__boton_guardar  .disabled = True
            self.__filas_botones.deshabilitar_botones(True)
            # flag de estado
            self.__habilitado = False

    def leer_botones(self, filtrar_repetidos=True)->list[str]:
        """Lee todas las etiquetas habilitadas mediante los botones. Por defecto filtra los repetidos."""
        etiquetas = self.__filas_botones.leer_botones(filtrar_repetidos)
        return etiquetas

    def actualizar_botones(self):
        self.__filas_botones.actualizar_botones()

    def evento_click(self, funcion_etiquetas=None, funcion_grupo=None, funcion_comando=None):
        """Asigna una funcion para el click de todos los botones, segun sean de etiquetas o de grupos"""
        # self.funcion_comando = funcion_comando if funcion_comando!=None e
        self.__filas_botones.evento_click(funcion_etiquetas, funcion_grupo)
        if funcion_comando!=None:
            self.click_botones = funcion_comando


    def mostrar_tag(self, clave: str, duracion = 1000):
        """Mueve el scroll para mostrar el primer boton de etiquetado con la clave indicada."""
        self.__filas_botones.mostrar_tag(clave, duracion)
        self.__filas_botones.update()
        # self.scroll_to(key=clave)


    def agregar_tags_texto(self, e):
        """Permite el agregado manual de etiquetas desde la entrada de texto."""
        # texto = entrada_tags_agregar.value
        texto = self.__entrada_texto.value
        # conversion a lista de etiquetas
        texto = separar_etiquetas([texto]).keys()
        texto = list(texto)
        # descarte de entradas vacias
        if len(texto)== 0:
            return

        self.agregar_linea_dataset(texto)
        self.__entrada_texto.value = ""
        self.update()


################## EJECUCION DEMO ###################

if __name__ == "__main__":

    ########### FUNCIONES TEST #####################

    def funcion_etiqueta(e: ft.ControlEvent):
        boton = e.control
        valor = boton.text
        print( "[bold green]Etiqueta afectada!")
        print(f"[bold blue]Valor etiqueta: [bold yellow]{valor}")


    def funcion_comando(e: ft.ControlEvent):
        boton = e.control
        valor = boton.text
        print( "[bold magenta]Comando activado!")
        print(f"[bold blue]Comando: [bold yellow]{valor} [bold blue]activado!")


    def funcion_grupos(e: ft.ControlEvent):
        boton = e.control
        valor = boton.data
        print( "[bold cyan]Grupo afectado!")
        print(f"[bold blue]Indice grupo: [bold yellow]{valor}")


    ################## FUNCION PRINCIPAL ####################

    def main(page: ft.Page):

        archivo_dataset = "demo/dataset.png"
        archivo_etiquetas = "demo/etiquetas_imagen.jpg"


        print( "[bold green]        DEMO ETIQUETADOR        ")
        print()
        print("[bold blue]Este archivo simula las operaciones de etiquetado de una imagen.")
        print("[bold blue]Los archivos del demo están incluidos en la carpeta 'demo'.")
        print(f"[bold cyan] Archivo dataset: [bold yellow]{archivo_dataset} ")
        print(f"[bold cyan] Archivo salida : [bold yellow]{archivo_etiquetas} ")

        # Recordar: se ignora la extension del archivo de etiqueta
        # éste siempre es TXT

        # componente etiquetador
        etiquetador = EtiquetadorBotones()

        page.add( etiquetador)

        page.add( BotonBiestable("soy un boton sobrante"))

        dataset     = Etiquetas(archivo_dataset) 
        etiquetas   = Etiquetas(archivo_etiquetas) 

        # dataset = Etiquetas()   # borrado forzoso

        etiquetador.altura = 800
        etiquetador.base = 600
        # carga de archivos (sentido inverso)
        etiquetador.setear_salida( etiquetas )      # carga el estado de los botones desde archivo
        etiquetador.leer_dataset(   dataset   )     # crea los botones de etiquetado y de grupo
        # etiquetador.leer_dataset( dataset, False )     # crea sólo los botones de etiquetado

        # configuracion de eventos ante el click sobre los botones
        etiquetador.evento_click(funcion_etiqueta, funcion_grupos, funcion_comando)

        # reporte de etiquetas almacenadas
        leido = etiquetador.leer_botones()
        print("[cyan]Etiquetas leidas")
        print(leido)


        page.title = "Botones etiquetado"
        page.window_height      = 800
        page.window_min_height  = 800
        page.window_width       = 600
        page.update()

        # cambios con delay
        import time 
        time.sleep(2)
        # etiquetas agregadas desde el programa
        nuevos_tags = ["3","4","5","6", "Aquiles Brinco"] 
        etiquetador.agregar_tags(nuevos_tags, False)

        # reporte de etiquetas almacenadas
        leido = etiquetador.leer_botones()
        print("[cyan]Tags agregados - etiquetas leidas")
        print(leido)
        etiquetador.mostrar_tag("6")


        time.sleep(2)
        # etiquetas agregadas desde el programa
        nuevos_tags = ["3","4","5","6", "15","Aquiles Brinco"] 
        etiquetador.agregar_tags(nuevos_tags, True)


        # reporte de etiquetas almacenadas
        leido = etiquetador.leer_botones()
        print("[cyan]Sobreescritura de tags - etiquetas leidas")
        print(leido)
        etiquetador.mostrar_tag("fuente")

        time.sleep(2)
        etiquetador.mostrar_tag("6")

        def redimensionar_botonera(e):

            etiquetador.base   = page.width
            etiquetador.altura = page.height
            etiquetador.update()

        page.on_resized = redimensionar_botonera


        page.title = "Botones etiquetado"
        page.window_height      = 800
        page.window_min_height  = 800
        page.window_width       = 600
        page.update()



    ft.app(target=main)