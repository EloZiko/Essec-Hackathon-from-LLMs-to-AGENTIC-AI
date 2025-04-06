from tkinter import Frame, Label, Entry, Button, StringVar, messagebox

class SearchPanel(Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        self.search_label = Label(self, text="Enter your search query:")
        self.search_label.pack(pady=10)

        self.search_var = StringVar()
        self.search_entry = Entry(self, textvariable=self.search_var, width=50)
        self.search_entry.pack(pady=5)

        self.search_button = Button(self, text="Get Recommendations", command=self.get_recommendations)
        self.search_button.pack(pady=10)

    def get_recommendations(self):
        query = self.search_var.get()
        if query:
            self.controller.generate_recommendations(query)
        else:
            messagebox.showwarning("Input Error", "Please enter a search query.")