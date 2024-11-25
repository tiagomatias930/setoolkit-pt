RATTE (Remote Administration Tool Tommy Edition) é um módulo de carga útil e de terceiros adicionado/criado ao SET por
Thomas Werth.

Algumas coisas a serem observadas sobre o RATTE é que seu principal propósito e design é evitar completamente as restrições de saída e firewall, aproveitando comunicações puramente HTTP para os comandos de ida e volta.
O RATTE foi estendido para ser muito personalizável.
Por enquanto, você pode definir:
- Conectar IP de volta
- Conectar porta de volta
- Para requisitos de download e se você estiver usando python3 ou pip3, use pip3 install -r requirements.txt
- Se o RATTE é persistente ou não (exemplo: para testes de firewall de rede, não há necessidade de ser persistente. Em um teste de penetração, as coisas podem parecer diferentes)
- um nome de arquivo personalizado que o RATTE usa para execução, de modo que firewalls locais e usuários podem ser enganados usando nomes como iexplore.exe ou firefox.exe e em ...

Se o RATTE for persistente, ele tenta em sistemas NTFS injetar-se no binário do arquivo do navegador padrão e substitui
os executáveis ​​com uma parte de seu próprio código nele também. Se isso falhar, o RATTE se salvará como aplicativo de execução automática usando o nome de arquivo personalizado especificado. Se este estiver faltando, ele será exibido como iexplore.exe.

O RATTE depende de comunicações com microsoft.com para identificar o caminho para fora da rede.