import tkinter as tk

large_font = ("Verdana", 12)
class MainGui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column = 0, sticky = "nsew")

        self.show_frame(StartPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

def qf(sting):
    print(sting)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "Start Page", font = large_font)
        label.pack(pady = 10, padx = 10)

        button = tk.Button(self, text = "Visit Page 1", command=lambda:controller.show_frame(PageOne))
        button.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "Page one", font = large_font)
        label.pack(pady = 10, padx = 10)

        button1 = tk.Button(self, text = "Back to Home", command=lambda:controller.show_frame(StartPage))
        button1.pack()

app = MainGui()
app.mainloop()
