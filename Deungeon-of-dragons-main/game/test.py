import pygame
import sys

pygame.init()
scr = pygame.display.set_mode((1250, 750))
pygame.display.set_caption("Dungeons and Dragons")

icon = pygame.image.load('foto/icon/Avatar.jpg')
pygame.display.set_icon(icon)

menu_music = 'Music/nejnoe-spokoynoe-bezmyatejnoe-raznogolosoe-penie-ptits-v-lesu.mp3'
scene1_music = 'Music/morning-garden-acoustic-chill-15013_[cut_68sec].mp3'

pygame.mixer.music.load(menu_music)
pygame.mixer.music.play(-1)

font = pygame.font.SysFont('arial', 40)
WHITE = (255, 255, 255)

background = pygame.image.load('foto/scene/Menu_bg.jpg')
level1 = pygame.image.load('foto/scene/Tutorial_BG.png')
jorj = pygame.image.load('foto/5253577204917465249.jpg')

btn_play = pygame.image.load('foto/batton/image.png').convert_alpha()
btn_exit = pygame.image.load('foto/batton/imageQuti.png').convert_alpha()

def draw_animated_button(image, x, y, scale_hover=1.1, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = image.get_rect(topleft=(x, y))

    if button_rect.collidepoint(mouse):
        w, h = image.get_size()
        new_size = (int(w * scale_hover), int(h * scale_hover))
        scaled_img = pygame.transform.smoothscale(image, new_size)
        new_rect = scaled_img.get_rect(center=button_rect.center)
        scr.blit(scaled_img, new_rect.topleft)

        if click[0] == 1 and action:
            pygame.time.delay(200)
            action()
    else:
        scr.blit(image, (x, y))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15
            self.on_ground = False

        self.vel_y += 1  
        if self.vel_y > 10:
            self.vel_y = 10
        dy = self.vel_y

        self.on_ground = False


        self.rect.x += dx
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0:
                    self.rect.right = platform.rect.left
                if dx < 0:
                    self.rect.left = platform.rect.right


        self.rect.y += dy
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dy > 0: 
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.vel_y = 0
                elif dy < 0: 
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0



        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > 1250: self.rect.right = 1250
        if self.rect.top > 750: self.rect.topleft = (50, 500)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((139, 69, 19))  
        self.rect = self.image.get_rect(topleft=(x, y))


def main_menu():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)

    running = True
    while running:
        scr.blit(background, (0, 0))

        draw_animated_button(btn_play, 500, 300, action=tutorial)
        draw_animated_button(btn_exit, 500, 430, action=quit_game)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()

def tutorial():

    running = True
    while running:

        scr.blit(level1, (0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()




def scene1():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(scene1_music)
    pygame.mixer.music.play(-1)

    player = Player(50, 500)
    platforms = pygame.sprite.Group()
    platform_list = [
        Platform(0, 700, 1250, 50),
        Platform(200, 600, 150, 20),
        Platform(400, 500, 150, 20),
        Platform(100, 600, 10, 200),
        Platform(1000, 650, 100, 20),
    ]
    platforms.add(platform_list)

    goal = pygame.Rect(1150, 670, 80, 80)

    all_sprites = pygame.sprite.Group(player)
    running = True
    while running:
        scr.blit(level1, (0, 0))
        scr.blit(jorj, (250, 630))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.update(platform_list)
        all_sprites.draw(scr)
        platforms.draw(scr)

        pygame.draw.rect(scr, (255, 215, 0), goal)

        if player.rect.colliderect(goal):
            scene2()
            running = False

        pygame.display.update()
        pygame.time.Clock().tick(60)

def scene2():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(scene1_music)
    pygame.mixer.music.play(-1)

    player = Player(50, 500)
    platforms = pygame.sprite.Group()
    platform_list = [
        Platform(0, 700, 1250, 50),
        Platform(300, 620, 200, 20),
        Platform(550, 540, 150, 20),
        Platform(800, 460, 150, 20),
        Platform(1050, 380, 150, 20),  
    ]
    platforms.add(platform_list)

    goal = pygame.Rect(1150, 300, 80, 80)

    all_sprites = pygame.sprite.Group(player)
    running = True
    while running:
        scr.blit(level1, (0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.update(platform_list)
        all_sprites.draw(scr)
        platforms.draw(scr)

        pygame.draw.rect(scr, (0, 255, 0), goal)  

        if player.rect.colliderect(goal):
            print("Ви виграли!")
            running = False

        pygame.display.update()
        pygame.time.Clock().tick(60)

def quit_game():
    pygame.quit()
    sys.exit()

main_menu()