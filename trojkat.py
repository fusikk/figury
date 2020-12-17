# Dany jest zbiór punktów leżących na płaszczyźnie opisany przy pomocy struktury:
# 𝑑𝑎𝑛𝑒 = [(𝑥1,𝑦1),(𝑥2,𝑦2),(𝑥3,𝑦3),...(𝑥𝑁 ,𝑦𝑁 )].
# Proszę napisać funkcję, która zwraca wartość 𝑇𝑟𝑢𝑒 jeżeli w zbiorze istnieją 3 punkty wyznaczające trójkąt prostokątny
# o  bokach  przyprostokątnych  niebędących  równoległymi  do  osi  układu kartezjańskiego oraz wewnątrz, którego nie ma
# żadnych innych punktów. Do funkcji należy przekazać strukturę opisującą położenie punktów.


class Punkt:
    def __init__(self, x, y):
        self.indeks_wlasny = None
        self.indeksy_innych = []    #Do sprawdzania z ktorymi punktami juz utworzono prosta

        self.x = x
        self.y = y


class Prosta:
    def __init__(self, A, B, C, indeksy):
        #Ax + By + C = 0
        self.A = A
        self.B = B
        self.C = C

        if self.A == 0 or self.B == 0:
            self.poprawna = False
        else:
            self.poprawna = True

        self.indeksy_punktow = sorted(indeksy)
        self.indeksy_sprawdzonych = []

        self.wypisz_prosta()


    def wypisz_prosta(self):
        linia = str(self.A) + 'x'
        if self.B < 0:
            linia += str(self.B) + 'y'
        elif self.B > 0:
            linia += '+' + str(self.B) + 'y'

        if self.C < 0:
            linia += str(self.C) + '=0'
        elif self.C > 0:
            linia += '+' + str(self.C) + '=0'
        else:
            linia += '=0'

        print(linia)


class Trojkat:
    def __init__(self, indeksy_punkt, indeksy_prost=[]):
        self.indeksy_punktow = sorted(indeksy_punkt)
        self.indeksy_prostych = sorted(indeksy_prost)

    #Sprwadz czy aby na pewno sa tylko 3 wierczholki, a nie np. 4, bo 2 leza na jednej linii
    def sprawdz_poprawnosc(self):
        if len(self.indeksy_punktow) != 3:
            return True
        else:
            return False

    def wypisz_trojkat(self, lista_punktow):
        s1 = "({}, {})".format(lista_punktow[self.indeksy_punktow[0]].x, lista_punktow[self.indeksy_punktow[0]].y)
        s2 = "({}, {})".format(lista_punktow[self.indeksy_punktow[1]].x, lista_punktow[self.indeksy_punktow[1]].y)
        s3 = "({}, {})".format(lista_punktow[self.indeksy_punktow[2]].x, lista_punktow[self.indeksy_punktow[2]].y)

        return "{}, {}, {}".format(s1, s2, s3)


def oblicz_prosta(punkt1, punkt2):
    a = -1*(punkt2.y - punkt1.y)
    b = punkt2.x - punkt1.x
    c = -punkt1.y*punkt2.x + punkt1.y*punkt1.x + punkt1.x*punkt2.y - punkt1.x*punkt1.y

    return Prosta(a, b, c, [punkt1.indeks_wlasny, punkt2.indeks_wlasny])


def znajdz_prosta(indeksy_punktow, lista_prostych):
    for prosta in lista_prostych:
        if sorted(indeksy_punktow) == prosta.indeksy_punktow:
            return lista_prostych.index(prosta)


#Funkcja sprawdzajaca czy dany punkt lezy wewnatrz trojkata przy pomocy koordynatow barycentrycznych
def sprawdz_czy_wewnatrz(p, trojkat, lista_punktow):
    p1 = lista_punktow[trojkat.indeksy_punktow[0]]
    p2 = lista_punktow[trojkat.indeksy_punktow[1]]
    p3 = lista_punktow[trojkat.indeksy_punktow[2]]

    alpha = ((p2.y - p3.y) * (p.x - p3.x) + (p3.x - p2.x) * (p.y - p3.y)) /\
            ((p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y))

    beta = ((p3.y - p1.y) * (p.x - p3.x) + (p1.x - p3.x) * (p.y - p3.y)) /\
           ((p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y))

    gamma = 1 - alpha - beta;

    alpha = (alpha > 0)
    beta = (beta > 0)
    gamma = (gamma > 0)

    return (alpha and beta and gamma)


def stworz_punkty(punkty):
    lista_punktow = []
    for element in punkty:
        lista_punktow.append(Punkt(element[0], element[1]))
        lista_punktow[-1].indeks_wlasny = len(lista_punktow) - 1
    return lista_punktow


#Znajdowanie równań prostych
def znajdz_rownania_prostych(lista_punktow):
    lista_prostych = []

    for punkt_1 in lista_punktow:
        for punkt_2 in lista_punktow:
            if punkt_1 == punkt_2 or punkt_2.indeks_wlasny in punkt_1.indeksy_innych:
                continue

            else:
                lista_prostych.append(oblicz_prosta(punkt_1, punkt_2))

                punkt_1.indeksy_innych.append(punkt_2.indeks_wlasny)
                punkt_2.indeksy_innych.append(punkt_1.indeks_wlasny)

    return lista_prostych


#Znajduje proste prostopadle, zwraca indeksy tych prostych w przekazanej liscie
def znajdz_proste_prostopadle(lista_prostych):
    pary_prostopadlych = []

    for prosta_1 in lista_prostych:
        for prosta_2 in lista_prostych:
            if prosta_1.indeksy_punktow == prosta_2.indeksy_punktow or lista_prostych.index(prosta_1)\
                    in prosta_2.indeksy_sprawdzonych:
                continue

            else:
                #Warunek prostopadlosci
                if prosta_1.poprawna and prosta_2.poprawna and prosta_1.A * prosta_2.A == -1 * prosta_1.B * prosta_2.B:
                    pary_prostopadlych.append([lista_prostych.index(prosta_1), lista_prostych.index(prosta_2)])
                prosta_1.indeksy_sprawdzonych.append(lista_prostych.index(prosta_2))
                prosta_2.indeksy_sprawdzonych.append(lista_prostych.index(prosta_1))

    return pary_prostopadlych


def wygeneruj_trojkaty_prostopadle(lista_prostych, pary_prostopadlych):
    lista_trojkatow = []

    for para in pary_prostopadlych:
        indeksy_punktow_trojkata = []
        indeksy_prostych_trojkata = para

        indeksy_do_wyszukania = []

        if lista_prostych[para[0]].indeksy_punktow[0] not in lista_prostych[para[1]].indeksy_punktow:
            indeksy_do_wyszukania.append(lista_prostych[para[0]].indeksy_punktow[0])
        elif lista_prostych[para[0]].indeksy_punktow[1] not in lista_prostych[para[1]].indeksy_punktow:
            indeksy_do_wyszukania.append(lista_prostych[para[0]].indeksy_punktow[1])

        if lista_prostych[para[1]].indeksy_punktow[0] not in lista_prostych[para[0]].indeksy_punktow:
            indeksy_do_wyszukania.append(lista_prostych[para[1]].indeksy_punktow[0])
        elif lista_prostych[para[1]].indeksy_punktow[1] not in lista_prostych[para[0]].indeksy_punktow:
            indeksy_do_wyszukania.append(lista_prostych[para[1]].indeksy_punktow[1])
        # print(indeksy_do_wyszukania)
        indeksy_prostych_trojkata.append(znajdz_prosta(indeksy_do_wyszukania, lista_prostych))

        for indeks in lista_prostych[para[0]].indeksy_punktow:
            if indeks not in indeksy_punktow_trojkata: indeksy_punktow_trojkata.append(indeks)

        for indeks in lista_prostych[para[1]].indeksy_punktow:
            if indeks not in indeksy_punktow_trojkata: indeksy_punktow_trojkata.append(indeks)

        lista_trojkatow.append(Trojkat(indeksy_punktow_trojkata, indeksy_prostych_trojkata))
        # print(lista_trojkatow[-1].indeksy_prostych)
        if lista_trojkatow[-1].sprawdz_poprawnosc():
            del lista_trojkatow[-1]

    return lista_trojkatow


def wypisz_poprawne_trojkaty(lista_trojkatow, lista_punktow):
    wynik = False

    indeks_trojkata = 0
    while indeks_trojkata < len(lista_trojkatow):
        wewnatrz = False
        for punkt in lista_punktow:
            if punkt.indeks_wlasny in lista_trojkatow[indeks_trojkata].indeksy_punktow:
                continue
            wewnatrz = sprawdz_czy_wewnatrz(punkt, lista_trojkatow[indeks_trojkata], lista_punktow)
            if wewnatrz:
                #print("{} {}".format(punkt.x, punkt.y))
                break

        if wewnatrz:
            del lista_trojkatow[indeks_trojkata]
            continue

        else:
            print("Trojkat spelniajacy zalozenia: {}".format(lista_trojkatow[indeks_trojkata].
                                                             wypisz_trojkat(lista_punktow)))
            wynik = True
            indeks_trojkata += 1

    return wynik


def sprawdzenie_plaszyczny(punkty):

    lista_punktow = stworz_punkty(punkty)
    lista_prostych = znajdz_rownania_prostych(lista_punktow)
    pary_prostopadlych = znajdz_proste_prostopadle(lista_prostych)
    lista_trojkatow = wygeneruj_trojkaty_prostopadle(lista_prostych, pary_prostopadlych)

    wynik = wypisz_poprawne_trojkaty(lista_trojkatow, lista_punktow)

    return wynik
