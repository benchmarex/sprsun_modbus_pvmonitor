

definicje = {}  #pusty słownik

while(True):


    print("1: Dodać definicję")
    print("2: Znajdź definicję")
    print("3: Usuń definicję")
    print("4: Zakończ")

    wybor = input ("Co chcesz zrobić? ")

    if (wybor == "1"):
        klucz = input ("Podaj klucz (słowo) do zdefiniowania: ")
        definicja = input ("podaj definicję: ")
        definicje[klucz] = definicja
        print ("definicja dodana pomyslnie ")
    elif (wybor=='2'):
        klucz = input ("Czego szukasz ?")
        if klucz in (definicje):
            print(definicje[klucz])
        else:
            print("Nie znalezionio definicji/n", klucz )
    elif (wybor=="3"):
        klucz = input("Jaką def chcesz usunąć? ")
        if klucz in  definicje :
            del definicje[klucz]
            print('usunieto def o nazwie', klucz )
        else:
            print("Nie znalezionio definicji/n", klucz)
    elif (wybor =="4"):
        print('koniec')
        break
    else:
         print("poza zakresem")

