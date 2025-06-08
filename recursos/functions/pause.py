import pygame

def pause(tela, fonte_titulo, tamanho_tela):
    pausado = True

    # Texto principal "PAUSE"
    texto_pause = fonte_titulo.render("PAUSE", True, (255, 0, 0))
    rect_pause = texto_pause.get_rect(center=(tamanho_tela[0] // 2, tamanho_tela[1] // 2 - 50))

    # Pressione [ESPAÇO] para continuar
    fonte_instrucao = pygame.font.SysFont("comicsans", 32)
    texto_instrucao = fonte_instrucao.render("Pressione [ESPAÇO] para continuar...", True, (255, 255, 255))
    rect_instrucao = texto_instrucao.get_rect(center=(tamanho_tela[0] // 2, tamanho_tela[1] // 2 + 30))

    # Fundo preto
    overlay = pygame.Surface(tamanho_tela)
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))

    clock = pygame.time.Clock()

    # Pausar música se estiver tocando
    pygame.mixer.music.pause()

    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = False

        tela.blit(overlay, (0, 0))
        tela.blit(texto_pause, rect_pause)
        tela.blit(texto_instrucao, rect_instrucao)
        pygame.display.update()
        clock.tick(10)

    # Retomar música
    pygame.mixer.music.unpause()
