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


def predict_crossing_time_gaus(pedestrians, model_reg, model_ogr, parametr):

    liczba_przechodniow_reguralnych = pedestrians[0] + pedestrians[2]
    liczba_przechodniow_o_ogr_mob = pedestrians[1] + pedestrians[3]

    czasy = []

    for i in range(liczba_przechodniow_reguralnych):
        czasy.append(model_reg.sample()[0][0])
    for i in range(liczba_przechodniow_o_ogr_mob):
        czasy.append(model_ogr.sample()[0][0])

    czas_potrzebny_na_przejscie = max(czasy) + parametr
    return czas_potrzebny_na_przejscie


if __name__ == "__main__":
    file_path = "Dataset.xlsx"
    sheet_name_single_cross = "Jednostkowy czas przejścia"
    sheet_name_group_cross = "Czas przejścia grupy"
    indeks_testowy = 0
    parameter_list = np.arange(2, 3.001, 0.01)
    
    gaus_model_reg = pickle.load(open('models/gaus_reg.pickle', 'rb'))
    gaus_model_ogr = pickle.load(open('models/gaus_ogr.pickle', 'rb'))

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

    average_score_per_parameter = []
    for k in range(len(parameter_list)):
        print("testowanie wartości parametru", parameter_list[k], "to wartość ", k + 1 , "/", len(parameter_list))
        average_score_per_run = []
        for i in range(len(data_group_corss_people)):
            score_per_run = []
            for j in range(200):
                czas_potrzebny_na_przejście = predict_crossing_time_gaus(data_group_corss_people[i], gaus_model_reg, gaus_model_ogr, parameter_list[k])
                score_per_run.append(abs(czas_potrzebny_na_przejście-data_group_corss_times[i])[0])
            average_score_per_run.append(mean(score_per_run))
        average_score_per_parameter.append(mean(average_score_per_run))
    

    pickle.dump(average_score_per_parameter, open('models/parameter_average_error_2_3.pickle', 'wb'))
    plt.style.use('bmh')
    plt.title("Średni błąd bezwzględny w zależności od parametru")
    plt.xlabel("Wartość parametru d")
    plt.ylabel("Wartość błędu bezwzględnego")
    plt.plot(parameter_list, average_score_per_parameter)
    plt.grid(True)
    plt.show()


