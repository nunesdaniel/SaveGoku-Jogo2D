import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from recursos.functions.functions import inicializarBancoDeDados
from recursos.functions.functions import escreverDados
from recursos.functions.functions import reconhecimento_inicial
from recursos.functions.pause import pause
import json
import pyttsx3
from datetime import datetime


if os.name == "posix":
    root = tk.Tk()
    root.update()
    root.destroy()

pygame.init()
tts = pyttsx3.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Save Goku!")
icone  = pygame.image.load("recursos/icons/icon.png")
pygame.display.set_icon(icone)
branco = (255,255,255)
verde = (0, 255, 10)
preto = (0, 0 ,0 )
sol = (255, 245, 225)
goku = pygame.image.load("recursos/images/goku.png").convert_alpha()
mascara_goku = pygame.mask.from_surface(goku)
fundoStart = pygame.image.load("recursos/images/menu.jpg")
fundoJogo = pygame.image.load("recursos/images/background.jpg")
fundoDead = pygame.image.load("recursos/images/lost.jpg")
missel = pygame.image.load("recursos/images/vegeta-collision.png").convert_alpha()
missel = pygame.transform.scale(missel, (145, 125))
mascara_vegeta = pygame.mask.from_surface(missel)
missileSound = pygame.mixer.Sound("recursos/sounds/missile.wav")
explosaoSound = pygame.mixer.Sound("recursos/sounds/explosion.wav")
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("recursos/sounds/soundtrack.mp3")
nuvem = pygame.image.load("recursos/images/nuvem.png").convert_alpha()
nuvem = pygame.transform.scale(nuvem, (120, 60))  # Ajuste o tamanho se necessário
sol = (255, 245, 225)
amarelo = (255, 255, 0)


def tela_boas_vindas(nome):
    instrucoes = [
        f"Bem-vindo, {nome}!",
        "Use as setas direcionais < > ou as teclas A / D para se mover.",
        "Pressione ESPAÇO para pausar o jogo.",
        "Desvie das capsulas do Vegeta para proteger o Goku!",
        "Pressione ENTER para começar."
    ]

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                return  # Começa o jogo

        tela.fill(preto)

        # Centraliza as instruções verticalmente
        altura_total = len(instrucoes) * 30
        y_inicial = (tela.get_height() - altura_total) // 2

        for i, linha in enumerate(instrucoes):
            texto = fonteMenu.render(linha, True, branco)
            x = (tela.get_width() - texto.get_width()) // 2
            y = y_inicial + i * 30
            tela.blit(texto, (x, y))

        pygame.display.update()
        relogio.tick(60)





def jogar():

    largura_janela = 300
    altura_janela = 50
    def obter_nome():
        global nome
        nome = entry_nome.get()  # Obtém o texto digitado
        if not nome:  # Se o campo estiver vazio
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")  # Exibe uma mensagem de aviso
        else:
            #print(f'Nome digitado: {nome}')  # Exibe o nome no console
            root.destroy()  # Fecha a janela após a entrada válida

    # Criação da janela principal
    root = tk.Tk()
    # Obter as dimensões da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)

    # Entry (campo de texto)
    entry_nome = tk.Entry(root)
    entry_nome.pack()

    # Botão para pegar o nome
    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()


    # Inicia o loop da interface gráfica
    root.mainloop()
    tela_boas_vindas(nome)
    # Falar o nome e desejar boa-sorte!
    tts.say(f"Boa sorte {nome}!")
    tts.runAndWait()
    posicaoXPersona = 426
    posicaoYPersona = 367
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXMissel = 400
    posicaoYMissel = -240
    velocidadeMissel = 1
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    pontos = 0
    #larguraPersona = 147
    #alturaPersona = 265
    #larguraVegetaCollision  = 200
    #alturaVegetaCollision  = 185
    #dificuldade = 0

    # Nuvem
    posicaoXNuvem = random.randint(0, 1000)
    posicaoYNuvem = random.randint(50, 150)
    velocidadeNuvem = random.choice([0.5, 1, 1.5])

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 15
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -15
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_d:
                movimentoXPersona = 15
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_a:
                movimentoXPersona = -15
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_d:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_a:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pause(tela, fonteMorte, tamanho)
        posicaoXPersona = posicaoXPersona + movimentoXPersona            
        posicaoYPersona = posicaoYPersona + movimentoYPersona            
        
        if posicaoXPersona < 0 :
            posicaoXPersona = 0
        elif posicaoXPersona >853:
            posicaoXPersona = 853
            
        if posicaoYPersona < 0 :
            posicaoYPersona = 0
        elif posicaoYPersona > 435:
            posicaoYPersona = 435
        
            
        tela.fill(branco)
        tela.blit(fundoJogo, (0,0))                          # Fundo
        pygame.draw.circle(tela, amarelo, (80, 80), 50)      # Sol

        #pygame.draw.circle(tela, (255, 165, 0), (200,40), tamanhoSol, tamanhoCircle )
        tela.blit( goku, (posicaoXPersona, posicaoYPersona) )
        
        posicaoYMissel = posicaoYMissel + velocidadeMissel
        if posicaoYMissel > 700:
            posicaoYMissel = -185
            pontos = pontos + 1
            velocidadeMissel = velocidadeMissel + 1
            posicaoXMissel = random.randint(0,1000)
            pygame.mixer.Sound.play(missileSound)
            
            
        tela.blit( missel, (posicaoXMissel, posicaoYMissel) )
        
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (15,15))
        
        texto = fonteMenu.render("Press Space to Pause Game", True, verde)
        tela.blit(texto, (15,45))

#        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
#        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
#        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + larguraVegetaCollision))
#        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + alturaVegetaCollision))
#        
#        os.system("cls")
#        # print( len( list( set(pixelsMisselX).intersection(set(pixelsPersonaX))   ) )   )
#        if  len( list( set(pixelsMisselY).intersection(set(pixelsPersonaY))) ) > dificuldade:
#            if len( list( set(pixelsMisselX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
#                escreverDados(nome, pontos)
#                dead()
#                
#            else:
#                print("Ainda Vivo, mas por pouco!")
#        else:
#            print("Ainda Vivo")

        # Calcula o deslocamento (offset) entre a posição do míssil e a posição do personagem (Goku)
        # Isso é necessário porque a função de colisão .overlap() precisa saber onde a segunda máscara (do míssil)
        # está posicionada em relação à primeira máscara (do personagem).
        offset = (
            int(posicaoXMissel - posicaoXPersona),  # Diferença horizontal entre o míssil e o personagem
            int(posicaoYMissel - posicaoYPersona)   # Diferença vertical entre o míssil e o personagem
        )

        # Verifica se houve colisão pixel a pixel entre as duas máscaras
        # A função .overlap() retorna a posição da colisão (x, y) se houver colisão entre pixels sólidos (não transparentes)
        # Caso contrário, retorna None.
        # Aqui, a máscara do personagem é usada como base, e a máscara do míssil é verificada na posição relativa (offset).
        colidiu = mascara_goku.overlap(mascara_vegeta, offset)


        # Se colidiu for diferente de None, houve colisão
        if colidiu:
            print("Morreu")  # Houve colisão entre os pixels sólidos
        else:
            print("Vivo")    # Não houve colisão, personagem ainda está ileso

        if colidiu:
            horario = datetime.now().strftime("%H:%M:%S")
            escreverDados(nome, pontos)
            dead()
            
        # Atualiza posição da nuvem
        posicaoXNuvem -= velocidadeNuvem
        if posicaoXNuvem < -120:
            posicaoXNuvem = 1000
            posicaoYNuvem = random.randint(50, 150)
            velocidadeNuvem = random.choice([0.5, 1, 1.5])  # Nova velocidade aleatória

        # Desenha a nuvem
        tela.blit(nuvem, (posicaoXNuvem, posicaoYNuvem))
        pygame.display.update()
        relogio.tick(60)


def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
            
            
        tela.fill(branco)
        tela.blit(fundoStart, (0,0) )

        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))
        
        pygame.display.update()
        relogio.tick(60)


def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    
    
    # Try para carregar e organizar os registros do log
    try:
        with open("./recursos/logs/log.dat", "r") as arquivo:
            log_partidas = json.load(arquivo)
    except:
        log_partidas = {}

    # Ordena e seleciona os 5 mais recentes
    registros_ordenados = sorted(log_partidas.items(), key=lambda x: x[1][1], reverse=True)
    ultimos_5_logs = registros_ordenados[:5]
    #root = tk.Tk()
    #root.title("Tela da Morte")

    # Adiciona um título na tela
    #label = tk.Label(root, text="Log das Partidas", font=("Arial", 16))
    #label.pack(pady=10)

    ## Criação do Listbox para mostrar o log
    #listbox = tk.Listbox(root, width=50, height=10, selectmode=tk.SINGLE)
    #listbox.pack(pady=20)

    ## Adiciona o log das partidas no Listbox
    #log_partidas = open("./recursos/logs/log.dat", "r").read()
    #log_partidas = json.loads(log_partidas)
    #for chave in log_partidas:
    #    listbox.insert(tk.END, f"Pontos: {log_partidas[chave][0]} na data: {log_partidas[chave][1]} - Nickname: {chave}")  # Adiciona cada linha no Listbox
    #
    #root.mainloop()
    while True:
        # Função do log para exibir os últimos 5 registros.
        # Carrega os registros do log
        try:
            with open("./recursos/logs/log.dat", "r") as arquivo:
                log_partidas = json.load(arquivo)
        except:
            log_partidas = {}

        # Ordena os logs pela data (valor [1]) ou qualquer outro critério se quiser
        registros_ordenados = sorted(log_partidas.items(), key=lambda x: x[1][1], reverse=True)
        ultimos_5_logs = registros_ordenados[:5]  # Pega os 5 últimos registros

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
        
            
            
        tela.fill(branco)
        tela.blit(fundoDead, (0,0) )

        # Título dos registros
        titulo = fonteMenu.render("Ranking das 5 Melhores Pontuações:", True, branco)
        tela.blit(titulo, (690, 20))

        # Exibe os últimos 5 registros
        for i, (nick, dados) in enumerate(ultimos_5_logs):
            texto = f"{i+1}. {nick} - Pontos: {dados[0]} - Data: {dados[1]}"
            linha = fonteMenu.render(texto, True, branco)
            tela.blit(linha, (535, 50 + i * 30))  # Linha inicial + espaçamento


        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))

        pygame.display.update()
        relogio.tick(60)
reconhecimento_inicial()
start()