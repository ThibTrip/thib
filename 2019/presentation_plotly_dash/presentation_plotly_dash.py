#!/usr/bin/env python
# coding: utf-8

# # Data visualization and web apps with Dash
# 
# ![Dash example](https://user-images.githubusercontent.com/1280389/30086123-97c58bde-9267-11e7-98a0-7f626de5199a.gif)
# 
# _Example dash app found on https://github.com/plotly/dash_

# # My quest for the ideal data vizualization software

# ## How I discovered Dash
# 
# I have had to produce quite complex charts for my work. I have mostly used Tableau for it and became fed up with it.
# This is why I have come up with a checklist of conditions that I tested against many other vizualization software.

# - [ ] no messing around with CSS, HTML or Javascript or any IT tool which would consume 90% of my time (I'm exaggerating a bit)
# - [ ] interactivity (dynamic data selection and transformation via the use of buttons e.g. a date range)
# - [ ] programmatic or at least very reusable
# - [ ] stable!!
# - [ ] some basic charts available: bar, pie, map, treemap...
# - [ ] dashboarding (multiple charts on the same page)
# - [ ] charts crossfiltering which means filtering a chart by clicking/interacting with another one (this is a rare option)
# - [ ] quick to use
# - [ ] can read from PostgreSQL
# - [ ] bonus: free and open-source

# ### Non programmatic solutions
# 
# Although [Tableau](https://www.tableau.com/fr-fr) ticks all boxes except being free and open source (also the reusable part does not work so well), I have found it to be slow, not reusable, as well as not flexible and stable enough. It is also hard to document your work with it.
# 
# I tested [Metabase](https://github.com/metabase/metabase) a little a while ago and found it really great. However it does not support charts crossfiltering (as of 2019-07-09 at least).
# 
# [Microsoft PowerBI](https://powerbi.microsoft.com) seems to tick all the boxes except for beeing free and open source. I have very limited knowledge of it but my colleagues have shown me very cool dashboards.

# ### Programmatic solutions
# 
# I have found nothing as complete and easy as **Dash + Plotly** in the programmatic world. Other solutions I have researched included bokeh, Python + JSON + HTML + CSS + D3 (this is too much work...), altair and some others I forgot.
# 
# Perhaps R Shiny would also fit but then you have to learn R obviously...
# 
# We will see the advantages and disadvantages of using Dash with the examples through the presentation.

# ## Some dashboard examples using Dash

# In[ ]:


get_ipython().run_line_magic('run', 'crossfilter_hover.py')


# In[ ]:


get_ipython().run_line_magic('run', 'dual_axis_multitype_chart.py')


# # More infos on Dash and Plotly
# 
# <cite>Dash is a Python framework for building analytical web applications. No JavaScript required.</cite>
# 
# <cite>Plotly's team maintains the fastest growing open-source visualization libraries for R, Python, and JavaScript.</cite>
# 
# * Dash is made by the company Plotly
# * You can integrate Plotly charts in a Dash app (as shown in the gif below)
# * Dash is used to create an app layout (buttons, dropdowns, text, charts in combination with plotly, ...) and manage user interactions
# * Dash is based (amongst other) on Flask

# # Dash and Plotly crash course
# 
# This is a very very quick tutorial to demonstrate how Dash works. If you want to know more you should definitely check out the [official tutorial](https://dash.plot.ly/) which is quite well made.

# ## Installing dash
# ```
# pip install dash
# pip install dash_core_components
# pip install dash_html_components
# pip install dash_table
# ```
# 
# or with conda:
# 
# ```
# conda install -c conda-forge dash
# conda install -c conda-forge dash-core-components
# conda install -c conda-forge dash-html-components
# conda install -c conda-forge dash-table
# ```
# 
# * dash contains the Dash class (object where you will put all your app layout and interactions and with which you'll run the app)
# * dash_core_components is for constructing dash specific components such as markdown
# * dash_html_components is for constructing html elements such as inputs
# * dash_table is for displaying tables

# ## Installing plotly
# ```
# pip install plotly
# ```
# 
# or with conda:
# 
# ```
# conda install -c plotly
# ```

# ## Let's make "hello world" in Dash
# 
# This will show you how to:
# * create a Dash app
# * create the layout of a Dash app
# * run the app

# In[ ]:


import dash
import dash_core_components as dcc # this is a convention
import dash_html_components as html # this is also a convention

# a dash.Dash instance is usally named app
app = dash.Dash('hello_world_app') # give a name to your application (you can also use __name__)

# prepare the layout to put in app
title = html.H1('Hello world') # the first argument is always "children". children can also be list like. 
# title = dcc.Markdown('# Hello world') will produce the same results
layout = html.Div(title)

# add the layout to the app
app.layout = html.Div(layout)

# if you are running the script directly and not from an import then run the app
if __name__ == '__main__':
    app.run_server(debug=False)  # debug must be False for Jupyter Notebooks


# ## How to add user interactions to a Dash app
# 
# Example of a button generating a random number

# In[ ]:


import random

import dash
import dash_core_components as dcc
import dash_html_components as html

# imports for callbacks
from dash.dependencies import Output,Input,State
from dash.exceptions import PreventUpdate

# create app object
app = dash.Dash('app_with_callback')

# prepare the layout to put in app
## give ids to the components of your layouts that will be used in the interactions
## (see create the components below)
random_number_button_id = 'button_rd_nb'
display_number_div_id = 'display_number'

## create the components
### button to generate random numbers
random_number_button = html.Button('Show me a random number', # button text
                                   id = random_number_button_id)

### button to display the random number generated by the button
display_number_div = dcc.Markdown(id = display_number_div_id)

## assemble layout
layout = html.Div([random_number_button, display_number_div])

# put the layout in the app
app.layout = layout

# create callback function (display random number when button is clicked)
# I highly recommand puttin your callbacks in functions so that
# you can move them and import them from other modules
def create_generate_random_number_callback(app):
    @app.callback(Output(component_id = display_number_div_id, component_property = 'children'),
                  [Input(random_number_button_id,'n_clicks')])
    def generate_random_number(n_clicks): # matches inputs and states (a State is for collecting information without triggering a callback)
        
        # on app start and page load all callbacks are executed, prevent this by using PreventUpdate (see import for callbacks above)
        if n_clicks is None: # at app start n_clicks is None
            raise PreventUpdate # do not trigger the rest of the callback
            
        return str(random.randint(0,100)) # has to be a string for some reasons

# create callback (puts the callback in the app)
create_generate_random_number_callback(app)

# run the app
if __name__ == '__main__':
    app.run_server(debug=False)


# ## Creating a simple Plotly chart
# 
# Here is the "traditional way" of using plotly.
# 
# You can also use the new plotly express. It can't do as much but it can create complex charts in one line of code. See examples in this [Jupyter notebook](https://nbviewer.jupyter.org/github/plotly/plotly_express/blob/gh-pages/walkthrough.ipynb)

# In[ ]:


import plotly.graph_objects as go # convention
import datetime

# the line below is for plotting in Jupyter Notebook or Lab
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

# get/create data
y = [1,2,4,3]
x = [datetime.date(2019,1,i) for i in range(1,len(y) + 1)]
title = "My fruits consumption"

# create trace(s)
trace = go.Bar(x = x , y = y)

# create layout
layout = go.Layout(title = title, 
                   # format xaxis (note: instead of a dict you can also use a go.layout.XAxis object)
                   xaxis = {'type': 'category', # if you set the type to "date" (seems logical right?) it adds additional irrelevant ticks... 
                                                # this is one of the many annoying things of plotly
                            'tickformat': '%Y-%m-%d', 
                            'title':'Date'},
                   yaxis = {'title':'Number of fruits'})

# put your trace(s) in a figure object
fig = go.Figure(data = [trace], layout = layout)


iplot(fig)


# ## How to put a Plotly chart inside a Dash app and interact with it
# 
# One of the major benefits of Dash is that it uses Python. This means you can use any Python library you want for your app (for the backend at least, since the frontend - so what the user sees - needs to be interpretable by the browser).
# 
# I find this extremely exciting since for instance I can use pandas 🐼 library for data wrangling*. It is extremely powerful and fast. Its main object is the pandas DataFrame (sort of a table object). It also reads from and writes to lots of formats (json, csv, excel, SQL, HDF5, parquet, feather, pickle...).
# 
# I am even using my own libraries in one of my apps (see chapter below "Web applications with Dash").
# 
# Note that in this case all users of the app receive a version of the same data. If you have different data for each user then you will need to manage user's data and it gets a little bit more complicated (we will see an example of it later with my data cleaning app).
# 
# _*means any data operation so aggregating, transforming, cleaning..._

# In[ ]:


import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output,Input,State
from dash.exceptions import PreventUpdate

# read data
data_path = 'https://raw.githubusercontent.com/plotly/datasets/master/dash-stock-ticker-demo.csv'
df = pd.read_csv(data_path).iloc[:,1:] # remove first column in csv it's a standard range index
df['Date'] = pd.to_datetime(df['Date']) # make sure "Date" is recognized as a datetime Series by pandas

# create app object
app = dash.Dash('interactive_chart_app')

# layout ids
dropdown_period_id = 'dropdown_period'
dropdown_stock_id = 'dropdown_stock'
chart_div_id = 'chart'

# create the components
drodpdown_period = dcc.Dropdown(options = [{'label':period,'value':period} for period in ['date','year-month','year']],
                                id = dropdown_period_id,
                                value = 'date') # default option

dropdown_stock = dcc.Dropdown(options = [{'label':stock,'value':stock} for stock in df['Stock'].unique()],
                              id = dropdown_stock_id,
                              multi = True,
                              value = df['Stock'].unique()) # all stocks are selected by default

chart = dcc.Graph(id = chart_div_id) # filled in callback with a plotly figure

# assemble layout and put it in the app
layout = html.Div([drodpdown_period, dropdown_stock, chart])
app.layout = layout

# create callback function to update the DataFrame on user input
def create_update_chart_callback(app):
    @app.callback(Output(chart_div_id, 'figure'),
                  [Input(dropdown_period_id,'value'),
                   Input(dropdown_stock_id,'value')])             
    def update_chart(period, stocks):

        # preprare grouping by the period
        if period == 'date':
            grouper = df['Date'].dt.date
            x_axis_format = {'type': 'category', 'tickformat': '%Y-%m-%d', 'title':'Date'}
        elif period == 'year-month':
            grouper = df['Date'].dt.strftime('%Y-%m') # a list as grouper with [year, month] won't play well with plotly so just format the date
            x_axis_format = {'type': 'category', 'tickformat': '%Y-%m', 'title':'Year-Month'}
        elif period == 'year':
            grouper = df['Date'].dt.year
            x_axis_format = {'type': 'category', 'tickformat': '%Y', 'title':'Year'}
        else:
            raise ValueError(f'Unexpected value for period ({period})')

        # select stock then group by grouper (double the brackets before sum so a DataFrame is always returned and not a Series)
        # IMPORTANT: if you want to modify the original object do a copy before: df.copy(deep = True)
        new_df = (df.loc[df['Stock'].isin(stocks),:]                  .groupby(grouper)[['Volume']].sum()                  .reset_index()) # reset index so we can select 'Date'

        # create a figure
        ## create traces
        traces = [go.Bar(x = new_df['Date'], y = new_df['Volume'])]

        ## create layout
        layout = go.Layout(title = 'Stocks', 
                           # format xaxis (note: instead of a dict you can also use a go.layout.XAxis object)
                           xaxis = x_axis_format,
                           yaxis = {'title':'Volume'})

        fig = go.Figure(data = traces, layout = layout)

        return fig

# create callback (puts the callback in the app)
create_update_chart_callback(app)

# run the app
if __name__ == '__main__':
    app.run_server(debug=False)


# # Web applications with Dash (example with my data cleaning app)

# ## Live demo 
# 
# For people at the presentation in Freiburg only 😉. The code is confidential however I can show this animation of the app below:
# 
# <span style="color:red">_ADD GIF HERE_</span>

# ## Additional libraries used by the data cleaning app
# 
# I highly recommend these libraries!
# 
# ### dash-bootstrap-components
# 
# <cite>[dash-bootstrap-components](https://github.com/facultyai/dash-bootstrap-components) reduces boilerplate by providing standard layouts and high-level components</cite>
# 
# ```
# pip install dash-bootstrap-components
# ```
# 
# or with conda:
# 
# ```
# conda install -c conda-forge dash-bootstrap-components
# 
# ```
# 
# 
# ### dash_database (it's from me 😄)
# 
# This is for managing user data in a Dash app (so for instance sharing data between callbacks). More info and usage can be found in the [repository](https://github.com/ThibTrip/dash_database).
# 
# 
# Installation with:
# 
# ```
# pip install dash-database
# ```

# # Deployment
# 
# Well Andrew T Baker has done a great [video](https://www.youtube.com/watch?v=vGphzPLemZE) on deploying a Python web app at pycon. You should definitely watch it.

# # Other usage examples for Dash
# 
# Here are some other examples of what you could use Dash for.
# 
# * Online forms (my colleagues are interested in making a subscription form with Dash or Flask for newsletter)
# * Webpages or even websites
# * Reports (for instance https://dash-gallery.plotly.host/dash-financial-report/)
