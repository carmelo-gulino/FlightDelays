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
        pass
