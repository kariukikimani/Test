# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:35:57 2020

@author: Syamanthaka B
"""
### Necessary imports
import plotly.graph_objects as go
import pandas as pd
import xml.etree.ElementTree as ET

### Read the main inputs
## Config of graphs
graph_tree = ET.parse('data/graph_config.xml')
graph_root = graph_tree.getroot()

## Graph data
annual_df = pd.read_csv('data/annual_data.csv')
#Extract names of facilities from facility column
#This also becomes a drop down on screen
facility = annual_df['Facility name'].unique() 

## KPI notes data
notes_df = pd.read_excel('data/Kenya KPI dashboard notes.xlsx')

## Config of KPIs
kpi_tree = ET.parse('data/KPI_config.xml')
kpi_root = kpi_tree.getroot()

### Various Functions
## Create dropdown of graphs, from graph config tags
## This is rendered on screen for user to select required graph
def graph_dropdown():
    graph_lst = [x.tag for x in graph_root]
    return graph_lst
graph_lst = graph_dropdown()

## Generate table about description information eg. location, country, description, objectives etc
def gen_desc_content(facility):
    info_df = annual_df.iloc[:,0:9] # First 9 columns contain description info
    info_df_fac = info_df[info_df['Facility name'] == facility] # Filter for chosen facility
    
    ### Transpose description information
    desc_df = pd.DataFrame(columns=['Col_name', 'Values'])
    for col in info_df_fac.columns:
        uniq_vals = info_df_fac[col].unique()
        if (len(uniq_vals) == 1):
            the_val = uniq_vals[0]
        elif (len(uniq_vals) > 1):
            the_val = [x + "\n" for x in uniq_vals]
        else:
            the_val = ''
        desc_df = desc_df.append({'Col_name' : col, 'Values' : the_val}, ignore_index=True)
    
    # Transposed description table is generated as graph object Table 
    info_tab = go.Figure(data=[go.Table(
        header=dict(fill_color='white', line_color='black'),
        cells=dict(values=[desc_df['Col_name'], desc_df['Values']],
                   fill_color='white',
                   align='left',
                   font_size=16,
                   line_color='black',
                   height=25
                   ))
            ])
    # info_tab.layout['template']['data']['table'][0]['header']['fill']['color']='rgba(0,0,0,0)' #Not displaying header
    info_tab.update_layout(
        margin=dict(l=10, r=10, t=25, b=10), #Plotly padding reduction
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Arial, Helvetica, sans-serif",
            size=16
            )
    )
    return info_tab
#Calling above function with default option for first time display
desc_table = gen_desc_content(facility[0]) 

## Function to generate the main graph
def gen_main_graph(facility, sel_graph):
    #Filter data by selected facility
    fac_filter = annual_df[annual_df['Facility name'] == facility]
    
    #Get details of type of graph etc from graph config
    sel_tag = graph_root.find(sel_graph)
    
    sel_tag_type = sel_tag.find('type')
    graph_type = sel_tag_type.text
    
    sel_tag_title = sel_tag.find('title')
    graph_title = sel_tag_title.text
    
    sel_tag_y = sel_tag.find('y_title')
    y_title = sel_tag_y.text
    
    main_grf = go.Figure()
    
    #Single colum graph
    if graph_type == 'bar':
        sel_tag_y = sel_tag.find('col1')
        y_axis = sel_tag_y.text
        main_grf.add_trace(
            go.Bar(x=fac_filter['Year'], y=fac_filter[y_axis], marker_color='#008080')
        )
    #Two column graph -> bar-bar and bar-line
    else:
        sel_tag_col1 = sel_tag.find('col1')
        y1 = sel_tag_col1.text
        sel_tag_col2 = sel_tag.find('col2')
        y2 = sel_tag_col2.text
        main_grf.add_trace(
            go.Bar(x=fac_filter['Year'], y=fac_filter[y1], name=y1, marker_color='#008080')
        )
        if graph_type == 'bar-bar':
            main_grf.add_trace(
                go.Bar(x=fac_filter['Year'], y=fac_filter[y2], name=y2, marker_color='#c2c2a3')
            )
        else:
            main_grf.add_trace(
                go.Scatter(x=fac_filter['Year'], y=fac_filter[y2], name=y2, marker_color='#ff9900', marker_size=5, marker_line_width=5)
            )
        
    #Padding and bg color
    main_grf.update_layout(
        margin=dict(l=10, r=10, t=45, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    main_grf.update_layout(
        title= graph_title + ' for ' + facility,
        xaxis_title='Year',
        yaxis_title=y_title,
        font=dict(
            family="Arial, Helvetica, sans-serif",
            size=18
            )
        )
    
    return main_grf
#Calling above function with default option for first time display
main_graph = gen_main_graph(facility[0], graph_lst[0])


###############################################################
### KPI Section
## Function for generating KPI notes section based on Quadruple aim selected by user, clicking on image section
def qa_descs(sel_aim, facility):
    try:
        selected_aim = sel_aim.split('#')[1]
    except:
        return 'No information available', {'visibility':'hidden'}, go.Figure()
    
    # Filter data by aim and facility
    facility_df = notes_df[notes_df['Facility'] == facility]
    facility_aim_df = facility_df[facility_df['Quadruple Aim'] == selected_aim]
    
    try:
        generic_kpi_note = facility_aim_df['KPI'].unique()[0]
    except IndexError:
        return 'No information available', {'visibility':'hidden'}, go.Figure()

    # Return KPI notes information as graph object table
    facility_kpi_table = facility_aim_df.iloc[:, 3:6]
    kpi_table = go.Figure(data=[go.Table(
        header=dict(values=['Indicator', 'Indicator description', 'Results'],
                    line_color='black',
                    fill_color='#ccff33'),
        cells=dict(values=[facility_kpi_table['Indicator'], facility_kpi_table['Indicator description'], facility_kpi_table['Results']],
                   fill_color='#ebebe0',
                   align='left',
                   font_size=18,
                   line_color='black',
                   height=30
                   ))
            ])
   
    kpi_table.update_layout(
        margin=dict(l=10, r=10, t=25, b=10), #Plotly padding reduction
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Arial, Helvetica, sans-serif",
            size=18
            )
    )
    
    return generic_kpi_note, {'visibility':'visible'}, kpi_table
#Calling above function with default option for first time display - default is empty figure, with visibility set to hidden   
kpi_table = go.Figure()

## Function to generate KPI metrics
def kpi_graphs(sel_aim, facility, visibility):
    if visibility == {'visibility':'hidden'}:
        return 0
    selected_aim = sel_aim.split('#')[1]
    selected_aim = selected_aim.lower()

    facility_df = annual_df[annual_df['Facility name'] == facility]
   
    kpi_df = pd.DataFrame(columns=['KPI','Start Year', 'End Year', 'Start Year Value', 'End Year Value', 'Change %', 'Status'])
   
    #Get KPI metric info from KPI config file
    aim_tag = kpi_root.find(selected_aim)
    for i,each in enumerate(aim_tag):
        col_tag = each.find('col')
        col_name = col_tag.text
        
        kpi_name_tag = each.find('kpiname')
        kpi_name = kpi_name_tag.text
        
        req_df_temp = facility_df[['Year', col_name]]
        req_df = req_df_temp.dropna()
        
        start_year = min(req_df['Year'])
        end_year = max(req_df['Year'])
        start_val = req_df[req_df['Year'] == start_year][col_name].values[0]
        end_val = req_df[req_df['Year'] == end_year][col_name].values[0]
        if start_val == 0:
            change = 'inf'
        else:
            change = round((end_val - start_val)/start_val * 100, 1)
        cell_color = 'green' if float(change) > 0 else 'red'#Positive change is green and -ve is red
        
        
        kpi_df = kpi_df.append({'KPI': kpi_name,
                                'Start Year' : start_year,
                                'End Year': end_year,
                                'Start Year Value': start_val,
                                'End Year Value': end_val,
                                'Change %': change,
                                'Status': cell_color}, ignore_index=True)
    
    # Return metrics as graph object Table, with color for hange value to indicate red or green status
    kpi_chart = go.Figure(data=[go.Table(
        header=dict(values=list(kpi_df.columns[:-1]),
                    line_color='black',
                    fill_color='#ccff33'),
        cells=dict(values=[kpi_df['KPI'], kpi_df['Start Year'], kpi_df['End Year'], kpi_df['Start Year Value'], kpi_df['End Year Value'], kpi_df['Change %']],
                   fill_color=['#ebebe0','#ebebe0','#ebebe0','#ebebe0','#ebebe0', kpi_df['Status']],
                   align='left',
                   font_size=16,
                   line_color='black',
                   height=30
                   ))
            ])
   
    kpi_chart.update_layout(
        margin=dict(l=10, r=10, t=25, b=10), #Plotly padding reduction
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Arial, Helvetica, sans-serif",
            size=18
            )
    )
    return kpi_chart
#Calling above function with default option for first time display as invisible object
kpi_chart = go.Figure()
kpi_chart.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
    )
    
    