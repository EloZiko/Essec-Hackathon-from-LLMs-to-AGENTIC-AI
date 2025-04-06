from tkinter import Tk, Frame, Label, Entry, Button, Listbox, Scrollbar, messagebox
from components.recommendation_card import RecommendationCard
from components.search_panel import SearchPanel
from components.results_panel import ResultsPanel
from controllers.recommendation_controller import RecommendationController

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Recommendation Generator")
        self.root.geometry("600x400")

        self.controller = RecommendationController()

        self.search_panel = SearchPanel(self.root, self.controller)
        self.search_panel.pack(fill="x")

        self.results_panel = ResultsPanel(self.root, self.controller)
        self.results_panel.pack(fill="both", expand=True)

        self.controller.set_results_panel(self.results_panel)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    app.run()