
# Task 4: Practice Exercise

# 1. Import required libraries
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Read the airline dataset
airline_data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
    encoding='ISO-8859-1',
    dtype={
        'Div1Airport': str,
        'Div1TailNum': str,
        'Div2Airport': str,
        'Div2TailNum': str
    }
)

print("Dataset loaded successfully!")
print(airline_data.shape)

# 2. Create a Dash application
app = dash.Dash(__name__)

# Create dashboard layout
app.layout = html.Div(children=[

    html.H1(
        'Total number of flights to the destination state split by reporting airline',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
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
                    'font-size': 35
                }
            )
        ],
        style={'font-size': 40}
    ),

    html.Br(),
    html.Br(),

    html.Div(
        dcc.Graph(id='bar-plot')
    )

])

# 3. Add callback decorator
@app.callback(
    Output(
        component_id='bar-plot',
        component_property='figure'
    ),
    Input(
        component_id='input-year',
        component_property='value'
    )
)

# 4. Define callback graph function
def get_graph(entered_year):

    if entered_year is None:
        return px.bar(title='Please enter a year')

    # Select data based on the entered year
    df = airline_data[
        airline_data['Year'] == int(entered_year)
    ]

    # Group by destination state and reporting airline
    bar_data = (
        df.groupby(['DestState', 'Reporting_Airline'])
        .size()
        .reset_index(name='Flights')
    )

    # Create a blue bar chart
    fig = px.bar(
        bar_data,
        x='DestState',
        y='Flights',
        title='Flights to Destination State',
        color_discrete_sequence=['#636EFA']
    )

    # Update chart layout
    fig.update_layout(
        xaxis_title='DestState',
        yaxis_title='Flights',
        xaxis_tickangle=0,
        showlegend=False,
        height=500,
        barmode='stack'
    )

    return fig


# 5. Run the application
if __name__ == '__main__':
    app.run(debug=False, port=8053)
