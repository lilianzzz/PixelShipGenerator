# Pixel Ship Generator

For #procjam 2016

Сonvert to Python 3 add customisation in constants.py for ease of setup


CUSTOM_PATH = None #"C:\proj\PixelShipGenerator" # set to None to not use custom exports folder

SCALE = 1

SHIPW = 200 * SCALE # ship width
SHIPH = 200 * SCALE # ship width

CONFORMITY = .55 # conformity is percentage of tiles per component that should be in frame(defaults to .55)
SIZE = .15 # size is % of frame that must be filled to complete component stage(defaults to .15)
COMPONENTS = 400 # how many components to generate. (defaults to 100)
PLASEMENTS = 20 # how many placements to try before giving up on component placement (defaults to 20)
SEED = None # if None, generate a random seed else use this seed (defaults to None)


GRID_W = SCREENWIDTH // SHIPW # auto grid ships in program
GRID_H = SCREENHEIGHT // SHIPH # auto grid ships in program
