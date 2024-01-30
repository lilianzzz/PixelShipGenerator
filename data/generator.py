from .constants import *
from .ship.ship import Ship
from .state import State
from .button import Button
from .ship.mirror import Mirror
import os


anim = False


class Generator(State):

    gridw = GRID_W
    gridh = GRID_H
    gridsize = gridw * gridh
    grid_list = list(range(gridsize))

    @classmethod
    def set_grid_ref(cls):
        grid = {}

        gridw = cls.gridw

        for key in cls.grid_list:
            x = key % gridw
            y = (key // gridw)
            grid[key] = (x, y)

        return grid

    @staticmethod
    def generate_ship(w=descale(SHIPW), h=descale(SHIPH), animating=anim):
        s = Ship((w, h), animating)
        return s

    def __init__(self, main):

        State.__init__(self, main)

        self.generating = True
        self.slot_cursor = 0

        self.grid_ref = self.set_grid_ref()
        self.point_ref = self.set_point_ref()
        self.ship_grid = self.init_ship_grid()

        self.selection_grid = self.set_selection_grid()
        self.selector, self.selrect = self.set_selector()

        self.saved_grid = self.set_saved_grid()
        self.saved_icon = pygame.image.load('assets/saved.png')
        self.saved_rect = self.saved_icon.get_rect()

        self.buttons = self.set_buttons()

        self.show_frame = False
        self.show_spine = False

    def set_selector(self):

        i = pygame.Surface((SHIPW, SHIPH))
        r = i.get_rect()
        i.fill(WHITE)
        i.set_colorkey(WHITE)
        pygame.draw.rect(i, YELLOW, r, 1)

        return i, r

    def set_selection_grid(self):

        sel = {}

        for point in list(self.point_ref.keys()):
            sel[point] = False

        return sel

    def set_saved_grid(self):

        saved = {}

        for point in list(self.point_ref.keys()):
            saved[point] = False

        return saved

    def set_point_ref(self):

        points = {}

        for x, y in list(self.grid_ref.values()):
            cx = x * SHIPW
            cy = y * SHIPH + BUTTONMARGIN
            points[(x, y)] = (cx, cy)

        return points

    def init_ship_grid(self):

        ship_grid = {}

        for i in Generator.grid_list:

            point = self.grid_ref[i]

            ship_grid[point] = None

        return ship_grid

    def draw_saved_icon(self, surface, xxx_todo_changeme):

        (px, py) = xxx_todo_changeme
        self.saved_rect.topleft = (px, py)
        surface.blit(self.saved_icon, self.saved_rect)

    def draw(self, surface):

        for (x, y), ship in list(self.ship_grid.items()):
            if ship is None:
                continue
            point = self.point_ref[(x, y)]
            i, r = ship.get_image(self.show_frame, self.show_spine)
            r.topleft = point
            surface.blit(i, r)

            if self.saved_grid[(x, y)]:
                self.draw_saved_icon(surface, point)

        for button in self.buttons:
            button.draw(surface)

        self.draw_selection_grid(surface)

    def draw_selection_grid(self, surface):

        for point, state in list(self.selection_grid.items()):
            if not state:
                continue
            self.selrect.topleft = self.point_ref[point]
            surface.blit(self.selector, self.selrect)

    def handle_input(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                self.main.end_main()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.main.end_main()

                elif event.key == K_SPACE:
                    self.toggle_generate_mode()

                elif event.key == K_i:
                    self.main.show_instructions()

                elif event.key == K_q:
                    self.screenshot()

                elif event.key == K_s:
                    self.save()

                elif event.key == K_f:
                    self.toggle_frame()

                elif event.key == K_v:
                    self.ver_flip()
                elif event.key == K_h:
                    self.hor_flip()
                elif event.key == K_n:
                    self.clockwise()
                elif event.key == K_b:
                    self.counter_clockwise()

            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_buttons(mouse_pos)
                self.check_grid(mouse_pos)

    def check_buttons(self, pos):

        for button in self.buttons:
            if button.mouse_over(pos):
                button.click()

    def check_grid(self, pos):

        for point in list(self.grid_ref.values()):
            if self.mouse_over_ship(point, pos):
                self.toggle_ship(point)

    def mouse_over_ship(self, xxx_todo_changeme1, xxx_todo_changeme2):
        (x, y) = xxx_todo_changeme1
        (mx, my) = xxx_todo_changeme2
        cx, cy = self.point_ref[(x, y)]
        return cx < mx < cx + SHIPW and cy < my < cy + SHIPH

    def toggle_ship(self, point):

        if self.ship_grid[point] is None:
            return

        if self.selection_grid[point]:
            self.selection_grid[point] = False
        else:
            self.selection_grid[point] = True

    def toggle_frame(self):

        if self.show_frame:
            self.show_frame = False
        else:
            self.show_frame = True

    def select(self):
        for point in list(self.point_ref.keys()):
            if self.ship_grid[point]:
                self.selection_grid[point] = True

    def deselect(self):
        for point in list(self.point_ref.keys()):
            self.selection_grid[point] = False

    def save(self):

        for point in list(self.selection_grid.keys()):
            if self.selection_grid[point]:
                ship = self.ship_grid[point]
                filename = '../exports/ship%s.png' % ship.ship_id

                if not os.path.isfile(filename):

                    i, r = ship.get_image()
                    pygame.image.save(i, filename)
                    self.saved_grid[point] = True

    def transform(self, method):

        for point in list(self.selection_grid.keys()):
            if self.selection_grid[point]:
                ship = self.ship_grid[point]
                ship.transform(method)
                ship.update_image()
                self.saved_grid[point] = False

    def ver_flip(self):
        self.transform('ver_flip')

    def hor_flip(self):
        self.transform('hor_flip')

    def clockwise(self):
        self.transform('clockwise')

    def counter_clockwise(self):
        self.transform('counter_clockwise')

    def mirror(self, mtype, mid):
        for point in list(self.selection_grid.keys()):
            if self.selection_grid[point]:
                ship = self.ship_grid[point]
                if ship.mirrored is not None:
                    ship.revert()
                mir = Mirror.get_mirror(ship, mtype)
                mir.run()
                ship.mirrored = mid
                ship.update_image()
                ship.update_id()
                self.saved_grid[point] = False

    def mirror_va(self):
        self.mirror('vertical_a', 'mirrorva')

    def mirror_vb(self):
        self.mirror('vertical_b', 'mirrorvb')

    def mirror_ha(self):
        self.mirror('horizontal_a', 'mirrorha')

    def mirror_hb(self):
        self.mirror('horizontal_b', 'mirrorhb')

    def mirror_tl(self):
        self.mirror('quad_tl', 'mirrortl')

    def mirror_tr(self):
        self.mirror('quad_tr', 'mirrortr')

    def mirror_bl(self):
        self.mirror('quad_bl', 'mirrorbl')

    def mirror_br(self):
        self.mirror('quad_br', 'mirrorbr')

    def revert(self):
        for point in list(self.selection_grid.keys()):
            if self.selection_grid[point]:
                ship = self.ship_grid[point]
                ship.revert()
                ship.update_image()
                self.saved_grid[point] = False

    def set_buttons(self):

        bw = 78
        sbw = 24

        buttons = [Button('generate', (0, 0), self.toggle_generate_mode),
                   Button('save', (bw, 0), self.save),
                   Button('select', (2*bw, 0), self.select),
                   Button('deselect', (3*bw, 0), self.deselect),
                   Button('clkws', (4*bw, 0), self.clockwise),
                   Button('cntrclkws', (4*bw+sbw, 0), self.counter_clockwise),
                   Button('flipv', (4*bw+2*sbw, 0), self.ver_flip),
                   Button('fliph', (4*bw+3*sbw, 0), self.hor_flip),
                   Button('color_rand', (4*bw + 4*sbw, 0), self.reset_color_palette),
                   Button('color_mono_vary', (4*bw + 5*sbw, 0), self.toggle_mono),
                   Button('mirrorva', (4*bw + 7*sbw, 0), self.mirror_va),
                   Button('mirrorvb', (4 * bw + 8 * sbw, 0), self.mirror_vb),
                   Button('mirrorha', (4 * bw + 9 * sbw, 0), self.mirror_ha),
                   Button('mirrorhb', (4 * bw + 10 * sbw, 0), self.mirror_hb),
                   Button('mirrortl', (4 * bw + 11 * sbw, 0), self.mirror_tl),
                   Button('mirrortr', (4 * bw + 12 * sbw, 0), self.mirror_tr),
                   Button('mirrorbl', (4 * bw + 13 * sbw, 0), self.mirror_bl),
                   Button('mirrorbr', (4 * bw + 14 * sbw, 0), self.mirror_br),
                   Button('unmirror', (4*bw + 15*sbw, 0), self.revert),
                   Button('i', (SCREENWIDTH-24, 0), self.main.show_instructions)]

        return buttons

    def screenshot(self):

        screen = pygame.display.get_surface()
        sr = screen.get_rect()
        sr.topleft = (0, -BUTTONMARGIN)
        pic = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
        pic.blit(screen, sr)

        print('taking screen')
        pygame.image.save(pic, '../exports/screenshot.png')

    def update(self):

        if not self.generating:
            return

        slot = self.get_slot_to_generate()
        if slot is None:
            self.generating = False
            return

        self.fill_slot(slot)

    def get_slot_to_generate(self):

        for grid_id in range(self.slot_cursor, Generator.gridsize):
            point = self.grid_ref[grid_id]
            if not self.selection_grid[point]:
                self.increment_slot_cursor(grid_id)
                return point
            else:
                self.increment_slot_cursor(grid_id)

    def increment_slot_cursor(self, grid_id):

        self.slot_cursor = grid_id + 1
        if self.slot_cursor >= Generator.gridsize:
            self.slot_cursor = 0
            self.generating = False

    def fill_slot(self, point):

        ship = self.generate_ship()

        self.ship_grid[point] = ship
        self.saved_grid[point] = False

    def toggle_generate_mode(self):

        if self.generating:
            self.generating = False
        else:
            self.generating = True

    def reset_color_palette(self):

        for point in list(self.selection_grid.keys()):
            if self.selection_grid[point]:
                ship = self.ship_grid[point]
                ship.reset_color_palette()
                self.saved_grid[point] = False

    def toggle_mono(self):

        for point in list(self.selection_grid.keys()):
            if self.selection_grid[point]:
                ship = self.ship_grid[point]
                ship.toggle_mono_color()
                self.saved_grid[point] = False
