#!/usr/bin/python
#
# quick installer for SET
#
#
from __future__ import print_function
import subprocess
import os
print("[*]Instalando os requirements.txt...")
subprocess.Popen("pip3 install -r requirements.txt", shell=True).wait()
print("[*] Instalando setoolkit para /usr/local/share/setoolkit-pt")
print(os.getcwd())
subprocess.Popen("mkdir /usr/local/share/setoolkit-pt/;mkdir /etc/setoolkit-pt/;cp -rf * /usr/local/share/setoolkit-pt/;cp src/core/config.baseline /etc/setoolkit-pt/set.config", shell=True).wait()
print("[*] Criando o executável setoolkit-pt...")
filewrite = open("/usr/local/bin/setoolkit-pt", "w")
filewrite.write("#!/bin/sh\ncd /usr/local/share/setoolkit-pt\n./setoolkit-pt")
filewrite.close()
print("[*] Feito. Chmoding +x.... ")
subprocess.Popen("chmod +x /usr/local/bin/setoolkit-pt", shell=True).wait()
print("[*] FinishTerminado. Inicia 'setoolkit-pt' para começar o Social Engineer Toolkit-Pt.")
