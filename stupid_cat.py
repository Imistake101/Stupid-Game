import pygame
import random

pygame.init()

# Window dimensions (windowed mode only)
window_width = 800
window_height = 550
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Stupid Cat")

# Load images
background = pygame.image.load("photos/background.png")
cat = pygame.image.load("photos/cat.png")
bomb_img = pygame.image.load("photos/bomb.png")

# Load sound
meow = pygame.mixer.Sound("sounds/meow.mp3")

# Set the window icon
pygame.display.set_icon(cat)

# Load custom fonts
title_font = pygame.font.Font("RobotoMono-Bold.ttf", 60)
level_font = pygame.font.Font("RobotoMono-Bold.ttf", 36)

# Scale images
background = pygame.transform.scale(background, (window_width, window_height))
cat = pygame.transform.scale(cat, (80, 60))
bomb_img = pygame.transform.scale(bomb_img, (65, 65))  # Bomb size changed to 65x65

# Game variables
cat_x = 50
cat_y = window_height // 1
gravity = 0.80
cat_velocity = 0
cat_flap = -10

# Settings
meow_enabled = True

# Level and distance
level = 1
distance = 0

# Bomb variables
bombs = []
bomb_gap = 200  # Gap between each bomb (distance to the next bomb)
bomb_speed = 5
bomb_frequency = 25  # Frequency at which bombs are created

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, rect)

def draw_button(text, font, surface, x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color = (0, 122, 204)
    hover_color = (0, 162, 255)
    
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(surface, hover_color, (x, y, w, h), border_radius=10)
        
        if click[0] == 1 and action is not None:
            if not hasattr(draw_button, "button_clicked") or not draw_button.button_clicked:
                action()
                draw_button.button_clicked = True
        else:
            draw_button.button_clicked = False
    else:
        pygame.draw.rect(surface, color, (x, y, w, h), border_radius=10)
    
    text_obj = font.render(text, True, (255, 255, 255))
    rect = text_obj.get_rect(center=(x + w / 2, y + h / 2))
    surface.blit(text_obj, rect)

def game_over_screen():
    font_over = pygame.font.Font(None, 74)
    text = font_over.render("Game Over", True, (255, 255, 255))
    screen.blit(text, (window_width // 2, window_height // 2 - 90))
    pygame.display.update()
    button_font = pygame.font.Font(None, 36)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.blit(pygame.transform.scale(background, (window_width, window_height)), (0, 0))
        draw_button("Menu", button_font, screen, window_width // 2 - 75, window_height // 2 - 60, 150, 50, main_menu)
        draw_button("Try Again", button_font, screen, window_width // 2 - 75, window_height // 2, 150, 50, start_game)
        draw_button("Exit", button_font, screen, window_width // 2 - 75, window_height // 2 + 60, 150, 50, pygame.quit)
        pygame.display.update()

def main_menu():
    while True:
        screen.blit(pygame.transform.scale(background, (window_width, window_height)), (0, 0))
        draw_text("Stupid Cat", title_font, (255, 255, 255), screen, window_width // 2, window_height // 4)
        draw_button("Start Game", pygame.font.Font(None, 36), screen, window_width // 2 - 75, window_height // 2, 150, 50, start_game)
        draw_button("Settings", pygame.font.Font(None, 36), screen, window_width // 2 - 75, window_height // 2 + 60, 150, 50, settings_menu)
        draw_button("Exit", pygame.font.Font(None, 36), screen, window_width // 2 - 75, window_height // 2 + 120, 150, 50, pygame.quit)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def settings_menu():
    back_rect = pygame.Rect(window_width // 2 - 75, window_height // 2 + 60, 150, 50)
    while True:
        screen.blit(pygame.transform.scale(background, (window_width, window_height)), (0, 0))
        draw_text("Settings", title_font, (255, 255, 255), screen, window_width // 2, window_height // 4)
        draw_button(f"Sounds: {'On' if meow_enabled else 'Off'}", pygame.font.Font(None, 36), screen, window_width // 2 - 75, window_height // 2, 150, 50, toggle_meow_sound)
        draw_button("Back", pygame.font.Font(None, 36), screen, back_rect.x, back_rect.y, back_rect.width, back_rect.height)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return

def toggle_meow_sound():
    global meow_enabled
    meow_enabled = not meow_enabled

def start_game():
    global cat_x, cat_y, cat_velocity, level, distance, running, bombs
    running = True
    cat_x = 50
    cat_y = window_height // 2
    cat_velocity = 0
    level = 1
    distance = 0
    bombs = []  # Reset bombs each time a new game starts
    game_loop()

def create_bomb():
    # Create a bomb with a random y position
    gap_position = random.randint(100, window_height - 200)  # Ensure a good gap for the player
    bomb = pygame.Rect(window_width, gap_position, 65, 65)  # Bomb size set to 65x65
    bombs.append(bomb)

def game_loop():
    global cat_x, cat_y, cat_velocity, level, distance, running, bombs
    clock = pygame.time.Clock()

    # Track the distance based on the Y position of the cat (or another metric like time)
    last_cat_y = cat_y  # Store the initial position of the cat

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cat_velocity = cat_flap
                    if meow_enabled:
                        meow.play()

        cat_velocity += gravity
        cat_y += cat_velocity

        # Check for collision with top and bottom of the screen
        if cat_y < 0 or cat_y > window_height:
            game_over_screen()

        # Track the distance moved vertically (or consider using time instead)
        distance += abs(cat_y - last_cat_y)  # Increment based on Y position difference
        last_cat_y = cat_y  # Update the last Y position

        # Increment level every 1000 distance
        level = distance // 1000 + 1

        # Create new bombs randomly
        if random.randint(1, bomb_frequency) == 1:
            create_bomb()

        # Move bombs and check for collision
        for bomb in bombs[:]:
            bomb.x -= bomb_speed
            if bomb.colliderect(pygame.Rect(cat_x, cat_y, cat.get_width(), cat.get_height())):
                game_over_screen()
                running = False
            if bomb.x < 0:
                bombs.remove(bomb)

        # Draw everything
        screen.blit(pygame.transform.scale(background, (window_width, window_height)), (0, 0))
        screen.blit(cat, (cat_x, cat_y))

        # Draw bombs
        for bomb in bombs:
            screen.blit(bomb_img, bomb.topleft)

        # Draw level
        draw_text(f"Level: {level}", level_font, (255, 255, 255), screen, window_width // 2, 30)

        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    exit()

if __name__ == "__main__":
    main_menu()
