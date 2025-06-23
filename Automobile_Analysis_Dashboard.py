# Uncomment to Install the Following 
# pip3.8 install setuptools
# python3.8 -m pip install packaging
# python3.8 -m pip install pandas dash
# pip install more-itertools

# Import Necessary Libraries
import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load and Read the Data
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Create the Dash App
app = dash.Dash(__name__)

# Years List
year_list = [i for i in range(1980, 2024, 1)]

# Dashboard Layout
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style = {'textAlign': 'center', 'color': '#503D36',
                                'font-size': 24}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                    ],
            value='Select Statistics',
            placeholder='Select a report type'
        )
    ]),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='Select-year', 
            placeholder='Select-year'
        )),
    html.Div([
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    ])
])
# Created a Callback to Update the Input Container Based on the Selected Statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True

# Created a Callback to Update the Input Container Based on the Selected Statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='select-year', 
    component_property='value')])


def update_output_container(selected_statistics, input_year):
    if  selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

# Graphs for Recession Period Statistics
# Plot 1: Line Graph for Automobile sales fluctuate over Recession Period 
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()

        figure = px.line(
            yearly_rec,
            x='Year',
            y='Automobile_Sales',
            title="Average Automobile Sales fluctuation over Recession Period"
        )

        figure.update_layout(
            title=dict(
                text="Average Automobile Sales Fluctuation Over Recession Period",
                x=0.5,
                xanchor='center'
            ),
            xaxis_title="Year",
            yaxis_title="Average Automobile Sales"
        )

        R_chart1 = dcc.Graph(figure=figure)


#Plot 2: Bar Chart for Average Automobile Sales by Vehicle Type  
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()

        figure2 = px.bar(
            average_sales,
            x='Vehicle_Type',
            y='Automobile_Sales',
            title="Average Automobile Sales by Vehicle Type"
        )

        figure2.update_layout(
            title=dict(
                text="Average Automobile Sales by Vehicle Type",
                x=0.5,
                xanchor='center'
            ),
            xaxis_title="Vehicle Type",
            yaxis_title="Average Automobile Sales"
        )

        R_chart2 = dcc.Graph(figure=figure2)

# Plot 3: Pie chart for Advertising Expenditure by Vehicle Type
        xp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()

        figure3 = px.pie(
            xp_rec,
            values='Advertising_Expenditure',
            names='Vehicle_Type',
            title="Advertising Expenditure by Vehicle Type"
        )

        figure3.update_layout(
            title=dict(
                text="Advertising Expenditure by Vehicle Type",
                x=0.5,
                xanchor='center'
            )
        )

        R_chart3 = dcc.Graph(figure=figure3)

# Plot 4: Bar Chart for Effect of Unemployment Rate on Vehicle Type and Sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()

        figure4 = px.bar(
            unemp_data,
            x='unemployment_rate',
            y='Automobile_Sales',
            color='Vehicle_Type',  
            labels={
                'unemployment_rate': 'Unemployment Rate',
                'Automobile_Sales': 'Average Automobile Sales',
                'Vehicle_Type': 'Vehicle Type'
            },
            title='Effect of Unemployment Rate on Vehicle Type and Sales'
        )

        figure4.update_layout(
            title=dict(
                text='Effect of Unemployment Rate on Vehicle Type and Sales',
                x=0.5,
                xanchor='center'
            ),
            xaxis_title='Unemployment Rate',
            yaxis_title='Average Automobile Sales'
        )

        R_chart4 = dcc.Graph(figure=figure4)

# Return Graphs for Display
        return [
             html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart4)],style={'display': 'flex'})
            ]


# Graphs for Yearly Report Statistics                       
    elif (input_year and selected_statistics=='Yearly Statistics') :
        yearly_data = data[data['Year'] == input_year]
                              
                          
# Plot 1: Line Graph for Average Automobile Sales Fluctuation Over the Years
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()

        figY1 = px.line(
            yas,
            x='Year',
            y='Automobile_Sales',
            title="Average Automobile Sales Fluctuation Over the Years"
        )

        figY1.update_layout(
            title=dict(
                text="Average Automobile Sales Fluctuation Over the Years",
                x=0.5,
                xanchor='center'
            ),
            xaxis_title="Year",
            yaxis_title="Average Automobile Sales"
        )

        Y_chart1 = dcc.Graph(figure=figY1)
                    
# Plot 2: Line Graph for Total Monthly Automobile Sales
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()

        figY2 = px.line(
            mas,
            x='Month',
            y='Automobile_Sales',
            title='Total Monthly Automobile Sales'
        )

        figY2.update_layout(
            title=dict(
                text='Total Monthly Automobile Sales',
                x=0.5,
                xanchor='center'
            ),
            xaxis_title='Month',
            yaxis_title='Total Automobile Sales'
        )

        Y_chart2 = dcc.Graph(figure=figY2)

# Plot 3: Bar Chart for Average Vehicles Sold by Vehicle Type in the Selected Year
        avr_vdata = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()

        figY3 = px.bar(
            avr_vdata,
            x='Year',
            y='Automobile_Sales',
            title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)
        )

        figY3.update_layout(
            title=dict(
                text='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year),
                x=0.5,
                xanchor='center'
            ),
            xaxis_title='Year',
            yaxis_title='Average Automobile Sales'
        )

        Y_chart3 = dcc.Graph(figure=figY3)

# Plot 4: Pie Chart for Total Advertisement Expenditure for Vehicle Type
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()

        figY4 = px.pie(
            exp_data,
            values='Advertising_Expenditure',
            names='Vehicle_Type',
            title='Total Advertisement Expenditure for Vehicle Type'
        )

        figY4.update_layout(
            title=dict(
                text='Total Advertisement Expenditure for Vehicle Type',
                x=0.5,
                xanchor='center'
            )
        )

        Y_chart4 = dcc.Graph(figure= figY4)

# Return Graphs for Display
        return [
                html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)],style={'display':'flex'}),
                html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)],style={'display':'flex'}),
        ]
    else:
        return None
        
# Run the Server
if __name__ == '__main__':
    app.run(debug=True, port=8052)


