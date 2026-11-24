import pygame as py
py.init()
width = 500
height = 500
screen = py.display.set_mode((width, height))
clock = py.time.Clock()
font = py.font.SysFont(None, 35)

red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
gray = [128, 128, 128]

def draw_wall(color):
    wall_surf = py.Surface((50, 50), py.SRCALPHA).convert_alpha()
    wall_points = [(0, 0), (0, 50), (50, 50), (50, 0)]
    py.draw.polygon(wall_surf, color, wall_points)
    return wall_surf
walls = []
def draw_bg(w, h, c_1):
    bg_surf = py.Surface((1, 2))
    bg_surf.set_at((0, 0), c_1)
    grad_surf = py.transform.smoothscale(bg_surf, (w, h))
    return grad_surf.convert()

def draw_player(color):
    player_surf = py.Surface((18, 18), py.SRCALPHA).convert_alpha()
    player_points = [(9, 0), (18, 9), (9, 18), (0, 9)]
    py.draw.polygon(player_surf, color, player_points)
    return player_surf
class Wall:
    def __init__(self, x, y, color):
        self.x, self.y = float(x), float(y)
        self.image = draw_wall(color)
        self.rect = self.image.get_rect(center=(x, y))
    def draw(self, scroll_x, scroll_y):
        screen.blit(self.image, (round(self.rect.x - scroll_x), round(self.rect.y - scroll_y)))
class Player:
    def __init__(self, x, y, color, controls):
        self.x, self.y = float(x), float(y)
        self.vel_x, self.vel_y = 0, 0
        self.color = color
        self.controls = controls
        self.image = draw_player(self.color)
        self.rect = self.image.get_rect(center=(x, y))
    def key_input(self):
        keys = py.key.get_pressed()
        self.vel_x = 0
        self.vel_y = 0
        if keys[self.controls['left']]:
            self.vel_x = -2 * 60
        if keys[self.controls['right']]:
            self.vel_x = 2 * 60
        if keys[self.controls['up']]:
            self.vel_y = -2 * 60
        if keys[self.controls['down']]:
            self.vel_y = 2 * 60
    def update(self):
        self.key_input()
        self.x += self.vel_x * dt
        self.rect.x = round(self.x)
        self.y += self.vel_y * dt
        self.rect.y = round(self.y)
    def draw(self, scroll_x, scroll_y):
        screen.blit(self.image, (round(self.rect.x - scroll_x), round(self.rect.y - scroll_y)))

        

def reset_game():
    x, y, scrollx, scrolly = 250, 250, 0, 0
    return x, y, scrollx, scrolly

controls = {'left': py.K_LEFT, 'right': py.K_RIGHT, 'up': py.K_UP, 'down': py.K_DOWN}
player = Player(250, 250, red, controls)
player.x, player.y, scroll_x, scroll_y = reset_game()
walls = []
walls.append(Wall(200, 200, gray))
bg = draw_bg(width, height, green)
level_width, level_height = 1000, 1000

run = True
while run:
    for event in py.event.get():
        if event == py.QUIT:
            run = False
    dt = min(clock.tick(60) / 1000, 0.05)

    player.update()
    target_scroll_x = player.rect.x - (width // 2)
    target_scroll_y = player.rect.y - (height // 2)
    scroll_x += (target_scroll_x - scroll_x) // 10
    scroll_y += (target_scroll_y - scroll_y) // 10
    if scroll_x < 0:
        scroll_x = 0
    if scroll_y < 0:
        scroll_y = 0
    if scroll_x > level_width:
        scroll_x = level_width
    if scroll_y > level_height:
        scroll_y = level_height

    screen.blit(bg, (0, 0))
    for wall in walls:
        wall.draw(scroll_x, scroll_y)
    player.draw(scroll_x, scroll_y)
    py.display.update()

py.quit()
sys.exit()