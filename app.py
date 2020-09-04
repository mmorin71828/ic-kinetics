import base64

# Dash/Plotly/Flask
import dash
from dash.dependencies import Input, Output, State
from flask import Flask, send_from_directory
import dash_core_components as dcc 
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Data wrangling
import numpy as np
import pandas as pd
import json
import os

from layout.layout import *

#APP_DIR = '/home/michael/Desktop/Biophysics/Dev/KineticsApp'
APP_DIR = os.getcwd()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server


app.title = "Kinetics Data Ion Channels"
app.config['suppress_callback_exceptions'] = True

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    #"padding": "2rem 1rem",
}

app.layout = html.Div([
    produce_sidebar(),
    dcc.Location(id="url"),
    html.Div(id="page-content", style=CONTENT_STYLE),

]
)


@app.callback(
    Output("isoform-dropdown", "options"),
    [Input("gating-radio", "value"),
    Input('selectivity-dropdown', 'value')
    ],
)
def isoform_option(gating, ion):
    empty_options = [{'label': '', 'value': ''}]
    if ion is not None:
        if 'vg' in gating:
            if 'K' in ion:
                isoforms = ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '2.1', '2.2', '3.1', '3.2', '3.3',
                            '3.4', '4.1', '4.2', '4.3', '5.1', '6.1', '6.2', '6.3', '6.4', '7.1', '7.2', '7.3', '7.4',
                            '7.5', '8.1', '8.2', '9.1', '9.2', '9.3', '10.1', '10.2', '11.1', '11.2', '11.3', '12.1',
                            '12.2', '12.3']
                return [{"value": f"Kv {x}", "label": f"Kv {x}"} for x in isoforms]

            elif 'Na' in ion:
                isoforms = ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '2', '2.1', '2.2', '2.3', '2.4',
                            '3.1']

                return [{"value": f"Nav {x}", "label": f"Nav {x}"} for x in isoforms]
            else:
                return empty_options
        else:
            return empty_options
    else:
        return empty_options




@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return produce_kinetics_ui()
    elif pathname == "/page-2":
        return produce_about_page()
    elif pathname == "/page-3":
        return produce_contact_page()
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised... The only pages are those accessible "
            f"through the sidebar."),
        ]
    )


def df_to_html_table(df: pd.DataFrame, text_align: object = 'center', header: object = True, padding='10px') -> object:
    """Transforms a Pandas DataFrame to an HTML table using Dash components
    Note: df.to_html() is useless here, as we need the html code wrapped as/by Python objects for Dash server"""

    head = [html.Tr([html.Th(col, style={'text-align': text_align, 'padding': padding}) for col in df.columns])] if header else []
    return html.Table(
                head +
                [html.Tr([
                    html.Td(df.iloc[i][col], style={'text-align': text_align, 'padding': padding}) for col in df.columns
                        ]) for i in range(len(df))],
                # contentEditable='True'
                style={'margin': 'auto'}
            )


def update_db(df, selectivity, isoform, mutant, new_res, act_v50, act_time, inact_v50, inact_time, inact_z, act_z,
              source_input):
    restore_db()

    if 'cl' in selectivity.lower():
        sign = '-'
    else:
        sign = '+'
    new_row = {'selectivity': selectivity+sign, 'isoform': isoform, 'mutant': mutant, 'new_residue': new_res,
               'act_v50': act_v50, 'act_time': act_time, 'inact_v50': inact_v50, 'inact_time': inact_time,
               'act_z':act_z, 'inact_z':inact_z, 'source': source_input}
    new_row = pd.DataFrame(new_row, index=[len(df)])
    new_df = df.append(new_row, ignore_index=True)
    new_df.to_csv('db/test.csv', sep='\t', index=False)
    return new_df

def clear_db():
    df = pd.read_csv('db/test-bk.csv', sep='\t', header=0)
    df[0:0].to_csv('db/test.csv', sep='\t', index=False)
    return True


def restore_db():
    df = pd.read_csv('db/test-bk.csv', sep='\t', header=0)
    df.to_csv('db/test.csv', sep='\t', index=False)
    return df


def filter_db(df, isoform, mutant, selectivity):

    if isoform:
        df = df[df.isoform == isoform]
    if mutant:
        df = df[df.mutant == mutant]

    if selectivity:
        if 'Cl' == selectivity:
            sign = '-'
        else:
            sign = '+'

        df = df[df.selectivity == selectivity + sign]
    return df

@app.callback(
    Output('consult-data-div', 'children'),
    [Input('gating-radio', 'value'),
    Input('selectivity-dropdown', 'value'),
    Input('isoform-dropdown', 'value'),
    Input('mutant-input', 'value'),
    Input('new-residue-dropdown', 'value')
    ]
    )
def render_content(gating_radio, selectivity, isoform, mutant, new_res):

    df = pd.read_csv('db/test.csv', sep='\t', header=0)

    df = filter_db(df, isoform, mutant, selectivity)

    return html.Div([
        html.P('Filter the database with the fields above, or leave empty for all data.'),
        df_to_html_table(df)
    ],
        style={'margin-bottom': '50px'}
    )


@app.callback(
    Output('click-confirmation-div', 'children'),
    [Input('submit-button', 'n_clicks')],
    [
    State('gating-radio', 'value'),
    State('selectivity-dropdown', 'value'),
    State('isoform-dropdown', 'value'),
    State('mutant-input', 'value'),
    State('new-residue-dropdown', 'value'),
    State('Inactivation-V50', 'value'),
    State('Activation-V50', 'value'),
    State('Inactivation-Time', 'value'),
    State('Activation-Time', 'value'),
    State('Inactivation-Z', 'value'),
    State('Activation-Z', 'value'),
    State('source-input', 'value'),
    ]
    )
def render_content(n_clicks, gating_radio, selectivity, isoform, mutant, new_res, inact_v50, act_v50,
                   inact_time, act_time, inact_z, act_z, source_input):
    restore_db()
    if n_clicks:
        try:
            df = pd.read_csv('db/test.csv', sep='\t', header=0)
        except:
            restore_db()
            df = pd.read_csv('db/test.csv', sep='\t', header=0)
        if len(df) == 0:
            restore_db()
        if source_input:

            if source_input == 'secret':
                restored_df = restore_db()
                return html.Div(df_to_html_table(restored_df, padding='15px'), style={'text-align': 'center'})

            else:
                new_df = update_db(df, selectivity, isoform, mutant, new_res, act_v50, act_time, inact_v50, inact_time,
                                   inact_z, act_z, source_input)

                return html.Div(df_to_html_table(new_df), style={'text-align': 'center'})
        else:
            df.to_csv('db/test.csv', sep='\t', index=False)
            return html.Div(
                [
                    df_to_html_table(df, padding='20px')
                ],
                style={'text-align': 'center'}
            )
    else:
        return None


def get_db_cols():
    return list(pd.read_csv('db/test-bk.csv', sep='\t', header=0).columns)


@app.callback(
    Output('hist-selector', 'options'),
    [Input('mother-tabs', 'value')]
)
def render_content(tab):
    db_cols = [x for x in get_db_cols() if x not in ['selectivity', 'isoform', 'mutant', 'new_residue', 'source']]
    df = pd.read_csv('db/test.csv', sep='\t', header=0)
    dff = df[db_cols]

    return [{'label': col, 'value' :col} for col in db_cols]

@app.callback(
    Output('consult-graph', 'figure'),
    [Input('hist-selector', 'value'),
    Input('gating-radio', 'value'),
    Input('selectivity-dropdown', 'value'),
    Input('isoform-dropdown', 'value'),
    Input('mutant-input', 'value'),
    Input('new-residue-dropdown', 'value'),
    ]
)
def render_content(hist_variables, gating_radio, selectivity, isoform, mutant, new_res):

    df = pd.read_csv('db/test.csv', sep='\t', header=0)
    df = filter_db(df, isoform, mutant, selectivity)

    fig = go.Figure()
    for variable in hist_variables:
        fig.add_trace(
            go.Histogram(
                x=df[variable],
                name=variable
            ))

    fig.update_layout(
        title_text=f'Distribution of {hist_variables}',
        title_x=0.5,
        xaxis_title_text='Value',
        yaxis_title_text='Count',
        bargap=0.2,
        bargroupgap=0.1
    )
    return fig


@app.callback(Output('tabs-div-container', 'children'),
              [Input('mother-tabs', 'value')])
def render_content(tab):
    if tab == 'insert-tab':
        return html.Div([
            dcc.Markdown(
                """
                Please enter as many of the following fields and a credible source. (*If you have a lot of data, [email Michael](mailto:michael.morin.1@umontreal.ca), he can mass insert for you*).
                """
            ),
            produce_kinetics_subform(type='Act.'),
            produce_kinetics_subform(type='Inact.'),
            html.Div(source_input, style={"margin-top": "20px"}),
            email_input,
            html.Div(
                dbc.Button(
                    id='submit-button',
                    children='Submit Data!',
                    color="primary",
                    className="btn btn-primary",
                    style={
                        'float': 'center',
                        'margin-bottom': '40px',
                        'text-align': 'center'
                    }
                ),
                style={
                    'float': 'center',
                    'text-align': 'center'
                }
            ),

            html.Div(id='click-confirmation-div')
        ])

    else:
        return html.Div([
            html.Div(id='consult-data-div'),
            html.H6('Select your desired Statistics',
                    style={'textAlign': 'center', 'padding': '20px', 'font-size': '18px', 'margin-top': '90px'}),
            dcc.Dropdown(
                id='hist-selector',
                multi=True,
                value=['act_v50', 'inact_v50'],
                style={
                    'margin-bottom': 'px',
                    #'width': '92.5%',
                    }
            ),

            html.Div([
                dbc.Row([
                    dbc.Col(html.Div(id='stats-table', style={'margin-top': '50px',})),
                    dbc.Col(dcc.Graph(id='consult-graph', style={'margin-top': '0px'})),

                ]),

            ]
            )

        ]),

@app.callback(
    Output('stats-table', 'children'),
    [Input('hist-selector', 'value'),
     Input('gating-radio', 'value'),
     Input('selectivity-dropdown', 'value'),
     Input('isoform-dropdown', 'value'),
     Input('mutant-input', 'value'),
     Input('new-residue-dropdown', 'value'),
     ]
)
def stats_table(selected_variables, gating_radio, selectivity, isoform, mutant, new_res):

    df = pd.read_csv('db/test.csv', sep='\t', header=0)
    df = filter_db(df, isoform, mutant, selectivity)
    stats_df = get_stats(df, selected_variables)
    stats_df = stats_df.round(2)
    return df_to_html_table(stats_df)


def get_stats(df, selected_cols):
    dff = df[selected_cols]
    stats_df = dff.describe()
    stats_df['stats'] = stats_df.index
    cols = list(stats_df.columns)
    cols = [cols[-1]] + cols[:-1]
    stats_df = stats_df[cols]
    return stats_df


if __name__ == "__main__":
    app.run_server(
        port=8050,
        #dev_tools_ui=False, dev_tools_props_check=False,
        debug=True,
        )