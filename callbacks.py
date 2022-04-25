# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:35:13 2020

@author: Syamanthaka
"""

from dash.dependencies import Input, Output
import flask

from app import app
import data_n_graphs as grf

@app.server.route("/get_report")
def get_report():
    return flask.send_from_directory('scripts/', "report.html")

@app.callback([Output('qa_generic', 'children'), 
               Output('kpi-content', 'style'),
               Output('kpi_table', 'figure'),
               Output('kpi-content2', 'style'),
               Output('kpi_chart', 'figure')],
              [Input('url', 'hash'),
               Input('facility_select', 'value')])
def display_page(pathname, facility):
    generic_notes, kpi_content_style, facility_kpi_table = grf.qa_descs(pathname, facility)
    kpi_content2 = kpi_content_style
    kpi_chart = grf.kpi_graphs(pathname,facility, kpi_content_style)
    return generic_notes, kpi_content_style, facility_kpi_table, kpi_content2, kpi_chart
    
    
@app.callback([Output('desc_table', 'figure'),
               Output('bar_graph', 'figure')],
              [Input('facility_select', 'value'),
               Input('graph_id', 'value')])
def facility_updates(facility, graph_id):
    desc_tab = grf.gen_desc_content(facility)
    bar_graph = grf.gen_main_graph(facility, graph_id)
    return desc_tab, bar_graph
    
