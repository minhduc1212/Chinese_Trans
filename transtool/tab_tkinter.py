import tkinter as tk
from tkinter import ttk

def save_text():
    current_tab = tabControl.tab(tabControl.select(), "text")
    text = text_widgets[current_tab].get("1.0", "end-1c")
    print("Text in", current_tab, "tab:", text)

root = tk.Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Tab 1')
tabControl.add(tab2, text='Tab 2')
tabControl.pack(expand=1, fill="both")

text_widgets = {}

text_widget1 = tk.Text(tab1)
text_widget1.pack(fill="both", expand=True)
text_widgets["Tab 1"] = text_widget1

text_widget2 = tk.Text(tab2)
text_widget2.pack(fill="both", expand=True)
text_widgets["Tab 2"] = text_widget2

save_button = ttk.Button(root, text="Save", command=save_text)
save_button.pack()

root.mainloop()