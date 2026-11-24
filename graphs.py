#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 13:20:48 2024

@author: reitze
"""

"""
dependencies: Kaleido: sudo conda install -c conda-forge python-kaleido
or conda install -c conda-forge python-kaleido=0.1.0
Also statsmodels
"""
import pandas as pd
import textwrap
import plotly.express as px
import plotly.io as pio
from PIL import Image
import json
import plotly.graph_objects as go
from copy import deepcopy
# Makes scatter displayed in streamlit
def scatter(dtaAgg, dtaselected, size, start, year, levels, highlight, legend, showlabel, showtrend, color_level, population, jobs=False, compare_rgva_hours=False, xrange = None, yrange=None, animate=False, delay=3, transition=2):
    pio.renderers.default='browser'

    metric = 'Average Annual log percentage change' #options are: 'Percentage change', 'Log percentage change', 'Average Annual Percentage change', 'Average Annual log percentage change'
    if compare_rgva_hours:
        x_column = 'Average Annual log percentage change in Hours'
        y_column = 'Average Annual log percentage change in RGVA'
        xaxistitle = str(start) + '-' + str(year) + ' average annual hours growth'
        yaxistitle = str(start) + '-' + str(year) + ' average annual RGVA growth'
        figure_subtitle = str(start) + '-' + str(year) + ' hours growth vs. RGVA growth'
    else:
        x_column = 'GVA per hour'
        y_column = metric
        xaxistitle = str(year) + ' output per hour worked (£)'
        yaxistitle = str(start) + '-' + str(year) + ' ' + metric + ' in productivity'
        figure_subtitle = str(year) + ' Nominal smoothed GVA per hour, vs. ' + str(start) + '-' + str(year) + ' productivity change'

    itl_string = ','.join(levels)
    figure_title = 'UK ' + itl_string + ' regions<br>' +\
                    '<sup>' + figure_subtitle + '</sup>'

                    # '<sup><b>By ' + level.upper() + ' region</b></sup>'

    dtaselected['Plot X'] = dtaselected[x_column]
    dtaselected['Plot Y'] = dtaselected[y_column]
    dtaAgg['Plot X'] = dtaAgg[x_column]
    dtaAgg['Plot Y'] = dtaAgg[y_column]
    bubble_column = 'Jobs' if jobs else ('Population' if population else None)
    bubble_label = 'Jobs' if bubble_column == 'Jobs' else 'Population'
    dtaselected['Bubble Size'] = dtaselected[bubble_column] if bubble_column else 0
    dtaAgg['Bubble Size'] = dtaAgg[bubble_column] if bubble_column else 0

    custom_data = ['name', 'code', 'Plot X', 'Plot Y', 'Bubble Size', 'level']
    if compare_rgva_hours:
        x_hover = str(start) + '-' + str(year) + ' hours growth: %{customdata[2]:.2%}'
        y_hover = str(start) + '-' + str(year) + ' RGVA growth: %{customdata[3]:.2%}'
    else:
        x_hover = str(year) + ' Productivity: £%{customdata[2]:.4} per hour'
        y_hover = 'Productivity growth: %{customdata[3]:.2%}'
    hover_lines = [
        '<b> %{customdata[0]}</b>',
        '%{customdata[5]} code: %{customdata[1]}',
        x_hover,
        y_hover,
    ]
    if bubble_column:
        hover_lines.append(bubble_label + ': %{customdata[4]:,.0f}')
    hovertemp = '<br>'.join(hover_lines)

    # averages = ['UKX','MCA']
    # avgcolors = ['purple', 'blue']
    averages = ['UKX']
    avgcolors = ['grey']
    with open("src/colormaps.json", "r") as file:
        colour_maps = json.load(file)

    # Access the individual dictionaries
    if color_level == 'MCA':
        colormap = colour_maps[3]
    else:
        colormap = colour_maps[int(color_level[3]) - 1]

    if showlabel:
        labels = 'name'
    else: labels = None

    if showtrend and not animate:
        trend = 'ols'
    else: trend = None

    if bubble_column:
        if dtaselected['Bubble Size'].max() - dtaselected['Bubble Size'].min() == 0:
            dtaselected['Scaled Bubbles'] = 1
        else:
            dtaselected['Scaled Bubbles'] = (10 + ((dtaselected['Bubble Size'] - dtaselected['Bubble Size'].min()) * (40 - 10)) / (dtaselected['Bubble Size'].max() - dtaselected['Bubble Size'].min())) * size
    if not animate:
        #Style plot
        if bubble_column:
            fig = px.scatter(dtaselected.reset_index(), x='Plot X', y='Plot Y',
                        text=labels,
                        color=color_level.lower() + 'name',
                        color_discrete_map=colormap,
                        custom_data=custom_data,
                        trendline=trend,
                        trendline_scope="overall",
                        trendline_color_override="red",
                        size='Scaled Bubbles',
                        width=1000*size,
                        height=700*size,
                        )
        else:
            fig = px.scatter(dtaselected.reset_index(), x='Plot X', y='Plot Y',
                        text=labels,
                        color=color_level.lower() + 'name',
                        color_discrete_map=colormap,
                        custom_data=custom_data,
                        trendline=trend,
                        trendline_scope="overall",
                        trendline_color_override="red",
                        width=1000*size,
                        height=700*size,
                        )
            fig.update_traces(marker=dict(size=10*size))
        fig.update_traces(textposition='top center', textfont_size=10*size)
    else:
        #Style plot
        if bubble_column:
            fig = px.scatter(dtaselected.reset_index(), x='Plot X', y='Plot Y',
                        text=labels,
                        color=color_level.lower() + 'name',
                        color_discrete_map=colormap,
                        custom_data=custom_data,
                        trendline=trend,
                        trendline_scope="overall",
                        trendline_color_override="red",
                        size='Scaled Bubbles',
                        width=1000*size,
                        height=700*size,
                        animation_frame='year',
                        animation_group='name',
                        )
        else:
            fig = px.scatter(dtaselected.reset_index(), x='Plot X', y='Plot Y',
                        text=labels,
                        color=color_level.lower() + 'name',
                        color_discrete_map=colormap,
                        custom_data=custom_data,
                        trendline=trend,
                        trendline_scope="overall",
                        trendline_color_override="red",
                        width=1000*size,
                        height=700*size,
                        animation_frame='year',
                        animation_group='name',
                        )
            fig.update_traces(marker=dict(size=10*size))
        fig.update_traces(textposition='top center', textfont_size=10*size)
    x_min = dtaselected['Plot X'].min()
    x_max = dtaselected['Plot X'].max()
    y_min = dtaselected['Plot Y'].min()
    y_max = dtaselected['Plot Y'].max()

    # if showlabel:
    #     # Update label positions
    #     for i, row in dtaselected.reset_index().iterrows():
    #         fig.add_annotation(
    #             x=row['GVA per hour'] + row['x_offset'],
    #             y=row[metric] + row['y_offset'],
    #             text=row['name'],
    #             showarrow=False,
    #             font=dict(size=9)
    #         )
    #add the scatter point for the reference average, 1 for UK as whole one for UK excluding London:
    for i, v in enumerate(averages):
        if v == 'UKX':
            dtaAgg['flag'] = 'UK'
        else:
            subset = dtaAgg.loc[(v, slice(None), slice(None)), ['Plot X', 'Plot Y', 'Population', 'Jobs']]
            
            dtaAgg.loc[('Average', v, f'{v} average'), ['Plot X', 'Plot Y', 'Population', 'Jobs']] = subset.mean().to_numpy()
            dtaAgg.to_csv('test.csv')
            dtaAgg['flag'] = '▲'
            
        if not animate:
            avgUK = dtaAgg.loc[(slice(None), v, slice(None)),['Plot X', 'Plot Y', 'Population', 'Jobs', 'Bubble Size', 'flag']].reset_index()
            ukavg = px.scatter(avgUK.reset_index(), x='Plot X', y='Plot Y',
                            text='flag',
                            custom_data=custom_data,
                            )
        else:
            avgUK = dtaAgg.loc[(slice(None), v, slice(None)),['Plot X', 'Plot Y', 'Population', 'Jobs', 'Bubble Size', 'year', 'flag']].reset_index()
            ukavg = px.scatter(avgUK.reset_index(), x='Plot X', y='Plot Y',
                            text='flag',
                            custom_data=custom_data,
                            animation_frame='year',
                            animation_group='name',
                            )
            hlines = []
            vlines = []

            for _, row in avgUK.iterrows():
                year = row['year']
                x_avg = row['Plot X']
                y_avg = row['Plot Y']

                # Horizontal line (constant y)
                hlines.append({
                    'x': x_min, 'y': y_avg, 'year': year, 'group': f'{year}_h'
                })
                hlines.append({
                    'x': x_max, 'y': y_avg, 'year': year, 'group': f'{year}_h'
                })

                # Vertical line (constant x)
                vlines.append({
                    'x': x_avg, 'y': y_min, 'year': year, 'group': f'{year}_v'
                })
                vlines.append({
                    'x': x_avg, 'y': y_max, 'year': year, 'group': f'{year}_v'
                })

            hlines_df = pd.DataFrame(hlines)
            vlines_df = pd.DataFrame(vlines)

            hlines_trace = px.line(
                hlines_df,
                x="x",
                y="y",
                animation_frame="year",
                line_group="group",  # important for animating multiple lines per frame
                color_discrete_sequence=[avgcolors[i]],
                hover_name=None,
            )

            vlines_trace = px.line(
                vlines_df,
                x="x",
                y="y",
                animation_frame="year",
                line_group="group",  # important for animating multiple lines per frame
                color_discrete_sequence=[avgcolors[i]],
                hover_name=None,
            )

            for htrace, vtrace in zip(hlines_trace.data, vlines_trace.data):
                htrace.update(line=dict(dash='dash'))
                vtrace.update(line=dict(dash='dash'))

        #styling for the UK average 'trace' or layer.
        ukavg.update_traces(marker=dict(
                                        size=2,
                                        # size=15,
                                        color=avgcolors[i],
                                        # line=dict(width=2, color = 'black')
                                        ),
                            textfont_size = 17,
                            # fillcolor = 'white',
                            # textfont_color = 'black',
                            textposition='middle center')
        # Add UK average trace to initial frame
        fig.add_trace(ukavg.data[0])
        if animate:
            fig.add_trace(hlines_trace.data[0])
            fig.add_trace(vlines_trace.data[0])
        else:
            fig.add_hline(y=avgUK.loc[0, 'Plot Y'], line_width=1, line_dash="dash", line_color=avgcolors[i])
            fig.add_vline(x=avgUK.loc[0, 'Plot X'], line_width=1, line_dash="dash", line_color=avgcolors[i])
            print()

        if animate:
            # Ensure fig.frames exists
            if fig.frames is None:
                fig.frames = []

            for j, (uk_frame, h_frame, v_frame) in enumerate(zip(ukavg.frames, hlines_trace.frames, vlines_trace.frames)):
                year = int(uk_frame.name)
                for htrace, vtrace in zip(h_frame.data, v_frame.data):
                    htrace.update(line=dict(dash='dash'))
                    vtrace.update(line=dict(dash='dash'))

                # Safely merge with existing frame
                if j < len(fig.frames):
                    frame = fig.frames[j]
                    # Apply to initial traces
                    for trace in frame.data:
                        trace.customdata = trace.customdata
                        trace.hovertemplate = hovertemp
                    for trace in uk_frame.data:
                        trace.customdata = trace.customdata
                        trace.hovertemplate = hovertemp
                    frame.data += uk_frame.data
                    frame.data += h_frame.data
                    frame.data += v_frame.data
                else:
                    fig.frames.append(go.Frame(
                        data=uk_frame.data+h_frame.data+v_frame.data,
                        name=str(year)
                    ))

            fig.update_layout(
                xaxis=dict(range=[x_min, x_max]),
                yaxis=dict(range=[y_min, y_max]),
                updatemenus=[{
                    "type": "buttons",
                    "showactive": True,
                    "buttons": [
                        {
                            "label": "Play",
                            "method": "animate",
                            "args": [
                                None,
                                {
                                    "frame": {"duration": (transition+delay)*1000, "redraw": True},      # Time each year is shown
                                    "transition": {"duration": transition*1000},                 # Delay before next year starts (with animation)
                                    "fromcurrent": True
                                }
                            ]
                        },
                        {
                            "label": "Pause",
                            "method": "animate",
                            "args": [[None], {"frame": {"duration": 0}, "mode": "immediate"}]
                        }
                    ]
                }]
            )

    '''Add scatter labels for selected regions'''
    if highlight != None and not animate:
        highlight = ['<br>'.join(textwrap.wrap(x, width = 15)) for x in highlight]
        dtaHighlight = pd.DataFrame()
        temp = dtaselected.loc[(dtaselected.index.get_level_values('level').isin(levels), slice(None), highlight),:].reset_index()
        dtaHighlight = pd.concat([dtaHighlight, temp], ignore_index=True)
        #Add names with arrow
        for i, v in dtaHighlight.iterrows():
            text = textwrap.wrap(v['name'], width = 20)
            text = '<br>'.join(text)
            fig.add_annotation({
                            'text': '<b>' + v['name'] + '</b>',
                            # 'text': text,
                            'x': v['Plot X'],
                            'y': v['Plot Y'],
                            'font': {'size': 10*size, 'color': 'black'},
                            'showarrow': True,
                            'arrowwidth': 1,
                            'arrowhead': 0,
                            'ay': -50, #This creates a different y-position of the text, so that when the graph is reduced in width the text won't overlap
                            # 'ax': prm['highlight'][v['code']][1],

                            # textangle=0,
                            # xanchor='right',
                            # align:'left',
                            'bgcolor': 'rgba(237, 237, 237,0.0)',
                            'opacity': 1,
                            'xref': "x",
                            'yref': "y"
                        }
                        )


    #Plot formatting
    fig.update_layout(font = {'size': 18*size},
                      showlegend=legend,
                      legend_title = color_level + ' Region',
                      legend_title_font_size = 12*size,
                      legend_font_size = 12*size,
                      plot_bgcolor = 'rgba(237, 237, 237,0.5)',
                      paper_bgcolor = 'white',
                      title = {
                                'text': figure_title, #set main title
                                'x': 0.04,
                                'font_size': 15*size, #Title text size
                                },


                      margin = {
                          'l': 100*size,
                          'r': 100*size,
                          't': 100*size,
                          'b': 100*size,
                          },
                      )

    fig.layout.yaxis.tickformat =  '.1%'
    if compare_rgva_hours:
        fig.update_xaxes(tickformat='.1%')
    else:
        fig.update_xaxes(tickprefix='£')
    fig.update_yaxes(title = yaxistitle, tickfont=dict(size=12*size), title_font=dict(size=12*size))
    fig.update_xaxes(title = xaxistitle, tickfont=dict(size=12*size), title_font=dict(size=12*size))

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(199, 197, 197, 0.2)', zerolinewidth=1, zerolinecolor='rgba(199, 197, 197, 0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(199, 197, 197, 0.2)', zerolinewidth=1, zerolinecolor='rgba(199, 197, 197, 0.2)')

    if xrange != None:
        if compare_rgva_hours:
            xrange = [i / 100 for i in xrange]
        fig.update_xaxes(range=xrange)
    if yrange != None:
        yrange = [i/100 for i in yrange]

        fig.update_yaxes(range=yrange)
    if compare_rgva_hours:
        if xrange is None and yrange is None:
            axis_min = min(x_min, y_min)
            axis_max = max(x_max, y_max)
            padding = (axis_max - axis_min) * 0.05
            if padding == 0:
                padding = 0.01
            xrange = [axis_min - padding, axis_max + padding]
            yrange = xrange
            fig.update_xaxes(range=xrange)
            fig.update_yaxes(range=yrange)
        x_bounds = xrange if xrange is not None else [x_min, x_max]
        y_bounds = yrange if yrange is not None else [y_min, y_max]

    #Update the traces to inlcude the tootlip information
    fig.update_traces(hovertemplate=hovertemp)


    tsize = 12*size

    if compare_rgva_hours:
        line_start = max(min(x_bounds), min(y_bounds))
        line_end = min(max(x_bounds), max(y_bounds))
        if line_start <= line_end:
            fig.add_shape(
                type='line',
                x0=line_start,
                y0=line_start,
                x1=line_end,
                y1=line_end,
                line=dict(color='rgba(80, 80, 80, 0.8)', width=1, dash='dash'),
            )

        fig.add_annotation(dict(font=dict(size=tsize),
                                x=0.01,
                                y=0.97,
                                showarrow=False,
                                text="Increase in productivity",
                                xanchor='left',
                                align='left',
                                opacity=0.8,
                                xref="paper",
                                yref="paper"
                                ))

        fig.add_annotation(dict(font=dict(size=tsize),
                                x=0.99,
                                y=0.03,
                                showarrow=False,
                                text="Decrease in productivity",
                                xanchor='right',
                                align='right',
                                opacity=0.8,
                                xref="paper",
                                yref="paper"
                                ))
    else:
        fig.add_annotation(dict(font=dict(size=tsize),
                                x=0.99,
                                y=0.03,
                                showarrow=False,
                                text="Losing ground",
                                textangle=0,
                                xanchor='right',
                                align='left',
                                opacity=0.8,
                                xref="paper",
                                yref="paper"
                                ))

        fig.add_annotation(dict(font=dict(size=tsize),
                                x=0.99,
                                y=0.97,
                                showarrow=False,
                                text="Steaming ahead",
                                textangle=0,
                                xanchor='right',
                                align='left',
                                opacity=0.8,
                                xref="paper",
                                yref="paper"
                                ))

        fig.add_annotation(dict(font=dict(size=tsize),
                                x=0.01,
                                y=0.97,
                                showarrow=False,
                                text="Catching up",
                                textangle=0,
                                xanchor='left',
                                align='left',
                                opacity=0.8,
                                xref="paper",
                                yref="paper"
                                ))

        fig.add_annotation(dict(font=dict(size=tsize),
                                x=0.01,
                                y=0.03,
                                showarrow=False,
                                text="Falling behind",
                                textangle=0,
                                xanchor='left',
                                align='left',
                                opacity=0.8,
                                xref="paper",
                                yref="paper"
                                ))

    return fig

def scatter_3D(dtaselected, size, start, year, levels, legend, showlabel, color_level, population, z, jobs=False):
    metric = 'Average Annual log percentage change' #options are: 'Percentage change', 'Log percentage change', 'Average Annual Percentage change', 'Average Annual log percentage change'
    itl_string = ','.join(levels)
    figure_title = 'UK ' + itl_string + ' regions<br>' +\
                    '<sup>' + str(year) + ' Nominal smoothed GVA per hour, vs. ' + str(start) + '-' + \
                    str(year) + ' productivity change</sup>'
  
    yaxistitle = str(start) + '-' + str(year) + ' ' + metric + ' in productivity'
    xaxistitle = str(year) + ' output per hour worked (£)'
    with open("src/colormaps.json", "r") as file:
        colour_maps = json.load(file)

    if showlabel:
        labels = 'name'
    else: labels = None

    # Access the individual dictionaries
    if color_level == 'MCA':
        colormap = colour_maps[3]
    else:
        colormap = colour_maps[int(color_level[3]) - 1]
    
    bubble_column = 'Jobs' if jobs else ('Population' if population else None)
    if bubble_column:
        dtaselected['Bubble Size'] = dtaselected[bubble_column]
        if dtaselected['Bubble Size'].max() - dtaselected['Bubble Size'].min() == 0:
            dtaselected['Scaled Bubbles'] = 1
        else:
            dtaselected['Scaled Bubbles'] = (10 + ((dtaselected['Bubble Size'] - dtaselected['Bubble Size'].min()) * (40 - 10)) / (dtaselected['Bubble Size'].max() - dtaselected['Bubble Size'].min())) * size
    else:
        dtaselected['Bubble Size'] = 0
        dtaselected['Scaled Bubbles'] = 1
    
    indicator = z.to_frame().columns[0]
    z = z.reset_index()
    z = z.loc[z['year'] == year].drop(columns='year')
    dtaselected = dtaselected.reset_index(['level', 'name']).join(z.set_index('code'))
    fig = px.scatter_3d(
        dtaselected.reset_index(),
        text=labels,
        x='GVA per hour', 
        y=metric, 
        z=indicator,  # Choose an appropriate third dimension
        color=color_level.lower() + 'name',
        color_discrete_map=colormap,
        custom_data=['name', 'code', 'GVA per hour', metric, 'Bubble Size', 'level', indicator],
        size='Scaled Bubbles',
        width=1200 * size,
        height=900 * size,
    )
    hover_lines = [
        "<b> %{customdata[0]}</b>",
        "%{customdata[5]} code: %{customdata[1]}",
        str(year) + " Productivity: £%{customdata[2]:.4} per hour",
        "Productivity growth: %{customdata[3]:.2%}",
    ]
    if bubble_column:
        hover_lines.append(bubble_column + ": %{customdata[4]:,.0f}")
    hover_lines.append(indicator + ": %{customdata[6]:.2%}")
    hovertemp = "<br>".join(hover_lines)

    fig.update_traces(textposition='top center', textfont_size = 10*size, hovertemplate=hovertemp)

    fig.update_layout(font = {'size': 12},
                      showlegend=legend,
                      legend_title = color_level + ' Region',
                      legend_title_font_size = 12*size,
                      legend_font_size = 12*size,
                      plot_bgcolor = 'rgba(237, 237, 237,0.5)',
                      paper_bgcolor = 'white',
                      title = {
                                'text': figure_title, #set main title
                                'x': 0.04,
                                'font_size': 15*size, #Title text size
                                },


                      margin = {
                          'l': 100*size,
                          'r': 100*size,
                          't': 100*size,
                          'b': 100*size,
                          },
                      )
    fig.layout.yaxis.tickformat =  '.1%'
    fig.update_xaxes(tickprefix='£')

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(199, 197, 197, 0.2)', zerolinewidth=1, zerolinecolor='rgba(199, 197, 197, 0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(199, 197, 197, 0.2)', zerolinewidth=1, zerolinecolor='rgba(199, 197, 197, 0.2)')
    return fig