import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants

info_object = pygame.display.Info()
WIDTH, HEIGHT = int(info_object.current_w * 0.98), int(info_object.current_h * 0.8)
PLAYER_SIZE = int(WIDTH * 0.03)
BULLET_SIZE = int(WIDTH * 0.006)
ENEMY_SIZE = int(WIDTH * 0.02)
POWERUP_SIZE = int(WIDTH * 0.01)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PLAYER_SPEED = int(WIDTH * 0.0048)
BULLET_SPEED = int(WIDTH * 0.0028)
ENEMY_SPEED = int(WIDTH * 0.0017)
ENEMY_SPAWN_INTERVAL = 1000
POWERUP_SPAWN_INTERVAL = 5000
POWERUP_FIRE_RATE = "fire_rate"
POWERUP_SHIELD = "shield"

# Overheating Bar Constants
OVERHEAT_MAX = 200  # Maximum overheating value
OVERHEAT_COOLDOWN = 3000  # Cooldown duration in milliseconds (3 seconds)
OVERHEAT_DECREMENT = 10  # Rate at which overheating decreases per frame

# Player Health Constants
PLAYER_MAX_HEALTH = 100
HEALTH_REGEN_RATE = 0.5  # Health regeneration rate per second

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two-Player Shooting Game")

# Fonts
font = pygame.font.Font(None, int(WIDTH * 0.02))

# Player 1
player1_img = pygame.image.load("assets/spaceship-1.png")
player1_img = pygame.transform.scale(player1_img, (PLAYER_SIZE, PLAYER_SIZE))
player1 = player1_img.get_rect()
player1.x = WIDTH // 4
player1.y = HEIGHT - 2 * PLAYER_SIZE
player1_speed_x = 0
player1_speed_y = 0
player1_bullets = []
player1_fire_rate = 1  # Bullet firing rate multiplier
player1_shielded = False
player1_shield_end_time = 0
player1_health = PLAYER_MAX_HEALTH
player1_score = 0
player1_overheat = 0
player1_overheat_cooldown = 0
player1_can_shoot = True  # Indicates if player 1 can shoot
player1_last_shot_time = 0
fire_rate_delay = 500

# Player 2
player2_img = pygame.image.load("assets/spaceship-2.png")
player2_img = pygame.transform.scale(player2_img, (PLAYER_SIZE, PLAYER_SIZE))
player2 = player2_img.get_rect()
player2.x = 3 * WIDTH // 4
player2.y = HEIGHT - 2 * PLAYER_SIZE
player2_speed_x = 0
player2_speed_y = 0
player2_bullets = []
player2_fire_rate = 1  # Bullet firing rate multiplier
player2_shielded = False
player2_shield_end_time = 0
player2_health = PLAYER_MAX_HEALTH
player2_score = 0
player2_overheat = 0
player2_overheat_cooldown = 0
player2_can_shoot = True  # Indicates if player 2 can shoot
player2_last_shot_time = 0

# Enemies
enemy_img = pygame.image.load("assets/enemy-ship.jpg")
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_SIZE, ENEMY_SIZE))
enemies = []

# Power-ups
powerups = []

# Game variables
level = 1
last_enemy_spawn_time = 0
last_powerup_spawn_time = 0
game_over = False
winner = None

# Time tracking for health regeneration
health_regeneration_timer = pygame.time.get_ticks()

# Initialize enemy rotation angle
enemy_rotation_angle = 0  # Initial rotation angle for enemy ships

# Function to draw text on the screen
def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to reset player position and status
def reset_player(player):
    player.x = WIDTH // 4 if player == player1 else 3 * WIDTH // 4
    player.y = HEIGHT - 2 * PLAYER_SIZE
    player_speed_x = 0
    player_speed_y = 0
    if player == player1:
        player1_bullets.clear()
    else:
        player2_bullets.clear()
    player_fire_rate = 1
    player_shielded = False
    player_shield_end_time = 0

def draw_health_bar(player_health, player_x, player_y):
    bar_width = int(PLAYER_SIZE * 1.5)
    health_bar_length = int(bar_width * (player_health / PLAYER_MAX_HEALTH))
    health_bar_rect = pygame.Rect(player_x, player_y - 10, health_bar_length, 5)
    pygame.draw.rect(screen, GREEN, health_bar_rect)
    pygame.draw.rect(screen, WHITE, (player_x, player_y - 10, bar_width, 5), 1)

# Game loop
clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Player 1 controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player1_speed_x = -PLAYER_SPEED
    elif keys[pygame.K_d]:
        player1_speed_x = PLAYER_SPEED
    else:
        player1_speed_x = 0

    if keys[pygame.K_w]:
        player1_speed_y = -PLAYER_SPEED
    elif keys[pygame.K_s]:
        player1_speed_y = PLAYER_SPEED
    else:
        player1_speed_y = 0

    if keys[pygame.K_SPACE]:
        if keys[pygame.K_SPACE] and player1_can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - player1_last_shot_time > fire_rate_delay:
                bullet = pygame.Rect(
                    player1.x + PLAYER_SIZE // 2 - BULLET_SIZE // 2,
                    player1.y,
                    BULLET_SIZE, BULLET_SIZE)
                player1_bullets.append(bullet)
                player1_last_shot_time = current_time
                player1_overheat += 10

    # Player 2 controls
    if keys[pygame.K_LEFT]:
        player2_speed_x = -PLAYER_SPEED
    elif keys[pygame.K_RIGHT]:
        player2_speed_x = PLAYER_SPEED
    else:
        player2_speed_x = 0

    if keys[pygame.K_UP]:
        player2_speed_y = -PLAYER_SPEED
    elif keys[pygame.K_DOWN]:
        player2_speed_y = PLAYER_SPEED
    else:
        player2_speed_y = 0

    if keys[pygame.K_RETURN]:
        if keys[pygame.K_RETURN] and player2_can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - player2_last_shot_time > fire_rate_delay:
                bullet = pygame.Rect(
                    player2.x + PLAYER_SIZE // 2 - BULLET_SIZE // 2,
                    player2.y,
                    BULLET_SIZE, BULLET_SIZE)
                player2_bullets.append(bullet)
                player2_last_shot_time = current_time
                player2_overheat += 10

    # Player 1 movement
    player1.x += player1_speed_x
    player1.y += player1_speed_y

    # Player 2 movement
    player2.x += player2_speed_x
    player2.y += player2_speed_y

    # Boundary checking for players
    player1.x = max(0, min(player1.x, WIDTH - PLAYER_SIZE))
    player1.y = max(0, min(player1.y, HEIGHT - PLAYER_SIZE))
    player2.x = max(0, min(player2.x, WIDTH - PLAYER_SIZE))
    player2.y = max(0, min(player2.y, HEIGHT - PLAYER_SIZE))

    # Move and update bullets
    for bullet in player1_bullets:
        bullet.y -= BULLET_SPEED

    for bullet in player2_bullets:
        bullet.y -= BULLET_SPEED

    # Spawn enemies
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time > ENEMY_SPAWN_INTERVAL:
        enemy_x = random.randint(0, WIDTH - ENEMY_SIZE)
        enemy_y = -ENEMY_SIZE  # Start enemies above the screen
        enemy = enemy_img.get_rect()
        enemy.x = enemy_x
        enemy.y = enemy_y
        enemies.append(enemy)
        last_enemy_spawn_time = current_time

    # Update enemy positions
    for enemy in enemies:
        enemy.y += ENEMY_SPEED

    # Rotate enemy images
    enemy_rotation_angle += 1  # Adjust the speed of rotation as needed

    # Cooldown for player 1
    current_time = pygame.time.get_ticks()
    if player1_overheat >= OVERHEAT_MAX:
        player1_can_shoot = False
        if current_time >= player1_overheat_cooldown:
            player1_can_shoot = True
            player1_overheat_cooldown = current_time + OVERHEAT_COOLDOWN  # Set cooldown end time
    else:
        player1_can_shoot = True

    # Cooldown for player 2
    if player2_overheat >= OVERHEAT_MAX:
        player2_can_shoot = False
        if current_time >= player2_overheat_cooldown:
            player2_can_shoot = True
            player2_overheat_cooldown = current_time + OVERHEAT_COOLDOWN  # Set cooldown end time
    else:
        player2_can_shoot = True

    # Decrease overheating for player 1
    if not player1_can_shoot and player1_overheat > 0:
        player1_overheat -= OVERHEAT_DECREMENT

    # Decrease overheating for player 2
    if not player2_can_shoot and player2_overheat > 0:
        player2_overheat -= OVERHEAT_DECREMENT

    # Check for collisions between bullets and enemies
    for bullet in player1_bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                player1_score += 1
                player1_bullets.remove(bullet)
                enemies.remove(enemy)

    for bullet in player2_bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                player2_score += 1
                player2_bullets.remove(bullet)
                enemies.remove(enemy)

    # Check for collisions between players and enemies
    for enemy in enemies:
        if player1.colliderect(enemy):
            if not player1_shielded:
                player1_health -= 10  # Deduct 10% health
                if player1_health <= 0:
                    winner = "Player 2 Wins!"
                    game_over = True
                    break
            enemies.remove(enemy)

        if player2.colliderect(enemy):
            if not player2_shielded:
                player2_health -= 10  # Deduct 10% health
                if player2_health <= 0:
                    winner = "Player 1 Wins!"
                    game_over = True
                    break
            enemies.remove(enemy)

    # Check for collisions between players and power-ups
    powerups = [(powerup, powerup_type) for (powerup, powerup_type) in powerups if powerup.y < HEIGHT]
    for (powerup, powerup_type) in powerups:
        powerup.y += 1  # Move the power-up downward

        if player1.colliderect(powerup):
            if powerup_type == POWERUP_FIRE_RATE:
                player1_fire_rate = 2
            elif powerup_type == POWERUP_SHIELD:
                player1_shielded = True
                player1_shield_end_time = pygame.time.get_ticks() + 5000  # Shield lasts for 5 seconds
            powerups.remove((powerup, powerup_type))

        if player2.colliderect(powerup):
            if powerup_type == POWERUP_FIRE_RATE:
                player2_fire_rate = 2
            elif powerup_type == POWERUP_SHIELD:
                player2_shielded = True
                player2_shield_end_time = pygame.time.get_ticks() + 5000  # Shield lasts for 5 seconds
            powerups.remove((powerup, powerup_type))

    # Check for power-up expiration
    current_time = pygame.time.get_ticks()
    if player1_fire_rate == 2 and current_time - player1_shield_end_time > 0:
        player1_fire_rate = 1
    if player2_fire_rate == 2 and current_time - player2_shield_end_time > 0:
        player2_fire_rate = 1

    # Health regeneration
    if current_time - health_regeneration_timer >= 1000:  # 1000 milliseconds = 1 second
        player1_health = min(PLAYER_MAX_HEALTH, player1_health + (HEALTH_REGEN_RATE * 1))
        player2_health = min(PLAYER_MAX_HEALTH, player2_health + (HEALTH_REGEN_RATE * 1))
        health_regeneration_timer = current_time

    # Draw everything
    screen.fill((0, 0, 0))

    screen.blit(player1_img, player1)
    screen.blit(player2_img, player2)

    # Draw overheating bars
    pygame.draw.rect(screen, WHITE, (10, 10, player1_overheat, 20))
    pygame.draw.rect(screen, WHITE, (WIDTH - 10 - player2_overheat, 10, player2_overheat, 20))

    for bullet in player1_bullets:
        pygame.draw.rect(screen, RED, bullet)

    for bullet in player2_bullets:
        pygame.draw.rect(screen, BLUE, bullet)

    for enemy in enemies:
        # Rotate and draw enemy images
        rotated_enemy = pygame.transform.rotate(enemy_img, enemy_rotation_angle)
        screen.blit(rotated_enemy, enemy)

    for (powerup, _) in powerups:
        pygame.draw.rect(screen, GREEN, powerup)

    # Display overheating warning for player 1
    if not player1_can_shoot:
        if current_time % 1000 < 500:  # Blink effect every 500 milliseconds
            draw_text("OVERHEATING", 10, 120, RED)

    # Display overheating warning for player 2
    if not player2_can_shoot:
        if current_time % 1000 < 500:  # Blink effect every 500 milliseconds
            draw_text("OVERHEATING", WIDTH - 200, 120, RED)

    health_bar_offset = 25

    # Draw health bars for both players
    draw_health_bar(player1_health, player1.x + (PLAYER_SIZE // 2) - int(PLAYER_SIZE * 0.75),
                    player1.y + PLAYER_SIZE + health_bar_offset)
    draw_health_bar(player2_health, player2.x + (PLAYER_SIZE // 2) - int(PLAYER_SIZE * 0.75),
                    player2.y + PLAYER_SIZE + health_bar_offset)

    pygame.display.flip()

    clock.tick(60)

# Display the winner and offer the option to restart or quit the game
play_again = False
while True:  # Keep this loop running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            # Reset the game
            game_over = False
            winner = None
            reset_player(player1)
            reset_player(player2)
            player1_health = PLAYER_MAX_HEALTH
            player2_health = PLAYER_MAX_HEALTH
            player1_score = 0
            player2_score = 0
            player1_overheat = 0
            player2_overheat = 0
            last_enemy_spawn_time = pygame.time.get_ticks()
            last_powerup_spawn_time = pygame.time.get_ticks()
            powerups = []
            enemies = []
            health_regeneration_timer = pygame.time.get_ticks()
            winner = None  # Reset the winner
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

    if winner:
        screen.fill((0, 0, 0))
        draw_text(winner, WIDTH // 2 - 100, HEIGHT // 2 - 20, WHITE)
        draw_text("Press 'P' to Play Again or 'Q' to Quit", WIDTH // 2 - 200, HEIGHT // 2 + 40, WHITE)
        pygame.display.flip()
    else:
        screen.fill((0, 0, 0))
        draw_text(f"Player 1 Health: {int(player1_health)}%", 10, 50, WHITE)
        draw_text(f"Player 1 Score: {player1_score}", 10, 90, WHITE)
        draw_text(f"Player 2 Health: {int(player2_health)}%", WIDTH - 200, 50, WHITE)
        draw_text(f"Player 2 Score: {player2_score}", WIDTH - 200, 90, WHITE)

        # Display overheating warning for player 1
        if not player1_can_shoot:
            if current_time % 1000 < 500:  # Blink effect every 500 milliseconds
                draw_text("OVERHEATING", 10, 120, RED)

        # Display overheating warning for player 2
        if not player2_can_shoot:
            if current_time % 1000 < 500:  # Blink effect every 500 milliseconds
                draw_text("OVERHEATING", WIDTH - 200, 120, RED)

        pygame.display.flip()

    clock.tick(60)
