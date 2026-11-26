import pygame as py
import random
import sys
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
def draw_bg(w, h, c_1, c_2):
    bg_surf = py.Surface((1, 2))
    bg_surf.set_at((0, 0), c_1)
    bg_surf.set_at((0, 1), c_2)
    grad_surf = py.transform.smoothscale(bg_surf, (w, h))
    return grad_surf.convert()
def draw_player(color):
    player_surf = py.Surface((18, 18), py.SRCALPHA).convert_alpha()
    player_points = [(9, 0), (18, 9), (9, 18), (0, 9)]
    py.draw.polygon(player_surf, color, player_points)
    return player_surf
def draw_enemy(color):
    enemy_surf = py.Surface((20, 20), py.SRCALPHA).convert_alpha()
    enemy_points = [(0, 0), (0, 20), (20, 20), (20, 0)]
    py.draw.polygon(enemy_surf, color, enemy_points)
    return enemy_surf
def draw_projectile(color):
    p_surf = py.Surface((40, 10), py.SRCALPHA).convert_alpha()
    p_points = [(0, 3), (0, 7), (35, 7), (35, 10), (40, 5), (35, 0), (35, 3)]
    py.draw.polygon(p_surf, color, p_points)
    return p_surf
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
        self.speed = 1.5
        self.controls = controls
        self.image = draw_player(self.color)
        self.rect = self.image.get_rect(center=(x, y))
    def key_input(self):
        keys = py.key.get_pressed()
        self.vel_x = 0
        self.vel_y = 0
        if keys[self.controls['left']]:
            self.vel_x = -1 * self.speed * 60
        if keys[self.controls['right']]:
            self.vel_x = self.speed * 60
        if keys[self.controls['up']]:
            self.vel_y = -1 * self.speed * 60
        if keys[self.controls['down']]:
            self.vel_y = self.speed * 60
    def update(self):
        self.key_input()
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.vel_x < 0 and self.rect.centerx > wall.rect.right:
                    self.x -= self.vel_x * dt
                    self.rect.left = wall.rect.right
                elif self.vel_x > 0 and self.rect.centerx < wall.rect.left:
                    self.x -= self.vel_x * dt
                    self.rect.right = wall.rect.left
                if self.vel_y < 0 and self.rect.centery > wall.rect.bottom:
                    self.rect.top = wall.rect.bottom
                    self.y -= self.vel_y * dt
                elif self.vel_y > 0 and self.rect.centery < wall.rect.top:
                    self.rect.bottom = wall.rect.top
                    self.y -= self.vel_y * dt
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
    def draw(self, scroll_x, scroll_y):
        screen.blit(self.image, (round(self.rect.x - scroll_x), round(self.rect.y - scroll_y)))

class Enemy:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.vel_x, self.vel_y = 0, 0
        self.color = color
        self.speed = random.uniform(1, 2)
        self.image = draw_enemy(color)
        self.rect = self.image.get_rect(center = (x, y))
    def update(self):
        if self.x < player.rect.centerx:
            self.vel_x = self.speed * 60
        elif self.x > player.rect.centerx:
            self.vel_x = -1 * self.speed * 60
        if self.y < player.rect.centery:
            self.vel_y = self.speed * 60
        elif self.y > player.rect.centery:
            self.vel_y = -1 * self.speed * 60
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.vel_x < 0 and self.rect.centerx > wall.rect.right:
                    self.x -= self.vel_x * dt
                    self.rect.left = wall.rect.right
                elif self.vel_x > 0 and self.rect.centerx < wall.rect.left:
                    self.x -= self.vel_x * dt
                    self.rect.right = wall.rect.left
                if self.vel_y < 0 and self.rect.centery > wall.rect.bottom:
                    self.y -= self.vel_y * dt
                    self.rect.top = wall.rect.bottom
                elif self.vel_y > 0 and self.rect.centery < wall.rect.top:
                    self.y -= self.vel_y * dt
                    self.rect.bottom = wall.rect.top
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
    def draw(self, scroll_x, scroll_y):
        screen.blit(self.image, (round(self.rect.x - scroll_x), round(self.rect.y - scroll_y)))

class Projectile:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.speed = 5
        self.vel_y, self.vel_x = 0, 0
        if player.vel_x > 0:
            self.vel_x = self.speed * 60
        elif player.vel_x < 0:
            self.vel_x = self.speed * -60
        if player.vel_y > 0:
            self.vel_y = self.speed * 60
        elif player.vel_y < 0:
            self.vel_y = self.speed * -60
        if player.vel_x == 0 and player.vel_y == 0:
            self.vel_x = self.speed * 60
        self.color = color
        self.image_right = draw_projectile(color)
        self.image_left = py.transform.rotate(self.image_right, 180)
        self.image_down = py.transform.rotate(self.image_right, 270)
        self.image_up = py.transform.rotate(self.image_right, 90)
        self.rect = self.image_right.get_rect(center = (x, y))
        image = self.image_right
    def update(self):
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        for wall in walls:
            if self.rect.colliderect(wall):
                return False
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
        return True
    def draw(self, scroll_x, scroll_y):
        image = self.image_right
        if self.vel_x > 0:
            if self.vel_y == 0:
                image = self.image_right
        elif self.vel_x < 0:
            if self.vel_y == 0:
                image = self.image_left
        elif self.vel_x == 0:
            if self.vel_y < 0:
                image = self.image_up
            elif self.vel_y > 0:
                image = self.image_down
            else:
                image = self.image_right
        screen.blit(image, (round(self.rect.x - scroll_x), round(self.rect.y - scroll_y)))
def reset_game():
    x, y, scrollx, scrolly, gamestate = 250, 250, 0, 0, 'playing'
    return x, y, scrollx, scrolly, gamestate

level_width, level_height = 1000, 1000
controls = {'left': py.K_LEFT, 'right': py.K_RIGHT, 'up': py.K_UP, 'down': py.K_DOWN, 'shoot': py.K_SPACE}
player = Player(250, 250, red, controls)
e1_list = []
for i in range(5):
    e1_list.append(Enemy(random.randint(0, level_width), random.randint(0, level_height), blue))
player.x, player.y, scroll_x, scroll_y, gamestate = reset_game()
walls = []
for i in range(5):
    walls.append(Wall(random.randint(0, level_width), random.randint(0, level_height), gray))
player_proj = []
bg = draw_bg(width, height, green, green)
counter = 0

run = True
while run:
    for event in py.event.get():
        if event == py.QUIT:
            run = False
        if event.type == py.KEYDOWN:
            keys = py.key.get_pressed()
            if keys[player.controls['shoot']]:
                player_proj.append(Projectile(player.rect.centerx, player.rect.centery, player.color))

    dt = min(clock.tick(60) / 1000, 0.05)

    if gamestate == 'playing':
        counter += 1
        player.update()
        player_proj = [p for p in player_proj if p.update() == True]
        for e in e1_list:
            e.update()
            for p in player_proj[:]:
                if e.rect.colliderect(p):
                    e1_list.remove(e)
                    player_proj.remove(p)
                    e1_list.append(Enemy(0, 0, blue))
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
        for e in e1_list:
            if player.rect.colliderect(e):
                gamestate = 'lose'
    if gamestate == 'lose':
        run = False

    screen.blit(bg, (0, 0))
    for wall in walls:
        wall.draw(scroll_x, scroll_y)
    player.draw(scroll_x, scroll_y)
    for e in e1_list:
        e.draw(scroll_x, scroll_y)
    for p in player_proj:
        p.draw(scroll_x, scroll_y)
    py.display.update()

py.quit()
sys.exit()