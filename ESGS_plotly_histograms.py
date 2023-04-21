#!/usr/bin/env python
# coding: utf-8

# In[2]:


# mount google drive
# from google.colab import drive
# drive.mount('/content/drive')

# change to our working directory
# %cd /content/drive/MyDrive/GSDC


# In[3]:


#!pip install plotly


# In[4]:


import plotly.graph_objs as go
import plotly.io as pio


# In[5]:

import pandas as pd
url = 'https://raw.githubusercontent.com/Yingtong-Z/green-space-index-dash-app/73dcb28a2a33375380e501af417d8eaf5305d0b7/merge_final2.csv'
df = pd.read_csv(url, encoding='latin')
#df = pd.read_csv('/Users/angel_zhong/Documents/GitHub/green-space-dash-app/merge_final2.csv')
df['state_county'] = df.COUNTY + ', ' + df.STATE
df


# In[6]:


fitness_cols = ['1kAccessibleParks', 'Access_to_exercise_opportunities_raw_value_2021']
greenery_cols = ['RISK_SCORE', 'Share_of_the_tract_s_land_area_that_is_covered_by_impervious_2', 
        'NDVI_summertime_max', 'Tree_canopy_cover', 'Public_park_cover']
wellness_cols = ['Life_expectancy_raw_value_2021', 'Adult_smoking_raw_value_2021', 
        'Excessive_drinking_raw_value_2021', 'Uninsured_raw_value_2021', 'Adult_obesity_raw_value_2021']
county = ['state_county']
selected_cols2 = county+fitness_cols+greenery_cols+wellness_cols
df_use = df[selected_cols2]
df_use


# In[7]:


df_use.columns


# In[8]:


column_mapping = {
    '1kAccessibleParks': 'Accessible parks',
    'Access_to_exercise_opportunities_raw_value_2021': 'Access to exercise opportunities',
    'RISK_SCORE': 'Natural Hazard risk',
    'Share_of_the_tract_s_land_area_that_is_covered_by_impervious_2': 'Imperious surface',
    'NDVI_summertime_max': 'NDVI summertime max',
    'Tree_canopy_cover': 'Tree canopy cover',
    'Public_park_cover': 'Public park cover',
    'Life_expectancy_raw_value_2021': 'Life expectancy',
    'Adult_smoking_raw_value_2021': 'Smoking',
    'Excessive_drinking_raw_value_2021': 'Excessive drinking',
    'Adult_obesity_raw_value_2021': 'Obesity',
    'Uninsured_raw_value_2021': 'Uninsured individuals'
}

df_use = df_use.rename(columns=column_mapping)

selected_cols = [
    'Accessible parks',
    'Access to exercise opportunities',
    'Natural Hazard risk',
    'Imperious surface',
    'NDVI summertime max',
    'Tree canopy cover',
    'Public park cover',
    'Life expectancy',
    'Smoking',
    'Excessive drinking',
    'Obesity',
    'Uninsured individuals'
]

df_use.head()


# In[9]:


# mean_values = df_use.mean()
# df3 = pd.DataFrame(mean_values).T
# df3


# ##standalone plot
# 

# In[10]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots

selected_county = 'Hamilton, Iowa'

num_cols = 3
num_rows = (len(selected_cols) + num_cols - 1) // num_cols
fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=selected_cols)

for idx, col in enumerate(selected_cols, 1):
    row, col_idx = (idx - 1) // num_cols + 1, (idx - 1) % num_cols + 1

    histogram = go.Histogram(x=df_use[col], nbinsx=50, name=col, marker_color='#2b3d19')
    fig.add_trace(histogram, row=row, col=col_idx)

    county_value = df_use.loc[df_use['state_county'] == selected_county, col].values[0]
    fig.add_vline(x=county_value, line_width=3,line_dash="dash", line_color="#E67A35", row=row, col=col_idx)

fig.update_layout(
    height=200 * num_rows,
    showlegend=False,
    margin=dict(t=100)
)

fig.show()


# ## dash plot

# In[11]:


get_ipython().system('pip install dash dash-core-components dash-html-components plotly jupyter-dash')


# In[12]:


df_use.head()


# In[13]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from jupyter_dash import JupyterDash

# Assuming df_use is the DataFrame with the selected columns and 'state_county' column

# Initialize JupyterDash app
app = JupyterDash(__name__)
server = app.server

# Create a list of unique county names
county_names = df_use['state_county'].unique()

# Define app layout
app.layout = html.Div([
    html.H1('Histograms of Features Constucting ESGS Index',style={'color': '#2b3d19',
                                                                   'textAlign': 'center'}),
    html.P('Choose a county from the drop-down to display its feature values within the histograms', style={'textAlign': 'center', 
                                                                                                            'fontSize': '14px', 
                                                                                                            'margin': '0px 0px 10px',
                                                                                                            'color': '#b8bdb1'}),
    dcc.Dropdown(
        id='county-dropdown',
        options=[{'label': county, 'value': county} for county in county_names],
        value=county_names[0]
    ),
    dcc.Graph(id='histograms')
])

# Define callback function to update histograms based on selected county
@app.callback(
    Output('histograms', 'figure'),
    [Input('county-dropdown', 'value')]
)
def update_histograms(selected_county):
    num_cols = 2
    num_rows = (len(selected_cols) + num_cols - 1) // num_cols
    fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=selected_cols,
                        vertical_spacing=0.04, horizontal_spacing=0.08)

    for idx, col in enumerate(selected_cols, 1):
        row, col_idx = (idx - 1) // num_cols + 1, (idx - 1) % num_cols + 1

        histogram = go.Histogram(x=df_use[col], nbinsx=50, name=col, marker_color='#127a36')
        fig.add_trace(histogram, row=row, col=col_idx)

        county_value = df_use.loc[df_use['state_county'] == selected_county, col].values[0]
        fig.add_vline(x=county_value, line_width=3, line_dash="dash", line_color="#E67A35", row=row, col=col_idx)

    fig.update_layout(
        height=250 * num_rows,
        showlegend=False,
        margin=dict(t=50, b=10, l=30, r=30)
    )

    return fig

# Run the app in external mode
app.run_server(mode='external')


# In[14]:


# import plotly.graph_objects as go

# fig = go.Figure(go.Barpolar(
#     r=[3.5, 1.5, 2.5, 4.5, 4.5, 4, 3],
#     theta=[65, 15, 210, 110, 312.5, 180, 270],
#     width=[20,15,10,20,15,30,15,],
#     marker_color=["#E4FF87", '#709BFF', '#709BFF', '#FFAA70', '#FFAA70', '#FFDF70', '#B6FFB4'],
#     marker_line_color="black",
#     marker_line_width=2,
#     opacity=0.8
# ))

# fig.update_layout(
#     template=None,
#     polar = dict(
#         radialaxis = dict(range=[0, 5], showticklabels=False, ticks=''),
#         angularaxis = dict(showticklabels=False, ticks='')
#     )
# )

# fig.show()

