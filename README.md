### O Toolkit de Engenharia Social (SET)  
**Copyright © 2020**  
**Autor:** David Kennedy (ReL1K) @HackingDave  & Tiago Matias
**Empresa:** TrustedSec  

---

### Descrição  
O Toolkit de Engenharia Social é um framework de código aberto projetado para testes de penetração focados em engenharia social. O SET possui diversos vetores de ataque personalizados que permitem criar ataques realistas de forma rápida. O SET é um produto da **TrustedSec, LLC**, uma empresa de consultoria em segurança da informação localizada em Cleveland, Ohio.  

**AVISO:** Esta ferramenta é apenas para fins de teste e deve ser usada estritamente com consentimento explícito. **Não utilize esta ferramenta para fins ilegais, em hipótese alguma.** Leia o arquivo de licença em `readme/LICENSE` para mais detalhes sobre a licença do SET.  

---

### Plataformas Suportadas:  
- **Linux**  
- **Mac OS X** (experimental)  

---

### Instalação  

#### Via `requirements.txt`:  
```bash
pip3 install -r requirements.txt
python3 setup.py
```  

---

#### Instalar o SET no Mac OS X:  
Se estiver usando um Macbook com processador M2, é necessário configurar um ambiente virtual. Siga as instruções abaixo no terminal dentro do diretório do SET:  
```bash
# Para instalar as dependências:
python3 -m venv path/to/venv
source path/to/venv/bin/activate
python3 -m pip install -r requirements.txt

# Para instalar o SET:
sudo python3 setup.py
```  

---

#### Instalação no Windows 10 (WSL/WSL2 com Kali Linux):  
Para o Windows Subsystem for Linux (WSL/WSL2) com o Kali Linux:  
```bash
sudo apt install set -y
```  
O Kali Linux no Windows 10 vem com uma instalação mínima, sem ferramentas pré-instaladas. Com o comando acima, é possível instalar facilmente o Social-Engineer Toolkit sem precisar do `pip`.  

---

#### Instalação no Linux:  
```bash
git clone https://github.com/tiagomatias930/setoolkit-pt.git
cd setoolkit-pt
pip3 install -r requirements.txt
python3 setup.py
```  

---

### Tutorial do SET  
Para um manual completo de uso do SET, acesse o **manual do usuário do SET**.  

--- 

Precisa de algo mais ou deseja personalizar a tradução? 😊
