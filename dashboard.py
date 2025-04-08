import pandas as pd
import plotly.express as px
from data_processing import DataAnalyzer



def make_line_chart(input_data, x, y, title, x_title, y_title, color=None):
    fig = px.line(input_data, x=x, y=y, title=title, color=color)
    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        showlegend=True
    )
    return fig

def make_bar_chart(input_data, x, y, title, x_title, y_title, color=None):
    fig = px.bar(input_data, x=x, y=y, title=title, color=color)
    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        showlegend=True
    )
    return fig

def make_pie_chart(input_data, labels, values, title, color=None):
    fig = px.pie(input_data, labels, values, title=title)
    fig.update_layout(
        xaxis_title='ads',
        yaxis_title='asd',
        showlegend=True
    )
    return fig
    





from dash import Dash, dcc, html, Input, Output, callback

# Initialize the Dash app
app = Dash(__name__)
data_analyzer = DataAnalyzer('games.csv', 'genres.csv', 'themes.csv', 'platforms.csv', 'game_engines.csv')

# # Define the layout
app.layout = html.Div([
    html.H1("Trends Over the Years"),
    dcc.Dropdown(
        id='category-dropdown',
        options=[
            {'label': 'Number of Games Per Year', 'value': 'game_num'},
            {'label': 'Number of Games for each genre Per Year', 'value': 'genre'},
            {'label': 'Number of Games for each theme Per Year', 'value': 'theme'}

        ],
        value='genre',
        style={'width': '50%'}
    ),
    dcc.Graph(id='trend-graph'),
        html.H1("Bar Charts"),
    dcc.Dropdown(
        id='bar-dropdown',
        options=[
            {'label': 'Number of games per month', 'value': 'months'},

        ],
        value='months',
        style={'width': '50%'}
    ),
    dcc.Graph(id='bar-graph'),

            html.H1("Pie Charts"),
    dcc.Dropdown(
        id='pie-dropdown',
        options=[
            {'label': 'Platform Distribution', 'value': 'platforms'},
            {'label': 'Game Engine Distribution', 'value': 'game_engines'}

        ],
        value='platforms',
        style={'width': '50%'}
    ),
    dcc.Graph(id='pie-graph'),
])




# Callback to update graph based on dropdown
@callback(
    Output('trend-graph', 'figure'),
    Input('category-dropdown', 'value')
)
def update_graph(category):
    print("lalalala")
    color = None
    if category == 'game_num':
        data = data_analyzer.count_games_per_year()
        title = 'Trend of Games Over the Years'
        x_title = 'Year'
        y_title = 'Number of Games'
        x = 'year'
        y = 'num_games'
        fig = make_line_chart(data, x, y, title, x_title, y_title, color)

    elif category == 'genre':
        x_title = 'release_year'
        y_title = 'num_games'
        title = 'Trend of Games by Genre Over the Years'
        data = data_analyzer.count_genre_games_per_year()
        color = 'genre_name'
        x = 'release_year'
        y = 'num_games'
        fig = make_line_chart(data, x, y, title, x_title, y_title, color)

    elif category == 'theme':
        x_title = 'release_year'
        y_title = 'num_games'
        title = 'Trend of Games by Theme Over the Years'
        data = data_analyzer.count_theme_games_per_year()
        color = 'theme_name'
        x = 'release_year'
        y = 'num_games'
        fig = make_line_chart(data, x, y, title, x_title, y_title, color)
    else:
        return
    
    return fig

# Callback to update graph based on dropdown
@callback(
    Output('bar-graph', 'figure'),
    Input('bar-dropdown', 'value')
)
def update_graph(category):
    print("bar drop down")
    if category == 'months':
        x_title = 'release_month'
        y_title = 'Number of Games'
        title = 'Number of Games Per Month'
        data = data_analyzer.count_games_per_month()
        color = None
        x = 'month_name'
        y = 'num_games'
        fig = make_bar_chart(data, x, y, title, x_title, y_title, color)

    else:
        return

    return fig



# Callback to update graph based on dropdown
@callback(
    Output('pie-graph', 'figure'),
    Input('pie-dropdown', 'value')
)
def update_graph(category):
    print("pie drop down")
    if category == 'platforms':

        title = 'Platform Distribution'
        data = data_analyzer.count_platforms()
        color = None
        fig = make_pie_chart(data, labels = data['name'], values = data['count'], title= title, color=color)
    elif category == 'game_engines':
        title = 'Game Engine Distribution'
        data = data_analyzer.count_game_engines()
        color = None
        fig = make_pie_chart(data, labels = data['name'], values = data['count'], title= title, color=color)

    else:
        return

    return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True)