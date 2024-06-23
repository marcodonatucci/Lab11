import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._selected_product = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        colors = self._model.getColori()
        for i in range(2015, 2019):
            self._view._ddyear.options.append(ft.dropdown.Option(str(i)))
        for color in colors:
            self._view._ddcolor.options.append(ft.dropdown.Option(str(color)))
        self._view.update_page()

    def handle_graph(self, e):
        self._view.txtOut.controls.clear()
        if self._view._ddyear.value is None or self._view._ddcolor.value is None:
            self._view.txtOut.controls.append(ft.Text("Inserisci un anno e un colore!", color='red'))
            self._view.update_page()
            return
        flag = self._model.buildGraph(self._view._ddyear.value, self._view._ddcolor.value)
        if flag:
            self._view.txtOut.controls.append(ft.Text(self._model.getGraphDetails()))
            results, ripetuti = self._model.analyze()
            self._view.txtOut.controls.append(ft.Text(f"Top 3 archi:"))
            for result in results:
                self._view.txtOut.controls.append(ft.Text(f"{result[0]} -> {result[1]}, peso: {result[2]}"))
            self._view.txtOut.controls.append(ft.Text(f"Nodi ripetuti:"))
            for ripetuto in ripetuti:
                self._view.txtOut.controls.append(ft.Text(f"{ripetuto}"))
            self.fillDDProduct()
            self._view.update_page()
            return
        else:
            self._view.txtOut.controls.append(ft.Text("Errore nella creazione del grafo!", color='red'))
            self._view.update_page()
            return

    def fillDDProduct(self):
        self._view._ddnode.options.clear()
        nodi = self._model.get_nodes()
        for n in nodi:
            self._view._ddnode.options.append(
                ft.dropdown.Option(text=n.Product_number, data=n, on_click=self.readDDProducts))
        self._view.update_page()

    def handle_search(self, e):
        self._view.txtOut2.controls.clear()
        if len(self._model.graph.nodes) == 0:
            self._view.txtOut2.controls.append(ft.Text("Creare un grafo!", color='red'))
            self._view.update_page()
            return
        if self._selected_product is None:
            self._view.txtOut2.controls.append(ft.Text("Selezionare un prodotto!", color='red'))
            self._view.update_page()
            return
        componenti = self._model.getPath(self._selected_product)
        if componenti:
            self._view.txtOut2.controls.append(ft.Text(f"Lunghezza: {len(componenti)-1}"))
            for c in componenti:
                self._view.txtOut2.controls.append(ft.Text(f"{c}"))
            self._view.update_page()
            return
        else:
            self._view.txtOut2.controls.append(ft.Text("Errore durante l'analisi dei componenti!", color='red'))
            self._view.update_page()
            return

    def readDDProducts(self, e):
        if e.control.data is None:
            self._selected_product = None
        else:
            self._selected_product = e.control.data

