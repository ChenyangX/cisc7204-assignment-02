
# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Read the airline data into the pandas dataframe
airline_data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
    encoding="ISO-8859-1",
    dtype={
        'Div1Airport': str,
        'Div1TailNum': str,
        'Div2Airport': str,
        'Div2TailNum': str
    }
)

print("Dataset loaded successfully!")
print(airline_data.shape)

# Create a dash application
app = dash.Dash(__name__)

# Create application layout
app.layout = html.Div(children=[

    html.H1(
        'Airline Performance Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'fontSize': 40
        }
    ),

    html.Div(
        [
            "Input Year: ",
            dcc.Input(
                id='input-year',
                value=2010,
                type='number',
                style={
                    'height': '50px',
                    'fontSize': 35,
                    'width': '350px'
                }
            )
        ],
        style={'fontSize': 40}
    ),

    html.Br(),
    html.Br(),

    html.Div(
        dcc.Graph(
            id='line-plot',
            style={'width': '100%', 'height': '500px'}
        ),
        style={'width': '100%'}
    )
])

# Task 3 - Add callback decorator
@app.callback(
    Output(component_id='line-plot', component_property='figure'),
    Input(component_id='input-year', component_property='value')
)

# Add computation to callback function and return graph
def get_graph(entered_year):

    if entered_year is None:
        return go.Figure()

    # Select data based on the entered year
    df = airline_data[
        airline_data['Year'] == int(entered_year)
    ]

    # Group data by Month and compute average arrival delay
    line_data = (
        df.groupby('Month')['ArrDelay']
        .mean()
        .reset_index()
    )

    # Create green line chart
    fig = go.Figure(
        data=go.Scatter(
            x=line_data['Month'],
            y=line_data['ArrDelay'],
            mode='lines',
            marker=dict(color='green')
        )
    )

    # Update chart layout
    fig.update_layout(
        title='Month vs Average Flight Delay Time',
        xaxis_title='Month',
        yaxis_title='ArrDelay',
        height=500,
        margin=dict(l=60, r=30, t=80, b=60)
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=False)
