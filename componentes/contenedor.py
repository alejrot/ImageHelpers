
# import cv2 as cv

import flet as ft

# Contenedor con eventos integrados
# pensado para contener imagenes
class Contenedor(ft.UserControl):

    # MANEJADORES DE EVENTOS 
    # Se configuran mediante metodos dedicados
    def longpress(self, e):
        self.funcion_longpress()
        self.update()

    def hover(self,e):
        self.funcion_hover()
        self.update()

    def click(self, e):
        self.funcion_click()
        self.update()

    # INICIALIZACION
    def build(self):
        # acciones para los eventos  - Anulados por defecto
        self.funcion_hover      = lambda: nada()
        self.funcion_click      = lambda: nada()
        self.funcion_longpress  = lambda: nada()
        self.contenedor = ft.Container(
                margin=10,
                padding=10,
                width   = 200,
                height  = 200,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE,
                # border_radius=0,           # redondeo
                animate=ft.animation.Animation(200, "bounceOut"),
                # EVENTOS:  
                on_long_press = self.longpress,
                on_hover = self.hover,
                on_click = self.click, 
            )
        return self.contenedor
    
    #METODOS
    def setContenido(self, imagen: ft.Image ):
        self.contenedor.content  = imagen 
        self.update()

    def setDimensiones(self, base: int, altura: int):
        self.contenedor.height= altura
        self.contenedor.width = base
        self.update()

    def setBGColor(self, color: ft.colors):
        self.contenedor.bgcolor = color
        self.update()
        
    def setRedondeo(self, radio: int):
        self.contenedor.border_radius = radio
        self.update()

    # los eventos se configuran aquí
    # deben asignarse funciones lambda
    def setHover(self, funcion):
        self.funcion_hover = funcion
        self.update()

    def setClick(self, funcion):
        self.funcion_click = funcion
        self.update()    

    def setLongpress(self, funcion):
        self.funcion_longpress = funcion
        self.update()


# Funcion auxiliar: sirve para anular eventos
def nada():
    pass


# FUNCION MAIN

def pagina(page: ft.Page):

    contenedor = Contenedor()
    page.add(contenedor)

    def funcion_click():
        contenedor.setRedondeo(200)
        contenedor.setBGColor(ft.colors.RED)

    def funcion_hover():
        contenedor.setRedondeo(20)
        contenedor.setBGColor(ft.colors.AMBER)

    def estilo_defecto():   
        contenedor.setRedondeo(0)
        contenedor.setDimensiones(500,420)
        contenedor.setBGColor(ft.colors.BLUE)            

    # se asignan las funciones SIN argumentos como LAMBDAS
    contenedor.setClick(lambda: funcion_click())
    contenedor.setHover(lambda: funcion_hover())
    contenedor.setLongpress(lambda: estilo_defecto())

    # Las propiedades de los elementos se pueden editar DESPUES de añadirlos a la pagina
    estilo_defecto()

    # Contenido para el container: imagen remota
    imagen_actual = ft.Image(
        src = "https://picsum.photos/200/200?0",
        width = 400,
        height = 400 ,
        fit=ft.ImageFit.CONTAIN,
        repeat=ft.ImageRepeat.NO_REPEAT,
        border_radius=ft.border_radius.all(50),
    )

    contenedor.setContenido( imagen_actual )
    page.update()


ft.app(target = pagina)