import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output
from dash.dependencies import Input, Output


app = dash.Dash()

app.layout = html.Div(children=[
    html.Header(children=[
        html.Div(children=[
            html.Div(children=[
                html.H1(children=[
                    'Praca Programisty w Polsce'
                ])
            ]),

        ]),
        html.Nav(children=dcc.RadioItems(
            ['Porównanie Zarobków', 'Popularność Języków',
             'Oferty Zdalne', 'Ilość Ofert w Polsce',
             'Zarobki w Polsce'],
            'Porównanie Zarobków',
            id='graph_select'
        )
        )
    ]),
    html.Main(children=[
        dcc.Graph(id='graph'),
    ]),
    html.Section()
])


@ app.callback(
    Output(component_id="graph", component_property="figure"),
    Input('graph_select', 'value')
)
def display_graph(selected_graph):
    match selected_graph:
        case 'Porównanie Zarobków':
            return compare_income()
        case 'Popularność Języków':
            return compare_languages_pop()
        case 'Oferty Zdalne':
            return compare_offers_remote()
        case 'Ilość Ofert w Polsce':
            return offers_amt_poland()
        case 'Zarobki w Polsce':
            return offers_salary_poland()


def compare_income() -> go.Figure:
    porownanie_srednich_woj_inf = pd.read_csv(
        '../data/wojewodztwa_srednia.csv', encoding='utf-8')

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=porownanie_srednich_woj_inf['wojewodztwo'],
        y=porownanie_srednich_woj_inf['srednie_zarobki_wojewodztwo'],
        histfunc="sum",
        name='Średnia krajowa w danym województwie',
        marker_color='#fde65a',
        opacity=0.90
    ))
    fig.add_trace(go.Histogram(
        x=porownanie_srednich_woj_inf['wojewodztwo'],
        y=porownanie_srednich_woj_inf['srednie_zarobki_inf'],
        histfunc="sum",
        name='Średnie zarobki informatyków w danym województwie',
        marker_color='#551ebc',
        opacity=0.90
    ))

    fig.update_layout(
        title_text='Porównanie średnich zarobków w danych województwach',
        yaxis_title_text='Zarobki [zł]',
        bargap=0.2,
        bargroupgap=0.1,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#cab656'
    )

    return fig


def compare_languages_pop() -> go.Figure:
    df_jezyki = pd.read_csv("../data/zbior_jezyki_zdalnie.csv")
    df_jezyki["ilosc_ofert"] = df_jezyki.zdalnieT + df_jezyki.zdalnieN
    fig = px.pie(df_jezyki, values='ilosc_ofert',
                 names="dziedzina", color_discrete_sequence=px.colors.sequential.thermal)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)', font_color='#cab656')
    fig.update_traces(textposition='inside')
    return fig


def compare_offers_remote() -> go.Figure:
    df_jezyki = pd.read_csv("../data/zbior_jezyki_zdalnie.csv")
    df_jezyki["ilosc_ofert"] = df_jezyki.zdalnieT + df_jezyki.zdalnieN
    labels = ["Praca Zdalna", "Praca Stacjonarna"]
    values = [df_jezyki.sum()["zdalnieT"], df_jezyki.sum()["zdalnieN"]]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=['#fde65a', '#551ebc'])], layout=go.Layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#cab656'))
    fig.update_traces(textinfo='percent+value')
    return fig


def offers_amt_poland() -> go.Figure:
    with open("../data/wojewodztwa-medium.geojson") as pl_geojson:
        pl_woj_json = json.load(pl_geojson)

    df_woj_amt = pd.read_csv(
        "../data/wojewodztwa_ilosc_ofert.csv", index_col=0)
    fig = px.choropleth_mapbox(df_woj_amt, geojson=pl_woj_json,
                               locations=df_woj_amt.index, featureidkey="properties.nazwa",
                               mapbox_style="carto-darkmatter", color='ilosc',
                               center={"lat": 52.2248, "lon": 19.3120}, zoom=4.85, labels={'ilosc': "Ilość Ofert"})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#cab656')
    return fig


def offers_salary_poland() -> go.Figure:
    with open("../data/wojewodztwa-medium.geojson") as pl_geojson:
        pl_woj_json = json.load(pl_geojson)

    df_woj_mean = pd.read_csv(
        "../data/wojewodztwa_srednie_zarobki.csv", index_col=0)

    fig = px.choropleth_mapbox(df_woj_mean, geojson=pl_woj_json,
                               locations=df_woj_mean.index, featureidkey="properties.nazwa",
                               mapbox_style="carto-darkmatter", color='srednie_zarobki',
                               center={"lat": 52.2248, "lon": 19.3120}, zoom=4.85, labels={'srednie_zarobki': "Średnie Zarobki Brutto"})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#cab656')
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
