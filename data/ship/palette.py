import data.ship.components.basic_hull as bh
import data.ship.components.angles as an
import data.ship.components.compound_components as cc
import data.ship.components.curves as cv
from random import *


class Palette(object):

    basic = ((bh.Rect, 0), (bh.Rect, 1), (bh.Rect, 3), (bh.Square, 0), (bh.Rect, 4))
    connector = ((bh.Rect, 2), (bh.Square, 1))
    angles = ((an.Angle, 0), (an.Angle, 1), (an.Angle, 2),
              (an.Angle, 3), (cc.Diamond, 0), (an.Angle, 4), (an.Angle, 5))
    special = ((cc.Circle, 0),)
    curves = ((cv.LongCurve, 0), (cv.LongCurve, 1), (cv.LongCurve, 2), (cv.LongCurve, 3),
              (cv.LongInvCurve, 0), (cv.LongInvCurve, 1), (cv.LongInvCurve, 2), (cv.LongInvCurve, 3)
              )

    def __init__(self):

        self.basic = randint(4, 12)
        self.connector = randint(0, 4)
        self.angles = randint(0, 1)
        self.curves = randint(0, 1)
        self.special = randint(0, 2)

        self.component_list = self.set_component_list()

    def get_component(self, color_code):

        generator, style = choice(self.component_list)
        component = generator.generate(style)
        component.set_color_code(color_code)

        return component

    def set_component_list(self):

        c_list = []

        for i in range(self.basic):
            c_list.append(choice(Palette.basic))

        for i in range(self.connector):
            c_list.append(choice(Palette.connector))

        for i in range(self.angles):
            c_list.append(choice(Palette.angles))

        for i in range(self.curves):
            c_list.append(choice(Palette.curves))

        for i in range(self.special):
            c_list.append(choice(Palette.special))

        return c_list
