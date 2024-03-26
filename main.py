import pygame
import random

pygame.init()

HEIGHT_SCREEN = 448
WIDTH_SCREEN = 800
game_run = True
text_font = pygame.font.Font('FONT/flappy-font.ttf', 50)
d = 0
score = 0
depassement = False

# set the screen
screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption('Flappy_Py')
background = pygame.image.load("Graphics/background_flappy_bird.png")
base = pygame.image.load('Graphics/base_flappy_bird.png')
game_over = pygame.image.load('Graphics/gameover_flappy-bird.png')
game_over_rect = game_over.get_rect(center=(400, 224))
button_start = pygame.image.load('Graphics/Start-button-sprite-flappy-bird.png')
button_start_rect = button_start.get_rect(center=(400, 325))
menu_surface = pygame.surface.Surface((300, 200))
menu_surface_rect = menu_surface.get_rect(midtop=(game_over_rect.centerx, 175))
base_rect = base.get_rect(topleft=(0, 400))
base_rect1 = base.get_rect(topleft=(400, 400))
base_rect2 = base.get_rect(topleft=(800, 400))
base_rect3 = base.get_rect(topleft=(1200, 400))
base_rect4 = base.get_rect(topleft=(1600, 400))

clock = pygame.time.Clock()


class Obstacle:

    def __init__(self, player_rect):
        self.collition = False
        self.player_rect = player_rect
        self.obstaclex = 850
        self.obstacle1_y = random.randint(200, 335)
        self.obstacle2_y = self.obstacle1_y - 610
        self.obstacle1 = pygame.image.load('Graphics/pipe-green 6.png').convert_alpha()
        self.obstacle1_rect = self.obstacle1.get_rect(midtop=(self.obstaclex, self.obstacle1_y))
        self.obstacle2 = pygame.image.load('Graphics/pipe-green 1.png').convert_alpha()
        self.obstacle2_rect = self.obstacle2.get_rect(midtop=(self.obstaclex, self.obstacle2_y))

    def movement(self):
        self.obstacle1_rect.left -= 4
        self.obstacle2_rect.left -= 4

    def check_collition(self):
        if self.obstacle1_rect.colliderect(self.player_rect) or self.obstacle2_rect.colliderect(self.player_rect):
            self.collition = True
        else:
            self.collition = False


class Player:

    def __init__(self):
        self.gravity = 0
        self.animate = 0
        self.angle = 0
        self.list_sprite = []
        self.player1 = pygame.image.load('Player/bluebird-upflap.png')
        self.player2 = pygame.image.load('Player/bluebird-flappy bird(2).png')
        self.player3 = pygame.image.load('Player/bluebird-downflap.png')
        self.player_rect = self.player2.get_rect(center=(200, 224))
        self.list_sprite.append(self.player1)
        self.list_sprite.append(self.player2)
        self.list_sprite.append(self.player3)
        self.player = pygame.transform.rotate(self.list_sprite[self.animate], self.angle)

    def movement(self):
        self.gravity = -9
        self.angle = 29

    def gravity_apply(self):
        self.gravity += 0.6
        self.angle -= 2
        self.player_rect.bottom += player.gravity
        self.player = pygame.transform.rotate(self.list_sprite[int(self.animate)], self.angle)

    def animation(self):
        self.player = self.list_sprite[int(self.animate)]
        self.animate += 0.2
        if self.animate >= len(self.list_sprite):
            self.animate = 0


def put_obstacle_on_screen(obstacles):
    screen.blit(obstacles.obstacle1, obstacles.obstacle1_rect)
    screen.blit(obstacles.obstacle2, obstacles.obstacle2_rect)
    obstacles.movement()
    obstacles.check_collition()


def point_sys(obs):
    global score, depassement
    if not depassement and obs.obstacle1_rect.right < player.player_rect.left:
        score += 1
        depassement = True
    elif depassement and obs.obstacle1_rect.right > player.player_rect.left:
        depassement = False


player = Player()
obstacle = [Obstacle(player.player_rect)]

while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if game_run:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.movement()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                player.movement()
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and button_start_rect.collidepoint(event.pos):
                button_start_rect.bottom += 5
            if event.type == pygame.MOUSEBUTTONUP and button_start_rect.collidepoint(event.pos):
                button_start_rect.bottom -= 5
                game_run = True
                player.player_rect.center = (200, 224)
                score = 0
                d = 0
                depassement = False
                obstacle = [Obstacle(player.player_rect)]

    if game_run:
        d += 1
        score_txt = text_font.render(str(score), True, 'black')
        score_txt_rect = score_txt.get_rect(center=(400, 125))
        screen.blit(background, (0, 0))
        screen.blit(player.player, player.player_rect)
        player.animation()
        for i in obstacle:
            put_obstacle_on_screen(i)
            if i.collition:
                game_run = False
        screen.blit(base, base_rect)
        screen.blit(base, base_rect1)
        screen.blit(base, base_rect2)
        screen.blit(base, base_rect3)
        screen.blit(base, base_rect4)
        base_rect.left -= 4
        base_rect1.left -= 4
        base_rect2.left -= 4
        base_rect3.left -= 4
        base_rect4.left -= 4
        screen.blit(score_txt, score_txt_rect)
        point_sys(obstacle[0])
        player.gravity_apply()
        if d == 100:
            d = 0
            obstacle.append(Obstacle(player.player_rect))
        if player.player_rect.bottom >= 400:
            player.player_rect.bottom = 400
            player.angle = 0
        if base_rect.right <= 0:
            base_rect.left = base_rect4.right
        if base_rect1.right <= 0:
            base_rect1.left = base_rect.right
        if base_rect2.right <= 0:
            base_rect2.left = base_rect1.right
        if base_rect3.right <= 0:
            base_rect3.left = base_rect2.right
        if base_rect4.right <= 0:
            base_rect4.left = base_rect3.right
        for i in obstacle:
            if i.obstacle1_rect.right <= -100:
                obstacle.remove(i)

    else:
        pygame.draw.rect(screen, '#e3c96b', menu_surface_rect, border_radius=20)
        screen.blit(game_over, game_over_rect)
        screen.blit(button_start, button_start_rect)

    # update the screen
    pygame.display.update()
    clock.tick(65)
