import pygame
import random
import math

# Inicializando o Pygame
pygame.init()

custom_font_path = "Pixeboy-z8XGD.ttf"
custom_font = pygame.font.Font(custom_font_path, 36)

# Definindo as dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Definindo título da janela
pygame.display.set_caption("Space Invaders")

# Carregar e redimensionar a imagem de fundo para cobrir toda a tela
background_img = pygame.transform.scale(pygame.image.load(r"background.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
background_gameover = pygame.transform.scale(pygame.image.load(r"game_over_background.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
background_victory = pygame.transform.scale(pygame.image.load(r"victory_background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
player_img = pygame.image.load(r"ship.png")
enemy_img = pygame.image.load(r"enemy.png")
bullet_img = pygame.image.load(r"bullet.png")
heart_img = pygame.image.load(r"heart.png")
enemy_bullet_img = pygame.image.load(r"bullet_enemy.png")

# Configurações do jogo
PLAYER_SPEED = 7.0
BULLET_SPEED = 20.0
ENEMY_SPEED = 0.8
ENEMY_BULLET_SPEED = 4.0
FIRE_COOLDOWN = 450  # Tempo de espera entre os disparos do jogador

class Player:
    def __init__(self):
        self.x = 370
        self.y = 480
        self.change_x = 0
        self.lives = 3
        self.last_shot_time = 0

    def move(self):
        self.x += self.change_x
        self.x = max(0, min(self.x, SCREEN_WIDTH - 64))  # Restringir movimento dentro da tela

    def can_fire(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > FIRE_COOLDOWN:
            self.last_shot_time = current_time
            return True
        return False

    def draw(self):
        screen.blit(player_img, (self.x, self.y))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.change_x = ENEMY_SPEED
        self.visible = True

    def move(self, move_down):
        if self.visible:
            if move_down:
                self.y += 40
                self.change_x *= -1
            self.x += self.change_x

    def draw(self):
        if self.visible:
            screen.blit(enemy_img, (self.x, self.y))

class Bullet:
    def __init__(self, x, y):
        self.x = x + 16  # Ajuste para centralizar o tiro no jogador
        self.y = y + 10
        self.active = False

    def fire(self, x, y):
        self.x = x + 16
        self.y = y + 10
        self.active = True

    def move(self):
        if self.active:
            self.y -= BULLET_SPEED
            if self.y < 0:  # Se sair da tela, reinicia o estado
                self.active = False

    def draw(self):
        if self.active:
            screen.blit(bullet_img, (self.x, self.y))

class EnemyBullet:
    def __init__(self, x, y):
        self.x = x + 16  # Ajuste para centralizar o tiro no inimigo
        self.y = y + 10

    def move(self):
        self.y += ENEMY_BULLET_SPEED

    def draw(self):
        screen.blit(enemy_bullet_img, (self.x, self.y))

def is_collision(obj1_x, obj1_y, obj2_x, obj2_y):
    distance = math.sqrt((obj1_x - obj2_x) ** 2 + (obj1_y - obj2_y) ** 2)
    return distance < 27

def draw_lives(lives):
    for i in range(lives):
        screen.blit(heart_img, (SCREEN_WIDTH - 40 * (i + 1), SCREEN_HEIGHT - 40))

def show_game_over_menu():
    screen.blit(background_gameover), (0, 0)
    text = custom_font.render("Derrota!", True, (255, 0, 0))
    screen.blit(text, (300, 200))

    restart_text = custom_font.render("Pressione Enter para reiniciar", True, (255, 255, 255))
    exit_text = custom_font.render("Pressione Esc para sair", True, (255 ,255 ,255))
    
    screen.blit(restart_text, (200 ,300))
    screen.blit(exit_text, (200 ,350))
    
    pygame.display.update()

    # Aguardar a ação do usuário
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Pressionar Enter para reiniciar
                    game_loop()
                if event.key == pygame.K_ESCAPE:  # Pressionar Esc para sair
                    pygame.quit()
                    return

def show_victory_menu():
    screen.blit(background_victory), (0, 0)
    text = custom_font.render("salvou o mundo!", True, (0, 255, 0))
    screen.blit(text, (300, 200))

    restart_text = custom_font.render("Pressione ENTER para reiniciar", True, (255, 255, 255))
    exit_text = custom_font.render("Pressione ESC para sair", True, (255, 255, 255))
    
    screen.blit(restart_text, (200, 300))
    screen.blit(exit_text, (200, 350))

    pygame.display.update()

    # Aguardar a ação do usuário
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Pressionar Enter para reiniciar
                    game_loop()
                if event.key == pygame.K_ESCAPE:  # Pressionar Esc para sair
                    pygame.quit()
                    return

def show_start_menu():
    screen.blit(background_victory), (0, 0)
    font = pygame.font.Font(None, 74)
    text = custom_font.render("Space Invaders", True, (0, 0, 255))
    screen.blit(text, (300, 200))

    font = pygame.font.Font(None, 36)
    start_text = custom_font.render("Pressione Enter para iniciar", True, (255, 255, 255))
    exit_text = custom_font.render("Pressione Esc para sair", True, (255, 255, 255))
    

    screen.blit(start_text, (200, 300))
    screen.blit(exit_text, (200, 350))

    pygame.display.update()

    # Aguardar a ação do usuário
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Pressionar Enter para iniciar
                    return
                if event.key == pygame.K_ESCAPE:  # Pressionar Esc para sair
                    pygame.quit()
                    return

def reset_game():
    global player
    
    player.lives = 3
    player.x = 370

def game_loop():
    global player
    
    clock = pygame.time.Clock()
    
    player = Player()
    
    enemies_list = [Enemy(col * 80 + 50, row * 60 + 50) for row in range(3) for col in range(6)]
    
    player_bullet = Bullet(player.x, player.y)
    enemy_bullets = []
    
    while True:
        screen.blit(background_img, (0, 0))  # Desenhar fundo cobrindo toda a tela

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            # Movimento do jogador.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.change_x = -PLAYER_SPEED   
                if event.key == pygame.K_RIGHT:
                    player.change_x = PLAYER_SPEED   
                if event.key == pygame.K_SPACE and not player_bullet.active and player.can_fire():  
                    player_bullet.fire(player.x, player.y)  

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.change_x = 0

        player.move()

        # Verificar movimento dos inimigos como um bloco
        move_down = False
        for enemy in enemies_list:
            if enemy.visible:
                if enemy.x <= 0 or enemy.x >= SCREEN_WIDTH - 64:
                    move_down = True
                    break

        for enemy in enemies_list:
            enemy.move(move_down)

            # Verificar colisão entre os inimigos e o jogador.
            if enemy.visible and is_collision(enemy.x, enemy.y, player.x, player.y):
                player.lives -= 1
                enemy.visible = False  
                if player.lives <= 0:
                    show_game_over_menu()

            enemy.draw()

            # Lógica de disparo dos inimigos.
            if random.random() < 0.002 and enemy.visible:  # Ajustando a frequência dos tiros inimigos
                enemy_bullet = EnemyBullet(enemy.x + enemy_img.get_width() / 2 - enemy_bullet_img.get_width() / 2,
                                           enemy.y + enemy_img.get_height())
                enemy_bullets.append(enemy_bullet)

        player_bullet.move()
        player_bullet.draw()

        for bullet in enemy_bullets[:]:
            bullet.move()
            bullet.draw()

            # Verificar se a bala do jogador colidiu com os inimigos.
            for enemy in enemies_list:
                if player_bullet.active and enemy.visible and is_collision(player_bullet.x, player_bullet.y, enemy.x, enemy.y):
                    player_bullet.active = False
                    enemy.visible = False  
                    break

            # Verificar se a bala do inimigo colidiu com o jogador.
            if bullet.y > SCREEN_HEIGHT:
                enemy_bullets.remove(bullet)

            if is_collision(bullet.x, bullet.y, player.x, player.y):
                player.lives -= 1
                enemy_bullets.remove(bullet)
                if player.lives <= 0:
                    show_game_over_menu()

        # Desenhar o jogador e as vidas na tela.
        player.draw()
        
        draw_lives(player.lives)

        # Verifica se todos os inimigos foram derrotados e mostra o menu de vitória.
        if all(not enemy.visible for enemy in enemies_list):
            show_victory_menu()

        # Atualizar a tela.
        pygame.display.update()
        
        clock.tick(60)


# Exibir o menu de inicialização.
show_start_menu()

# Iniciar o jogo.
game_loop()
