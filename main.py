import pygame as py
py.init()
width = 500
height = 500
screen = py.display.set_mode((width, height))
clock = py.time.Clock()
font = py.font.SysFont(None, 35)

run = True
while run:
    for event in py.event.get():
        if event == py.QUIT:
            run = False

    clock.tick(60)
    py.display.update()

py.quit()
sys.exit()