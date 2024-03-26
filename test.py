import pygame
import random

pygame.init()

# Paramètres de l'écran
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paramètres de l'oiseau
bird_x = 50
bird_y = 200
bird_width = 20
bird_height = 20
bird_velocity = 0

# Paramètres des tuyaux
pipe_width = 50
pipe_gap = 150
pipe_velocity = 3
pipes = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Fonction pour créer un nouveau tuyau
def create_pipe():
    random_y = random.randint(50, SCREEN_HEIGHT - 200)
    top_pipe = {'x': SCREEN_WIDTH, 'y': random_y}
    bottom_pipe = {'x': SCREEN_WIDTH, 'y': random_y + pipe_gap}
    pipes.extend((top_pipe, bottom_pipe))

# Fonction pour afficher le score
def show_score():
    score_surface = font.render(f"Score: {score}", True, WHITE)
    SCREEN.blit(score_surface, (10, 10))

# Boucle de jeu
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -8

    # Mouvement de l'oiseau
    bird_velocity += 0.5
    bird_y += bird_velocity

    # Mouvement des tuyaux
    for pipe in pipes:
        pipe['x'] -= pipe_velocity

        # Vérifie les collisions avec l'oiseau
        if (bird_x < pipe['x'] + pipe_width and
            bird_x + bird_width > pipe['x'] and
            bird_y < pipe['y'] + pipe_width and
            bird_y + bird_height > pipe['y']):
            # Collision détectée, fin de jeu
            running = False

        # Si le tuyau a dépassé l'oiseau sans collision, ajoute 1 au score
        if pipe['x'] + pipe_width < bird_x and not pipe['scored']:
            pipe['scored'] = True
            score += 1

    # Supprime les tuyaux qui sont sortis de l'écran
    pipes = [pipe for pipe in pipes if pipe['x'] > -pipe_width]

    # Crée de nouveaux tuyaux si nécessaire
    if len(pipes) == 0 or pipes[-1]['x'] < SCREEN_WIDTH - 200:
        create_pipe()

    # Dessine l'arrière-plan
    SCREEN.fill(BLACK)

    # Dessine l'oiseau
    pygame.draw.rect(SCREEN, WHITE, (bird_x, bird_y, bird_width, bird_height))

    # Dessine les tuyaux
    for pipe in pipes:
        pygame.draw.rect(SCREEN, WHITE, (pipe['x'], 0, pipe_width, pipe['y']))
        pygame.draw.rect(SCREEN, WHITE, (pipe['x'], pipe['y'] + pipe_gap, pipe_width, SCREEN_HEIGHT))

    # Affiche le score
    show_score()

    # Met à jour l'écran
    pygame.display.update()

    # Limite le jeu à 60 FPS
    clock.tick(60)

# Une fois la boucle terminée (fin de jeu), affiche le score final pendant quelques secondes
game_over_surface = font.render(f"Game Over. Final Score: {score}", True, WHITE)
SCREEN.blit(game_over_surface, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
pygame.display.update()
pygame.time.delay(3000)  # Attend 3 secondes avant de fermer la fenêtre

pygame.quit()


