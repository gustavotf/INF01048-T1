import copy
import heapq
import time

TAMANHO = 3
OBJETIVO = '12345678_'

class Nodo:
    def __init__(self, estado, pai, acao, custo):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo


    def expande(self):
        lista_nodos = []
        sucessores = sucessor(self.estado)

        for suc in sucessores:
            n = Nodo('', None, '', 0)
            n.estado = suc[1]
            n.acao = suc[0]
            n.pai = self
            n.custo = self.custo + 1

            lista_nodos.append(n)

        return lista_nodos

    def caminho(self):
        s = []
        while (self.pai != None):
            s.append(self.acao)
            self = self.pai

        return s[::-1]

class Moldura:
    def __init__(self):
        self.lista = [] #[ [1,2,3].[4,5,6],[7,8,'_'] ]
        self.buraco = (TAMANHO-1, TAMANHO-1)
        self.movimentos = ['C', 'B', 'D', 'E']

    def str_p_lista(self, string): #modifica a lista
        self.lista = []
        index = 0
        for linha in range(0, TAMANHO):
            self.lista.append([])
            for coluna in range(0, TAMANHO):
                self.lista[linha].append(string[index])
                if string[index] == '_':
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

def expande(nodo): ##mesma função expande() da classe Nodo, em outro escopo, para realizar os testes de testa_solucao
    lista_nodos = []
    sucessores = sucessor(nodo.estado)

    for suc in sucessores:
        n = Nodo('', None, '', 0)
        n.estado = suc[1]
        n.acao = suc[0]
        n.pai = nodo
        n.custo = nodo.custo + 1

        lista_nodos.append(n)

    return lista_nodos

def sucessor(estado):
    aux_moldura = Moldura()
    aux_moldura.str_p_lista(estado)
    sucessores = []

    for direcao in aux_moldura.movimentos:
        palavra = ''
        if direcao == 'C':
            palavra = 'acima'
        if direcao == 'B':
            palavra = 'abaixo'
        if direcao == 'E':
            palavra = 'esquerda'
        if direcao == 'D':
            palavra = 'direita'

        if (aux_moldura.mover(direcao) == 1):
            sucessores.append((palavra, aux_moldura.lista_p_string()))
        aux_moldura.str_p_lista(estado) #renova a lista para testar o prox movimento

    return sucessores

def bfs(estado): #FRONTEIRA = FILA
    explorados = {}
    fronteira = []
    new = Nodo('', None, '', 0)
    new.estado = estado
    fronteira.append(new)

    while fronteira:
        n = fronteira.pop(0) #primeiro q entrou
        if n.estado == OBJETIVO:
            print(f'Explorados BFS: {len(explorados)}')
            return n.caminho()
        if n.estado not in explorados:
            explorados[n.estado] = n
            for vizinho in n.expande():
                fronteira.append(vizinho)
    print(f'Explorados BFS: {len(explorados)}')
    return None

def dfs(estado): #FRONTEIRA = PILHA
    explorados = {}
    fronteira = []
    new = Nodo('', None, '', 0)
    new.estado = estado
    fronteira.append(new)

    while fronteira:
        n = fronteira.pop(-1) #ultimo q entrou
        if n.estado == OBJETIVO:
            print(f'Explorados DFS: {len(explorados)}')
            return n.caminho()
        if n.estado not in explorados:
            explorados[n.estado] = n
            for vizinho in n.expande():
                fronteira.append(vizinho)
    print(f'Explorados DFS: {len(explorados)}')
    return None

def astar_hamming(estado): #NUM DE PECAS FORA DO LUGAR
    # h(v) = numero de pecas fora do lugar
    def h_hamming(estado):
        h = 0
        for index, num in enumerate(estado):
            if not num == OBJETIVO[index]:
                h += 1
        #print(h, estado)
        return h

    i = 0
    explorados = {}
    fronteira = []
    new = Nodo('', None, '', 0)
    new.estado = estado
    new.custo = h_hamming(estado)
    heapq.heappush(fronteira, (new.custo, i, new)) #i = tiebreaker

    while fronteira:
        n = heapq.heappop(fronteira)[2] #[2] -> posicao do obj Nodo na tupla

        if n.estado == OBJETIVO:
            print(f'Explorados A* Hamming: {len(explorados)}')
            return n.caminho()
        if n.estado not in explorados:
            explorados[n.estado] = n
            for vizinho in n.expande():
                i += 1
                heapq.heappush(fronteira, (vizinho.custo+h_hamming(vizinho.estado), i, vizinho))
    print(f'Explorados A* Hamming: {len(explorados)}')

    return None

def astar_manhattan(estado): #SOMA DISTANCIA MANHATTAN

    def h_manhattan(estado):
        h = 0
        for index, num in enumerate(estado):
            if not num == OBJETIVO[index]:
                coord = (int(index/3), index%3)
                obj_index = OBJETIVO.find(num)
                obj_coord = (int(obj_index/3), obj_index%3)
                #print(f'Coord: {coord} Obj_coord: {obj_coord} Num: {num} Obj_find: {obj_index}')
                h += abs(obj_coord[0]-coord[0]) + abs(obj_coord[1]-coord[1])
        return h

    i = 0
    explorados = {}
    fronteira = []
    new = Nodo('', None, '', 0)
    new.estado = estado
    new.custo = h_manhattan(estado)
    heapq.heappush(fronteira, (new.custo, i, new)) #i = tiebreaker

    while fronteira:
        n = heapq.heappop(fronteira)[2] #[2] -> posicao do obj Nodo na tupla

        if n.estado == OBJETIVO:
            print(f'Explorados A* Manhattan: {len(explorados)}')
            return n.caminho()
        if n.estado not in explorados:
            explorados[n.estado] = n
            for vizinho in n.expande():
                i += 1
                heapq.heappush(fronteira, (vizinho.custo+h_manhattan(vizinho.estado), i, vizinho))
    print(f'Explorados A* Manhattan: {len(explorados)}')

    return None

##################### TESTES ##########################

t = time.time()
#achou = astar_hamming('2_3541687')
#achou = astar_manhattan('2_3541687')
#achou = bfs('2_3541687')
achou = dfs('2_3541687')
#
#print(f'Caminho: {achou}')
print(f'Tempo decorrido: {time.time() - t}')
if achou != None:
    print(f'Custo: {len(achou)}')
    #print(achou.pai)
else:
    print('Nao achou')


