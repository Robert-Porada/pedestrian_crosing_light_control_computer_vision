from  src.algorithms_time import time_algorithms

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

def test_classical(y):
    classical_light_time = 14
    times = []
    danger_times = []
    times_predicted = []
    for i in range(len(y)):
        times.append(abs(y[i]-14))
        times_predicted.append(14)
        if classical_light_time + light_blinking_time < y[i]:
            danger_times.append(y[i] - (classical_light_time + light_blinking_time))
        else:
            danger_times.append(0)
    absolute_error_mean = mean(times)
    danger_time_mean = mean(danger_times)
    return absolute_error_mean, danger_time_mean, times, danger_times, times_predicted

def test_tree(x, y):
    times = []
    danger_times = []
    times_predicted = []
    for i in range(len(x)):
        tree_time = algorithms.predict_crossing_time_tree(x[i])
        times_predicted.append(tree_time)
        times.append(abs(y[i]-tree_time)[0])
        if tree_time + light_blinking_time < y[i]:
            danger_times.append(y[i] - (tree_time + light_blinking_time)[0])
        else:
            danger_times.append(0)
    absolute_error_mean = mean(times)
    danger_time_mean = mean(danger_times)
    return absolute_error_mean, danger_time_mean, times, danger_times, times_predicted

def test_gauss(x, y):
    times = []
    times_predicted = []
    times_predicted_each_run = []
    times_each_run = []
    danger_times = []
    danger_times_each_run = []
    for i in range(len(x)):
        times_each_run = []
        danger_times_each_run = []
        times_predicted_each_run = []
        for j in range(1):
            gauss_time = algorithms.predict_crossing_time_gaus(x[i])
            times_predicted_each_run.append(gauss_time)
            times_each_run.append(abs(y[i]-gauss_time))
            if gauss_time + light_blinking_time < y[i]:
                danger_times_each_run.append(y[i] - (gauss_time + light_blinking_time))
            else:
                danger_times_each_run.append(0)
        times.append(mean(times_each_run))
        danger_times.append(mean(danger_times_each_run))
        times_predicted.append(mean(times_predicted_each_run))
    absolute_error_mean = mean(times)
    danger_time_mean = mean(danger_times)
    return absolute_error_mean, danger_time_mean, times, danger_times, times_predicted


if __name__ == "__main__":
    file_path = "Dataset.xlsx"
    sheet_name_single_cross = "Jednostkowy czas przejścia"
    sheet_name_group_cross = "Czas przejścia grupy"
    light_blinking_time = 4
    algorithms = time_algorithms()

    # reading the group crossing data
    data_group_corss = read_xlsx_sheet(file_path, sheet_name_group_cross)
    kolumny_wejsciowe = [
        "Osoby reg. lewa", 
        "Osoby ogr. mob. lewa", 
        "Osoby reg. prawa", 
        "Osoby ogr. mob. prawa"
        ] 
    kolumny_wyjsciowe = "Czas przechodzenia od zielonego"
    data_group_corss_people = data_group_corss[kolumny_wejsciowe].values.tolist()
    data_group_corss_times = data_group_corss[kolumny_wyjsciowe].tolist()

    data_group_corss_people = data_group_corss_people[50:]
    data_group_corss_times = data_group_corss_times[50:]


    class_abs_error, class_danger_time, class_times, class_danger_times, class_times_predicted = test_classical(data_group_corss_times)
    print(f"Classical absolute error average:{class_abs_error:.4f} danger time average:{class_danger_time:.4f}")

    tree_abs_error, tree_danger_time, tree_times, tree_danger_times, tree_times_predicted = test_tree(data_group_corss_people, data_group_corss_times)
    print(f"Tree absolute error average:{tree_abs_error:.4f} danger time average:{tree_danger_time:.4f}")

    gaus_abs_error, gaus_danger_time, gaus_times, gaus_danger_times, gauss_times_predicted = test_gauss(data_group_corss_people, data_group_corss_times)
    print(f"Gauss absolute error average:{gaus_abs_error:.4f} danger time average:{gaus_danger_time:.4f}")


    data_group_corss_times, class_times_predicted, tree_times_predicted, gauss_times_predicted, class_times, tree_times, gaus_times, class_danger_times, tree_danger_times, gaus_danger_times = zip(*sorted(zip(data_group_corss_times, class_times_predicted, tree_times_predicted, gauss_times_predicted, class_times, tree_times, gaus_times, class_danger_times, tree_danger_times, gaus_danger_times)))
    
    
    x = np.arange(15)
    plt.style.use('bmh')
    plt.title("Czasy poszczególnych algorytmów a czas rzeczywisty")
    plt.xlabel("Numer przypadku testowego")
    plt.ylabel("Czas [s]")
    plt.scatter(x, data_group_corss_times, label="Czas potrzebny na przejście", alpha=0.7, s=100, marker="v", edgecolors="black")
    plt.scatter(x, class_times_predicted, label="Predykcja - podejście klasyczne", alpha=0.7, s=100, edgecolors="black")
    plt.scatter(x, tree_times_predicted, label="Predykcja - drzewo decyzyjne", alpha=0.7, s=100, edgecolors="black")
    plt.scatter(x, gauss_times_predicted, label="Predykcja - algorytm autorski", alpha=0.7, s=100, edgecolors="black")
    plt.grid(True)
    plt.legend()
    plt.show()

    x = np.arange(15)
    plt.style.use('bmh')
    plt.title("Błąd bezwzględny poszczególnych algorytmów")
    plt.xlabel("Numer przypadku testowego")
    plt.ylabel("Czas [s]")
    plt.scatter(x, class_times, label="Błąd bezwzględny - podejście klasyczne", alpha=0.7, s=100, edgecolors="black")
    plt.scatter(x, tree_times, label="Błąd bezwzględny - drzewo decyzyjne", alpha=0.7, s=100, edgecolors="black")
    plt.scatter(x, gaus_times, label="Błąd bezwzględny - algorytm autorski", alpha=0.7, s=100, edgecolors="black")
    plt.grid(True)
    plt.legend()
    plt.show()

    x = np.arange(15)
    plt.style.use('bmh')
    plt.title("Czas zagrożenia poszczególnych algorytmów")
    plt.xlabel("Numer przypadku testowego")
    plt.ylabel("Czas [s]")
    plt.scatter(x, class_danger_times, label="Czas zagrożenia - podejście klasyczne", alpha=0.7, s=100, edgecolors="black")
    plt.scatter(x, tree_danger_times, label="Czas zagrożenia - drzewo decyzyjne", alpha=0.7, s=100, edgecolors="black")
    plt.scatter(x, gaus_danger_times, label="Czas zagrożenia - algorytm autorski", alpha=0.7, s=100, edgecolors="black")
    plt.grid(True)
    plt.legend()
    plt.show()

