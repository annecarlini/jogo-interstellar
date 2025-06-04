
import pygame # Importando a biblioteca de jogos do Python
import random # Biblioteca que permite colocar o objeto em posição aleatória.
import pygame.image # Carrega uma imagem a partir de um arquivo
import cv2 # Biblioteca para exibir vídeo
import numpy as np

# Inicia o jogo:
pygame.init()

# Inicializando o mixer para a música:
pygame.mixer.init()

# Configurações da tela:
dis_width = 1200
dis_height = 700
screen = pygame.display.set_mode((dis_width, dis_height))  # Cria a tela com as medidas que definimos acima
clock = pygame.time.Clock() # Controla tempo e a taxa de atualização do jogo
pygame.display.set_caption("Interstellar")  
icon = pygame.image.load("icon_title.png")  
pygame.display.set_icon(icon)  # Coloca o ícone para aparecer na barra de tarefas.

# Definindo elementos visuais do jogo:
White = (255, 255, 255)

background = pygame.image.load("teste_bgbg.jpg")  # Variável definindo a imagem de fundo do jogo
background = pygame.transform.scale(background, (dis_width, dis_height)) # Váriavel redimensionando com base nas medidas width/height

game_over = pygame.image.load("gameover.png")
game_over_img = pygame.transform.scale(game_over, (dis_width, dis_height))

# Efeito sonoro do jogo:
def play_background_music():
    pygame.mixer.music.load("Space Harrier.MP3") 
    pygame.mixer.music.set_volume(0.7) # Ajusta o volume 
    pygame.mixer.music.play(-1) # Toca a música em loop infinito

def stop_background_music():
    pygame.mixer.music.stop()

# Definindo a tecla específica 'r' para reiniciar o jogo
KEY_RESTART = pygame.K_r 
KEY_START = pygame.K_s

# Parâmetros do jogo:
game_block = 50  # Dimensão dos elementos do jogo//pixel
game_speed = 6  # Velocidade do jogo//FPS

# Carregando novas skins:
astronaut_skins = {
    "astronaut1": pygame.transform.scale(pygame.image.load("astronaut.png"), (game_block, game_block)),
    "astronaut2": pygame.transform.scale(pygame.image.load("et 2.png"), (game_block, game_block))
}
select_skin = "astronaut1"

# Função para tela de seleção de personagem
def selection_screen():
    global select_skin
    running = True
    font = pygame.font.Font('Courier New.ttf', 16)

    intro_video("space.mov")  # Exibe o vídeo apenas uma vez antes da seleção de skin
    
    while running:
        screen.blit(background, (0, 0))  # Exibe o fundo corretamente
        text = font.render("Selecione seu astronauta: (1) Skin (2) Skin ", True, (255, 255, 255))
        screen.blit(text, (50, 50))

        # Exibindo as opções de seleção
        astronaut1 = pygame.image.load("astronaut.png")
        astronaut2 = pygame.image.load("et 2.png")
        
        # Exibe as imagens de skins
        screen.blit(astronaut1, (100, 100))
        screen.blit(astronaut2, (dis_width // 2, 100))
        
        pygame.display.flip()

        # Tratamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    select_skin = "astronaut1"
                    running = False  # Sai do loop para continuar o jogo
                elif event.key == pygame.K_2:
                    select_skin = "astronaut2"
                    running = False  # Sai do loop para continuar o jogo


# Carregando ícones:
astronaut_icon = pygame.image.load("astronaut.png")  # Astronauta
astronaut_icon = pygame.transform.scale(astronaut_icon, (game_block, game_block))  # Usada para redimensionar uma imagem.

star_icon = pygame.image.load("star_star.png")  # Estrela
star_icon = pygame.transform.scale(star_icon, (game_block, game_block)) # Usada para redimensionar uma imagem.

boost_star_icon = pygame.image.load("boost_star.png")
boost_star_icon = pygame.transform.scale(boost_star_icon, (game_block, game_block))

# Função para exibir o vídeo na introdução:
def intro_video(video_path):
    cap = cv2.VideoCapture(video_path) # Abre o arquivo de vídeo
    font = pygame.font.Font("SpaceHorizon-Regular.ttf", 15) # Define a fonte do texto
    
    # Loop principal 
    while True:
        ret, frame = cap.read() # Lê um frame do vídeo
        if not ret: # Se não conseguir ler, reinicia o vídeo
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue


        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Converte a imagem para RGB//formato usado pelo Pygame
        frame = cv2.resize(frame, (dis_height, dis_width)) # Resimensiona para o tamanho da tela
        frame = pygame.surfarray.make_surface(frame) # Converte o frame para superfice Pygame
        screen.blit(frame, (0,0))

       # Para criar a instrução em texto:
        font_text = font.render("Pressione 'S' para iniciar", True, (255, 255, 255))
        text_rect = font_text.get_rect() # Posição do retângulo para centralizar
        text_rect.center = (dis_width / 2, dis_height/ 1.2) # Posição do texto
        screen.blit(font_text, text_rect) 
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    cap.release()
                    return
                
    cap.release()
    

# Função de desenhar a estrela
def draw_food(food_x, food_y, star_type):
    if star_type == "normal": # Se for to tipo normal
        screen.blit(star_icon, (food_x, food_y))
    elif star_type == "boost": # Se for do tipo boost, que aumenta a velocidade
        screen.blit(boost_star_icon, (food_x, food_y))

# Função de desenhar o astronauta
def draw_astronaut(collected_stars): # Lista que armazena a posição das estrelas
    for star in collected_stars[:-1]: # Pega todos os elementos menos o último, porque o último representa o astronauta do inicio
        screen.blit(star_icon, (star[0], star[1]))  # Desenha as estrelas (corpo)

# Desenha a cabeça do astronauta
def draw_head(x, y):
    screen.blit(astronaut_skins[select_skin], (x, y)) # Posição x e y de onde fica o astronauta

# Função para criar as estrelas/comida:
def create_food(collected_stars):
    # Gera um número aleatório entre 0 e 1 para decidir o tipo de estrela
    star_type = random.choice(["normal", "boost"])

    while True:
        food_x = random.randrange(0, dis_width - game_block, game_block)  # Usa o módulo random para gerar posição aleatória
        food_y = random.randrange(0, dis_height - game_block, game_block) # Garante que a comida não seja gerada fora dos limites verticais da tela, define o espaçamento da grade
        
        # Verifica se a estrela não colide com o corpo do astronauta
        if (food_x, food_y) not in collected_stars:
            return food_x, food_y, star_type

# Função para criar a imagem de game over:
def show_game_over():
    screen.blit(game_over_img, (0, 0))  # Exibe a imagem
    pygame.display.update()  # Atualiza a tela
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Se clicar no "X", fecha o jogo
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:  #Se pressionar "R" reinicia o jogo
             if event.key == KEY_RESTART:
                 selection_screen()
                 waiting = False
                 gameLoop ()

# Função de selecionar direção/velocidade para definir a movimentação do astronauta:
def select_speed(keynote, speed_x, speed_y):
    if keynote == pygame.K_DOWN and speed_y != -game_block:
        speed_x = 0
        speed_y = game_block 
    elif keynote == pygame.K_UP and speed_y != game_block:
        speed_x = 0
        speed_y = -game_block
    elif keynote == pygame.K_RIGHT and speed_x != -game_block:
        speed_x = game_block
        speed_y = 0
    elif keynote == pygame.K_LEFT and speed_x != game_block:
        speed_x = -game_block
        speed_y = 0
    return speed_x, speed_y

# Função de desenhar a pontuação
def draw_score(score):
    font = pygame.font.SysFont("Courier New.ttf", 30)  # Escolhe a fonte e o tamanho.
    text = font.render(f"Estrelas coletadas: {score}", True, White)  # Renderiza o texto
    screen.blit(text, [500, 10])  # Posição da pontuação

play_background_music() # Inicia a música do jogo

selection_screen()

# Função que inicia o jogo:
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

    # Posição inicial da estrela
    food_x, food_y, star_type = create_food(collected_stars)
    
    # Variáveis para gerenciar o tempo de boost da boost_star
    boost_active = False
    boost_timer = 0

    while not end_game:  # Enquanto o jogo não acabar
        screen.blit(background, (0, 0))  # Coloca a imagem de fundo na posição 0,0 da tela.

        # Condição para verificar se ele bateu na parede: 
        if x < 0 or x >= dis_width or y < 0 or y >= dis_height:
            show_game_over()  # Exibe a tela de Game Over e espera uma tecla
            end_game = True  # Define o fim do jogo, não chama gameLoop() novamente

        # Pegar as interações do usuário:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Se o evento for de sair do jogo
                end_game = True
            elif event.type == pygame.KEYDOWN:  # Se pressionar uma tecla
                speed_x, speed_y = select_speed(event.key, speed_x, speed_y)  # Atualiza a velocidade/direção com base na tecla pressionada

        # Atualiza a posição do astronauta
        x += int(speed_x) # Atualiza a posição somando com speed_x ou speed_y
        y += int(speed_y)  # Garante que o número seja inteiro
        collected_stars.append((x, y))  # Atualiza o corpo do astronauta

        # Mantendo o comprimento do corpo e garante que é o mesmo até que ele colete novas estrelas
        if len(collected_stars) > length_astronaut:
            del collected_stars[0]  # Remove a última posição se o astronauta não pegar mais estrelas

        # Verificando se o astronauta bateu no próprio corpo
        for star in collected_stars[:-1]:
            if star == (x, y):  # Se a cabeça do astronauta for igual a algum pixel do corpo dele
                end_game = True  # Ele bateu nele mesmo e acabou o jogo
                show_game_over()  # Exibe a tela de Game Over e espera a resposta do usuário. 

        # Desenhando as estrelas como o corpo do astronauta
        draw_astronaut(collected_stars)
        draw_head(x, y)

        # Desenha a estrela normal ou boost
        draw_food(food_x, food_y, star_type)

        # Se pegar a estrela, armazena e gera uma nova posição
        if abs(x - food_x) < game_block and abs(y - food_y) < game_block: # Verifica se a posição do astronauta está proxima a estrela
            if star_type == "normal":
                length_astronaut += 1  # Se ele pegar, aumenta o tamanho do astronauta com as estrelas.
            elif star_type == "boost":
                length_astronaut += 3 # Aumenta a quantidade de estrelas coletadas com a boost também
                game_speed += 6 # Aumenta a velocidade, quando pega a boost_star
                boost_active = True
                boost_timer = 1200 # Tempo do boost ( 1200quadros)
        
            # Cria uma nova estrela e gera uma nova posição
            food_x, food_y, star_type = create_food(collected_stars)  

        # Diminui o timer do boost até retornar a velocidade original
        if boost_active:
            boost_timer -=1
            if boost_timer <= 0:
                game_speed -=6 # Retorna a velocidade original
                boost_active = False

        # Desenhando a pontuação:
        draw_score(length_astronaut - 1)

        # Atualização da tela após desenhar tudo:
        pygame.display.update()

        # Controla a taxa de quadros do jogo:
        clock.tick(game_speed)

    # Para a música:
    stop_background_music() 

gameLoop()  # Inicia o jogo
