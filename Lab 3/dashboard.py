# !usr/bin/env python
# -*- coding:utf-8 _*-

import dash
from dash import Dash, dcc, html
import pandas as pd
from util import *

app = Dash(__name__)

df = pd.read_csv('dataset/google-play-store-apps/googleplaystore.csv', encoding="ISO-8859-1")
df.dropna(inplace=True)

# 数据预处理
category_list = df['Category'].unique()
rating_list = df['Content Rating'].unique()
type_list = ['Free', 'Paid']

# 组件样式
dropdown_css = {
    'width': '40%',
    'display': 'inline-block',
    'padding': '10px 50px',
    'margin-top': '2%'
}
graph_css = {
    'width': '40%',
    'display': 'inline-block',
    'margin-top': '1%'
}
radio_css = {
    'padding': '10px 50px',
    'margin': '0 auto',
    'margin-bottom': '1%'
}
pie_css = {
    'width': '50%',
    'margin-top': '2%'
}

app.layout = html.Div([
    html.H1(
        children='Reviews on google play store apps',
        style={
            'textAlign': 'center'
        }
    ),

    html.Div([

        html.Div([
            dcc.Graph(
                id='rating-graph'
            )
        ], style=pie_css),

        html.Div([
            dcc.Dropdown(
                id='Category',
                options=[{'label': i, 'value': i} for i in category_list],
                value=category_list[0]
            )
        ], style=dropdown_css),

        html.Div([
            dcc.Dropdown(
                id='Type',
                options=[{'label': i, 'value': i} for i in type_list],
                value=type_list[0]
            )
        ], style=dropdown_css)

    ]),

    html.Div([
        dcc.RadioItems(
            id='rating-radio',
            options=[{'label': i, 'value': i} for i in rating_list],
            value=rating_list[0],
            labelStyle={'padding': '0 20px', 'display': 'inline-block'}
        )
    ], style=radio_css),

    html.Div([

        html.Div([
            dcc.Graph(
                id='installs-rating',
                animate=True
            )
        ], style=graph_css),

        html.Div([
            dcc.Graph(
                id='reviews-rating',
                animate=True
            )
        ], style=graph_css),

        html.Div([
            dcc.Graph(
                id='reviews-installs',
                animate=True
            )
        ], style=graph_css),

        html.Div([
            dcc.Graph(
                id='installs-size',
                animate=True
            )
        ], style=graph_css)

    ])

])


@app.callback(
    dash.dependencies.Output('rating-graph', 'figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value')
    ]
)
def refresh_pie(category, type_):
    dff = df[(df['Category'] == category) & (df['Type'] == type_)]

    label_list = list(rating_list)
    value_list = [0 for _ in range(len(label_list))]

    for index, row in dff.iterrows():
        value_list[label_list.index(row[8])] += 1

    return draw_pie(label_list, value_list)


@app.callback(
    dash.dependencies.Output('installs-rating', 'figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value'),
        dash.dependencies.Input('rating-radio', 'value')
    ]
)
def refresh_installs_rating(category, type_, radio):
    dff = df[(df['Category'] == category) & (df['Type'] == type_) & (df['Content Rating'] == radio)]

    installs = [0, 0, 0, 0, 0, 0]
    ratings = ['0~1', '1~2', '2~3', '3~4', '4~5', '5+']

    for index, row in dff.iterrows():
        installs[int(float(row['Rating']))] += int(row['Installs'][:-1].replace(",", ""))

    return draw_bar(ratings, 'Rating', installs, 'Installs', 'Installs-Rating Diagram (Bar)')


@app.callback(
    dash.dependencies.Output('reviews-rating', 'figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value'),
        dash.dependencies.Input('rating-radio', 'value')
    ]
)
def refresh_reviews_rating(category, type_, radio):
    dff = df[(df['Category'] == category) & (df['Type'] == type_) & (df['Content Rating'] == radio)]

    reviews = [0, 0, 0, 0, 0, 0]
    ratings = ['0~1', '1~2', '2~3', '3~4', '4~5', '5+']

    for index, row in dff.iterrows():
        reviews[int(float(row['Rating']))] += int(row['Reviews'])

    return draw_bar(ratings, 'Rating', reviews, 'Reviews', 'Reviews-Rating Diagram (Bar)')


@app.callback(
    dash.dependencies.Output('reviews-installs', 'figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value'),
        dash.dependencies.Input('rating-radio', 'value')
    ]
)
def refresh_reviews_installs(category, type_, radio):
    dff = df[(df['Category'] == category) & (df['Type'] == type_) & (df['Content Rating'] == radio)]

    reviews, installs, names = [], [], []

    for index, row in dff.iterrows():
        reviews.append(row['Reviews'])
        installs.append(row['Installs'])
        names.append(row['App'])

    return draw_scatter(installs, 'Installs', reviews, 'Reviews', names, 'Reviews-Installs Diagram (Scatter)')


@app.callback(
    dash.dependencies.Output('installs-size', 'figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value'),
        dash.dependencies.Input('rating-radio', 'value')
    ]
)
def refresh_installs_size(category, type_, radio):
    dff = df[(df['Category'] == category) & (df['Type'] == type_) & (df['Content Rating'] == radio)]

    installs = [0, 0, 0, 0, 0, 0, 0, 0]
    sizes = [
        '0~300k', '300k~600k', '600k~900k', '900k~25m', '25m~50m',
        '50m~75m', '75m~100m', 'Varies with device'
    ]

    for index, row in dff.iterrows():
        if row['Size'] == 'Varies with device':
            installs[-1] += int(row['Installs'][:-1].replace(",", ""))

        else:
            tmp = float(row['Size'][:-1])
            i = int(tmp // 300) if row['Size'][-1] == 'k' else int(tmp // 25) + 3
            installs[i] += int(row['Installs'][:-1].replace(",", ""))

    return draw_line(sizes, 'Size', installs, 'Installs', 'Installs-Size Diagram (Line)')


if __name__ == '__main__':
    app.run_server()
