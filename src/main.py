#!/usr/bin/env python
# -*- coding: UTF-8 -*-


__author__ = "Eduardo dos Santos Pereira"
__data__ = "14/02/2012"
__email__ = "pereira.somoza@gmail.com"

"""
Salve a Tartaruga: O urubu joga a tartaruga de dentro da sua viola
voce deve resgata-la com sua cesta. Baseado na historia popular
A festa no Ceu.
"""


import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.vector import Vector
from kivy.factory import Factory
from kivy.clock import Clock
from random import randint
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader





class LancaTartaruga(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    pontos = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class MoveUrubu(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class MoveCesto(Widget):
    pontos = NumericProperty(0)
    perdas = NumericProperty(0)


class TartarugaGame(Widget):

    tartaruga = ObjectProperty(None)
    urubu = ObjectProperty(None)
    cesto = ObjectProperty(None)
    btn1 = ObjectProperty(None)
    estado = "ON"
    imageBotao = "./icon/sonButton1.png"
    SomFundo = ObjectProperty(None)

    #SomFundo = SoundLoader.load('./music/backGroundSon.wav')
    grito =ObjectProperty(None)

    #SoundLoader.load('./music/grito.wav')
    popup = None

    def serve_tartaruga(self):
        self.tartaruga.center = self.center
        self.tartaruga.velocity = -Vector(0, 4).rotate(0)
        self.btn1.bind(on_press=self.LigaDesliga)

    def serve_urubu(self):
        self.urubu.center = self.center
        self.urubu.velocity = Vector(4, 0).rotate(0)

    def StopGame(self):
        self.tartaruga.velocity = Vector(0, 0).rotate(0)
        self.urubu.velocity = Vector(0, 0).rotate(0)
        self.urubu.center = self.width / 2, self.top - 100
        self.tartaruga.center = self.width / 2, self.top - 170

    def Sair(self, instance):
        import sys
        sys.exit()

    def RestartGame(self, instance):
        self.popup.dismiss()
        self.cesto.pontos = 0
        self.cesto.perdas = 0
        self.urubu.center = self.width / 2, self.top - 100
        self.tartaruga.center = self.width / 2, self.top - 170
        self.urubu.velocity = Vector(4, 0).rotate(0)
        self.tartaruga.velocity = - Vector(0, 4).rotate(0)

    def GameOver(self):

        content = BoxLayout(orientation='horizontal', size_hint_y=.7)

        if (self.cesto.pontos >= 100):
            texto = """
        Voce fez %s Pontos.
        Essa é a pontuacao maxima parabens.
        Se quiser jogar novamente aperte o botao: Reiniciar!
        Ou clique em Sair para terminar o Jogo\n
        Creditos: Eduardo S. Pereira
        email: pereira.somoza@gmail.com\n
        """ % self.cesto.pontos

        else:

            texto = """
        Voce fez %s Pontos.
        Tente novamente, botao Reiniciar!, ou clique em Sair
        para terminar o Jogo\n
        Creditos: Eduardo S. Pereira
        email: pereira.somoza@gmail.com\n
        """ % self.cesto.pontos

        replay = Button(text='Reiniciar!')
        sair = Button(text="Sair")
        label = Label(text=texto)
        info = BoxLayout(spacing=10, orientation="horizontal")
        action = BoxLayout(spacing=10, orientation='horizontal',\
                           size_hint_y=.3)
        content = BoxLayout(spacing=10, orientation='vertical')
        info.add_widget(label)
        action.add_widget(replay)
        action.add_widget(sair)
        content.add_widget(info)
        content.add_widget(action)

        replay.bind(on_press=self.RestartGame)
        sair.bind(on_press=self.Sair)

        self.StopGame()

        self.popup = Popup(title='Fim:',\
                      content=content, \
                      size_hint=(None, None),\
                      size=(400, 400),\
                      auto_dismiss=False)

        self.popup.open()

    def update(self, dt):
        self.tartaruga.move()
        self.urubu.move()

        if ((self.tartaruga.y <= 55) and (self.tartaruga.y >= 50)):

            if ((self.tartaruga.center_x <= self.cesto.center_x + 20) \
                and (self.tartaruga.center_x >= self.cesto.center_x - 20)):
                self.cesto.pontos += 1

                if(self.cesto.pontos >= 100):
                    self.GameOver()
            else:

                self.cesto.perdas += 1

                if(self.cesto.perdas <= 3):
                    self.Grito()
                if(self.cesto.perdas >= 3):
                    self.GameOver()

        if (self.tartaruga.y < 50):
            self.tartaruga.center = self.urubu.pos[0], self.top - 170
            self.tartaruga.velocity_y *= 1.1

            if(self.tartaruga.velocity_y < -15.0):
                self.tartaruga.velocity_y = 4 * abs(self.tartaruga.velocity_y)\
                                             / self.tartaruga.velocity_y

        if(self.urubu.x < 25) or (self.urubu.x > self.width - 150):
            self.urubu.velocity_x *= -1.0

    def on_touch_move(self, touch):
        self.cesto.center_x = touch.x

    def LigaDesliga(self, value):
        if(self.estado):
            if(self.estado == "ON"):
                self.estado = "OFF"

            elif(self.estado == "OFF"):
                self.estado = "ON"

    def MusicaFundo(self,dt):
        if(self.SomFundo):
            if(self.estado == "ON"):
                if (self.SomFundo.status == "stop"):
                    self.SomFundo.play()
            if(self.SomFundo.status == "play"):
                if (self.estado == "OFF"):
                    self.SomFundo.stop()

    def Grito(self):

        if(self.estado):
            if(self.estado == "ON"):

                def paraGrito(dt):
                    self.grito.stop()

                self.grito.play()
                Clock.schedule_once(paraGrito, 1.0)

Factory.register("MoveCesto", MoveCesto)
Factory.register("MoveUrubu", MoveUrubu)
Factory.register("LancaTartaruga", LancaTartaruga)


class TartarugaApp(App):

    icon = "./icon/Tartaruga2.png"
    title = "Salve a Tartaruga"

    def build(self):
        game = TartarugaGame()
        game.serve_tartaruga()
        game.serve_urubu()
        #game.SomFundo = SoundLoader.load('./music/backGroundSon.wav')
        game.grito = SoundLoader.load('./music/grito.wav')


        Clock.schedule_interval(game.update, 1.0 / 60)
        #Clock.schedule_interval(game.MusicaFundo, 1.0 / 60.0)

        return game

if __name__ in ('__android__', '__main__'):
    TartarugaApp().run()
