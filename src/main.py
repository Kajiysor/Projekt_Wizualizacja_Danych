import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas
import zipfile
import os
import re
import json
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from bs4 import BeautifulSoup


def compare_income() -> go.Figure:
    porownanie_srednich_woj_inf = pd.read_csv(
        '../data/wojewodztwa_srednia.csv', encoding='utf-8')

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=porownanie_srednich_woj_inf['wojewodztwo'],
        y=porownanie_srednich_woj_inf['srednie_zarobki_wojewodztwo'],
        histfunc="sum",
        # name used in legend and hover labels
        name='Średnia krajowa w danym województwie',
        marker_color='#EB89B5',
        opacity=0.75
    ))
    fig.add_trace(go.Histogram(
        x=porownanie_srednich_woj_inf['wojewodztwo'],
        y=porownanie_srednich_woj_inf['srednie_zarobki_inf'],
        histfunc="sum",
        # name used in legend and hover labels
        name='Średnie zarobki informatyków w danym województwie',
        marker_color='#330C73',
        opacity=0.75
    ))

    fig.update_layout(
        title_text='Porównanie średnich zarobków w danych województwach',  # title of plot
        yaxis_title_text='Zarobki [zł]',  # yaxis label
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1  # gap between bars of the same location coordinates
    )

    return fig


def compare_languages_pop() -> go.Figure:
    df_jezyki = pd.read_csv("../data/zbior_jezyki_zdalnie.csv")
    df_jezyki["ilosc_ofert"] = df_jezyki.zdalnieT + df_jezyki.zdalnieN
    return px.pie(df_jezyki, values='ilosc_ofert', names="jezyk")


def compare_offers_remote() -> go.Figure:
    df_jezyki = pd.read_csv("../data/zbior_jezyki_zdalnie.csv")
    df_jezyki["ilosc_ofert"] = df_jezyki.zdalnieT + df_jezyki.zdalnieN
    labels = ["Zdalnie", "Stacjonarnie"]
    values = [df_jezyki.sum()["zdalnieT"], df_jezyki.sum()["zdalnieN"]]
    return go.Figure(data=[go.Pie(labels=labels, values=values)])


def offers_amt_poland() -> go.Figure:
    with open("../data/wojewodztwa-medium.geojson") as pl_geojson:
        pl_woj_json = json.load(pl_geojson)

    df_woj_amt = pd.read_csv(
        "../data/wojewodztwa_ilosc_ofert.csv", index_col=0)
    fig = px.choropleth_mapbox(df_woj_amt, geojson=pl_woj_json,
                               locations=df_woj_amt.index, featureidkey="properties.nazwa",
                               mapbox_style="open-street-map", color='ilosc',
                               center={"lat": 52.2248, "lon": 19.3120}, zoom=4.85)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


def offers_salary_poland() -> go.Figure:
    with open("../data/wojewodztwa-medium.geojson") as pl_geojson:
        pl_woj_json = json.load(pl_geojson)

    df_woj_mean = pd.read_csv(
        "../data/wojewodztwa_srednie_zarobki.csv", index_col=0)

    fig = px.choropleth_mapbox(df_woj_mean, geojson=pl_woj_json,
                               locations=df_woj_mean.index, featureidkey="properties.nazwa",
                               mapbox_style="open-street-map", color='srednie_zarobki',
                               center={"lat": 52.2248, "lon": 19.3120}, zoom=4.85)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


if __name__ == "__main__":
    pass
