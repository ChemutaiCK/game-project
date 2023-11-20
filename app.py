import sys
import pygame
import cairo
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SIZE = 50
OBSTACLE_SIZE = 50
OBSTACLE_SPEED = 5

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Game")

# Load player and obstacle images
player_image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
pygame.draw.circle(player_image, RED, (PLAYER_SIZE // 2, PLAYER_SIZE // 2), PLAYER_SIZE // 2)

obstacle_image = pygame.Surface((OBSTACLE_SIZE, OBSTACLE_SIZE), pygame.SRCALPHA)
pygame.draw.rect(obstacle_image, RED, (0, 0, OBSTACLE_SIZE, OBSTACLE_SIZE))

# Initialize Pycairo surface for drawing
cairo_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
cr = cairo.Context(cairo_surface)

# Game variables
player_pos = [WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - PLAYER_SIZE - 10]
obstacles = []

clock = pygame.time.Clock()

score = 0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update player position
    keys = pygame.key.get_pressed()
    player_pos[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5

    # Ensure the player stays within the screen boundaries
    player_pos[0] = max(0, min(player_pos[0], WIDTH - PLAYER_SIZE))

    # Clear the entire surface
    cr.set_source_rgba(0, 0, 0, 0)
    cr.paint()

    # Draw player
    pygame_surface = pygame.image.tostring(player_image, 'RGBA')
    player_cairo_surface = cairo.ImageSurface.create_for_data(
        bytearray(pygame_surface), cairo.FORMAT_ARGB32, PLAYER_SIZE, PLAYER_SIZE
    )
    cr.save()  # Save the current context state
    cr.translate(player_pos[0], player_pos[1])  # Translate to the player position
    cr.set_source_surface(player_cairo_surface)
    cr.paint()
    cr.restore()  # Restore the context state to undo the translation

    # Generate obstacles
    if random.random() < 0.02:
        obstacle_pos = [random.randint(0, WIDTH - OBSTACLE_SIZE), 0]
        obstacles.append(obstacle_pos)

    # Move and draw obstacles
    for obstacle_pos in obstacles:
        obstacle_pos[1] += OBSTACLE_SPEED
        pygame_surface = pygame.image.tostring(obstacle_image, 'RGBA')
        obstacle_cairo_surface = cairo.ImageSurface.create_for_data(
            bytearray(pygame_surface), cairo.FORMAT_ARGB32, OBSTACLE_SIZE, OBSTACLE_SIZE
        )
        cr.set_source_surface(obstacle_cairo_surface, obstacle_pos[0], obstacle_pos[1])
        cr.paint()

    # Collision detection
    player_rect = pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE)
    for obstacle_pos in obstacles:
        obstacle_rect = pygame.Rect(obstacle_pos[0], obstacle_pos[1], OBSTACLE_SIZE, OBSTACLE_SIZE)
        if player_rect.colliderect(obstacle_rect):
            print("Game Over! Your Score:", score)
            pygame.quit()
            sys.exit()

    # Remove off-screen obstacles
    obstacles = [obstacle for obstacle in obstacles if obstacle[1] < HEIGHT]

    # Update and render the Pygame screen
    pygame_surface = pygame.image.frombuffer(cairo_surface.get_data(), (WIDTH, HEIGHT), "ARGB")
    screen.blit(pygame_surface, (0, 0))
    pygame.display.flip()

    # Increase score for each frame
    score += 1

    # Cap the frame rate
    clock.tick(FPS)
