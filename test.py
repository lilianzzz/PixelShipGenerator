import pygame
from pygame.locals import *
from constants import *
import data.ship.components.basic_hull as bh
import data.ship.components.compound_components as cc
import data.ship.components.curves as cv
import time
import data.ship.ship as ship
import data.ship.scan_outline as scan
from random import *


screen = pygame.display.get_surface()
sd=342968604
uss = ship.Ship((50, 50))
sc = scan.ScanOutline(uss)

uss.position((10, 10))
sc.position((10, 10))
uss.draw(screen)
sc.animate_trace()

pygame.display.update()

end = False
while not end:
    if pygame.event.wait().type in (KEYDOWN, QUIT):
        end = True

pygame.quit()
