from rich import print as print
import flet as ft
from manejo_texto.procesar_etiquetas import  Etiquetas
from componentes.botones import BotonBiestable, BotonGrupo


def nada( e ):
    pass



class FilasBotonesEtiquetas(ft.Column):
    """Este componente crea botones de activacion para cada etiqueta (descripcion) detectada en un archivo de texto"""
    def __init__(self):
        self.dataset: Etiquetas =  Etiquetas()
        self.etiquetas: Etiquetas =  Etiquetas()
        # self.etiquetas_archivo: Etiquetas =  Etiquetas()
        self.botones_etiquetas = []
        self.botones_grupo = []
        self.__filas_botones = []
        # self.__numero_grupos = 0
        self.__numero_colores = 0
        self.lista_colores_activo = [
            ft.colors.PURPLE_800,      
            ft.colors.BROWN_800,
            ft.colors.RED_800,
            ft.colors.ORANGE_800, 
            ft.colors.YELLOW_800,
            ft.colors.LIME_800,
            ft.colors.GREEN_800,
            ft.colors.GREEN_ACCENT_700,
            ft.colors.CYAN_800,        
            ft.colors.BLUE_800,           
            ]
        self.lista_colores_pasivo = [
            ft.colors.PURPLE_100,      
            ft.colors.BROWN_100,
            ft.colors.RED_100,
            ft.colors.ORANGE_100, 
            ft.colors.YELLOW_100,
            ft.colors.LIME_100,
            ft.colors.GREEN_100,
            ft.colors.GREEN_ACCENT_100,
            ft.colors.CYAN_100,        
            ft.colors.BLUE_100,           
            ]
        self.funcion_etiquetas = nada
        self.funcion_grupo = nada
        super().__init__(
            wrap=False,
            spacing=10,       # espaciado horizontal 
            run_spacing=50,     # espaciado vertical entre filas
            controls =  [], 
            scroll=ft.ScrollMode.AUTO,
            )

       
    def leer_dataset(self, dataset: Etiquetas, botones_grupo_visibles=True):
        """Lee TODAS las etiquetas (el 'dataset') desde la estructura de datos de entrada y crea los botones de activacion de la interfaz gráfica.
        El componente clasifica las etiquetas en distintos 'grupos' que pueden activarse o desactivarse solidariamente.
        Permite dejar los botones de grupo ocultos.
        """
        self.dataset = dataset
        tags = self.dataset.tags
        data = self.dataset.datos
        grupos = list(set(self.dataset.grupos))

        # conteo grupos de etiquetas
        # self.__numero_grupos = len(grupos)
        self.__numero_colores = len(self.lista_colores_activo)  

        # ordenamiento de los tags en filas por grupo
        tags_grupo = dict()
        # inicializacion
        for grupo in grupos:
            tags_grupo[grupo] = []
        for tag in tags:
            # todos los grupos donde está el tag actual
            grupos_tag = data[tag]
            # un mismo tag puede aparecer en varias filas
            for grupo in grupos_tag:
                tags_grupo[grupo].append(tag)
                

        # maquetado
        self.__filas_botones = []
        self.controls = self.__filas_botones
        self.botones_grupo = []
        self.botones_etiquetas = []


        for grupo in grupos:
            # print(grupo, type(grupo))
            lista_tags = tags_grupo[grupo]
            indice_color = int(grupo) % self.__numero_colores 
            self.agregar_linea_dataset(
                lista_tags=lista_tags, 
                indice_grupo=int(grupo), 
                indice_color=indice_color,
                boton_grupo_visible=botones_grupo_visibles)


        self.update()
        self.evento_click()


    def agregar_linea_dataset(self, 
        lista_tags: list[str],
        indice_grupo: int,
        indice_color: int=0, 
        boton_grupo_visible=True
        ):
        """
        El componente crea un 'grupo' de etiquetas con sus botones de activacion de la interfaz gráfica y los agrega al componente.
        Permite dejar los botones de grupo ocultos.
        """
        g = BotonGrupo()
        g.data = indice_grupo        # indice grupo
        g.on_click = self.conmutar_grupo    # evento
        g.visible = boton_grupo_visible
        g.bgcolor = self.lista_colores_activo[indice_color]
        # lista para acceso
        self.botones_grupo.append(g)
        # colocacion al comienzo de cada fila de botones
        filas_botones = ft.Row(
            controls = [g],
            wrap = True,
            )
        for tag in lista_tags:
        # creacion de boton (puede estar repetido)
            b = BotonBiestable(tag)
            self.botones_etiquetas.append(b)
            filas_botones.controls.append(b)
            # asignacion color
            b.color_false = self.lista_colores_pasivo[indice_color]
            b.color_true = self.lista_colores_activo[indice_color]

        self.__filas_botones.append(filas_botones)


    def guardar_dataset(self, etiquetas: Etiquetas, sobreescribir=False):
        """Añade o sobreescribe las etiquetas del archivo de dataset"""
        modo = "w" if sobreescribir else "a"
        guardado_exitoso = self.dataset.guardar(etiquetas, modo=modo)
        return guardado_exitoso


    def deshabilitar_botones(self, valor: bool):
        """Anula los botones del componente."""
        for boton in self.botones_grupo:
            boton.disabled = valor

        for boton in self.botones_etiquetas:
            boton.disabled = valor

    def setear_salida(self, etiquetas :Etiquetas):
        """Carga el archivo de etiquetas de salida y actualiza el etiquetador grafico"""
        self.etiquetas = etiquetas
        self.actualizar_botones()


    def agregar_tags(self, tags: list[str], sobreescribir:bool=False):
        """Ingresa las etiquetas desde una lista y actualiza los botones."""
        self.etiquetas.agregar_tags(tags,  sobreescribir=sobreescribir)
        self.actualizar_botones()


    def actualizar_botones(self):
        """Lee los estados de los botones en base a las etiquetas ingresadas al componente"""
        for boton in self.botones_etiquetas:
            tag = boton.text
            if tag in self.etiquetas.tags:
                boton.estado = True
            else:
                boton.estado = False
        self.update()



    def leer_botones(self, filtrar_repetidos=True)->list[str]:
        """Lee todas las etiquetas habilitadas mediante los botones. Por defecto filtra los repetidos."""
        etiquetas = []
        for boton in self.botones_etiquetas:
            if boton.estado:
                tag = boton.text
                etiquetas.append(tag)
        if filtrar_repetidos:
            set_etiquetas = set(etiquetas)
            return list(set_etiquetas)
        else:
            return etiquetas


    def leer_etiquetas_archivo(self):
        """Lee y carga las etiquetas ya guardadas en el archivo de salida"""
        # lectura de disco
        self.etiquetas.leer_archivo()  
        

    def conmutar_grupo(self, e: ft.ControlEvent ):
        """Esta funcion habilita o deshabilita un grupo completo de etiquetas"""
        boton_grupo = e.control
        grupo = boton_grupo.data
        # Se corrige el estado del grupo de modo que el click afecte al mayor numero de etiquetas posible
        # (mejora la respuesta al usuario)
        activados = 0
        desactivados = 0
        for boton in self.__filas_botones[grupo].controls:
            if boton.estado:
                activados += 1
            else:
                desactivados += 1
        boton_grupo.estado = True if activados >= desactivados else False
        # cambio de estado lógico de todo el grupo
        boton_grupo.estado = True if boton_grupo.estado == False else False 
        # cambio de icono
        if boton_grupo.estado :
            boton_grupo.icon = ft.icons.DESELECT_ROUNDED
        else:
            boton_grupo.icon = ft.icons.SELECT_ALL_ROUNDED 

        for boton in self.__filas_botones[grupo].controls:
            boton.estado = boton_grupo.estado
        # actualizacion
        self.__filas_botones[grupo].update()
        # funcion opcional
        boton_grupo.click_boton(e)



    def evento_click(self, funcion_etiquetas=None, funcion_grupo=None):
        """Asigna una funcion para el click de todos los botones según sean de etiquetas o de grupos"""
        if funcion_etiquetas != None:
            self.funcion_etiquetas = funcion_etiquetas 
        if funcion_grupo != None:
            self.funcion_grupo = funcion_grupo
        # asignacion de funciones a cada boton  
        for boton in self.botones_etiquetas:
            boton.click_boton =  self.funcion_etiquetas
        for boton in self.botones_grupo:
            boton.click_boton =  self.funcion_grupo

    def mostrar_tag(self, clave: str, duracion = 1000):
        """Mueve el scroll para mostrar el primer boton con la clave indicada."""
        self.scroll_to(key=clave, duration=duracion)
        self.update()


    @property
    def base(self):
        """Devuelve el ancho total del componente grafico"""
        return self.width

    @base.setter
    def base(self, valor):
        """Define el ancho total del componente grafico"""
        self.width = valor
        for fila in self.__filas_botones:
            fila.width = valor

    @property
    def altura(self):
        """Devuelve la altura total del componente grafico"""
        return self.height

    @altura.setter
    def altura(self, valor):
        """Define la altura total del componente grafico"""
        self.height = valor




if __name__=="__main__":

    def main(pagina: ft.Page):

        filas_demo = FilasBotonesEtiquetas()
        pagina.add(filas_demo)

        pagina.update()


    ft.app(target=main)       