import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
ENEMY_SIZE = 40
BULLET_SIZE = 10
POWERUP_SIZE = 30
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Competitive Two-Player Shooting Game")

# Players
player1_x = WIDTH // 4 - PLAYER_SIZE // 2
player2_x = 3 * WIDTH // 4 - PLAYER_SIZE // 2
player_y = HEIGHT - 2 * PLAYER_SIZE
player_speed = 5
player1 = pygame.Rect(player1_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
player2 = pygame.Rect(player2_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

# Bullets
bullets1 = []
bullets2 = []
bullet_speed = 7

# Enemies
enemies = []
enemy_speed = 2
enemy_spawn_delay = 1000  # in milliseconds
last_enemy_spawn_time = 0

# Power-ups
powerups = []
powerup_spawn_delay = 5000  # in milliseconds
last_powerup_spawn_time = 0

# Game variables
score1 = 0
score2 = 0
lives1 = 3
lives2 = 3
level = 1
font = pygame.font.Font(None, 36)

# Power-up types
POWERUP_FIRE_RATE = "fire_rate"
POWERUP_SHIELD = "shield"

# Player state
player1_shielded = False
player2_shielded = False
player1_shield_end_time = 0
player2_shield_end_time = 0

# Game loop
clock = pygame.time.Clock()
game_over = False
winner = None  # Stores the winner when the game is over

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()

    # Player 1 controls (arrow keys to move, space to shoot)
    if keys[pygame.K_LEFT] and player1.x > 0:
        player1.x -= player_speed
    if keys[pygame.K_RIGHT] and player1.x < WIDTH // 2 - PLAYER_SIZE:
        player1.x += player_speed

    if keys[pygame.K_SPACE]:
        if len(bullets1) < 5:  # Limit bullet count
            bullet = pygame.Rect(player1.x + PLAYER_SIZE // 2 - BULLET_SIZE // 2, player1.y, BULLET_SIZE, BULLET_SIZE)
            bullets1.append(bullet)

    # Player 2 controls (WASD to move, Enter/Return to shoot)
    if keys[pygame.K_a] and player2.x > WIDTH // 2:
        player2.x -= player_speed
    if keys[pygame.K_d] and player2.x < WIDTH - PLAYER_SIZE:
        player2.x += player_speed

    if keys[pygame.K_RETURN]:
        if len(bullets2) < 5:  # Limit bullet count
            bullet = pygame.Rect(player2.x + PLAYER_SIZE // 2 - BULLET_SIZE // 2, player2.y, BULLET_SIZE, BULLET_SIZE)
            bullets2.append(bullet)

    # Spawn enemies
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time > enemy_spawn_delay:
        enemy_x = random.randint(0, WIDTH - ENEMY_SIZE)
        enemy = pygame.Rect(enemy_x, 0, ENEMY_SIZE, ENEMY_SIZE)
        enemies.append(enemy)
        last_enemy_spawn_time = current_time

    # Spawn power-ups
    if current_time - last_powerup_spawn_time > powerup_spawn_delay:
        powerup_x = random.randint(0, WIDTH - POWERUP_SIZE)
        powerup_type = random.choice([POWERUP_FIRE_RATE, POWERUP_SHIELD])
        powerup = pygame.Rect(powerup_x, 0, POWERUP_SIZE, POWERUP_SIZE)
        powerups.append((powerup, powerup_type))
        last_powerup_spawn_time = current_time

    # Move bullets and enemies
    for bullet in bullets1:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets1.remove(bullet)

    for bullet in bullets2:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets2.remove(bullet)

    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemies.remove(enemy)

    for powerup, powerup_type in powerups:
        powerup.y += enemy_speed
        if powerup.y > HEIGHT:
            powerups.remove((powerup, powerup_type))

    # Check for collisions
    for bullet in bullets1:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                bullets1.remove(bullet)
                enemies.remove(enemy)
                score1 += 1

    for bullet in bullets2:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                bullets2.remove(bullet)
                enemies.remove(enemy)
                score2 += 1

    for enemy in enemies:
        if enemy.colliderect(player1) and not player1_shielded:
            lives1 -= 1
            enemies.remove(enemy)
        if enemy.colliderect(player2) and not player2_shielded:
            lives2 -= 1
            enemies.remove(enemy)

    for powerup, powerup_type in powerups:
        if powerup.colliderect(player1):
            if powerup_type == POWERUP_FIRE_RATE:
                bullet_speed += 1
            elif powerup_type == POWERUP_SHIELD:
                player1_shielded = True
                player1_shield_end_time = current_time + 5000  # Shield lasts for 5 seconds
            powerups.remove((powerup, powerup_type))

        if powerup.colliderect(player2):
            if powerup_type == POWERUP_FIRE_RATE:
                bullet_speed += 1
            elif powerup_type == POWERUP_SHIELD:
                player2_shielded = True
                player2_shield_end_time = current_time + 5000  # Shield lasts for 5 seconds
            powerups.remove((powerup, powerup_type))

    # Check if shields have expired
    if current_time > player1_shield_end_time:
        player1_shielded = False
    if current_time > player2_shield_end_time:
        player2_shielded = False

    # Check for level completion
    if len(enemies) == 0:
        level += 1
        enemy_spawn_delay -= 100  # Make enemies spawn faster
        last_enemy_spawn_time = current_time

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, RED, player1)
    pygame.draw.rect(screen, BLUE, player2)

    for bullet in bullets1:
        pygame.draw.rect(screen, WHITE, bullet)

    for bullet in bullets2:
        pygame.draw.rect(screen, WHITE, bullet)

    for enemy in enemies:
        pygame.draw.rect(screen, WHITE, enemy)

    for powerup, powerup_type in powerups:
        if powerup_type == POWERUP_FIRE_RATE:
            pygame.draw.rect(screen, GREEN, powerup)
        elif powerup_type == POWERUP_SHIELD:
            pygame.draw.rect(screen, BLUE, powerup)

    # Display scores, lives, and level
    score1_text = font.render(f"Player 1 Score: {score1}", True, RED)
    score2_text = font.render(f"Player 2 Score: {score2}", True, BLUE)
    lives1_text = font.render(f"Player 1 Lives: {lives1}", True, RED)
    lives2_text = font.render(f"Player 2 Lives: {lives2}", True, BLUE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score1_text, (10, 10))
    screen.blit(score2_text, (WIDTH // 2 + 10, 10))
    screen.blit(lives1_text, (10, 50))
    screen.blit(lives2_text, (WIDTH // 2 + 10, 50))
    screen.blit(level_text, (10, 90))

    # Display shields (if active)
    if player1_shielded:
        pygame.draw.rect(screen, GREEN, pygame.Rect(player1.x - 5, player1.y - 5, PLAYER_SIZE + 10, PLAYER_SIZE + 10), 3)

    if player2_shielded:
        pygame.draw.rect(screen, GREEN, pygame.Rect(player2.x - 5, player2.y - 5, PLAYER_SIZE + 10, PLAYER_SIZE + 10), 3)

    # Check for game over
    if lives1 <= 0 or lives2 <= 0:
        if score1 > score2:
            winner = "Player 1 Wins!"
        elif score2 > score1:
            winner = "Player 2 Wins!"
        else:
            winner = "It's a Tie!"

        game_over = True

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False

    # Display the winner
    winner_text = font.render(winner, True, WHITE)
    screen.blit(winner_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
    pygame.display.flip()

pygame.quit()
sys.exit()
