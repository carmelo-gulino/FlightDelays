from datetime import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choice_aeroportoP = None
        self._choice_aeroportoA = None

    def handleAnalizza(self, e):
        n_min_str = self._view._txtInNumC.value
        try:
            n_min = int(n_min_str)
        except ValueError:
            self._view.create_alert("Inserire un intero")
            return
        self._view._ddAeroportoP.disabled = False
        self._view._ddAeroportoA.disabled = False
        self._view._btnConnessi.disabled = False
        self._view._btnPercorso.disabled = False
        self._model.build_graph(n_min)
        self._view.txt_result.controls.append(ft.Text(f"Num nodi: {self._model.get_num_nodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Num archi: {self._model.get_num_archi()}"))
        self.fill_dd()
        self._view.update_page()

    def fill_dd(self):
        nodes = self._model.get_all_nodes()
        for n in nodes:
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(
                data=n,
                on_click=self.read_airport_p,
                text=n.AIRPORT
            ))
            self._view._ddAeroportoA.options.append(ft.dropdown.Option(
                data=n,
                on_click=self.read_airport_a,
                text=n.AIRPORT
            ))

    def read_airport_p(self, e):
        if e.control.data is None:
            self._choice_aeroportoP = None
        else:
            self._choice_aeroportoP = e.control.data

    def read_airport_a(self, e):
        if e.control.data is None:
            self._choice_aeroportoA = None
        else:
            self._choice_aeroportoA = e.control.data

    def handleConnessi(self, e):
        self._view.txt_result.controls.clear()
        if self._choice_aeroportoP is None:
            self._view.create_alert("Selezionare un aeroporto di partenza")
            return
        else:
            vicini = self._model.get_sorted_vicini(self._choice_aeroportoP)
            self._view.txt_result.controls.append(ft.Text(f"Ecco i vicini di {self._choice_aeroportoP}:"))
            for v in vicini:
                self._view.txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))
            self._view.update_page()

    def handleCercaItinerario(self, e):
        self._view.txt_result.controls.clear()
        v0 = self._choice_aeroportoP
        v1 = self._choice_aeroportoA
        t = int(self._view._txtInNumTratte.value)
        tic = datetime.now()
        path, nodi = self._model.get_cammino_ottimo(v0, v1, t)
        self._view.txt_result.controls.append(ft.Text(f"Cammino di {t} tratte trovato "
                                                      f"in {datetime.now() - tic} secondi"))
        self._view.txt_result.controls.append(ft.Text(f"Tratte:"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero totale di voli: {nodi}"))
        self._view.update_page()


    def handleTestConnessione(self, e):
        self._view.txt_result.controls.clear()
        self._view._txtInNumTratte.disabled = False
        self._view._btnCercaItinerario.disabled = False
        v0 = self._choice_aeroportoP
        v1 = self._choice_aeroportoA
        if not self._model.esiste_percorso(v0, v1):
            self._view.txt_result.controls.append(ft.Text(f"Non esiste un percorso fra {v0} e {v1}"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Esiste un percorso fra {v0} e {v1}"))
            path = self._model.trova_cammino_BFS(v0, v1)
            self._view.txt_result.controls.append(ft.Text(f"Il cammino con minor numero di archi fra {v0} e {v1} è:"))
            for p in path:
                self._view.txt_result.controls.append(ft.Text(f"{p}"))
            self._view.update_page()
