import pandas as pd
import pickle
from scipy.stats import norm
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import train_test_split
from sklearn import tree
from statistics import mean



class time_algorithms():
    def __init__(self) -> None:
        self.parameter_b = 2.63
        self.decision_tree_model = pickle.load(open('models/tree.pickle', 'rb'))
        self.gaus_model_reg = pickle.load(open('models/gaus_reg.pickle', 'rb'))
        self.gaus_model_ogr = pickle.load(open('models/gaus_ogr.pickle', 'rb'))

    def predict_crossing_time_tree(self, pedestrian_group):
        if pedestrian_group == [0,0,0,0]:
            return 14
        pedestrian_group = np.array(pedestrian_group)
        pedestrian_group = pedestrian_group.reshape(1, -1)
        czas_potrzebny_na_przejscie = self.decision_tree_model.predict(pedestrian_group)
        return czas_potrzebny_na_przejscie
    
    def predict_crossing_time_gaus(self, pedestrians):
        wyniki = []
        for i in range(500):
            liczba_przechodniow_reguralnych = pedestrians[0] + pedestrians[2]
            liczba_przechodniow_o_ogr_mob = pedestrians[1] + pedestrians[3]

            czasy = []

            for i in range(liczba_przechodniow_reguralnych):
                czasy.append(self.gaus_model_reg.sample()[0][0])
            for i in range(liczba_przechodniow_o_ogr_mob):
                czasy.append(self.gaus_model_ogr.sample()[0][0])
            if czasy:
                czas_potrzebny_na_przejscie = max(czasy) + self.parameter_b
            else:
                czas_potrzebny_na_przejscie = 14
            wyniki.append(czas_potrzebny_na_przejscie[0])
        wynik_koncowy = mean(wyniki)
        return wynik_koncowy
