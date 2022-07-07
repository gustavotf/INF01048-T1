import copy
import time

from queue import Queue

TAMANHO = 3

class Nodo:
    def __init__(self):
        self.estado = ''
        self.pai = None
        self.acao = ''
        self.custo = 0


    def expande(self):

        lista_nodos = []

        sucessores = sucessor(self.estado)

        for suc in sucessores:
            n = Nodo()
            n.estado = suc[0]
            n.acao = suc[1]
            n.pai = self
            n.custo = self.custo + 1


            lista_nodos.append(n)

        return lista_nodos
    def caminho(self):

        s = ''
        while (self.pai != None):
            s = s + self.acao
            self = self.pai

        return s[::-1]

class Moldura:
    def __init__(self):
        self.lista = [] #[ [1,2,3].[4,5,6],[7,8,' '] ]
        self.buraco = (2, 2)
        self.movimentos = ['C','B','D','E']
        num = 1
        # for linha in range(0,TAMANHO):
        #     self.lista.append([])
        #     for coluna in range(0, TAMANHO):
        #         self.lista[linha].append(str(num))
        #         num = num + 1
        #self.lista[self.buraco[0]][self.buraco[1]] = ' '


    def str_p_lista(self, string): #modifica a lista
        self.lista = []
        index = 0
        for linha in range(0, TAMANHO):
            self.lista.append([])
            for coluna in range(0, TAMANHO):
                self.lista[linha].append(string[index])
                if string[index] == ' ':
                    self.buraco = (int(index/TAMANHO), index % TAMANHO)
                index += 1
        return self.lista


    def lista_p_string(self): #nao modifica a lista
        aux_moldura = copy.deepcopy(self.lista)
        string = ''
        while aux_moldura:
            linha = aux_moldura.pop(0)
            while linha:
                string = string + str(linha.pop(0))
        return string


    def troca(self, pos1, pos2):
        aux = self.lista[pos1[0]][pos1[1]]
        self.lista[pos1[0]][pos1[1]] = self.lista[pos2[0]][pos2[1]]
        self.lista[pos2[0]][pos2[1]] = aux

    def mover(self, dir):
        if dir == 'E':
            r = self.esquerda()
        if dir == 'D':
            r = self.direita()
        if dir == 'C':
            r = self.cima()
        if dir == 'B':
            r = self.baixo()
        return r

    def cima(self):
        if self.buraco[0] != 0:
            self.troca((self.buraco[0] - 1, self.buraco[1]), self.buraco)
            self.buraco = self.buraco[0] - 1, self.buraco[1]
            return 1
        return 0

    def baixo(self):
        if self.buraco[0] != TAMANHO - 1:
            self.troca((self.buraco[0] + 1, self.buraco[1]), self.buraco)
            self.buraco = self.buraco[0] + 1, self.buraco[1]
            return 1
        return 0

    def esquerda(self):
        if self.buraco[1] != 0:
            self.troca((self.buraco[0], self.buraco[1] - 1), self.buraco)
            self.buraco = self.buraco[0], self.buraco[1] - 1
            return 1
        return 0

    def direita(self):
        if self.buraco[1] != TAMANHO - 1:
            self.troca((self.buraco[0], self.buraco[1] + 1), self.buraco)
            self.buraco = self.buraco[0], self.buraco[1] + 1
            return 1
        return 0


def sucessor(estado):
    aux_moldura = Moldura()

    aux_moldura.str_p_lista(estado)
    #print(aux_moldura.lista)
    sucessores = []

    for direcao in aux_moldura.movimentos:
        if (aux_moldura.mover(direcao) == 1):
            sucessores.append((aux_moldura.lista_p_string(), direcao))
        aux_moldura.str_p_lista(estado)

    return sucessores


#m = Moldura()

#print(m.str_p_lista('1234 5678'))
#print(f'buraco:  {m.buraco}')
#print(sucessor(m.lista_p_string()))

#n = Nodo()
#n.estado = '2 3541687'
#n.estado = '12345678 '
#expandidos =  n.expande()

#for e in expandidos:
#   print(e.estado, e.custo, e.acao, e.pai.estado)


def bfs(estado): #FRONTEIRA = FILA
    explorados = {}
    fronteira = []
    new = Nodo()
    new.estado = estado
    fronteira.append(new)

    while fronteira:

        n = fronteira.pop(0)
        if n.estado == '12345678 ':
            break
            #return n
        if n.estado not in explorados:
            explorados[n.estado] = n
            for vizinho in n.expande():
                #print(f'vizinho: {vizinho.estado} custo: {vizinho.custo}')
                #print(f'{len(explorados)} explorados')
                #print(f'{len(fronteira)} fronteira')

                fronteira.append(vizinho)


    return n    #




t = time.time()
achou = bfs('2 3541687')
print(achou.estado)
print(achou.acao)
print(achou.custo)
print(achou.pai)
print(time.time()-t)
print(achou.caminho())

# s = ''
# while achou.pai != None:
#     s = s + achou.acao
#     achou = achou.pai
#     print (s[::-1]) ###invertido




# DFS

# 12345678
# D
# 68539
# <__main__.Nodo object at 0x000002199E8AB0D0>
# 118.71603679656982
#



# BFS
# 12345678
# D
# 23
# <__main__.Nodo object at 0x000001496CA402B0>
# 191.9502773284912      segundos
#
# B
# BD
# BDB
# BDBE
# BDBEC
# BDBECD
# BDBECDC
# BDBECDCE
# BDBECDCEB
# BDBECDCEBE
# BDBECDCEBEC
# BDBECDCEBECD
# BDBECDCEBECDB
# BDBECDCEBECDBD
# BDBECDCEBECDBDC
# BDBECDCEBECDBDCE
# BDBECDCEBECDBDCEB
# BDBECDCEBECDBDCEBE
# BDBECDCEBECDBDCEBEC
# BDBECDCEBECDBDCEBECD
# BDBECDCEBECDBDCEBECDB
# BDBECDCEBECDBDCEBECDBB
# BDBECDCEBECDBDCEBECDBB



def dfs(estado): #FRONTEIRA = PILHA
    pass

def astar_hamming(estado): #NUM DE PECAS FORA DO LUGAR
    pass

def astar_manhattan(estado): #SOMA DISTANCIA MANHATTAN
    pass





