import pickle
import pandas as pd
from scipy.stats import norm
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import train_test_split
from sklearn import tree
from scipy.stats import shapiro
from statistics import mean
import matplotlib.pyplot as plt


def read_xlsx_sheet(file_path, sheet_name):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return None


def oblicz_błąd_bezwzględny(target, prediction):
    błędy_bezwzględne = []
    for i in range(len(target)):
        błędy_bezwzględne.append(abs(target[i] - prediction[i]))
    return błędy_bezwzględne


def oblicz_czas_zagriożenia(target, prediction):
    czasy_zagrożenia = []
    for i in range(len(prediction)):
        if prediction[i] + 4 < target[i]:
            czasy_zagrożenia.append(target[i] - (prediction[i] + 4))
        else:
            czasy_zagrożenia.append(0)
    return czasy_zagrożenia
    


if __name__ == "__main__":
    file_path = "Dataset.xlsx"
    sheet_name_results = "Wyniki"
    light_blinking_time = 4


    # reading the group crossing data
    data_group_corss = read_xlsx_sheet(file_path, sheet_name_results)
    kolumny_wyjsciowe = "Czas przechodzenia od zielonego"

    Czas_target = data_group_corss["Czas przechodzenia od zielonego"].tolist()
    Czas_klasyczny = data_group_corss["Czas podejście klasyczne"].tolist()
    Czas_dzewo_decyzyjne = data_group_corss["Czas dzewo decyzyjne "].tolist()
    Czas_algorytm_własny = data_group_corss["Czas algorytm własny"].tolist()

    Błąd_Bezwzględny_klasyczny = oblicz_błąd_bezwzględny(Czas_target, Czas_klasyczny)
    Błąd_Bezwzględny_dzewo_decyzyjne = oblicz_błąd_bezwzględny(Czas_target, Czas_dzewo_decyzyjne)
    Błąd_Bezwzględny_algorytm_własny = oblicz_błąd_bezwzględny(Czas_target, Czas_algorytm_własny)

    Czas_zagrożenia_klasyczny = oblicz_czas_zagriożenia(Czas_target, Czas_klasyczny)
    Czas_zagrożenia_dzewo_decyzyjne = oblicz_czas_zagriożenia(Czas_target, Czas_dzewo_decyzyjne)
    Czas_zagrożenia_algorytm_własny = oblicz_czas_zagriożenia(Czas_target, Czas_algorytm_własny)

    print(f"Classical absolute error average:{mean(Błąd_Bezwzględny_klasyczny):.4f} danger time average:{mean(Czas_zagrożenia_klasyczny):.4f}")
    print(f"Tree absolute error average:{mean(Błąd_Bezwzględny_dzewo_decyzyjne):.4f} danger time average:{mean(Czas_zagrożenia_dzewo_decyzyjne):.4f}")
    print(f"Gauss absolute error average:{mean(Błąd_Bezwzględny_algorytm_własny):.4f} danger time average:{mean(Czas_zagrożenia_algorytm_własny):.4f}")

    x = np.arange(15)
    plt.style.use('bmh')
    plt.title("Czasy wyznaczony przez aplikację a czas rzeczywisty")
    plt.xlabel("Numer przypadku testowego")
    plt.ylabel("Czas [s]")
    plt.scatter(x, Czas_target, label="Czas potrzebny na przejście", alpha=0.7, s=100, marker="v", edgecolors="black")
    plt.scatter(x, Czas_klasyczny, label="Predykcja - podejście klasyczne", alpha=0.7, s=100, edgecolors="black")
    plt.scatter(x, Czas_dzewo_decyzyjne, label="Predykcja - drzewo decyzyjne", alpha=0.7, s=100, edgecolors="black")
    plt.scatter(x, Czas_algorytm_własny, label="Predykcja - algorytm autorski", alpha=0.7, s=100, edgecolors="black")
    plt.grid(True)
    plt.legend()
    plt.show()

    x = np.arange(15)
    plt.style.use('bmh')
    plt.title("Błąd bezwzględny algorytmów w aplikacji")
    plt.xlabel("Numer przypadku testowego")
    plt.ylabel("Czas [s]")
    plt.scatter(x, Błąd_Bezwzględny_klasyczny, label="Błąd bezwzględny - podejście klasyczne", alpha=0.7, s=100, edgecolors="black")
    plt.scatter(x, Błąd_Bezwzględny_dzewo_decyzyjne, label="Błąd bezwzględny - drzewo decyzyjne", alpha=0.7, s=100, edgecolors="black")
    plt.scatter(x, Błąd_Bezwzględny_algorytm_własny, label="Błąd bezwzględny - algorytm autorski", alpha=0.7, s=100, edgecolors="black")
    plt.grid(True)
    plt.legend()
    plt.show()

    x = np.arange(15)
    plt.style.use('bmh')
    plt.title("Czas zagrożenia algorytmów w aplikacji")
    plt.xlabel("Numer przypadku testowego")
    plt.ylabel("Czas [s]")
    plt.scatter(x, Czas_zagrożenia_klasyczny, label="Czas zagrożenia - podejście klasyczne", alpha=0.7, s=100, edgecolors="black")
    plt.scatter(x, Czas_zagrożenia_dzewo_decyzyjne, label="Czas zagrożenia - drzewo decyzyjne", alpha=0.7, s=100, edgecolors="black")
    plt.scatter(x, Czas_zagrożenia_algorytm_własny, label="Czas zagrożenia - algorytm autorski", alpha=0.7, s=100, edgecolors="black")
    plt.grid(True)
    plt.legend()
    plt.show()