# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:09:17 2020

@author: Syamanthaka B
"""

import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True
