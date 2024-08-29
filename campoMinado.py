import random
import os

campo = "🟥"
bomba = "💣"
vizinhos = ["0️⃣  ","1️⃣  ","2️⃣  ","3️⃣  ","4️⃣  ","5️⃣  ","6️⃣  ","7️⃣  ","8️⃣  "]
colunaNum = ""

def gravaJogada(nome, jogadas, dificuldade):
    with open("jogadas.txt", 'a') as arq:
        arq.write(f"{nome};{jogadas};{dificuldade}\n")

def carregaJogadas():
    jogadas = []
    try:
        with open("jogadas.txt") as arq:
            for linha in arq:
                nome, jogada, dificuldade = linha.strip().split(";")
                jogadas.append((nome, int(jogada), dificuldade))
    except FileNotFoundError:
        pass
    except ValueError:
        print("Erro ao carregar o arquivo de ranking")
    return jogadas

def dificuldadeDef():
    print('|----------Selecione a dificuldade-----------|')
    print('| 1. Fácil (9x9 - 9 Bombas)                  |')
    print('| 2. Médio (16x16 - 40 Bombas)               |')
    print('| 3. Difícil (30x16 - 99 Bombas)             |')
    print('|--------------------------------------------|')
    escolha = input("Escolha..: ")

    if escolha == '1':
        colunaNum = "   1   2   3   4   5   6   7   8   9"
        return 9, 9, 9, 'Facil', colunaNum
    
    elif escolha == '2':
        colunaNum = "  1   2   3   4   5   6   7   8   9   10  11   12  13  14   15  16"
        return 16, 16, 40, 'Medio', colunaNum 
       
    elif escolha == '3':
        colunaNum =  "  1   2   3   4   5   6   7   8   9   10  11   12  13  14   15  16"
        return 30, 16, 99, 'Dificil', colunaNum

def criaCampo(linhas, colunas):
    campoMinado = []
    campoJogo = []
    for i in range(linhas):
        campoMinado.append([campo] * colunas)
        campoJogo.append([campo] * colunas)
    return campoJogo, campoMinado

def preencheCampo(campoMinado, bombas):
    linhas = len(campoMinado)
    colunas = len(campoMinado[0])
    bombasColocadas = 0
    while bombasColocadas < bombas:
        x = random.randint(0,linhas-1)
        y = random.randint(0,colunas-1)
        if campoMinado[x][y] != bomba:
            campoMinado[x][y] = bomba
            bombasColocadas += 1
    return campoMinado

def mostraCampo(campoJogo,  colunaNum):
    os.system("cls" if os.name == "nt" else "clear")
    print("Campo Minado")
    print("============")
    print(colunaNum)
    for i in range(len(campoJogo)):
        print(f"{i+1:2d}", end="")
        for j in range(len(campoJogo[0])):
            print(f"|{campoJogo[i][j]:2s}", end="")            
        print("|")

def verificaVizinhos(campoMinado, x, y):
    z = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            xi, yj = x + i, y + j
            if 0 <= xi < len(campoMinado) and 0 <= yj < len(campoMinado[0]) and campoMinado[xi][yj] == bomba:
                z += 1
    return z   
    
def procuraZeros(campoJogo, campoMinado, x, y):
    fila = [(x, y)]
    visitados = set((x, y))

    while fila:
        fx, fy = fila.pop(0)
        numVizinhos = verificaVizinhos(campoMinado, fx, fy)
        campoJogo[fx][fy] = vizinhos[numVizinhos]

        if numVizinhos == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    fxi, fyj = fx + i, fy + j
                    if 0 <= fxi < len(campoMinado) and 0 <= fyj < len(campoMinado[0]) and (fxi, fyj) not in visitados:
                        fila.append((fxi, fyj))
                        visitados.add((fxi, fyj))

def fazJogada(campoJogo, campoMinado, nome, dificuldade, colunaNum):
    jogadas = 0
    while True:
        mostraCampo(campoJogo, colunaNum)
        while True:
            try:
                jogadaLinha = int(input("Informe a linha: "))
                if jogadaLinha < 1 or jogadaLinha > len(campoMinado):
                    raise ValueError
                break
            except ValueError:
                print(f"Linha inválida! Digite um valor entre 1 e {len(campoMinado)}.")
        while True:
            try:
                jogadaColuna = int(input("Informe a coluna: "))
                if jogadaColuna < 1 or jogadaColuna > len(campoMinado[0]):
                    raise ValueError
                break
            except ValueError:
                print(f"Coluna inválida! Digite um valor entre 1 e {len(campoMinado[0])}.")

        x = jogadaLinha - 1
        y = jogadaColuna - 1
        jogadas += 1

        if campoMinado[x][y] == bomba:
            campoJogo[x][y] = bomba
            mostraCampo(campoMinado, colunaNum)
            print("Você perdeu!")
            gravaJogada(nome, jogadas, dificuldade)
            break
        else:
            numVizinhos = verificaVizinhos(campoMinado, x, y)
            if numVizinhos == 0:
                procuraZeros(campoJogo, campoMinado, x, y)
            else:
                campoJogo[x][y] = vizinhos[numVizinhos]
            
            if all(campoJogo[i][j] != campo for i in range(len(campoMinado)) for j in range(len(campoMinado[0])) if campoMinado[i][j] != bomba):
                mostraCampo(campoJogo, colunaNum)
                print("Você ganhou!")
                gravaJogada(nome, jogadas, dificuldade)
                break

while True:
    print('|--------------------------------------------|')
    print('| 1. Jogar                                   |')
    print('| 2. Ver Ranking                             |')
    print('| 3. Sair                                    |')
    print('|--------------------------------------------|')    
    opcao = input("Escolha..: ")
    
    if opcao == '1':
        nome = input("Informe o seu nome: ")
        linhas, colunas, bombas, dificuldade, colunaNum = dificuldadeDef()
        campoJogo, campoMinado = criaCampo(linhas, colunas)
        campoMinado = preencheCampo(campoMinado, bombas)
        fazJogada(campoJogo, campoMinado, nome, dificuldade, colunaNum)
    elif opcao == '2':
        jogadas = carregaJogadas()
        jogadas.sort(key=lambda x: x[1], reverse=True)
        print("Ranking")
        print("========")
        for i, j in enumerate(jogadas):
            print(f"{i+1}º - {j[0]} - {j[1]} jogadas - {j[2]}")
        input("Pressione ENTER para continuar...")
    elif opcao == '3':
        break
    
