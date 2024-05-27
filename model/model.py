import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allAirports = DAO.getAllAirports()
        self._idMap = {}
        for a in self._allAirports:
            self._idMap[a.ID] = a
        self._grafo = nx.Graph()

    def build_graph(self, n_min):
        self._nodi = DAO.getAllNodes(n_min, self._idMap)
        self._grafo.add_nodes_from(self._nodi)
        self.add_edges_v2()

    def add_edges_v1(self):
        """
        Aggiunge gli archi evitando le connessioni duplicate e verificando che i nodi siano presenti nel grafo
        """
        connessioni = DAO.get_all_edges_v1(self._idMap)
        for c in connessioni:
            v0 = c.v0
            v1 = c.v1
            peso = c.n
            if v0 in self._grafo and v1 in self._grafo:  #i nodi sono presenti e posso aggiungere l'arco
                if self._grafo.has_edge(v0, v1):  #se l'arco esiste già
                    self._grafo[v0, v1]['weight'] += peso  #aggiungo il peso a quello già esistente
                else:
                    self._grafo.add_edge(v0, v1, weight=peso)   #altrimenti aggiungo l'arco e il peso
        print(self._grafo)

    def add_edges_v2(self):
        """
        Aggiunge gli archi senza controlli perché sono già fatti su SQL
        """
        connessioni = DAO.get_all_edges_v2(self._idMap)
        for c in connessioni:
            v0 = c.v0
            v1 = c.v1
            peso = c.n
            if v0 in self._grafo and v1 in self._grafo:  # i nodi sono presenti e posso aggiungere l'arco
                self._grafo.add_edge(v0, v1, weight=peso)  # altrimenti aggiungo l'arco e il peso
        print(self._grafo)

    def get_num_nodi(self):
        return len(self._grafo.nodes)

    def get_num_archi(self):
        return len(self._grafo.edges)

    def get_all_nodes(self):
        return self._grafo.nodes

    def get_sorted_vicini(self, v0):
        vicini = self._grafo.neighbors(v0)
        vicini_tuple = []
        for v in vicini:
            vicini_tuple.append((v, self._grafo[v0][v]['weight']))
        vicini_tuple.sort(key=lambda tupla: tupla[1], reverse=True)
        return vicini_tuple
