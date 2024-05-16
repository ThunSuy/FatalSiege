import pygame

pygame.init()

WIDTH = 1200
HEIGHT = 640
SERVER = "localhost"
PORT = 5555

# Color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (62, 134, 151)
DARK_GRAY = (169, 169, 169)
OPTIONS_BG_COLOR = (255, 228, 181, 128)
OPTIONS_TEXT_COLOR = (139, 69, 19)
GREEN = (77, 176, 64)
PLAYER_1_COLOR = (170, 116, 101)
PLAYER_2_COLOR = (52, 98, 133)

GAMEPLAY_BG = (86, 54, 44)
WALL_COLOR = (72, 63, 66)
WALL_EDGE_COLOR = (64, 56, 54)

# Fonts
FONT_10 = pygame.font.SysFont('comicsans', 10)
FONT_15 = pygame.font.SysFont('comicsans', 15)
FONT_20 = pygame.font.SysFont('comicsans', 20)
FONT_25_bold = pygame.font.SysFont('comicsans', 25, bold=True)
FONT_30 = pygame.font.SysFont('comicsans', 30)
FONT_30_bold = pygame.font.SysFont('comicsans', 30, bold=True)
FONT_40 = pygame.font.SysFont('comicsans', 40)
FONT_40_bold = pygame.font.SysFont('comicsans', 40, bold=True)
FONT_50 = pygame.font.SysFont('comicsans', 50)
FONT_50_bold = pygame.font.SysFont('comicsans', 50, bold=True)
FONT_60 = pygame.font.SysFont('comicsans', 60)
FONT_60_bold = pygame.font.SysFont('comicsans', 60, bold=True)
FONT_80_bold = pygame.font.SysFont('comicsans', 80, bold=True)

# Background
start_bg = pygame.image.load(r"assets\images\background.png")
vs_img = pygame.image.load(r"assets\images\vs.png")

# Images
images_solider_red = []
for i in range(3):
    image = pygame.image.load(r"assets\images\solider_red_" + str(i) + ".png")
    images_solider_red.append(image)

images_solider_blue = []
for i in range(2):
    image = pygame.image.load(r"assets\images\solider_blue_" + str(i) + ".png")
    images_solider_blue.append(image)

img_bum_blue = pygame.image.load(r"assets\images\bum_blue.png")
img_wall = pygame.image.load(r"assets\images\wall.png")

images_cannon = []
for i in range(2):
    image = pygame.image.load(r"assets\images\db_blue_" + str(i) + ".png")
    images_cannon.append(image)
