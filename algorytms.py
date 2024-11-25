import pandas as pd
from scipy.stats import norm
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import train_test_split
from sklearn import tree
from scipy.stats import shapiro


def read_xlsx_sheet(file_path, sheet_name):
    """
    Reads the specified sheet from an xlsx file into a pandas DataFrame.

    Args:
        file_path (str): Path to the .xlsx file.
        sheet_name (str): Name of the sheet to read.

    Returns:
        pd.DataFrame: DataFrame containing the data from the specified sheet.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return None


def fit_normal_distribution(data):
    """
    Fits a normal distribution to the given data using Scipy and optionally Sklearn.

    Args:
        data (array-like): Input data to fit.

    Returns:
        dict: A dictionary containing:
              - 'mean': The mean of the fitted normal distribution.
              - 'std': The standard deviation of the fitted normal distribution.
              - 'sklearn_model': A GaussianMixture model fitted to the data (optional).
    """
    # Ensure data is a NumPy array
    data = data.to_numpy()
    data = np.array(data, dtype=float)

    # Fit the normal distribution using Scipy
    mean, std = norm.fit(data)

    res = shapiro(data)
    print("test statystyczny:", res.statistic, res.pvalue)

    # Fit using sklearn GaussianMixture for verification (if required)
    sklearn_model = GaussianMixture(n_components=1, covariance_type="full")
    sklearn_model.fit(data.reshape(-1, 1))  # Reshape data for sklearn input

    return mean, std, sklearn_model


def predict_crossing_time_gaus(pedestrians, data_reg, data_ogr):

    mean_reg, std_reg, model_reg = fit_normal_distribution(data_reg)
    mean_ogr, std_ogr, model_ogr = fit_normal_distribution(data_ogr)

    # print(
    #     f"Wartości rozkładu grupy reguralnej: średnia={mean_reg}, odchylenie={std_reg}"
    # )
    # print(
    #     f"Wartości rozkładu grupy o ograniczonej mobilności: średnia={mean_ogr}, odchylenie={std_ogr}"
    # )

    liczba_przechodniow_reguralnych = pedestrians[0] + pedestrians[2]
    liczba_przechodniow_o_ogr_mob = pedestrians[1] + pedestrians[3]

    czasy = []

    for i in range(liczba_przechodniow_reguralnych):
        czasy.append(model_reg.sample()[0][0])
    for i in range(liczba_przechodniow_o_ogr_mob):
        czasy.append(model_ogr.sample()[0][0])

    czas_potrzebny_na_przejscie = max(czasy) + 2
    return czas_potrzebny_na_przejscie


def predict_crossing_time_tree(pedestrians, X_train, y_train):
    pedestrians = np.array(pedestrians)
    pedestrians = pedestrians.reshape(1, -1)
    clf = tree.DecisionTreeRegressor()
    clf = clf.fit(X_train, y_train)
    czas_potrzebny_na_przejscie = clf.predict(pedestrians)
    return czas_potrzebny_na_przejscie


if __name__ == "__main__":
    file_path = "Dataset.xlsx"
    sheet_name_single_cross = "Jednostkowy czas przejścia"
    sheet_name_group_cross = "Czas przejścia grupy"
    indeks_testowy = 0

    # reading the single crossing time data
    data_single_cross = read_xlsx_sheet(file_path, sheet_name_single_cross)
    czasy_przejscia_single_df = pd.DataFrame()
    czasy_przejscia_single_df["czasy_grupa_regularna"] = data_single_cross[
        "Unnamed: 3"].iloc[1:]
    czasy_przejscia_single_df["czasy_grupa_ograniczonej_mobilności"] = data_single_cross[
        "Unnamed: 6"].iloc[1:]
    
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

    X_train, X_test, y_train, y_test = train_test_split(
        data_group_corss_people, 
        data_group_corss_times, 
        test_size=0.2, 
        random_state=42)
    

    grupa_testowa = X_test[indeks_testowy]
    wynik_testowy = y_test[indeks_testowy]

    print("predykcja dla grupy:", grupa_testowa)
    print("Czas potrzebny na przejście (target):", wynik_testowy)
    print("Czas systemu nie adaptacyjnego:", 14)
    czas_potrzebny_na_przejscie_tree = predict_crossing_time_tree(grupa_testowa, X_train, y_train)
    print("Czas dla drzewa decyzyjnego:", czas_potrzebny_na_przejscie_tree)

    czas_potrzebny_na_przejscie_gaus = predict_crossing_time_gaus(
        grupa_testowa,
        czasy_przejscia_single_df["czasy_grupa_regularna"],
        czasy_przejscia_single_df["czasy_grupa_ograniczonej_mobilności"],
    )
    print("Czas dla dopasowania rozkładu:", czas_potrzebny_na_przejscie_gaus)
