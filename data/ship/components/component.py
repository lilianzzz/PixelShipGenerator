import pygame
from constants import *
from ..pixel_map import PixelMap


class Component(PixelMap):

    """ This is the base class for a ship
    component. It should not be directly created.
    Create() must be overwritten by subclass. This
    sets the initial value of the map
    """

    def __init__(self, xxx_todo_changeme, coord=(0, 0), autocreate=True, autooutline=True):

        (w, h) = xxx_todo_changeme
        self.x, self.y = coord
        self.color_code = None

        PixelMap.__init__(self, (w, h))

        self.name = 'generic'

        if autocreate:
            self.create()
            if autooutline:
                self.outline()

    def set_color_code(self, code):
        self.color_code = code

        for y in range(self.h):
            for x in range(self.w):
                if self.map[x][y] >= 1:
                    self.map[x][y] = self.color_code

    def add_pixel(self, xxx_todo_changeme1, value=1):

        (x, y) = xxx_todo_changeme1
        self.map[x][y] = value
        self.points.add((x, y))

    def create(self):
        pass

    def outline(self, trim=False):

        outline = set()
        for x, y in self.points:

            if y == 0 or y == self.h-1 or x == 0 or x == self.w-1:
                outline.add((x, y))
                continue

            adj = self.get_adj((x, y))
            for ax, ay in adj:
                if self.map[ax][ay] == 0:
                    outline.add((x, y))
                    break

        for px, py in outline:
            self.add_edge((px, py))

        if trim:
            self.trim_outline(outline)

    # to be wrapped by outline in certain component types
    def alt_outline(self, trim=False):

        outline = set()

        for y in range(self.h):
            for x in range(self.w):
                if self.map[x][y] >= 1:
                    continue
                adj = self.get_adj((x, y))
                for ax, ay in adj:
                    if self.map[ax][ay] >= 1:
                        outline.add((x, y))
                        break

        for point in outline:
            self.add_edge(point)

        if trim:
            self.trim_outline(outline)

    def trim_outline(self, outline):

        trim = set()

        for x, y in outline:
            adj = self.get_adj((x, y))
            next_to_pixel = False
            for ax, ay in adj:
                if self.map[ax][ay] >= 1:
                    next_to_pixel = True
                    break
            if not next_to_pixel:
                trim.add((x, y))

        for tx, ty in trim:
            self.trim_point((tx, ty))

    ##################################################################
    # realized this floodfill to outline was needlessly complicated
    # and would also fail to outline internal details
    def flood_outline(self):

        # flood fill from edge of map to set a border or black
        # around component

        edge = self.get_edge_set()
        seen = set()

        while edge:
            next = set()
            for x, y in edge:
                seen.add((x, y))
                if self.map[x][y] == 1:
                    self.map[x][y] = -1
                elif self.map[x][y] == 0:
                    next.add((x, y))
            edge = self.get_next_edge(next, seen)

    def get_next_edge(self, next, seen):

        edge = set()

        for point in next:
            adj = self.get_adj(point)
            for p in adj:
                if p not in seen:
                    edge.add(p)
        return edge

    def get_edge_set(self):

        edge = set()

        for y in range(self.h):
            for x in range(self.w):
                if y == 0 or y == self.h - 1:
                    edge.add((x, y))
                elif x == 0 or x == self.w - 1:
                    edge.add((x, y))

        return edge
    ####################################################################

    def get_relative_points(self, edge=False):

        if edge:
            pointset = self.edges
        else:
            pointset = self.points

        rel = set()
        for x, y in pointset:
            nx = x + self.x
            ny = y + self.y
            rel.add((nx, ny))

        return rel

    # adds a component object's map to current map
    def add(self, component):

        sx = component.x
        sy = component.y
        w = component.w
        h = component.h

        for y in range(h):
            for x in range(w):
                mx = sx + x
                my = sy + y
                c_value = component.map[x][y]
                if c_value != 0:
                    self.add_pixel((mx, my), value=c_value)

    def move(self, xxx_todo_changeme2):

        (x, y) = xxx_todo_changeme2
        self.x = x
        self.y = y

    # adding to ship
    def is_connected_to_ship(self, ship):

        rel_points = self.get_relative_points()

        # check if connected to spine
        on_spine = rel_points.intersection(ship.spine.points)
        if on_spine:
            return True

        rel_edges = self.get_relative_points(edge=True)
        on_edges = rel_edges.intersection(self.edges)
        if on_edges:
            return True

        return False

    def is_overlapping(self, ship):

        rel_points = self.get_relative_points()

        overlap = rel_points.intersection(ship.points)

        if overlap:
            return True, len(overlap)
        else:
            return False, 0

    def is_in_frame(self, ship):

        rel_points = self.get_relative_points()
        max = float(len(rel_points))
        in_frame = 0

        for point in rel_points:
            if ship.frame.is_in_frame(point):
                in_frame += 1

        ratio = in_frame / max
        if ratio >= ship.conformity:
            return True
        return False
