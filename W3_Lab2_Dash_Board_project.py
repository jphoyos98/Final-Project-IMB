# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#Launch sites
launch_sites=spacex_df['Launch Site'].value_counts()
sites=pd.DataFrame(launch_sites)
sites=list(sites.index)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': sites[0], 'value': sites[0]},
                                        {'label': sites[1], 'value': sites[1]},
                                        {'label': sites[2], 'value': sites[2]},
                                        {'label': sites[3], 'value': sites[3]},
                                    ],
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                    ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, marks={0: '0', 100: '100'},
                                                                    value=[min_payload, max_payload]),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df

    if entered_site == 'ALL':
        
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches for All Sites')
        return fig
    else:
        filtered_df=filtered_df[spacex_df['Launch Site']==entered_site]
        fil=filtered_df.groupby(['Launch Site'])
        df2=fil['class'].value_counts()
        df2=pd.DataFrame(df2)
        df2=df2.rename(columns={'class':'count'})
        df2.reset_index(level='class',inplace=True)

        tit='Total Success Launches for Site '+entered_site
        fig=px.pie(df2, values='count',names='class', title=tit)

        return fig

        # return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))

def get_scatter_chart(entered_site, slider_range):

    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(slider_range[0],slider_range[1])]

    if entered_site == 'ALL':
        tit='Correlation Between Success and PayLoad for '+ entered_site
        fig = px.scatter(filtered_df, x='Payload Mass (kg)',y='class',color='Booster Version Category' ,title=tit)
        return fig
    else:
        filtered_df=filtered_df[spacex_df['Launch Site']==entered_site]
        tit='Correlation Between Success and PayLoad for '+ entered_site
        fig = px.scatter(filtered_df, x='Payload Mass (kg)',y='class',color='Booster Version Category' ,title=tit)
        return fig

        

# Run the app
if __name__ == '__main__':
    app.run_server()