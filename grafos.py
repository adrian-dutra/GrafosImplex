import random
from collections import deque
from concurrent.futures import ThreadPoolExecutor

class Grafo:
    def __init__(self, n, p):
        self.n = n
        self.p = p
        self.vertices = list(range(n))
        self.adjacencia = {v: [] for v in self.vertices}
        self.arestas = self.gerar_arestas()

    def gerar_arestas(self):
        arestas = []
        for u in self.vertices:
            for v in range(u + 1, self.n):
                if random.random() <= self.p:
                    arestas.append((u, v))
                    self.adjacencia[u].append(v)
                    self.adjacencia[v].append(u)
        return arestas

    def calcular_propriedades(self):
        graus = [len(self.adjacencia[v]) for v in self.vertices]
        num_vertices = len(self.vertices)
        num_arestas = len(self.arestas)
        grau_minimo = min(graus)
        grau_maximo = max(graus)
        grau_medio = sum(graus) / num_vertices
        diametro = self.calcular_diametro()

        return num_vertices, num_arestas, grau_minimo, grau_maximo, grau_medio, diametro

    def calcular_diametro(self):
        def bfs(origem):
            distancias = [float('inf')] * self.n
            distancias[origem] = 0
            fila = deque([origem])

            while fila:
                atual = fila.popleft()
                for vizinho in self.adjacencia[atual]:
                    if distancias[vizinho] == float('inf'):
                        distancias[vizinho] = distancias[atual] + 1
                        fila.append(vizinho)
            return distancias

        componente = bfs(0)
        if all(dist == float('inf') for dist in componente):
            return 0

        vertices_conectados = [i for i, dist in enumerate(componente) if dist != float('inf')]

        def diametro_subgrafo(origem):
            distancias = bfs(origem)
            return max(distancias[v] for v in vertices_conectados)

        with ThreadPoolExecutor() as executor:
            distancias_max = executor.map(diametro_subgrafo, vertices_conectados)

        return max(distancias_max)

def main(ini, fim, stp, p):
    random.seed(42)
    with open("valoresObtidos.txt", "w") as file:
        file.write("V      E     gmin  gmax  gmed  diam\n")
        file.write("-----------------------------------------------\n")
        print("V      E     gmin  gmax  gmed  diam")
        print("-----------------------------------------------")
        for n in range(ini, fim + 1, stp):
            grafo = Grafo(n, p)
            propriedades = grafo.calcular_propriedades()
            file.write(f"{propriedades[0]:<6} {propriedades[1]:<6} {propriedades[2]:<5} {propriedades[3]:<5} {propriedades[4]:<5.1f} {propriedades[5]}\n")
            
            print(f"{propriedades[0]:<6} {propriedades[1]:<6} {propriedades[2]:<5} {propriedades[3]:<5} {propriedades[4]:<5.1f} {propriedades[5]}")

if __name__ == "__main__":
    ini = 10
    fim = 200
    stp = 10
    p = 0.1
    main(ini, fim, stp, p)
