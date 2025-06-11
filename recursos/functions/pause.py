import pygame
import speech_recognition as sr
import pyttsx3
import threading

def pause(tela, fonte_titulo, tamanho_tela):
    pausado = True
    clock = pygame.time.Clock()
    comando_voz_detectado = {"continuar": False}  # Usamos dict mutável para compartilhar entre threads

    # Texto "PAUSE"
    texto_pause = fonte_titulo.render("PAUSE", True, (255, 0, 0))
    rect_pause = texto_pause.get_rect(center=(tamanho_tela[0] // 2, tamanho_tela[1] // 2 - 50))

    # Instruções
    fonte_instrucao = pygame.font.SysFont("comicsans", 32)
    texto_instrucao = fonte_instrucao.render("Pressione [ESPAÇO] ou diga 'continuar'", True, (255, 255, 255))
    rect_instrucao = texto_instrucao.get_rect(center=(tamanho_tela[0] // 2, tamanho_tela[1] // 2 + 30))

    # Fundo translúcido
    overlay = pygame.Surface(tamanho_tela)
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))

    # Pausa a música
    pygame.mixer.music.pause()

    # Fala com o jogador
    try:
        tts = pyttsx3.init()
        tts.say("Jogo pausado. Pressione espaço ou diga continuar para voltar ao jogo.")
        tts.runAndWait()
    except:
        pass

    # Função paralela para reconhecimento de voz
    def escutar_comando():
        reconhecedor = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                reconhecedor.adjust_for_ambient_noise(source)
                audio = reconhecedor.listen(source, timeout=5)
                resposta = reconhecedor.recognize_google(audio, language="pt-BR").lower()
                print("Você disse:", resposta)
                if "continuar" in resposta:
                    comando_voz_detectado["continuar"] = True
        except:
            pass

    # Inicia a thread de escuta
    thread_voz = threading.Thread(target=escutar_comando)
    thread_voz.start()

    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = False

        if comando_voz_detectado["continuar"]:
            pausado = False

        tela.blit(overlay, (0, 0))
        tela.blit(texto_pause, rect_pause)
        tela.blit(texto_instrucao, rect_instrucao)
        pygame.display.update()
        clock.tick(10)

    pygame.mixer.music.unpause()
