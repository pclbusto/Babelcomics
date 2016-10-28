from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from KivyComicBook import *
from kivy.core.window import Window

class KivyVisor(App):
    def on_touch_down(self,widget, event):
        '''
        vamos a capturar eventos en estas zonas
        *************************
        *1*       *0*         *2*
        ***       ***         ***
        *                       *
        *                       *
        * *                   * *
        *3*                   *4*
        * *                   * *
        *                       *
        *                       *
        *                       *
        ***                   ***
        *5*                   *6*
        *************************
        :param widget:
        :param event:
        :return:
        '''
        #zona1 = ((0, Window.width * 0.1), (Window.height, (Window.height - Window.height * 0.1)))
        #zona2 = ((Window.width - Window.width * 0.1, Window.width), (Window.height, (Window.height - Window.height * 0.1)))
        zona0 = ((Window.width*0.5-Window.width*0.1,Window.width*0.5+Window.width*0.1),(Window.height - Window.height * 0.1,Window.height))
        zona3 = ((0, Window.width * 0.1), (Window.height * 0.1 + Window.height * 0.5,Window.height * -0.1 + Window.height * 0.5 ))
        zona4 = ((Window.width - Window.width * 0.1, Window.width), (Window.height * 0.1 + Window.height * 0.5 , Window.height * -0.1 + Window.height * 0.5))

        if (zona3[0][0]< event.pos[0] and event.pos[0] < zona3[0][1]) and (event.pos[1]<zona3[1][0] and event.pos[1]>zona3[1][1]):
            self.comic.gotoPrevPage()
            self.scatter.remove_widget(self.imagenPagina)
            self.imagenPagina = self.comic.getImagePage()
            self.scatter.add_widget(self.imagenPagina)
        if (zona4[0][0]< event.pos[0] and event.pos[0] < zona4[0][1]) and (event.pos[1]<zona4[1][0] and event.pos[1]>zona4[1][1]):
            self.scatter.remove_widget(self.imagenPagina)
            self.comic.gotoNextPage()
            self.imagenPagina = self.comic.getImagePage()
            self.scatter.add_widget(self.imagenPagina)
        if (zona0[0][0]< event.pos[0] and event.pos[0] < zona0[0][1]) and (zona0[1][0]<event.pos[1] and event.pos[1]<zona0[1][1]):
            box = GridLayout(cols=5)
            box.add_widget(Button(text="Ancho"))
            botonCentrado = Button(text="Centrar")
            botonCentrado.bind(on_press=self.centrado)
            box.add_widget(botonCentrado)
            botonSalir = Button(text="salir")
            botonSalir.bind(on_press=self.salir)
            box.add_widget(botonSalir)
            botonSalir = Button(text="Rotar")
            botonSalir.bind(on_press=self.rotar)
            box.add_widget(botonSalir)

            p = Popup(title='Test popup',  size_hint=(None, None), size=(400, 150))
            p.add_widget(box)

            p.open()
            print("POP UP")
    def rotar(self,event):
        print("rotar")
    def salir(self,event):
        self.stop()
    def centrado(self,event):
        # print( Window.center)
        # print(Window.center[0] - (self.imagenPagina.width / 2), Window.center[1] - (self.imagenPagina.height / 2))
        self.scatter.scale = Window.height / self.imagenPagina.height
        self.scatter.pos=(0,0)
        #Window.center[0] - (self.imagenPagina.width ), 0)
        print("centrado")
        self.scatter.center = Window.center
    def build(self):
        flow = FloatLayout()
        flow.bind(on_touch_down=self.on_touch_down)
        self.comic = KivyComicBook("C:\\Users\\pclbu\\Pictures\\Detective Comics 942(2016)(2 covers)(Digital)(TLK-EMPIRE-HD).cbr")
        self.comic.openCbFile()
        self.scatter = Scatter()#scale_min=.5)

        self.imagenPagina = self.comic.getImagePage()
        self.scatter.size =self.imagenPagina.size
        self.scatter.size_hint = (None,None)
        self.scatter.add_widget(self.imagenPagina)
        self.scatter.do_rotation=False

        #centrar la imagen
        self.scatter.pos=(Window.center[0]-(self.imagenPagina.width/2),Window.center[1]-(self.imagenPagina.height/2))
        #ajustar tamañio a altura
        #alturaactual/#altura venta (regla de tres simple)
        self.scatter.scale=Window.height/self.imagenPagina.height
        flow.add_widget(self.scatter)
        return flow

if __name__ == "__main__":
    KivyVisor().run()
