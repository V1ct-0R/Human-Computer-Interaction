# !usr/bin/env python 
# -*- coding:utf-8 _*-

# 通用的绘制图形函数
import plotly.graph_objs as go


# 散点图
def draw_scatter(x_values, x_title, y_values, y_title, text, title):
    return {
        'data': [go.Scatter(
            x=x_values,
            y=y_values,
            text=text,
            mode="markers",
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {
                    'width': 0.5,
                    'color': 'white'
                },
                'color': 'green'
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': x_title
            },
            yaxis={
                'title': y_title
            },
            title=title,
            margin={
                'l': 130,
                'r': 40,
                't': 50,
                'b': 50
            },
            height=500,
            hovermode='closest'
        )
    }


# 折线图
def draw_line(x_values, x_title, y_values, y_title, title):
    return {
        'data': [{
            'x': x_values,
            'y': y_values,
            'mode': 'lines+markers',
            'type': 'Scatter',
            'name': 'Line',
            'line': dict(color='"rgb(153,204,102)"')
        }],
        'layout': go.Layout(
            xaxis={
                'title': x_title
            },
            yaxis={
                'title': y_title
            },
            title=title,
            margin={
                'l': 130,
                'r': 40,
                't': 50,
                'b': 50
            },
            height=500,
            hovermode='closest'
        )
    }


# 柱状图
def draw_bar(x_values, x_title, y_values, y_title, title):
    return {
        'data': [go.Bar(
            x=x_values,
            y=y_values,
            marker=dict(color="rgb(153,204,102)")
        )],
        'layout': go.Layout(
            xaxis={
                'title': x_title
            },
            yaxis={
                'title': y_title
            },
            title=title,
            margin={
                'l': 130,
                'r': 40,
                't': 50,
                'b': 50
            },
            height=500,
            hovermode='closest'
        )
    }


# 饼状图
def draw_pie(label_list, value_list):
    return {
        'data': [go.Pie(
            labels=label_list,
            values=value_list,
            marker=dict(colors=["rgb(153,204,102)"])
        )],
        'layout': go.Layout(
            margin={
                'l': 130,
                'r': 0,
                't': 50,
                'b': 30
            },
            height=300,
            hovermode='closest'
        )
    }
