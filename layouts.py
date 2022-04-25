# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:30:10 2020

@author: Syamanthaka B
"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import data_n_graphs as grf


## Main Home Page
##################################################################################################
#Nav bar items
heading = html.H1("Kenya Community Life Centers: KPIs dashboard", style={'text-align' : 'center'})
home_link = html.A("Home", href='/', className='nav_links_left')
report_img = html.A(html.Img(src='assets/download_img.jpg', alt='Report', style={
                    'height' : '50px',
                    'width' : '50px',
                    'padding-top' : 0,
                    'padding-right' : 0
                }, className='nav_links_right'), href='/get_report', target='_blank')
    
# clubbing navbar items
title = dbc.NavbarSimple(
    children=[heading, home_link, report_img],
    className="nav_bar",
)


body = html.Div([
    ### Heading Row
    title,
    dbc.Row(dbc.Col(html.Div(html.Hr()))),

    dbc.Row([
        ### Left Column for quadruple aims
        dbc.Col([
            html.Div("Quadruple aims"),
            dcc.Location(id='url', refresh=False),
            html.MapEl([
                html.Area(target='', alt='Aim1', title='Improved Patient Experience', href='#Aim1', coords='0,0,250,250', shape='rect'),
                html.Area(target='', alt='Aim2', title='Better Health Outcomes', href='#Aim2', coords='250,0,500,250', shape='rect'),
                html.Area(target='', alt='Aim3', title='Lower Cost of Care', href='#Aim3', coords='250,250,500,500', shape='rect'),
                html.Area(target='', alt='Aim4', title='Improved Staff Experience', href='#Aim4', coords='0,250,250,500', shape='rect'),
            ],name='map'),
            html.Img(src='assets/quad_aim.png', useMap='#map'),
            
            html.Div(id='qa_generic', className='kpi_text')
        ], width=4),
        
        ### Main column of graphs from annual_data
        dbc.Col([
            dbc.Row([
                
                ### Facility drop down
                html.Label(["Select Facility from the list", 
                dcc.Dropdown(
                    id='facility_select',
                    options=[{'label': i, 'value': i} for i in grf.facility],
                    value=grf.facility[0]
                )
                ]),
                
                html.Label(["Select graph to display", 
                dcc.Dropdown(
                    id='graph_id',
                    options=[{'label': i, 'value': i} for i in grf.graph_lst],
                    value=grf.graph_lst[0]
                )
                ], style={"margin-left": "15px"})
            ]),
            dbc.Row([
                
                dcc.Graph(
                    id='bar_graph',
                    figure=grf.main_graph,
                    style = {'width':'50%', 'height':'30%'} #
                ),
                ### Description
                dcc.Graph(
                    id='desc_table',
                    figure=grf.desc_table,
                    style = {'width':'50%', 'height':'30%'} #
                ),
                
            ]),
            
            
             dbc.Row([
                ### Quadruple aim
                dbc.Col([
                html.Div(id='kpi-content',
                    style={'visibility':'hidden'},
                    children = [
                        dcc.Graph(
                            id='kpi_table',
                            figure=grf.kpi_table,
                            style = {'width':'100%', 'height':'100%'} #
                        ),
                ])
                ]),
                dbc.Col([
                    html.Div(id='kpi-content2',
                        style={'visibility':'hidden'},
                        children = [
                            dcc.Graph(
                                id='kpi_chart',
                                figure=grf.kpi_chart,
                                style = {'width':'100%', 'height':'30%'}
                            )
                        ]
                    )
                ]),
                
            ])
        ]),
        
    ]),
    
    
    dbc.Row(dbc.Col(html.Div(html.Hr())))
])

##################################################################################################


main_page = dbc.Container([
      body
], fluid=True)
                
