import os, time
import json
from datetime import datetime


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
        
    data_br = datetime.now().strftime("%d/%m/%Y")
    dadosDict[nome] = (pontos, data_br)
    
    banco = open("./recursos/logs/log.dat","w")
    banco.write(json.dumps(dadosDict))
    banco.close()
    
    # END - inserindo no arquivo