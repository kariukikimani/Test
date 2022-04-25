# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:26:45 2020

@author: Syamanthaka
"""

import dash_html_components as html
import layouts as lyt
from app import app
import callbacks

app.title='CLC KPI'
app.layout = html.Div([
    lyt.main_page
])

app.config.suppress_callback_exceptions = True
if __name__ == '__main__':
    app.run_server(debug=False)