import warnings
warnings.filterwarnings('ignore')

import base64
from dash import Dash, html, dcc

from tools import *
from models import *
from static import *


# ----------- Simulation ------------------------------
steps = 30
model = abmodel(static_map_v0(), all_agents())
model.run_model(steps)
model_results = model.datacollector.get_model_vars_dataframe()

# ----------- Some Visualization Plot -----------------

central_bank_fig = plot_central_bank(model_results)
map_resource_fig = plot_map(model)

agent_position_df = built_agent_position_df(model, steps)
agent_movement_fig = plot_agent_movement(model, agent_position_df)
agent_population_fig = plot_agent_population(agent_position_df)

banks_lob_fig = model.bank_details.lob(steps, agent = 'Banks')
international_bank_lob_fig = model.international_bank_details.lob(steps, agent = 'International Banks')
bid_ask_price_fig = model.bank_details.price_plot()

def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return f'data:image/png;base64,{encoded_image}'

image_path = "ABM_FX/Central Bank Agent Behavior.png"
encoded_image = encode_image(image_path)

# ---------------------------------------------------

app = Dash(__name__, external_stylesheets=['custom_styles.css'])

app.layout = html.Div([
    
        html.Div(children = [html.Div(className = "div-logo", 
                                      style = {"background": "#2c5c97", 'padding': '20px', 'border-radius': '10px', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}, 
                                      children = [html.Img(className="logo", src = ("https://opendatabim.io/wp-content/uploads/2021/12/GitHub-Mark-Light-64px-1.png")), 
                        
                            html.H1("Agent-Based Modeling in Finance - Team Banana", style = {'font-size': '36px', 'font-family': 'Roboto', 'color': 'white', 'margin-left': '10px', 'margin-tap': '-50px'}) ]),
                    
                            html.A(id = 'gh-link', children = ['View on GitHub'], href = 'https://github.com/Gordonhosy/ABM_FX', style = {'font-size': '18px', 'text-align': 'center', 'color': 'white', 'text-decoration': 'none', 'display': 'block', 'margin-top': '-30px'})]),


        # Part 1 - Environment Setup
        html.Div([html.H1(children = "1. Environment Setup - Map, Resources, and Macroeconomic", style = {'textAlign': 'center', 'font-size': '25px', 'text-align': 'left'})]),

        # Map and Resources Paragraph
        html.P(children = "1-1.) Map & Resources", id = 'map_title', style = {'font-size': '20px', 'width': '50%', 'border-radius': '20px', 'text-align': 'left', "padding-left": "20px", 'font-family' : 'Roboto', "margin-left" : "20px", "margin-up" : "-120px", 'background' : 'rgb(233 238 246)'}),
        html.P(children = "We model the map and allocate resources based on the reality of the United States and Japan, with resource distribution determined by population level.", style = {'font-size': '20px', "margin-left" : "30px"}),
        dcc.Graph(id = "Map And Resource Chart", figure = map_resource_fig, style = {'margin-left' : '10px'}),
        html.P(children = "The original data sources can be found at https://simplemaps.com/data/us-cities.", style = {'font-size': '20px', "margin-left" : "30px"}),

        # Central and Macroeconomic Paragraph
        html.P(children = "1-2.) Central Bank & Macroeconomics Variable",
                id = 'central_bank_title',
                style = {'font-size': '20px', 
                         'width': '50%', 
                         'border-radius': '20px', 
                         'text-align': 'left', 
                         "padding-left": "20px", 
                         'font-family' : 'Roboto', 
                         "margin-left" : "20px", 
                         "margin-up" : "-120px", 
                         'background' : 'rgb(233 238 246)'}),

        html.P(children = "We aim to mimic the macroeconomic conditions in Japan and the USA, with one characterized by negative interest rates and lower growth, and the other by higher growth and inflation rates.", style = {'font-size': '20px', "margin-left" : "30px"}),
        dcc.Graph(id = "Central Bank Chart", figure = central_bank_fig, style = {'margin-left' : '10px'}),
        html.P(children = "Both central bank agent behaviors are modeled based on Taylor's rule. The fundamental concept behind Taylor’s rule model is to offer a systematic and transparent approach for central banks to adjust interest rates in response to changes in inflation and output.", style = {'font-size': '20px', "margin-left" : "30px"}),
        html.Img(src = encoded_image, style = {'width': '80%', 'height': '30%', 'margin-left' : '30px'}),

        # Part 2 - Simulation Result
        html.Div([html.H1(children = "2. Simulation Result", style = {'textAlign': 'center', 'font-size': '25px', 'text-align': 'left'})]),
        html.P(children = '2-1.) Movement of Corporate Agents', id = 'corporate_agent_movement_title', style = {'font-size': '20px', 
                                                                                           'width': '50%', 
                                                                                           'border-radius': '20px', 
                                                                                           'text-align': 'left', 
                                                                                           'padding-left': "20px", 
                                                                                           'font-family' : 'Roboto', 
                                                                                           "margin-left" : "20px", 
                                                                                           "margin-up" : "-120px", 
                                                                                           'background' : 'rgb(233 238 246)'}),
        dcc.Graph(id = "Agent Movement Chart", figure = agent_movement_fig, style = {'margin-left' : '10px'}),

        html.P(children = '2-2.) Agent Population & Bid/Ask Price', id = 'agent_population_title', style = {'font-size': '20px',
                                                                                                            'width': '50%', 
                                                                                                            'border-radius': '20px', 
                                                                                                            'text-align': 'left', 
                                                                                                            "padding-left": "20px", 
                                                                                                            'font-family' : 'Roboto', 
                                                                                                            "margin-left" : "20px", 
                                                                                                            "margin-up" : "-120px", 
                                                                                                            'background' : 'rgb(233 238 246)'}),
        html.Div(children = [dcc.Graph(id = "Agent Population Chart", figure = agent_population_fig, style = {'margin-left' : '10px'}), 
                             dcc.Graph(id = "Bid Ask Price Chart", figure = bid_ask_price_fig, style = {'margin-left':'10px'})],
                             style = {'display': 'flex', 'flexDirection': 'row', 'gap': '35px'}),

        html.P(children = '2-3.) Limit Order Book of Interbank Market at Final Step', id = 'limit_order_book_title', style = {'font-size': '20px', 
                                                                                                                 'width': '50%', 
                                                                                                                 'border-radius': '20px', 
                                                                                                                 'text-align': 'left', 
                                                                                                                 'padding-left': "20px", 
                                                                                                                 'font-family' : 'Roboto', 
                                                                                                                 'margin-left' : "20px", 
                                                                                                                 'margin-up' : "-120px", 
                                                                                                                 'background' : 'rgb(233 238 246)'}),

        html.Div(children = [dcc.Graph(id = "Banks LOB Chart", figure = banks_lob_fig, style = {'margin-left' : '10px'}),
                             dcc.Graph(id = "International Banks LOB Chart", figure = international_bank_lob_fig, style = {'margin-left' : '10px'}),
                            ], style = {'display': 'flex', 'flexDirection': 'row', 'gap': '35px'}),


        html.Footer("© 2024 Agent-Based Modeling Team Banana. All rights reserved.", style={'text-align': 'center', 'color': '#555', 'padding': '10px', 'margin-top': '20px'})
]) 


if __name__ == '__main__':
    app.run_server(debug=True)