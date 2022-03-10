import dash
#import dash_core_components as dcc
#import dash_html_components as html
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import pandas as pd


########### Define your variables ######

# here's the list of possible columns to choose from.
list_of_columns =['code', 'state', 'category', 'total exports', 'beef', 'pork', 'poultry',
       'dairy', 'fruits fresh', 'fruits proc', 'total fruits', 'veggies fresh',
       'veggies proc', 'total veggies', 'corn', 'wheat', 'cotton']

mycolumn='fruits fresh'
myheading1 = f"Wow! That's a lot of {list_of_columns}!"
mygraphtitle = 'Interactive 2011 US Agriculture Exports by State'
mycolorscale = 'ylorrd' # Note: The error message will list possible color scales.
mycolorbartitle = "Millions USD"
tabtitle = 'US Agriculture'
sourceurl = 'https://plot.ly/python/choropleth-maps/'
githublink = 'https://github.com/austinlasseter/dash-map-usa-agriculture'


########## Set up the chart

import pandas as pd
df = pd.read_csv('assets/usa-2011-agriculture.csv')

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1(myheading1),
    html.Div([
        html.Div([
                html.H6('Select a commodity of your choosing:'),
                dcc.Dropdown(
                    id='options-drop',
                    options=[{'label': i, 'value': i} for i in list_of_columns],
                    value='fruits fresh'
                ), 
        ], className='two columns'),
        html.Div([dcc.Graph( id='figure-1'),
                 ], className='ten columns'),
    ], className='twelve columns'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)
        
        
########## Define Callback
@app.callback(Output('figure-1', 'figure'),
              [Input('options-drop', 'value')])
def make_figure(mycolumn):
    mygraphtitle= f'Exports of {mycolumn} in 2011'
    mycolorscare= 'ylorrd'  # Note: The error message will list possible color scales.
    mycolorbartitle= 'Millions USD'
    
    fig = go.Figure(data=go.Choropleth(
        locations=df['code'], # Spatial coordinates
        z = df[mycolumn].astype(float), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = mycolorscale,
        colorbar_title = mycolorbartitle,
    ))

    fig.update_layout(
        title_text = mygraphtitle,
        geo_scope='usa',
        width=1200,
        height=800
    )

    
    
    return fig       

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)

    
    