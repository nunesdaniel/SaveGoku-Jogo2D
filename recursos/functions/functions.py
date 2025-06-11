import os, time
import json
from datetime import datetime
import speech_recognition as sr

def reconhecimento_inicial():
    try:
        # Fala com o jogador
        tts.say("Oi! Me diz algo antes de começarmos o jogo.")
        tts.runAndWait()

        # Inicia o reconhecedor
        reconhecedor = sr.Recognizer()
        with sr.Microphone() as source:
            print("Pode falar agora...")
            reconhecedor.adjust_for_ambient_noise(source)
            audio = reconhecedor.listen(source, timeout=5)
            resposta = reconhecedor.recognize_google(audio, language="pt-BR")
            print("Você disse:", resposta)

        # Responde com voz
        tts.say("Legal! Agora vamos jogar.")
        tts.runAndWait()

    except Exception as e:
        print(f"Reconhecimento ignorado. Erro: {e}")



def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # Garante que a pasta exista
    os.makedirs("./recursos/logs", exist_ok=True)

    try:
        banco = open("./recursos/logs/log.dat", "r")
        # leia algo se necessário
    except FileNotFoundError:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("./recursos/logs/log.dat", "w")
        banco.write("")  # pode escrever cabeçalho se quiser
    finally:
        banco.close()


def escreverDados(nome, pontos):
    # INI - inserindo no arquivo
    banco = open("./recursos/logs/log.dat","r")
    dados = banco.read()
    banco.close()
    print("dados",type(dados))
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}
        
    data_br = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    dadosDict[nome] = (pontos, data_br)
    
    banco = open("./recursos/logs/log.dat","w")
    banco.write(json.dumps(dadosDict))
    banco.close()
    
    # END - inserindo no arquivo