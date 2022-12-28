import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msb

#https://www.obliczeniowo.com.pl/506


class Application:

    klasa_1=1
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
        klasa_1=self.cb_value.get()
        print(klasa_1)



#Application()