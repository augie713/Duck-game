import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
DUCK_WIDTH, DUCK_HEIGHT = 50, 50
BG_COLOR = (135, 206, 235)
WHITE = (255, 255, 255)
TIMER_FONT_SIZE = 30
LEVEL_COMPLETE_TIME = 60  # Seconds per level

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Hunter")

# Load custom images
try:
    duck_image = pygame.image.load("duck image.jpg")
    duck_image = pygame.transform.scale(duck_image, (DUCK_WIDTH, DUCK_HEIGHT))
except pygame.error:
    print("Error: Could not load duck image. Using default green square.")
    duck_image = pygame.Surface((DUCK_WIDTH, DUCK_HEIGHT))
    duck_image.fill((0, 255, 0))

try:
    background_image = pygame.image.load("background1.jpg")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except pygame.error:
    print("Error: Could not load background image. Using default color.")
    background_image = None

# Font setup
font = pygame.font.SysFont('Arial', TIMER_FONT_SIZE)

# Game variables
score = 0
level = 1
time_remaining = LEVEL_COMPLETE_TIME


# Duck class
class Duck:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(100, HEIGHT - 100)
        self.speed = random.randint(2, 5) + level  # Increase speed with level
        self.direction = random.choice([1, -1])
        self.alive = True

    def move(self):
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= WIDTH - DUCK_WIDTH:
            self.direction *= -1
        self.y += random.randint(-1, 1)

    def draw(self):
        screen.blit(duck_image, (self.x, self.y))

    def is_clicked(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        return self.x < mouse_x < self.x + DUCK_WIDTH and self.y < mouse_y < self.y + DUCK_HEIGHT


# Main game loop
def game_loop():
    global score, level, time_remaining

    clock = pygame.time.Clock()
    running = True
    ducks = [Duck() for _ in range(level * 3)]  # More ducks per level
    start_ticks = pygame.time.get_ticks()

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for duck in ducks:
                        if duck.is_clicked(event.pos):
                            duck.alive = False
                            score += 1

        # Draw background
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BG_COLOR)

        # Update and draw ducks
        for duck in ducks:
            if duck.alive:
                duck.move()
                duck.draw()
            else:
                ducks.remove(duck)

        # Respawn ducks if cleared
        if len(ducks) == 0:
            level += 1
            ducks = [Duck() for _ in range(level * 3)]
            time_remaining = LEVEL_COMPLETE_TIME  # Reset timer for the next level
            start_ticks = pygame.time.get_ticks()

        # Update timer
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        time_remaining = max(0, LEVEL_COMPLETE_TIME - int(elapsed_seconds))

        # End game if time runs out
        if time_remaining <= 0:
            print("Game over! Your score:", score)
            running = False

        # Draw UI
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        timer_text = font.render(f"Time: {time_remaining}s", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        screen.blit(timer_text, (10, 90))

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


# Run the game
game_loop()
