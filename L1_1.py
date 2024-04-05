import os

MODELSIZE = 256
BUFSIZE = 512


# Structure to hold symbol and its count
class OpisSymbol:
    def __init__(self, symbol, licznosc):
        self.symbol = symbol
        self.licznosc = licznosc


modelShannon = [OpisSymbol(i, 0) for i in range(MODELSIZE)]
modelSortShannon = [OpisSymbol(i, 0) for i in range(MODELSIZE)]


def zmienRozszerzenieNazwy(nazwa, rozszerzenie):
    base_name = os.path.splitext(nazwa)[0]
    new_name = f"{base_name}{rozszerzenie}"
    return new_name



def wyznaczModel(nazwa):
    try:
        with open(nazwa, "rb") as plik:
            buf = plik.read(BUFSIZE)
            suma = 0
            while buf:
                for b in buf:
                    modelShannon[b].licznosc += 1
                    suma += 1
                buf = plik.read(BUFSIZE)

        nazwaIle = zmienRozszerzenieNazwy(nazwa, ".ileBajtow")
        with open(nazwaIle, "w") as plik:
            print(f"Odczytano {suma} bajtow")
            plik.write(f"{suma}\n")

        nazwaModel = zmienRozszerzenieNazwy(nazwa, ".model")
        with open(nazwaModel, "w") as plik:
            print("Model:")
            for symbol in modelShannon:
                if symbol.licznosc > 0:
                    print(f"Znak {symbol.symbol} licznosc {symbol.licznosc}")
                    plik.write(f"{symbol.symbol} {symbol.licznosc}\n")
    except IOError as e:
        print(f"Nie mozna otworzyc pliku: {e}")


def sortujModel(nazwa):
    global modelSortShannon
    modelSortShannon = sorted(modelShannon, key=lambda x: x.licznosc, reverse=True)

    nazwaModelSort = zmienRozszerzenieNazwy(nazwa, ".modelSort")
    with open(nazwaModelSort, "w") as plik:
        print("Model posortowany:")
        for symbol in modelSortShannon:
            if symbol.licznosc > 0:
                print(f"Znak {symbol.symbol} licznosc {symbol.licznosc}")
                plik.write(f"{symbol.symbol} {symbol.licznosc}\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print(f"Uzycie: {sys.argv[0]} nazwa_pliku")
        sys.exit(1)

    nazwa = sys.argv[1]
    wyznaczModel(nazwa)
    sortujModel(nazwa)
