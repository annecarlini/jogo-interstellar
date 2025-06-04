import pygame # Importando a biblioteca de jogos do Python
import random # Biblioteca que permite colocar o objeto em posição aleatória.
import pygame.image # Carrega uma imagem a partir de um arquivo
import cv2 # Biblioteca para exibir vídeo
import numpy as np

# Inicia o jogo
pygame.init()

# Configurações da tela
dis_width = 1200  # largura
dis_height = 700  # altura
screen = pygame.display.set_mode((dis_width, dis_height))  # Cria a tela com as medidas que definimos
clock = pygame.time.Clock() # Controla tempo e a taxa de atualização do jogo
pygame.display.set_caption("Jogo do astronauta")  # Nome que fica na barra de tarefas.
icon = pygame.image.load("icon.png")  # Ícone que fica ao lado do nome
# pygame.display.set_icon(icon)  # Coloca o ícone para aparecer na barra de tarefas.

# Definindo cores
White = (255, 255, 255)

# Definindo background
background = pygame.image.load("teste_bgbg.jpg")  # Variável definindo a imagem de fundo do jogo
background = pygame.transform.scale(background, (dis_width, dis_height)) # Váriavel redimensionando com base nas medidas width/height

# Definindo tela de game over
game_over = pygame.image.load("gameover.png")
game_over_img = pygame.transform.scale(game_over, (dis_width, dis_height)) # Váriavel redimensionando com base nas medidas width/height

# Efeito sonoro do jogo:
def play_background_music():
    pygame.mixer.music.load("Space Harrier.MP3") 
    pygame.mixer.music.set_volume(0.7) # Ajusta o volume 
    pygame.mixer.music.play(-1) # Toca a música em loop infinito

def stop_background_music():
    pygame.mixer.music.stop()

# Definindo a tecla específica 'r' para reiniciar o jogo
KEY_RESTART = pygame.K_r
flip_x = False

# Parâmetros do jogo
game_block = 50  # Dimensão dos pixels do jogo
game_speed = 6  # Velocidade do jogo

# Carregando personagens
astronaut_skins = {
    "astronaut1": pygame.transform.scale(pygame.image.load("astronaut.png"), (game_block, game_block)),
    "astronaut2": pygame.transform.scale(pygame.image.load("et 2.png"), (game_block, game_block))
}
selected_skin = "astronaut1"

star_icon = pygame.image.load("star_star.png")  # Estrela
star_icon = pygame.transform.scale(star_icon, (game_block, game_block)) # Usada para redimensionar uma imagem.

boost_star_icon = pygame.image.load("boost_star.png")
boost_star_icon = pygame.transform.scale(boost_star_icon, (game_block, game_block))

# Função para tela de seleção de personagem
def selection_screen():
    global selected_skin
    running = True
    font = pygame.font.Font(None, 36)
    
    while running:
        screen.fill(White)
        text = font.render("Selecione seu astronauta: (1) Skin 1     (2) Skin 2", True, (0, 0, 0))
        screen.blit(text, (50, 50))
        screen.blit(pygame.transform.scale(pygame.image.load("astronaut.png"), (dis_width//2, dis_height//2)), (100, 100))
        screen.blit(pygame.transform.scale(pygame.image.load("et 2.png"), (dis_width//2, dis_height//2)), (dis_width//2, 100))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_skin = "astronaut1"
                    running = False
                elif event.key == pygame.K_2:
                    selected_skin = "astronaut2"
                    running = False

# Função para exibir o vídeo na introdução
def intro_video(video_path):
    cap = cv2.VideoCapture(video_path)
    font = pygame.font.Font(pygame.font.get_default_font(), 15)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (dis_height, dis_width))
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0,0))
        
        font_text = font.render("Pressione ENTER para iniciar", True, (255, 255, 255))
        text_rect = font_text.get_rect()
        text_rect.center = (dis_width / 2, dis_height/ 4)
        screen.blit(font_text, text_rect)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    cap.release()
                    return
    cap.release()

# Função de desenhar o astronauta
def draw_head(x, y, spd_x):
    global flip_x
    if spd_x < 0:
        flip_x = True
    elif spd_x > 0:
        flip_x = False
    img = pygame.transform.flip(astronaut_skins[selected_skin], flip_x, False)
    screen.blit(img, (x, y))

# Função para desenhar o corpo do astronauta
def draw_astronaut(collected_stars):
    for star in collected_stars[:-1]:
        screen.blit(star_icon, (star[0], star[1]))

# Gera um número aleatório entre 0 e 1 para decidir o tipo de estrela
star_type = random.choice(["normal", "boost"])

# Função para criar a posição das estrelas
def create_food():
    food_x = random.randrange(0, dis_width - game_block, game_block)
    food_y = random.randrange(0, dis_height - game_block, game_block)
    return food_x, food_y

# Função de desenhar a estrela
def draw_food(food_x, food_y, star_type):
    if star_type == "normal": # Se for to tipo normal
        screen.blit(star_icon, (food_x, food_y))
    elif star_type == "boost": # Se for do tipo boost, que aumenta a velocidade
        screen.blit(boost_star_icon, (food_x, food_y))

# Função de desenhar o corpo do astronauta
def draw_astronaut(collected_stars): # Lista que armazena a posição das estrelas
    for star in collected_stars[:-1]: # Pega todos os elementos menos o último, porque o último representa o astronauta do inicio
        screen.blit(star_icon, (star[0], star[1]))  # Desenha as estrelas (corpo)

# Função para exibir o Game Over
def show_game_over():
    screen.blit(game_over_img, (0, 0))
    pygame.display.update()
    # pygame.time.delay(2000)
    key = None
    while key != pygame.K_r:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Se o evento for de sair do jogo
                return
            if event.type == pygame.KEYDOWN:
                key = event.key
    selection_screen()
    gameLoop()

# Função para selecionar velocidade
def select_speed(keynote, spd_x, spd_y):
    if keynote == pygame.K_DOWN:
        return 0, game_block
    elif keynote == pygame.K_UP:
        return 0, -game_block
    elif keynote == pygame.K_RIGHT:
        return game_block, 0
    elif keynote == pygame.K_LEFT:
        return -game_block, 0
    return spd_x, spd_y

play_background_music() # Inicia a música do jogo

# Vídeo de introdução
intro_video("space.mov")

# Função que inicia o jogo!
def gameLoop():

    global game_speed # Indica que você quer usar a variável global game_speed

    game_speed = 6 # Valor atribuido de game_speed

    end_game = False

    # Posição inicial do astronauta, por eixo. O astronauta sempre vai começar no meio da tela. 

    x = dis_width / 2 # Divide a posição inicial no meio da largura da tela
    y = dis_height / 2 # Divide a posição inicial no meio da altura da tela

    # Velocidade inicial do astronauta no jogo.
    speed_x = 0
    speed_y = 0

    # O tamanho que vai começar o astronauta
    length_astronaut = 1
    collected_stars = [(x, y)]  # Adiciona a posição inicial na lista

    # Posição da estrela
    food_x, food_y = create_food()

    while not end_game:  # Enquanto o jogo não acabar
        screen.blit(background, (0, 0))  # Coloca a imagem de fundo na posição 0,0 da tela.

        # Condição para verificar se ele bateu na parede
        if x < 0 or x >= dis_width or y < 0 or y >= dis_height:
            show_game_over()  # Exibe a tela de Game Over e espera uma tecla
            end_game = True  # Define o fim do jogo, não chama gameLoop() novamente
            
        # Pegar as interações do usuário
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Se o evento for de sair do jogo
                end_game = True
            elif event.type == pygame.KEYDOWN:  # Se pressionar uma tecla
                speed_x, speed_y = select_speed(event.key, speed_x, speed_y)  # Atualiza a velocidade/direção com base na tecla pressionada

        # Atualiza a posição do astronauta
        x += int(speed_x) # Atualiza a posição somando com speed_x ou speed_y
        y += int(speed_y)  # Garante que o número seja inteiro

        # Atualiza o corpo do astronauta
        collected_stars.append((x, y))

        # Mantendo o comprimento do corpo igual ao tamanho atual // Garante o comprimento do é o mesmo até que ele colete novas estrelas
        if len(collected_stars) > length_astronaut:
            del collected_stars[0]  # Remove a última posição se o astronauta não pegar mais estrelas

        # Verificando se o astronauta bateu no próprio corpo
        for star in collected_stars[:-1]:
            if star == (x, y):  # Se a cabeça do astronauta for igual a algum pixel do corpo dele
                end_game = True  # Ele bateu nele mesmo e acabou o jogo
                show_game_over()  # Exibe a tela de Game Over e espera uma tecla

        # Função para desenhar o astronauta (corpo do personagem)
        def draw_astronaut(collected_stars):
            for star in collected_stars[:-1]:  # Pega todas as partes do corpo, exceto a cabeça
                screen.blit(star_icon, (star[0], star[1]))  # Desenha as estrelas que formam o corpo
                
        def draw_score(points):
            font = pygame.font.SysFont("Courier New.ttf", 30) # Escolhe a fonte e o tamanho.
            txt = font.render(f'Estrelas Coletadas: {points}', False, (255,255,255)) # Renderiza o texto
            screen.blit(txt, (500,10)) # Posição da pontuação

        
        # Desenhando as estrelas como o corpo do astronauta
        draw_astronaut(collected_stars)

        # Desenhando o corpo (as estrelas)
        draw_head(x, y, speed_x)

        # Desenha a estrela normal ou boost
        draw_food(food_x, food_y, star_type)

    
        # Se pegar a estrela, armazena e gera uma nova posição
        if abs(x - food_x) < game_block and abs(y - food_y) < game_block: # Verifica se a posição do astronauta está proxima a estrela
            if star_type == "normal":
                length_astronaut += 1  # Se ele pegar, aumenta o tamanho do astronauta com as estrelas.
            elif star_type == "boost":
                length_astronaut += 1 # Aumenta a quantidade de estrelas coletadas com a boost também
                game_speed += 6 # Aumenta a velocidade, quando pega a boost_star
                boost_active = True
                boost_timer = 1200 # Tempo do boost ( 1200quadros)

        # Desenhando a pontuação
        draw_score(length_astronaut - 1)

        # Atualização da tela após desenhar tudo
        pygame.display.update()

        # Controla a taxa de quadros do jogo
        clock.tick(game_speed)

# Tela de seleção de personagem
selection_screen()

gameLoop()