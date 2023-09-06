import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1790, 1100
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

# Overheating Bar Constants
OVERHEAT_MAX = 200  # Maximum overheating value
OVERHEAT_COOLDOWN = 3000  # Cooldown duration in milliseconds (3 seconds)
OVERHEAT_DECREMENT = 10  # Rate at which overheating decreases per frame

# Health Constants
MAX_HEALTH = 100
HEALTH_REGEN_RATE = 0.5  # Health regeneration rate (0.5% per second)
ENEMY_HEALTH = 4  # Enemy health
BULLET_DAMAGE = 2  # Bullet damage
PLAYER_DAMAGE = 2  # Player collision damage

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two-Player Shooting Game")

# Fonts
font = pygame.font.Font(None, 36)

# Player 1
player1_img = pygame.image.load("/Users/gabrielsanandaji/pythongame/png-transparent-spaceshipone-spaceshiptwo-sprite-spacecraft-two-dimensional-space-spaceship-game-fictional-character-space.png")
 # Replace with your player 1 image path
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
player1_health = MAX_HEALTH
player1_lives = 3
player1_can_shoot = True  # Indicates if player 1 can shoot
player1_last_shot_time = 0

# Player 2
player2_img = pygame.image.load("/Users/gabrielsanandaji/pythongame/png-clipart-pokemon-character-illustration-asteroids-outpost-defender-miner-cube-pro-sprite-video-game-space-craft-game-symmetry.png")
 # Replace with your player 2 image path
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
player2_health = MAX_HEALTH
player2_lives = 3
player2_can_shoot = True  # Indicates if player 2 can shoot
player2_last_shot_time = 0
fire_rate_delay = 500

# Enemies
enemy_img = pygame.image.load("/Users/gabrielsanandaji/pythongame/png-transparent-digital-painting-decapoda-bird-exotic-pet-enemy-spaceship-spacecraft-pet-video-game.png")
  # Replace with your enemy image path
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_SIZE, ENEMY_SIZE))
enemies = []

# Power-ups
powerups = []

# Game variables
level = 1
last_enemy_spawn_time = 0
last_powerup_spawn_time = 0
game_over = False

# Overheating Bar Variables
# ... (rest of your overheating bar variables)

# Health Variables
health_regen_timer = pygame.time.get_ticks()

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
        enemy_y = 0
        enemy = enemy_img.get_rect()
        enemy.x = enemy_x
        enemy.y = enemy_y
        enemies.append(enemy)
        last_enemy_spawn_time = current_time

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

    # Move and update enemies
    for enemy in enemies:
        enemy.y += ENEMY_SPEED

        # Check if enemy is out of screen, remove it
        if enemy.y > HEIGHT:
            enemies.remove(enemy)

    # Check for collisions between bullets and enemies
    for bullet in player1_bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                enemy_health = enemy_health - BULLET_DAMAGE
                player1_bullets.remove(bullet)
                if enemy_health <= 0:
                    enemies.remove(enemy)

    for bullet in player2_bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                enemy_health = enemy_health - BULLET_DAMAGE
                player2_bullets.remove(bullet)
                if enemy_health <= 0:
                    enemies.remove(enemy)

    # Check for collisions between players and enemies
    for enemy in enemies:
        if player1.colliderect(enemy):
            if not player1_shielded:
                player1_health -= PLAYER_DAMAGE
                reset_player(player1)
            enemies.remove(enemy)

        if player2.colliderect(enemy):
            if not player2_shielded:
                player2_health -= PLAYER_DAMAGE
                reset_player(player2)
            enemies.remove(enemy)

    # Health Regeneration
    current_time = pygame.time.get_ticks()
    if current_time - health_regen_timer > 1000:  # Regenerate health every 1000ms (1 second)
        if player1_health < MAX_HEALTH:
            player1_health += HEALTH_REGEN_RATE
        if player2_health < MAX_HEALTH:
            player2_health += HEALTH_REGEN_RATE
        health_regen_timer = current_time

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
    if player1_health <= 0:
        winner_text = "Player 2 Wins!"
    elif player2_health <= 0:
        winner_text = "Player 1 Wins!"

    draw_text(winner_text, WIDTH // 2 - 100, HEIGHT // 2 - 20, WHITE)
    draw_text("Press 'C' to Continue or 'Q' to Quit", WIDTH // 2 - 200, HEIGHT // 2 + 120, WHITE)
    pygame.display.flip()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        # Reset the game
        player1_health = MAX_HEALTH
        player2_health = MAX_HEALTH
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
