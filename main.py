import sys
import datetime
import requests
import json
import tkinter
from tkinter import simpledialog

from tkinter import *

from pyModbusTCP.client import ModbusClient
#from libs import *
import time



'''
Read modbus data tcpip from Carel controller every 5sec. 
Sprsun heat pump, print in window, and send as rest API to pvmonitor.com every 3minutes.
'''


#pobranie i obrobka danych z pompy z modbus


   #     if B2_PC_Temp_Zas < 6 and B1_PC_Temp_Pow < 6 or B8_PC_Temp_CW < 6 or PC_Aktualne_Obroty_Spr < 0:
    #        print('Wadliwe dane z MODBUS - ponowne pobranie' + str(i))
   #         time.sleep(5)
   #     else:
  #          print('dobre dane z MODBUS - przerwanie petli powtorzeń')
  #          break

   # if i >= (ilosc_prob - 1):
  #      print('Wadliwe dane z MODBUS - zamknięcie programu')
     #   sys.exit()
  #  return ()
def data_converter(param):  # funkcja sprawdzajaca czy dodatnia czy ujemna

    if param > 0x8000:  # jest na minusie wartości
        par = param - 0x10000
        return par
    par = param
    return par

def pobranie_czasu():
    # pobranie czasu systemowego
    teraz = datetime.datetime.now()
    pm_solartime = teraz.strftime("%Y-%m-%dT%H:%M:%S")
    return (pm_solartime)
def heat_curve_CO():  #stworzenie tabelki z danymi z krzywej grzewcze j
    l = tkinter.Label(text='           Krzywa CO            ', relief=RIDGE, ).place(x=0, y=360)
    l = tkinter.Label(text='T.zewnętrzna ', relief=RIDGE, ).place(x=0, y=380)
    l = tkinter.Label(text='T.zadana ', relief=RIDGE, ).place(x=76, y=380)

    l = tkinter.Label(text='X1:', relief=RIDGE, ).place(x=0, y=400)
    l = tkinter.Label(text=Ogrzew_TempZewn_X1, relief=RIDGE, ).place(x=20, y=400)
    l = tkinter.Label(text='Y1:', relief=RIDGE, ).place(x=76, y=400)
    l = tkinter.Label(text=Ogrzew_TempWody_Y1, relief=RIDGE, ).place(x=96, y=400)

    l = tkinter.Label(text='X2:', relief=RIDGE, ).place(x=0, y=420)
    l = tkinter.Label(text=Ogrzew_TempZewn_X2, relief=RIDGE, ).place(x=20, y=420)
    l = tkinter.Label(text='Y2:', relief=RIDGE, ).place(x=76, y=420)
    l = tkinter.Label(text=Ogrzew_TempWody_Y2, relief=RIDGE, ).place(x=96, y=420)

    l = tkinter.Label(text='X3:', relief=RIDGE, ).place(x=0, y=440)
    l = tkinter.Label(text=Ogrzew_TempZewn_X3, relief=RIDGE, ).place(x=20, y=440)
    l = tkinter.Label(text='Y3:', relief=RIDGE, ).place(x=76, y=440)
    l = tkinter.Label(text=Ogrzew_TempWody_Y3, relief=RIDGE, ).place(x=96, y=440)

    l = tkinter.Label(text='X4:', relief=RIDGE, ).place(x=0, y=460)
    l = tkinter.Label(text=Ogrzew_TempZewn_X4, relief=RIDGE, ).place(x=20, y=460)
    l = tkinter.Label(text='Y4:', relief=RIDGE, ).place(x=76, y=460)
    l = tkinter.Label(text=Ogrzew_TempWody_Y4, relief=RIDGE, ).place(x=96, y=460)

    #   równanie do wyliczenia temperatury wedlug krzywej Y=((Y2-Y1)/(X2-X1))*(T.ZEWN-X1)+Y1
    # przypisanie zmeinnych tak żeby łatwiej podstawić pod równanie

    Temp_Zewnetrzna = float(B3_PC_Temp_Zewnetrzna)  # zamiana na float zeby zrobić obliczenia temp zewnetrznej
    X1 = float(Ogrzew_TempZewn_X1)
    X2 = float(Ogrzew_TempZewn_X2)
    X3 = float(Ogrzew_TempZewn_X3)
    X4 = float(Ogrzew_TempZewn_X4)

    Y1 = float(Ogrzew_TempWody_Y1)
    Y2 = float(Ogrzew_TempWody_Y2)
    Y3 = float(Ogrzew_TempWody_Y3)
    Y4 = float(Ogrzew_TempWody_Y4)

    # określenie z ktorego przedziału krzywej należy korzystac

    if Temp_Zewnetrzna < X2:  # Y12
        Y = ((Y2 - Y1) / (X2 - X1)) * (Temp_Zewnetrzna - X1) + Y1

    elif Temp_Zewnetrzna < X3:  # Y23
        Y = ((Y3 - Y2) / (X3 - X2)) * (Temp_Zewnetrzna - X2) + Y2

    else:
        Y = ((Y4 - Y3) / (X4 - X3)) * (Temp_Zewnetrzna - X3) + Y3  # Y34

    # zaokrąglenie do 2 miejsc po przecinku
    global Ys
    Ys = str(round(Y, 1))

    # wydruk na ekranie w oknie wartości zadanej
   # l = tkinter.Label(text='Temp_powrotu_CO_zadana:  ' + Ys + '°C  ', relief=RIDGE, fg="red").place(x=0, y=240)

    '''
    Y12 = ((Y2 - Y1) / (X2 - X1)) * (Temp_Zewnetrzna - X1) + Y1
    Y23=((Y3-Y2)/(X3-X2))*(Temp_Zewnetrzna-X2)+Y2
    Y34=((Y4-Y3)/(X4-X3))*(Temp_Zewnetrzna-X3)+Y3
    print(Y12, Y23, Y34)
    print(Ys)
    '''

    # e = tkinter.Entry(text='pole ' ).place(x=0, y=300)
    # Label(text=c, relief=RIDGE,  width=25).grid(row=30, column=0)
    # Entry(bg=c,   relief=SUNKEN, width=25).grid(row=30, column=1)

    # var = simpledialog.askstring("Name prompt", "enter your name")
    # print (var)

def send_pvmon():
    Id_Pvmonitor = jsonObject['Id_Pvmonitor']
    Password_Pvmonitor = jsonObject['Password_Pvmonitor']

    pm_solartime = pobranie_czasu()

    # z pompy ciepla
    url3 = 'http://dane.pvmonitor.pl/pv/get2.php?idl=' + str(Id_Pvmonitor) + '&p=' + str(
        Password_Pvmonitor) + '&tm=' + str(pm_solartime) + '&F22=' + str(B8_PC_Temp_CWU) \
           + '&F16=' + str(B3_PC_Temp_Zewnetrzna) + '&F12=' + str(B1_PC_Temp_Powrot) + '&F53=' + str(
        B9_PC_Temp_Parownika1) + '&F14=' + str(B4_PC_Temp_Czynnika_Sprezanie) \
           + '&F13=' + str(B5_PC_Temp_Ssanie) + '&F27=' + str(B7_PC_Cisnienie_Ssania) + '&F46=' + str(
        B6_PC_Cisnienie_Sprezania) + '&F500=' + str(PC_Aktualne_Obroty_Sprezarki) \
           + '&F61=' + str(PC_Przegrzanie_na_Ssaniu) + '&F11=' + str(B2_PC_Temp_Zasilanie) + '&F60=' + str(
        PC_Przegrzanie_na_Sprezaniu) \

    response3 = requests.post(url3)

  #  print('PVMONITOR3 PC', (response3.status_code))
    return (response3.status_code)


    # 12 temp powrót PC
    # 16 temp zewn
    # 22 temp CWU
    # 53 temp absorbera (parownik)
    # 14 temp gazu po wy ze sprezarki
    # 13 temp czynnika po wy ze skraplacza
    # 60 temp parowania
    # 61 temp przegrzania        na ssaniu
    # 27 Cisnienie ssania
    # 46 Cisnienie sprezania
    # 500(obroty generatora)
    # 11 temp zasilania z PC
def sprsun_modbus():
    # ilosc_prob = 5  # tyle prob pobrania danych z modbus jesli wystapą jakis przeklamania opisane w w warunku ponizej

    #  for i in range(ilosc_prob):
    global c
    c = ModbusClient()

    # uncomment this line to see debug message

    # c.debug(True)

    # define modbus server host, port

    # otwiera plik z danymi
    global jsonObject

    with open('C:/Users/Marek/PycharmProjects/config.json') as jsonFile:
    #with open('config1.json') as jsonFile:    uwaga jesli plik z haslem znajduje sie w katalogu projektu to trzeba odkomentować tą linijke  powyzej zakomentować
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    SERVER_HOST = jsonObject['SERVER_HOST']
    SERVER_PORT = jsonObject['SERVER_PORT']

    c.host(SERVER_HOST)
    c.port(SERVER_PORT)

    # open or reconnect TCP to server
    # global regs
    if not c.is_open():
        if not c.open():
            print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

            # if open() is ok, read register (modbus function 0x03)
        if c.is_open():

            regs = c.read_holding_registers(188, 125)  # 0x03
            # tu się zaczynają rejestry z danymi biezacymi w pompie ciepla adres 188 ilosc 30 rejestrów modbus
            regs0 = c.read_holding_registers(0, 125)
            # regs1 = c.read_input_registers(1,125)  #0x04
            # regs1 = c.read_discrete_inputs(0,125)  #0x02

            global PC_on_off
            PC_on_off = c.read_coils(40, 1)  # 0x01      #odczyt bitu True załaczana pompa False wyłaczona
            # PC_on_off=c.write_single_coil(40, False)   #wyłacza pompe
            # PC_on_off = c.write_single_coil(40, True)   #włącza pompe

            # regs1 = c.read_input_registers()

            # if success display registers
            # if regs:
            #    print("modbus registers values " + str(regs))

            regs1 = c.read_holding_registers(313, 125)

            # if success display registers
            if regs1:
                print("modbus registers1 values " + str(regs1))

            regs2 = c.read_holding_registers(500, 125)

            # if success display registers
            if regs2:
                print("modbus registers2 values " + str(regs2))
            if regs0:
                print("modbus registers0 values " + str(regs0))
            if regs1:
                print("modbus registers1 values " + str(regs1))


    global B1_PC_Temp_Powrot
    global B2_PC_Temp_Zasilanie
    global B3_PC_Temp_Zewnetrzna
    global B4_PC_Temp_Czynnika_Sprezanie
    global B5_PC_Temp_Ssanie
    global B6_PC_Cisnienie_Sprezania
    global B7_PC_Cisnienie_Ssania
    global B8_PC_Temp_CWU
    global B9_PC_Temp_Parownika1
    global B19_PC_Temp_Parownika2
    global Y1_PC_Wentylator_Obroty
    global Y3_PC_Pompa_Obiegowa
    global PC_Wydajnosc_Sprezarki_Wymagana
    global PC_Aktualne_Obroty_Sprezarki
    global PC_Przegrzanie_na_Sprezaniu
    global PC_Przegrzanie_na_Ssaniu
    global B2_PC_Temp_Zas
    global B1_PC_Temp_Pow
    global B8_PC_Temp_CW
    global PC_Aktualne_Obroty_Spr
    global Ogrzew_TempZewn_X1
    global Ogrzew_TempWody_Y1
    global Ogrzew_TempZewn_X2
    global Ogrzew_TempWody_Y2
    global Ogrzew_TempZewn_X3
    global Ogrzew_TempWody_Y3
    global Ogrzew_TempZewn_X4
    global Ogrzew_TempWody_Y4
    global PC_Temp_CO_Zadana
    global B1_PC_Temp_Powrot

    global Ogrzew_TempZewn_X1
    global Ogrzew_TempWody_Y1
    global Ogrzew_TempZewn_X2
    global Ogrzew_TempWody_Y2
    global Ogrzew_TempZewn_X3
    global Ogrzew_TempWody_Y3
    global Ogrzew_TempZewn_X4
    global Ogrzew_TempWody_Y4
    global PC_Temp_CO_Zadana
    global PC_Temp_CO_Zadana_dzien


    B1_PC_Temp_Powrot = str(data_converter((regs[0])) / 10)
    B2_PC_Temp_Zasilanie = str(data_converter((regs[1])) / 10)
    B3_PC_Temp_Zewnetrzna = str(data_converter((regs[2])) / 10)
    B4_PC_Temp_Czynnika_Sprezanie = str(data_converter((regs[3])) / 10)
    B5_PC_Temp_Ssanie = str(data_converter((regs[4])) / 10)
    B6_PC_Cisnienie_Sprezania = str((regs[5]) / 10)
    B7_PC_Cisnienie_Ssania = str((regs[6]) / 10)
    B8_PC_Temp_CWU = str(data_converter((regs[7])) / 10)
    B9_PC_Temp_Parownika1 = str(
        data_converter((regs[8])) / 10)  # mogą być ujemne musi przejśc funkcje sprawdzajaca czy dodatnia czy ujemna
    B19_PC_Temp_Parownika2 = str(data_converter((regs[18])) / 10)
    Y1_PC_Wentylator_Obroty = str((regs[9]))
    Y3_PC_Pompa_Obiegowa = str((regs[10]) / 10)
    PC_Wydajnosc_Sprezarki_Wymagana = str((regs[15]) / 10)
    PC_Wydajnosc_Sprezarki_Aktualna = str((regs[16]) / 10)
    PC_Aktualne_Obroty_Sprezarki = str(data_converter((regs[17])) / 10)
    PC_Przegrzanie_na_Sprezaniu = str(data_converter((regs[20])) / 10)
    PC_Przegrzanie_na_Ssaniu = str(data_converter((regs[23])) / 10)

    Ogrzew_TempZewn_X1 = str(data_converter((regs[92])) / 10)  # CO krzywa grzewcza
    Ogrzew_TempWody_Y1 = str(data_converter((regs[103])) / 10)

    Ogrzew_TempZewn_X2 = str(data_converter((regs[93])) / 10)
    Ogrzew_TempWody_Y2 = str(data_converter((regs[104])) / 10)

    Ogrzew_TempZewn_X3 = str(data_converter((regs[94])) / 10)
    Ogrzew_TempWody_Y3 = str(data_converter((regs[105])) / 10)

    Ogrzew_TempZewn_X4 = str(data_converter((regs[95])) / 10)
    Ogrzew_TempWody_Y4 = str(data_converter((regs1[24])) / 10)  # uwaga z innego banku

    PC_Temp_CO_Zadana = str(data_converter((regs[28])) / 10)

    PC_TRYB_Pracy = regs0[12]
    PC_Temp_CO_Zadana_dzien = str(data_converter((regs0[1])) / 10)

    '''
    # ----------------------------------------------------------------------------------------------
    # sprawdzenie czy nie ma przeklamań w odczycie z pompy potrafi czasami odczytywac same zera
    # jesli tak jest zakonczony program i kolejna proba przy nastepnym wywolaniu spelnione  warunki

    B2_PC_Temp_Zas = float(B2_PC_Temp_Zasilanie)
    B1_PC_Temp_Pow = float(B1_PC_Temp_Powrot)
    B8_PC_Temp_CW = float(B8_PC_Temp_CWU)
    PC_Aktualne_Obroty_Spr = float(PC_Aktualne_Obroty_Sprezarki)



    '''

    heat_curve_CO()

    spr_stat_Pc_on_off()

    l = tkinter.Label(text='Temp powrotu: ' + B1_PC_Temp_Powrot + '°C ', relief=RIDGE, fg="blue").place(x=0, y=0)
    l = tkinter.Label(text='Temp zasilania: ' + B2_PC_Temp_Zasilanie + '°C ').place(x=0, y=60)
    l = tkinter.Label(text='Temp zewnętrzna: ' + B3_PC_Temp_Zewnetrzna + '°C ').place(x=0, y=40)



    l = tkinter.Label(text='Temp_Ssania ' + B5_PC_Temp_Ssanie + '°C ').place(x=0, y=80)
    l = tkinter.Label(text='Ciśnienie_Sprężania ' + B6_PC_Cisnienie_Sprezania + ' BAR ').place(x=0, y=100)
    l = tkinter.Label(text='Ciśnienie_Ssania ' + B7_PC_Cisnienie_Ssania + ' BAR ').place(x=0, y=120)
    l = tkinter.Label(text='Temp_CWU ' + B8_PC_Temp_CWU + '°C ').place(x=0, y=140)
    l = tkinter.Label(text='Temp_Parownika1 ' + B9_PC_Temp_Parownika1 + '°C ').place(x=0, y=160)

    l = tkinter.Label(text='Temp_Parownika2 ' + B19_PC_Temp_Parownika2 + '°C ').place(x=0, y=180)
    l = tkinter.Label(text='Obroty_Wentylatora ' + Y1_PC_Wentylator_Obroty + ' RPM ').place(x=0, y=200)
    l = tkinter.Label(text='Wysterowanie_Pompy_Obiegowej ' + Y3_PC_Pompa_Obiegowa + ' % ').place(x=0, y=220)

    l = tkinter.Label(text='Temp_Czynnika_Sprężania ' + B4_PC_Temp_Czynnika_Sprezanie + '°C ').place(x=0, y=240)
    l = tkinter.Label(text='Wydajność_Sprężarki_Wymagana ' + PC_Wydajnosc_Sprezarki_Wymagana + ' % ').place(x=0, y=260)
    l = tkinter.Label(text='Wydajność_Sprężarki_Aktualna ' + PC_Wydajnosc_Sprezarki_Aktualna + ' % ').place(x=0, y=280)
    l = tkinter.Label(text='Aktualne_Obroty_Sprężarki ' + PC_Aktualne_Obroty_Sprezarki + ' RPM ').place(x=0, y=300)
    l = tkinter.Label(text='Przegrzanie_na_Sprężaniu ' + PC_Przegrzanie_na_Sprezaniu + '°C ').place(x=0, y=320)
    l = tkinter.Label(text='Przegrzanie_na_Ssaniu ' + PC_Przegrzanie_na_Ssaniu + '°C ').place(x=0, y=340)

    def str_tryb_pracy():
        l = tkinter.Label(text='TRYB: ' + str_PC_TRYB_Pracy).place(x=0, y=500)

    if PC_TRYB_Pracy==0:
        str_PC_TRYB_Pracy=' Dzień'
        str_tryb_pracy()
        l = tkinter.Label(text='Temp zadana CO powrotu:  ' + PC_Temp_CO_Zadana_dzien + '°C  ', relief=RIDGE, fg="red").place(x=0, y=20)

    elif PC_TRYB_Pracy == 1:
         str_PC_TRYB_Pracy = ' Noc'
         l = tkinter.Label(text='Temp zadana CO powrotu:  ' + 'NOC 41' + '°C  ', relief=RIDGE, fg="red").place(x=0, y=20)
            #uwaga tu nie dopisane jest pobieranie czasu temp noc

    elif PC_TRYB_Pracy == 2:
         str_PC_TRYB_Pracy = ' Krzywa Grzewcza'
         str_tryb_pracy()
         l = tkinter.Label(text='Temp zadana CO powrotu:  ' + Ys + '°C  ', relief=RIDGE, fg="red").place(x=0, y=20)

    elif PC_TRYB_Pracy == 3:
         str_PC_TRYB_Pracy = ' Serwisowy'
         str_tryb_pracy()






#wysyłka do Pvmonitor
def spr_stat_Pc_on_off():    #sprawdza czy bit wskazujacy na prace pompy jest ustawiony i wyswietla status i zmienia napis na przycisku

    if PC_on_off == [True]:
        l = tkinter.Label(text='Pompa Włączona ', fg="green").place(x=230, y=0)
        b = tkinter.Button(root, text='Wyłącz Pompę', width=15, bg='red', fg='white', command=funkcjaPrzycisku0)
        b.place(x=450, y=50)
    else:
        l = tkinter.Label(text='Pompa Wyłączona ', fg="red").place(x=230, y=0)
        b = tkinter.Button(root, text='Włącz Pompę', width=15, bg='green', fg='white', command=funkcjaPrzycisku0)
        b.place(x=450, y=50)

def funkcjaPrzycisku0():
    sprsun_modbus()
    spr_stat_Pc_on_off()
    global PC_on_off
    if PC_on_off == [True]:
        PC_on_off=c.write_single_coil(40, False)   #wyłacza pompe
        l = tkinter.Label(text='Wyłączanie pompy  ', fg="red").place(x=230, y=0)
        return
    PC_on_off = c.write_single_coil(40, True)   #włącza pompe
    l = tkinter.Label(text='Włączanie pompy  ', fg="green").place(x=230, y=0)


def funkcjaPrzycisku1():

    sprsun_modbus()

def funkcjaPrzycisku2():
    a=send_pvmon()

    l = tkinter.Label(text=f"PVMONITOR STATUS  {a}",bg='green').place(x=450, y=0)


def funkcjaPrzycisku4():
    print('Wcisnieto przycisk exit4')
  #  time.sleep(1)
    print('koniec')
    sys.exit(0)

#poczatek programu
    global Ys
    Ys='temp'


#poczatek petli głownej
#
#
#
#
#
root = tkinter.Tk()
root.geometry('600x680')
root.title('SPRSUN_MODBUS')


b=tkinter.Button(root, text='Wyłącz Pompę',width=15, bg='red', fg='white', command=funkcjaPrzycisku0)
b.place(x=450,y=50)

b=tkinter.Button(root, text='Pobierz MODBUS',width=15, bg='blue', fg='white', command=funkcjaPrzycisku1)
b.place(x=450,y=150)

b=tkinter.Button(root, text='Wyślij PVMONITOR',width=15, bg='blue', fg='white', command=funkcjaPrzycisku2)
b.place(x=450,y=200)

b=tkinter.Button(root, text='Wyjście',width=15, bg='black', fg='white', command=funkcjaPrzycisku4)
b.place(x=450,y=250)




'''
for i in range(5):
    for j in range(4):
        l = Label(text='%d.%d' % (i, j), relief=RIDGE)
        l.grid(row=i, column=j, sticky=NSEW)
'''


'''
e = tkinter.Entry(text='pole ' ).place(x=0, y=700)
Label(text='blue', relief=RIDGE,  width=25).grid(row=30, column=0)
Entry(bg='black',   relief=SUNKEN, width=25).grid(row=30, column=1)

var = simpledialog.askstring("Name prompt", "enter your name")
print (var)
'''

sprsun_modbus()




def timer1():   #co ile ms ma odczytywać dane z modbus
  #  print(datetime.datetime.now())
    sprsun_modbus()
    root.after(5000, timer1)

root.after(10000, timer1)

def timer2():                   #co ile ms ma wysyłać do pvmonitor
  #  print(datetime.datetime.now())
    a=send_pvmon()
    l = tkinter.Label(text=f"PVMONITOR STATUS  {a}", bg='green').place(x=450, y=0)
    root.after(120000, timer2)

root.after(120000, timer2)

def timer2a():  #(co ile ms ma wyszażać staus wysyłki do pvmon )
  #  print(datetime.datetime.now())
    #a=send_pvmon()
    a="---"
    l = tkinter.Label(text=f"PVMONITOR STATUS  {a}", bg='grey').place(x=450, y=0)
    root.after(50000, timer2a)

root.after(50000, timer2a)


root.mainloop()








