import copy

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
                    self._grafo.add_edge(v0, v1, weight=peso)  #altrimenti aggiungo l'arco e il peso
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

    def esiste_percorso(self, v0, v1):
        connessa = nx.node_connected_component(self._grafo, v0)
        if v1 in connessa:
            return True
        return False

    def trova_cammino_dijkstra(self, v0, v1):
        """
        Trova il cammino ottimo tramite dijkstra
        """
        return nx.dijkstra_path(self._grafo, v0, v1)

    def trova_cammino_BFS(self, v0, v1):
        """
        Trova una cammino BFS e poi aggiunge i nodi ad una lista
        """
        tree = nx.bfs_tree(self._grafo, v0)
        if v1 in tree:
            print(f"{v1} è presente nell'albero di visita BFS")
        path = [v1]  #tree è un grafo ma io voglio una lista di nodi, quindi vado a ritroso prendendo i predecessori
        while path[-1] != v0:  #aggiungo i predecessori a una lista di nodi
            path.append(list(tree.predecessors(path[-1]))[0])  #ogni volta aggiungo il predecessore
        path.reverse()
        return path

    def trova_cammino_DFS(self, v0, v1):
        """
        Trova una cammino DFS e poi aggiunge i nodi a una lista
        """
        tree = nx.dfs_tree(self._grafo, v0)
        if v1 in tree:
            print(f"{v1} è presente nell'albero di visita BFS")
        path = [v1]  #tree è un grafo ma io voglio una lista di nodi, quindi vado a ritroso prendendo i predecessori
        while path[-1] != v0:  #aggiungo i predecessori a una lista di nodi
            path.append(list(tree.predecessors(path[-1]))[0])  #ogni volta aggiungo il predecessore
        path.reverse()
        return path

    def get_cammino_ottimo(self, v0, v1, t):
        """
        Trova il cammino ottimo tramite un algoritmo ricorsivo e lo restituisce
        :param v0: partenza
        :param v1: arrivo
        :param t: lunghezza massima del percorso
        """
        self.best_path = []
        self.best_obj_fun = 0
        parziale = [v0]
        self.ricorsione(parziale, v1, t)
        return self.best_path, self.best_obj_fun

    def ricorsione(self, parziale, target, t):
        """
        :param parziale: lista di nodi
        :param target: nodo di arrivo
        :param t: lunghezza di parziale
        """
        if self.get_obj_fun(parziale) > self.best_obj_fun and parziale[-1] == target:
            self.best_obj_fun = self.get_obj_fun(parziale)
            self.best_path = copy.deepcopy(parziale)
            return
        if len(parziale) == t+1:
            return  #se parziale ha lunghezza t esco anche se non è una soluzione migliore
        for n in self._grafo.neighbors(parziale[-1]):   #itero sui i vicini dell'ultimo aggiunto
            if n not in parziale:   #controllo se ci sono già passato
                parziale.append(n)  #aggiungo il nodo
                self.ricorsione(parziale, target, t)
                parziale.pop()

    def get_obj_fun(self, nodes):
        """
        Itera sui nodi, calcola la somma degli archi e la restituisce
        """
        val = 0
        for i in range(len(nodes)-1):
            val = self._grafo[nodes[i]][nodes[i+1]]['weight']   #itero sui nodi ma considero gli archi
        return val
