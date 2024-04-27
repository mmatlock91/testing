# In this lab, you will be building a Plotly Dash application for users to perform interactive visual analytics on SpaceX launch data in
# real-time.

# This dashboard application contains input components such as a dropdown list and a range slider to
# interact with a pie chart and a scatter point chart. You will be guided to build this dashboard application via the following tasks:

# TASK 1: Add a Launch Site Drop-down Input Component
# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
# TASK 3: Add a Range Slider to Select Payload
# TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
# Note:Please take screenshots of the Dashboard and save them. Further upload your notebook to github.

# The github url and the screenshots are later required in the presentation slides.


# Which site has the largest successful launches?
# Which site has the highest launch success rate?
# Which payload range(s) has the highest launch success rate?
# Which payload range(s) has the lowest launch success rate?
# Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
# launch success rate?


# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("/workspaces/testing/DataScienceCapstone/app/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
# Create the application layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Task 1: Dropdown list to enable Launch Site selection
    # Default value is for ALL sites
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}
        ],
        value='ALL',  # Default value
        placeholder="Select a Launch Site",  # Placeholder text
        searchable=True  # Enable search functionality
    ),
    html.Br(),

    # Task 2: Pie chart to show the total successful launches count for all sites
    # If a specific launch site is selected, show the Success vs. Failed counts for that site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload Range (Kg):"),
    # Task 3: Slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={i: str(i) for i in range(int(min_payload), int(max_payload)+1, 1000)},
        value=[min_payload, max_payload]
    ),

    # Task 4: Scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Filter data for all sites
        filtered_df = spacex_df.copy()
        title = 'Total Successful Launches for All Sites'
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f'Success vs. Failure Count for {selected_site}'

    # Calculate successful and failed launch counts
    success_count = filtered_df[filtered_df['class'] == 1].shape[0]
    failure_count = filtered_df[filtered_df['class'] == 0].shape[0]

    # Create pie chart figure
    fig = px.pie(
        data_frame=filtered_df,
        names=['Success', 'Failure'],
        values=[success_count, failure_count],
        title=title
    )

    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df.copy()
        title = 'Payload Mass vs. Launch Outcome for All Sites'
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f'Payload Mass vs. Launch Outcome for {selected_site}'

    # Filter based on payload range
    filtered_df = filtered_df[
        (filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
        (filtered_df['Payload Mass (kg)'] <= payload_range[1])
    ]

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=title,
        hover_data=['Launch Site'],
        labels={'class': 'Launch Outcome (0: Success, 1: Failure)'}  # Customize y-axis label
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)