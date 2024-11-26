import random
from collections import deque

class Grafo:
    def __init__(self, n, p):
        self.n = n
        self.p = p
        self.vertices = list(range(n))
        self.arestas = self.gerar_arestas()

    def gerar_arestas(self):
        arestas = []
        for u in self.vertices:
            for v in self.vertices:
                if u != v and random.random() <= self.p:
                    arestas.append((u, v))
        return arestas

    def calcular_propriedades(self):
        graus = self.calcular_graus()
        num_vertices = len(self.vertices)
        num_arestas = len(self.arestas)
        grau_minimo = min(graus)
        grau_maximo = max(graus)
        grau_medio = sum(graus) / num_vertices
        diametro = self.calcular_diametro()

        return num_vertices, num_arestas, grau_minimo, grau_maximo, grau_medio, diametro

    def calcular_graus(self):
        graus = [0] * self.n
        for aresta in self.arestas:
            graus[aresta[0]] += 1
            graus[aresta[1]] += 1
        return graus

    def calcular_diametro(self):
        diametro = 0
        for s in self.vertices:
            distancias = self.bfs(s)
            maior_distancia = max(distancias)
            diametro = max(diametro, maior_distancia)

        return diametro

    def bfs(self, origem):
        visitados = [False] * self.n
        distancias = [0] * self.n

        fila = deque()
        fila.append((origem, 0))
        visitados[origem] = True
        distancias[origem] = 0

        while fila:
            vertice, distancia = fila.popleft()

            for vizinho in self.vizinhos(vertice):
                if not visitados[vizinho]:
                    visitados[vizinho] = True
                    fila.append((vizinho, distancia + 1))
                    distancias[vizinho] = distancia + 1

        return distancias

    def vizinhos(self, vertice):
        return [v for u, v in self.arestas if u == vertice] + [u for u, v in self.arestas if v == vertice]

def main(ini, fim, stp, p):
    print('Gerando arquivo')
    with open("valoresObtidos.txt", "a") as file:
        file.write("V      E     gmin  gmax  gmed  diam\n")
        file.write("-----------------------------------------------\n")
        for n in range(ini, fim + 1, stp):
            grafo = Grafo(n, p)
            propriedades = grafo.calcular_propriedades()
            file.write(f"{propriedades[0]:<6} {propriedades[1]:<6} {propriedades[2]:<5} {propriedades[3]:<5} {propriedades[4]:<5.1f} {propriedades[5]}\n")
    print("Arquivo gerado")
if __name__ == "__main__":
    ini = 10
    fim = 200
    stp = 10
    p = 0.1
    main(ini, fim, stp, p)