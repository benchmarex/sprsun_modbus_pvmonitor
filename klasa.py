'''

import tkinter as tk
from tkinter import ttk


from tkinter import *
from tkinter.ttk import *
okno = Tk()
okno.title("Pierwszy suwak w oknie dialogowym")
okno.geometry('650x200')
suwak = Combobox(okno)
suwak['values']= ('Dzień', 'Noc', 'Krzywa Grzewcza', 'Serwisowy')
suwak.current(0) #ustawienie co ma być wartością domyślną
suwak.grid(column=10, row=10)
print(suwak.current)

okno.mainloop()

'''
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msb

#https://www.obliczeniowo.com.pl/506


class Application:
    def __init__(self):
        self.window = tk.Tk()

        self.cb_value = tk.StringVar()  # zmienna typu StringVar, która zostanie podpięta pod kontrolkę Combobox

        self.combobox = ttk.Combobox(self.window, textvariable=self.cb_value)  # tworzenie kontrolki Combobox
        self.combobox.place(x=0, y=0)  # umieszczenie kontrolki na oknie głównym
        self.combobox['values'] = (
        'Dzień', 'Noc', 'Krzywa Grzewcza', 'Serwisowy')  # ustawienie elementów zawartych na liście rozwijanej
        self.combobox.current(0)  # ustawienie domyślnego indeksu zaznaczenia

        self.combobox.bind("<<ComboboxSelected>>",
                           self.on_select_changed)  # podpięcie metody pod zdarzenie zmiany zaznaczenia

        self.window.mainloop()

    def on_select_changed(self, event):
        msb.showinfo("Info", self.cb_value.get())


apl = Application()








