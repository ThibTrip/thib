#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""Source: ThibTrip (using dataset from plotly)"""

import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import numpy as np
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype
import os


# # Load the data

# In[ ]:


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/hello-world-stock.csv').iloc[:,1:] # drop first column
df['Date'] = pd.to_datetime(df['Date'])
df.head()


# # Create the app

# In[ ]:


app = dash.Dash(__name__)


# # Layout

# In[ ]:


# choose date resolution
date_resolution_dropdown = dcc.Dropdown(id='my-dropdown',
                                        options=[{'label': 'years', 'value': 'years'},
                                                 {'label': 'quarters', 'value': 'quarters'},
                                                 {'label': 'months', 'value': 'months'},
                                                 {'label': 'calendar week (monday based, overlapping years)','value':'calendar_weeks_start_monday'},
                                                 {'label': 'days', 'value': 'days'}],
                                        value='months')

# date picker
min_value = df['Date'].min().to_pydatetime()
max_value = df['Date'].max().to_pydatetime()

date_range_picker = dcc.DatePickerRange(id='my-date-picker-range',
                                        min_date_allowed = min_value,
                                        max_date_allowed = max_value,
                                        initial_visible_month = min_value,
                                        with_portal = True,
                                        end_date= max_value)

# create dropdown for choosing stocks
stock_dropdown = dcc.Dropdown(id="multi_dropdown",
                              options= [{'label':value,'value':value} for value in df['Stock'].unique()],
                              value= df['Stock'].unique(),
                              multi=True)

# div for displaying the chart (autofilled within callback)
chart_div = dcc.Graph(id='my-graph')


# assemble layout and add it to the app


app.layout = html.Div([dcc.Markdown('# Stocks'),
                       date_resolution_dropdown,
                       stock_dropdown,
                       date_range_picker,
                       chart_div])


# # Callback

# In[ ]:


@app.callback(Output('my-graph', 'figure'),
              [Input(component_id = 'my-dropdown',component_property = 'value'),
               Input('multi_dropdown','value'),
               Input('my-date-picker-range','start_date'),
               Input('my-date-picker-range','end_date')])


def update_graph(resolution,
                 stocks,
                 selected_start_date,
                 selected_end_date):
      
    # SELECT DATA
    # Select the date range - START WITH THIS, it needs the original data to be able to use to dt. accessor
    # Upon changing the date resolution a conversion to string can indeed occur (e.g. for quarters)
    if selected_start_date is None:
        selected_start_date = df['Date'].min()
        
    new_df = df[(df['Date'] >= pd.Timestamp(selected_start_date)) & 
                (df['Date'] <= pd.Timestamp(selected_end_date))].copy(deep = True) # IMPORTANT: COPY


    # Select the stock    
    new_df = new_df[new_df['Stock'].isin(stocks)]
    
    # AGGREGATE
    # Change date resolution and group
    if resolution == 'years':
        grouper = new_df['Date'].dt.to_period('Y').fillna('').astype(str)
        xaxis_layout = {'type':'category', 'tickformat': '%Y'} # avoids beeing interpreted as a number
        
    elif resolution == 'quarters':
        grouper = new_df['Date'].dt.to_period('Q').fillna('').astype(str)
        xaxis_layout = {'type':'category'}
    
    elif resolution == 'calendar_weeks_start_monday':
        grouper = new_df['Date'].dt.to_period('W').apply(lambda r: r.start_time)
        xaxis_layout = {'tickformat':'%Y%W'}
    
    elif resolution == 'days':
        grouper = new_df['Date'].dt.to_period('D').dt.to_timestamp()
        xaxis_layout = {'tickformat':'%d.%m.%Y'}
        
    elif resolution == 'months':
        grouper = new_df['Date'].dt.to_period('M').dt.to_timestamp()
        xaxis_layout = {'tickformat':'%Y-%m'}
    
    else:
        raise ValueError(f'Unexpected date resolution ({resolution})')
        
    new_df = new_df.groupby(grouper)[['Low','High','Volume']].sum().reset_index()
        
    # Prepare data for the graph
    data = [{'x': new_df['Date'],
             'y': new_df['Volume'], 
             'name':'volume',
             'type':'bar'},
            
            {'x': new_df['Date'],
             'y': new_df['Low'],
             'yaxis':'y2', # dual axis 
             'name':'low',
             'line': {'width': 3,
                      'shape': 'spline'}},
            
            {'x': new_df['Date'],
             'y': new_df['High'],
             'yaxis':'y2', # dual axis 
             'name':'high',
             'line': {'width': 3,
                      'shape': 'spline'}}]
    
    graph = {'data': data,
             'layout': {'margin': {'l': 30,
                                   'r': 20,
                                   'b': 30,
                                   't': 20},
                        'yaxis2':{'overlaying':'y',
                                  'anchor':'x',
                                  'side':'right',
                                  'showgrid':False},
                                                
                        'xaxis': xaxis_layout}}

    return graph


# # Launch the app

# In[ ]:


if __name__ == '__main__':
    app.run_server()

