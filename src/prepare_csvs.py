import numpy as np
import pandas as pd
import math
from collections import Counter
from bs4 import BeautifulSoup

if __name__ == "__main__":

    data = pd.read_csv("combined_data.csv")
    data.drop(columns=["zarobki", "Unnamed: 0"], inplace=True)
    data.drop(data[data.zarobki_min == "Brak danych"].index, inplace=True)
    lista_miast = []
    for miasta in data.miasto.to_list():
        if ("+" in miasta):
            lista_miast.append(miasta.split(
                "+")[0].split(",")[0].strip().upper())
        elif "," in miasta:
            for miasto in miasta.split(","):
                lista_miast.append(miasto.strip().upper())
        elif (miasta == "Nie podano"):
            pass
        else:
            lista_miast.append(miasta.upper())
    for miasto in lista_miast:
        if "SUCHY LAS" in miasto:
            lista_miast.remove(miasto)
            lista_miast.append("Poznań".upper())
        if "WARSAW" in miasto:
            lista_miast.remove(miasto)
            lista_miast.append("WARSZAWA")

    zbior_miast = set(lista_miast)
    offers_per_city = Counter(lista_miast)

    with open("miasta.html") as miasta:
        soup = BeautifulSoup(miasta, "html.parser")

    role = soup.find_all("tr", {"role": "row"})

    lista_miast = []
    for i in range(1, len(role)):
        dict = {"miasto": role[i].find_all("a")[0].text.strip().upper(
        ), "wojewodztwo": role[i].find_all("a")[2].text.strip().upper()}
        lista_miast.append(dict)

    df_woj = pd.DataFrame(lista_miast)
    df_woj['ilosc'] = 0

    for miasto in offers_per_city.keys():
        df_woj.loc[df_woj['miasto'] == miasto,
                   'ilosc'] = offers_per_city.get(miasto)

    df_woj = df_woj.drop(df_woj[df_woj.ilosc == 0].index)
    df_woj_amt = df_woj.drop(columns="miasto")
    df_woj_amt = df_woj_amt.groupby('wojewodztwo').sum()
    df_woj_amt.index = df_woj_amt.index.str.lower()
    df_woj_amt.sort_values('ilosc', ascending=True, inplace=True)

    df_woj_amt.to_csv("data/wojewodztwa_ilosc_ofert.csv")
##################################################################
    data2 = pd.read_csv("combined_data_with_average_salary.csv")
    data2 = data2.drop(columns=["Unnamed: 0"])

    lista_miast2 = []

    for i in range(0, len(data2)):
        miasta = data2.iloc[i].get('miasto')
        zarobki_srednie = data2.iloc[i].get('zarobki_srednie')

        if ("+" in miasta):
            lista_miast2.append(miasta.split(
                "+")[0].split(",")[0].strip().upper())
            lista_miast2.append(zarobki_srednie)
        elif "," in miasta:
            for miasto in miasta.split(","):
                lista_miast2.append(miasto.strip().upper())
                lista_miast2.append(zarobki_srednie)
        elif (miasta == "Nie podano"):
            pass

        else:
            lista_miast2.append(miasta.upper())
            lista_miast2.append(zarobki_srednie)

    dict_city_amt = {}
    for miasto, ilosc in offers_per_city.items():
        dict_city_amt[miasto] = ilosc

    dict_city_sum = {}
    for miasto, ilosc in offers_per_city.items():
        dict_city_sum[miasto] = 0.0

    for i in range(0, 14140):
        if(i % 2 == 0):
            if dict_city_amt.get(lista_miast2[i]) is not None:
                if np.isnan(lista_miast2[i+1]) == False:
                    dict_city_sum[lista_miast2[i]] += lista_miast2[i+1]

    dict_city_mean = {}
    for miasto, ilosc in offers_per_city.items():
        dict_city_mean[miasto] = 0.0

    for miasto in zbior_miast:
        dict_city_mean[miasto] = math.ceil(
            dict_city_sum.get(miasto) / dict_city_amt.get(miasto))

    df_woj_mean = pd.DataFrame(lista_miast)

    df_woj_mean['srednie_zarobki'] = 0
    for miasto in dict_city_mean.keys():
        df_woj_mean.loc[df_woj_mean['miasto'] == miasto,
                        'srednie_zarobki'] = dict_city_mean.get(miasto)

    df_woj_mean = df_woj_mean.drop(
        df_woj_mean[df_woj_mean['srednie_zarobki'] == 0].index)
    df_woj_mean = df_woj_mean.drop(columns='miasto')
    df_woj_mean = df_woj_mean.groupby('wojewodztwo').mean()

    df_woj_mean.index = df_woj_mean.index.str.lower()
    df_woj_mean.sort_values('srednie_zarobki', ascending=True, inplace=True)

    df_woj_mean.to_csv("data/wojewodztwa_srednie_zarobki.csv")
