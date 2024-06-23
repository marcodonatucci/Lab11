import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._bestdTot = 0
        self._bestComp = []
        self.graph = nx.Graph()
        self.idMap = {}

    def getColori(self):
        return DAO.getColori()

    def getGraphDetails(self):
        return f"Grafo creato con {len(self.graph.nodes)} nodi e {len(self.graph.edges)} archi."

    def get_nodes(self):
        return self.graph.nodes

    def buildGraph(self, year, color):
        self.graph.clear()
        nodes = DAO.getProducts(color)
        self.graph.add_nodes_from(nodes)
        for node in self.graph.nodes:
            self.idMap[node.Product_number] = node
        edges = DAO.getEdges(year, color, self.idMap)
        for edge in edges:
            if self.graph.has_edge(edge.product1, edge.product2):
                pass
            else:
                self.graph.add_edge(edge.product1, edge.product2, weight=edge.weight)
        return True

    def analyze(self):
        result = []
        for node1 in self.graph.nodes:
            for node2 in self.graph.nodes:
                if self.graph.has_edge(node1, node2) and (node2.Product, node1.Product, self.graph[node1][node2]['weight']) not in result:
                    result.append((node1.Product, node2.Product, self.graph[node1][node2]['weight']))
        result.sort(key=lambda x: x[2], reverse=True)
        result_tot = []
        for i in range(0, 3):
            result_tot.append(result[i])
        nodi_ripetuti = []
        for result in result_tot:
            name_to_count1 = result[0]
            count1 = sum(name_to_count1 in t for t in result_tot)
            name_to_count2 = result[1]
            count2 = sum(name_to_count2 in t for t in result_tot)
            if count1 > 1 and name_to_count1 not in nodi_ripetuti:
                nodi_ripetuti.append(name_to_count1)
            if count2 > 1 and name_to_count2 not in nodi_ripetuti:
                nodi_ripetuti.append(name_to_count2)
        return result_tot, nodi_ripetuti

    def getPath(self, p0):
        # caching con variabili della classe (percorso migliore e peso maggiore)
        self._bestComp = []
        self._bestdTot = 0
        # inizializzo il parziale con il nodo iniziale
        parziale = [p0]
        for p in self.graph.neighbors(p0):
            parziale.append(p)
            self._ricorsionev2(parziale)
            parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking
        return self._bestComp

    def _ricorsionev2(self, parziale):
        # verifico se soluzione è migliore di quella salvata in cache
        if len(parziale)-1 > self._bestdTot:
            # se lo è aggiorno i valori migliori
            self._bestComp = copy.deepcopy(parziale)
            self._bestdTot = len(parziale)-1
        # verifico se posso aggiungere un altro elemento
        for a in self.graph.neighbors(parziale[-1]):
            if a not in parziale and self.graph[parziale[-1]][a]["weight"] >= self.graph[parziale[-2]][parziale[-1]]["weight"]:
                parziale.append(a)
                self._ricorsionev2(parziale)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking
