from tkinter import Frame, Label, Button, Listbox, Scrollbar, StringVar, messagebox

class ResultsPanel(Frame):
    def __init__(self, master, recommendations, like_callback, dislike_callback):
        super().__init__(master)
        self.master = master
        self.recommendations = recommendations
        self.like_callback = like_callback
        self.dislike_callback = dislike_callback
        
        self.title_var = StringVar()
        self.description_var = StringVar()
        
        self.create_widgets()
        self.update_results()

    def create_widgets(self):
        self.title_label = Label(self, textvariable=self.title_var, font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.description_label = Label(self, textvariable=self.description_var, wraplength=400, justify="left")
        self.description_label.pack(pady=10)

        self.like_button = Button(self, text="Like", command=self.like_recommendation)
        self.like_button.pack(side="left", padx=20)

        self.dislike_button = Button(self, text="Dislike", command=self.dislike_recommendation)
        self.dislike_button.pack(side="right", padx=20)

        self.results_listbox = Listbox(self, width=50, height=10)
        self.results_listbox.pack(pady=10)

        self.scrollbar = Scrollbar(self, command=self.results_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.results_listbox.config(yscrollcommand=self.scrollbar.set)

    def update_results(self):
        self.results_listbox.delete(0, 'end')
        for recommendation in self.recommendations:
            self.results_listbox.insert('end', recommendation['nom'])

        if self.recommendations:
            self.results_listbox.select_set(0)
            self.display_selected_recommendation()

        self.results_listbox.bind('<<ListboxSelect>>', self.on_select)

    def on_select(self, event):
        self.display_selected_recommendation()

    def display_selected_recommendation(self):
        selected_index = self.results_listbox.curselection()
        if selected_index:
            recommendation = self.recommendations[selected_index[0]]
            self.title_var.set(recommendation['nom'])
            self.description_var.set(recommendation['description'])

    def like_recommendation(self):
        selected_index = self.results_listbox.curselection()
        if selected_index:
            recommendation = self.recommendations[selected_index[0]]
            self.like_callback(recommendation)
            messagebox.showinfo("Liked", f"You liked {recommendation['nom']}!")
        else:
            messagebox.showwarning("Select Recommendation", "Please select a recommendation to like.")

    def dislike_recommendation(self):
        selected_index = self.results_listbox.curselection()
        if selected_index:
            recommendation = self.recommendations[selected_index[0]]
            self.dislike_callback(recommendation)
            messagebox.showinfo("Disliked", f"You disliked {recommendation['nom']}!")
        else:
            messagebox.showwarning("Select Recommendation", "Please select a recommendation to dislike.")