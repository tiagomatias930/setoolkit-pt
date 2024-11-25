The Social-Engineer Toolkit (SET)
Copyright :copyright: 2020
Escrito por: David Kennedy (ReL1K) @HackingDave
Empresa: TrustedSec

Descrição
The Social-Engineer Toolkit é uma estrutura de teste de penetração de código aberto projetada para engenharia social. O SET tem vários vetores de ataque personalizados que permitem que você faça um ataque crível rapidamente. O SET é um produto da TrustedSec, LLC – uma empresa de consultoria em segurança da informação localizada em Cleveland, Ohio.
AVISO LEGAL: Isso é apenas para fins de teste e só pode ser usado quando consentimento estrito foi dado. Não use isso para fins ilegais, ponto final. Leia a LICENÇA em leia-me/LICENÇA para o licenciamento do SET.
Plataformas suportadas:
Linux
Mac OS X (experimental)
Instalação
Instalar via requirements.txt
pip3 install -r requirements.txt
python3 setup.py
Instalar SET
=======
Mac OS X
Você precisará usar um ambiente virtual para a instalação do Python se estiver usando um Macbook M2 com as seguintes instruções em sua CLI dentro do diretório social-engineer-toolkit.
# para instalar dependências, execute o seguinte:
python3 -m venv path/to/venv
source path/to/venv/bin/activate
python3 -m pip install -r requirements.txt

# para instalar SET
sudo python3 setup.py

Instalação
Windows 10 WSL/WSL2 Kali Linux
sudo apt install set -y
O Kali Linux no Windows 10 é uma instalação mínima, portanto, não tem nenhuma ferramenta instalada. Você pode instalar facilmente o Social Engineer Toolkit no WSL/WSL2 sem precisar do pip usando o comando acima.
Linux
git clone https://github.com/trustedsec/social-engineer-toolkit/ setoolkit/
cd setoolkit
pip3 install -r requirements.txt
python setup.py

Tutorial SET
Para um documento completo sobre como usar o SET, visite o manual do usuário do SET.

Bugs e melhorias
Para relatórios de bug ou melhorias, abra um problema aqui.
