
# coding: utf-8

#  The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 

# In[41]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()
#app.scripts.config.serve_locally = True
#app.config['suppress_callback_exceptions'] = True

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df= pd.read_csv('gdp_Data.csv')
label= pd.read_csv('gdp_Label.csv',delimiter="\t")

df=df[ ~ df['GEO'].str.contains('European Union')] 
df=df[ ~ df['GEO'].str.contains('Euro area')] 
df = df[df['UNIT'].str.contains('Current prices, million euro')]
df.to_csv('gdp_Data.csv',index=False) 

  
#print(df)
#print(label)

available_indicators1 = df['NA_ITEM'].unique()
available_indicators2 = df['GEO'].unique()         


# In[16]:


app = dash.Dash()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators1],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators1],
                value='Final consumption expenditure'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    )
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()


# The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' [(more here)](https://plot.ly/python/line-charts/) 

# In[15]:


app = dash.Dash(__name__)


app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in available_indicators2],
                value='Belgium'
            ),
            dcc.RadioItems(id='country-type')
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='GDP_indicators',
                options=[{'label': i, 'value': i} for i in available_indicators1],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(id='GDP_indicators-type')
        ],
            style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    

    dcc.Graph(id='graphic2'),])


@app.callback(
    dash.dependencies.Output('graphic2', 'figure'),
    [dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('GDP_indicators', 'value'),
     dash.dependencies.Input('country-type', 'value'),
     dash.dependencies.Input('GDP_indicators-type', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type):
    #dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            #x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            #y=dff[dff['NA_ITEM'] == zaxis_column_name]['Value'],
            #text=dff[dff['NA_ITEM'] == zaxis_column_name]['GEO'],
            x=df['TIME'].unique(),
            y=df[(df['GEO'] == xaxis_column_name) & (df['NA_ITEM'] == yaxis_column_name)]['Value'],
            text=xaxis_column_name,
            mode='lines',
            line ={
                'color' : ('rgb(10, 186, 181)'),
                'shape':'spline'}
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
            },
            yaxis={
                'title': yaxis_column_name,
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()


# * Two gragh in one page

# In[55]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server
app.config['suppress_callback_exceptions'] = True
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df= pd.read_csv('gdp_Data.csv')
#label= pd.read_csv('gdp_Label.csv',delimiter="\t")

df=df[ ~ df['GEO'].str.contains('European Union')] 
df=df[ ~ df['GEO'].str.contains('Euro area')] 
df = df[df['UNIT'].str.contains('Current prices, million euro')]
df.to_csv('gdp_Data.csv',index=False) 

  
#print(df)
#print(label)

available_indicators1 = df['NA_ITEM'].unique()
available_indicators2 = df['GEO'].unique()         

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                value='Linear',
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators1],
                value='Final consumption expenditure'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                value='Linear',
            )
        ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
       
        html.Div([
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in available_indicators2],
                value='Belgium'
            ),
            dcc.RadioItems(id='country-type')
        ],
            style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    

    dcc.Graph(id='indicator-graphic'),
    dcc.Graph(id='graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    )
])



@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' 
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }
@app.callback(
    dash.dependencies.Output('graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('country-type', 'value')])
def update_graph(xaxis_column_name, country_name,
                 xaxis_type, country_type):
    
    return {
        'data': [go.Scatter(
            
            x=df['TIME'].unique(),
            y=df[(df['GEO'] == country_name) & (df['NA_ITEM'] == xaxis_column_name)]['Value'],
            mode='lines',
            line = dict(color = ('rgb(205, 12, 24)'),
                        width = 4)
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
            },
            yaxis={
                'title': country_name,
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()

