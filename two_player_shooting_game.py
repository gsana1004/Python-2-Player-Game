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
player1 = pygame.Rect(WIDTH // 4, HEIGHT - 2 * PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
player1_speed_x = 0
player1_speed_y = 0
player1_bullets = []
player1_fire_rate = 1  # Bullet firing rate multiplier
player1_shielded = False
player1_shield_end_time = 0
player1_lives = 3
player1_score = 0

# Player 2
player2 = pygame.Rect(3 * WIDTH // 4, HEIGHT - 2 * PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
player2_speed_x = 0
player2_speed_y = 0
player2_bullets = []
player2_fire_rate = 1  # Bullet firing rate multiplier
player2_shielded = False
player2_shield_end_time = 0
player2_lives = 3
player2_score = 0

# Enemies
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
        if len(player1_bullets) < 5:
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
        if len(player2_bullets) < 5:
            bullet = pygame.Rect(
                player2.x + PLAYER_SIZE // 2 - BULLET_SIZE // 2,
                player2.y,
                BULLET_SIZE, BULLET_SIZE)
            player2_bullets.append(bullet)

    # Update player positions
    player1.x += player1_speed_x
    player1.y += player1_speed_y
    player2.x += player2_speed_x
    player2.y += player2_speed_y

    # Ensure players stay within screen boundaries
    player1.x = max(0, min(player1.x, WIDTH - PLAYER_SIZE))
    player1.y = max(0, min(player1.y, HEIGHT - 2 * PLAYER_SIZE))
    player2.x = max(0, min(player2.x, WIDTH - PLAYER_SIZE))
    player2.y = max(0, min(player2.y, HEIGHT - 2 * PLAYER_SIZE))

    # Spawn enemies
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time > ENEMY_SPAWN_INTERVAL:
        enemy_x = random.randint(0, WIDTH - ENEMY_SIZE)
        enemy = pygame.Rect(enemy_x, 0, ENEMY_SIZE, ENEMY_SIZE)
        enemies.append(enemy)
        last_enemy_spawn_time = current_time

    # Spawn power-ups
    if current_time - last_powerup_spawn_time > POWERUP_SPAWN_INTERVAL:
        powerup_x = random.randint(0, WIDTH - POWERUP_SIZE)
        powerup_type = random.choice([POWERUP_FIRE_RATE, POWERUP_SHIELD])
        powerup = pygame.Rect(powerup_x, 0, POWERUP_SIZE, POWERUP_SIZE)
        powerups.append((powerup, powerup_type))
        last_powerup_spawn_time = current_time

    # Move and update bullets
    player1_bullets = [bullet for bullet in player1_bullets if bullet.y > 0]
    player2_bullets = [bullet for bullet in player2_bullets if bullet.y > 0]

    for bullet in player1_bullets:
        bullet.y -= BULLET_SPEED

    for bullet in player2_bullets:
        bullet.y -= BULLET_SPEED

    # Move and update enemies
    enemies = [enemy for enemy in enemies if enemy.y < HEIGHT]
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
                player1_shield_end_time = current_time + 5000  # Shield lasts for 5 seconds
            powerups.remove((powerup, powerup_type))

        if player2.colliderect(powerup):
            if powerup_type == POWERUP_FIRE_RATE:
                player2_fire_rate = 2
            elif powerup_type == POWERUP_SHIELD:
                player2_shielded = True
                player2_shield_end_time = current_time + 5000  # Shield lasts for 5 seconds
            powerups.remove((powerup, powerup_type))

    # Check for power-up expiration
    if player1_fire_rate == 2 and current_time - player1_shield_end_time > 0:
        player1_fire_rate = 1
    if player2_fire_rate == 2 and current_time - player2_shield_end_time > 0:
        player2_fire_rate = 1

    # Check for game over
    if player1_lives <= 0 or player2_lives <= 0:
        game_over = True

    # Draw everything
    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, GREEN, player1)
    pygame.draw.rect(screen, BLUE, player2)

    for bullet in player1_bullets:
        pygame.draw.rect(screen, RED, bullet)

    for bullet in player2_bullets:
        pygame.draw.rect(screen, RED, bullet)

    for enemy in enemies:
        pygame.draw.rect(screen, WHITE, enemy)

    for (powerup, powerup_type) in powerups:
        if powerup_type == POWERUP_FIRE_RATE:
            pygame.draw.rect(screen, (255, 165, 0), powerup)
        elif powerup_type == POWERUP_SHIELD:
            pygame.draw.rect(screen, BLUE, powerup)

    draw_text(f"Player 1 Lives: {player1_lives}", 10, 10, WHITE)
    draw_text(f"Player 2 Lives: {player2_lives}", 10, 50, WHITE)
    draw_text(f"Player 1 Score: {player1_score}", WIDTH // 2 - 100, 10, WHITE)
    draw_text(f"Player 2 Score: {player2_score}", WIDTH // 2 - 100, 50, WHITE)
    draw_text(f"Level: {level}", WIDTH - 100, 10, WHITE)

    pygame.display.flip()
    clock.tick(60)

# Game over screen
while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    winner_text = "Player 1 Wins!" if player1_score > player2_score else "Player 2 Wins!" if player2_score > player1_score else "It's a Tie!"
    draw_text(f"Game Over - {winner_text}", WIDTH // 2 - 200, HEIGHT // 2 - 50, WHITE)
    draw_text(f"Player 1 Score: {player1_score}", WIDTH // 2 - 100, HEIGHT // 2, WHITE)
    draw_text(f"Player 2 Score: {player2_score}", WIDTH // 2 - 100, HEIGHT // 2 + 40, WHITE)
    draw_text("Press 'C' to Continue   Press 'Q' to Quit", WIDTH // 2 - 200, HEIGHT // 2 + 80, WHITE)
    pygame.display.flip()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        # Reset game state and continue
        if player1_lives <= 0:
            reset_player(player1)
        if player2_lives <= 0:
            reset_player(player2)
        enemies.clear()
        powerups.clear()
        level = 1
        last_enemy_spawn_time = 0
        last_powerup_spawn_time = 0
        game_over = False

    elif keys[pygame.K_q]:
        pygame.quit()
        sys.exit()

pygame.quit()
sys.exit()
