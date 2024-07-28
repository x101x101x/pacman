import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
GRID_SIZE = 40
PACMAN_SPEED = 5
GHOST_SPEED = 4
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PACMAN_RADIUS = 50
GHOST_RADIUS = 50
DOT_RADIUS = 5
DOT_COLOR = (255, 255, 255)
SCORE_FONT_SIZE = 36

# Load sounds
eat_sound = pygame.mixer.Sound('Pacman - Eating (Sound Effect).mp3')  # Replace with your sound file
game_over_sound = pygame.mixer.Sound('PacMan Death Game Over - QuickSounds.com.mp3')  # Replace with your sound file

# Load images
pacman_image = pygame.image.load('pacman.png')
ghost_image = pygame.image.load('ghost.png')

# Initialize game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Escape the Rat")

clock = pygame.time.Clock()

# Player class
class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pacman_image, (PACMAN_RADIUS * 2, PACMAN_RADIUS * 2))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = PACMAN_SPEED
        self.direction = 'RIGHT'

    def update(self):
        dx, dy = 0, 0
        if self.direction == 'UP':
            dy = -self.speed
        elif self.direction == 'DOWN':
            dy = self.speed
        elif self.direction == 'LEFT':
            dx = -self.speed
        elif self.direction == 'RIGHT':
            dx = self.speed

        # Move Pacman
        self.rect.x += dx
        self.rect.y += dy

        # Wrap around the screen
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0

    def change_direction(self, direction):
        self.direction = direction

# Ghost class
class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(ghost_image, (GHOST_RADIUS * 2, GHOST_RADIUS * 2))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.speed = GHOST_SPEED
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

    def update(self):
        dx, dy = 0, 0
        if self.direction == 'UP':
            dy = -self.speed
        elif self.direction == 'DOWN':
            dy = self.speed
        elif self.direction == 'LEFT':
            dx = -self.speed
        elif self.direction == 'RIGHT':
            dx = self.speed

        # Move Ghost
        self.rect.x += dx
        self.rect.y += dy

        # Wrap around the screen
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0

# Dot class
class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((DOT_RADIUS * 2, DOT_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, DOT_COLOR, (DOT_RADIUS, DOT_RADIUS), DOT_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Function to handle events
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pacman.change_direction('UP')
            elif event.key == pygame.K_DOWN:
                pacman.change_direction('DOWN')
            elif event.key == pygame.K_LEFT:
                pacman.change_direction('LEFT')
            elif event.key == pygame.K_RIGHT:
                pacman.change_direction('RIGHT')
            elif event.key == pygame.K_m:  # Mute sound toggle
                toggle_mute()
            elif event.key == pygame.K_PLUS:  # Increase volume
                increase_volume()
            elif event.key == pygame.K_MINUS:  # Decrease volume
                decrease_volume()

    return False

# Function to toggle mute
def toggle_mute():
    if pygame.mixer.get_volume() == 0:
        pygame.mixer.set_volume(1.0)
    else:
        pygame.mixer.set_volume(0.0)

# Function to increase volume
def increase_volume():
    current_volume = pygame.mixer.get_volume()
    if current_volume < 1.0:
        new_volume = min(current_volume + 0.1, 1.0)
        pygame.mixer.set_volume(new_volume)

# Function to decrease volume
def decrease_volume():
    current_volume = pygame.mixer.get_volume()
    if current_volume > 0.0:
        new_volume = max(current_volume - 0.1, 0.0)
        pygame.mixer.set_volume(new_volume)

# Function to generate dots in rows and columns
def generate_dots():
    dots = pygame.sprite.Group()
    num_rows = SCREEN_HEIGHT // GRID_SIZE
    num_cols = SCREEN_WIDTH // GRID_SIZE

    for row in range(num_rows):
        for col in range(num_cols):
            x = col * GRID_SIZE + GRID_SIZE // 2
            y = row * GRID_SIZE + GRID_SIZE // 2
            dot = Dot(x, y)
            dots.add(dot)

    return dots

# Initialize sprites
all_sprites = pygame.sprite.Group()
pacman = Pacman()
ghosts = [Ghost() for _ in range(3)]  # Three ghosts
dots = generate_dots()  # Generate dots in rows and columns
all_sprites.add(pacman)
all_sprites.add(*ghosts)
all_sprites.add(dots)

# Game variables
score = 0
lives = 3
level = 1
game_over = False
victory = False

# Fonts
font = pygame.font.SysFont(None, SCORE_FONT_SIZE)

# Main game loop
running = True
while running:
    clock.tick(30)

    # Handle events
    running = not handle_events()

    # Update sprites
    if not game_over and not victory:
        pacman.update()
        for ghost in ghosts:
            ghost.update()

        # Check collisions with dots
        dot_collisions = pygame.sprite.spritecollide(pacman, dots, True)
        for dot in dot_collisions:
            score += 10
            eat_sound.play()

        # Check collisions with ghosts
        ghost_collisions = pygame.sprite.spritecollide(pacman, ghosts, False)
        if ghost_collisions:
            lives -= 1
            if lives <= 0:
                game_over = True
                game_over_sound.play()
            else:
                pacman.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                pygame.time.delay(1000)  # Pause briefly after collision

        # Check if all dots are eaten
        if len(dots) == 0:
            level += 1
            dots = generate_dots()
            all_sprites.add(dots)

        # Check victory condition
        if level > 3:
            victory = True

    # Draw everything
    screen.fill('pink')
    all_sprites.draw(screen)

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 10))

    # Draw game over or victory message
    if game_over:
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
    elif victory:
        victory_text = font.render("You Win!", True, WHITE)
        screen.blit(victory_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))

    pygame.display.flip()

# Quit pygame
pygame.quit()
