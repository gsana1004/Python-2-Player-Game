import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
BULLET_SIZE = 10
ENEMY_SIZE = 30
POWERUP_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PLAYER_SPEED = 5
BULLET_SPEED = 5
ENEMY_SPEED = 3
ENEMY_SPAWN_INTERVAL = 1000
POWERUP_SPAWN_INTERVAL = 5000
POWERUP_FIRE_RATE = "fire_rate"
POWERUP_SHIELD = "shield"

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two-Player Shooting Game")

# Fonts
font = pygame.font.Font(None, 36)

# Player 1
player1_img = pygame.image.load("/Users/gabrielsanandaji/pythongame/png-transparent-spaceshipone-spaceshiptwo-sprite-spacecraft-two-dimensional-space-spaceship-game-fictional-character-space.png")
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
player1_lives = 3
player1_score = 0

# Player 2
player2_img = pygame.image.load("/Users/gabrielsanandaji/pythongame/png-clipart-pokemon-character-illustration-asteroids-outpost-defender-miner-cube-pro-sprite-video-game-space-craft-game-symmetry.png")
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
player2_lives = 3
player2_score = 0

# Enemies
enemy_img = pygame.image.load("/Users/gabrielsanandaji/pythongame/png-transparent-digital-painting-decapoda-bird-exotic-pet-enemy-spaceship-spacecraft-pet-video-game.png")
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_SIZE, ENEMY_SIZE))

enemies = []

# Power-ups
powerups = []

# Game variables
level = 1
last_enemy_spawn_time = 0
last_powerup_spawn_time = 0
game_over = False

def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

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
        bullet = pygame.Rect(
            player1.x + PLAYER_SIZE // 2 - BULLET_SIZE // 2,
            player1.y,
            BULLET_SIZE, BULLET_SIZE)
        player1_bullets.append(bullet)

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
        bullet = pygame.Rect(
            player2.x + PLAYER_SIZE // 2 - BULLET_SIZE // 2,
            player2.y,
            BULLET_SIZE, BULLET_SIZE)
        player2_bullets.append(bullet)

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
        enemy_y = 0
        enemy = enemy_img.get_rect()
        enemy.x = enemy_x
        enemy.y = enemy_y
        enemies.append(enemy)
        last_enemy_spawn_time = current_time

    # Move and update enemies
    for enemy in enemies:
        enemy.y += ENEMY_SPEED

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
                player1_lives -= 1
                reset_player(player1)
            enemies.remove(enemy)

        if player2.colliderect(enemy):
            if not player2_shielded:
                player2_lives -= 1
                reset_player(player2)
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

    # Check for game over
    if player1_lives <= 0 or player2_lives <= 0:
        game_over = True

    # Draw everything
    screen.fill((0, 0, 0))

    screen.blit(player1_img, player1)
    screen.blit(player2_img, player2)

    for bullet in player1_bullets:
        pygame.draw.rect(screen, RED, bullet)

    for bullet in player2_bullets:
        pygame.draw.rect(screen, BLUE, bullet)

    for enemy in enemies:
        screen.blit(enemy_img, enemy)

    for (powerup, _) in powerups:
        pygame.draw.rect(screen, GREEN, powerup)

    draw_text(f"Player 1 Lives: {player1_lives}", 10, 10, WHITE)
    draw_text(f"Player 1 Score: {player1_score}", 10, 50, WHITE)
    draw_text(f"Player 2 Lives: {player2_lives}", WIDTH - 200, 10, WHITE)
    draw_text(f"Player 2 Score: {player2_score}", WIDTH - 200, 50, WHITE)

    pygame.display.flip()

    clock.tick(60)

# Game over screen
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    winner_text = ""
    if player1_lives <= 0:
        winner_text = "Player 2 Wins!"
    elif player2_lives <= 0:
        winner_text = "Player 1 Wins!"

    draw_text(winner_text, WIDTH // 2 - 100, HEIGHT // 2 - 20, WHITE)
    draw_text(f"Player 1 Score: {player1_score}", WIDTH // 2 - 100, HEIGHT // 2 + 20, WHITE)
    draw_text(f"Player 2 Score: {player2_score}", WIDTH // 2 - 100, HEIGHT // 2 + 60, WHITE)
    draw_text("Press 'C' to Continue or 'Q' to Quit", WIDTH // 2 - 200, HEIGHT // 2 + 120, WHITE)
    pygame.display.flip()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        # Reset the game
        player1_lives = 3
        player2_lives = 3
        player1_score = 0
        player2_score = 0
        reset_player(player1)
        reset_player(player2)
        enemies.clear()
        powerups.clear()
        level = 1
        game_over = False
        last_enemy_spawn_time = 0
        last_powerup_spawn_time = 0

    if keys[pygame.K_q]:
        pygame.quit()
        sys.exit()

pygame.quit()
sys.exit()
