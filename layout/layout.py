import base64
# Dash/Plotly/Flask
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import os

#APP_DIR = '/home/michael/Desktop/Biophysics/Dev/KineticsApp'
APP_DIR = os.getcwd()
GEPROM_IMG = APP_DIR + '/img/geprom.png'
UDEM_IMG = APP_DIR + '/img/udem2.png'
TEAM_IMG = APP_DIR + '/img/Lab2014_sm.jpg'
CONFIG_DIR = APP_DIR + '/cfg'
ENCODED_IMG_GEPROM = base64.b64encode(open(GEPROM_IMG, 'rb').read())
ENCODED_IMG_UDEM= base64.b64encode(open(UDEM_IMG, 'rb').read())
ENCODED_IMG_TEAM= base64.b64encode(open(TEAM_IMG, 'rb').read())
RESIDUES = ['Ala (A)', 'Arg (R)', 'Asn (N)', 'Asp (D)', 'Cys (C)', 'Glu (E)',
            'Gln (Q)', 'Gly (G)', 'His (H)', 'Hyp (O)', 'Ile (I)', 'Leu (L)', 'Lys (K)', 'Met (M)', 'Phe (F)',
            'Pro (P)', 'Glp (U)', 'Ser (S)', 'Thr (T)', 'Trp (W)', 'Tyr (Y)', 'Val (V)']

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#e6eeff",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    #"padding": "2rem 1rem",
}

NAV_STYLE = {
    #"margin-left": "10%",
    "margin-right": "2rem",
    #"padding": "2rem 1rem",
}


def produce_sidebar():
    return html.Div(
    [
        html.A("Blunck's Lab", href="http://www.biophys.umontreal.ca/bluncklab/", className="navbar-brand",
               style={"color": "#000061", 'font-size': '37px', 'margin-top': '-20px'}
               ),
        html.Hr(),
        html.P(
            "A Simple UI to Integrate Kinetics Data for Research on Ion Channels (&mutants)",
            className="lead",
            style={'font-size': '1.1rem'}
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Ion Channels Kinetics", href="/page-1", id="page-1-link"),
                dbc.NavLink("About", href="/page-2", id="page-2-link"),
                dbc.NavLink("Contact", href="/page-3", id="page-3-link"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.Div(
            html.A(
                html.Img(
                    src='data:image/png;base64,{}'.format(ENCODED_IMG_GEPROM.decode()),
                    style={
                        "width": "75%",
                        "text-align": "center",
                        "margin-top": "10px"
                        }
                ),
                href="http://www.biophys.umontreal.ca/geprom/"
            ),
            style={
                "padding": "10px",
                "text-align": "center"
            }
        ),
        html.Div(
            html.A(
                html.Img(src='data:image/png;base64,{}'.format(ENCODED_IMG_UDEM.decode()),
                         style={"width": "75%", 'text-align': 'center'}),
                href="https://www.umontreal.ca/"
            ),
            style={
                "padding": "10px",
                "text-align": "center",
                "margin-top": "0px"
            }
        ),
    ],
        style=SIDEBAR_STYLE,
    )


radios_input = dbc.FormGroup(
    [
        dbc.Label("Gating", html_for="example-radios-row", width=2),
        dbc.Col(
            dbc.RadioItems(
                id="gating-radio",
                options=[
                    {"label": "Voltage", "value": "vg"},
                    {"label": "Ligand", "value": "lg"},
                ],
                value="vg"
            ),
            width=10,
        ),
    ],
    row=True,
)

selectivity_input = dbc.FormGroup(
    [
        dbc.Label("Selectivity", html_for="example-radios-row", width=2),
        dbc.Col(
            dcc.Dropdown(
                id='selectivity-dropdown',
                placeholder=f"Select the Ion for which your Channel is Selective",
                searchable=True,
                multi=False,
                options=[
                    {'label': 'Potassium K+', 'value': 'K'},
                    {'label': 'Sodium Na+', 'value': 'Na'},
                    {'label': 'Calcium Ca2+', 'value': 'Ca'},
                    {'label': 'Chloride Cl-', 'value': 'Cl'},
                ]
            ),

            width=10,
        ),
    ],
    row=True,
)

isoform_input = dbc.FormGroup(
    [
        dbc.Label("Isoform", html_for="example-password-row", width=2),
        dbc.Col(
            dcc.Dropdown(
                id="isoform-dropdown",
                placeholder="Search or pick your Channel's Isoform",
            ),
            width=10,
        ),
    ],
    row=True,
)



mutant_input = dbc.FormGroup(
    [
        dbc.Label("WT/Mutant", html_for="mutant-row", width=2),
        dbc.Col(
            dbc.Input(
                id="mutant-input",
                placeholder="Search for WT or the mutated residue",
            ),
            width=5,
        ),
        dbc.Col(
            dcc.Dropdown(
                id="new-residue-dropdown",
                placeholder="Mutant (new) Residue",
                options=[{'label': res, 'value': res} for res in RESIDUES]
            ),
            width=5,
        ),
    ],
    row=True,
)

source_input = dbc.FormGroup(
    [
        dbc.Label("Source", width=1),
        dbc.Col(
            [dbc.Input(id='source-input', placeholder="Please cite your source", type="text"),
                dbc.FormText("Any citation format is ok.")],
                width=11
        ),

    ],
    row=True,
    style={'margin-top': '020px'}
)


email_input = dbc.FormGroup(
    [
        dbc.Label("Email", html_for="example-email-row", width=1,
                  style={'font-style': 'italic', 'text-align': 'right', 'float': 'right'}),
        dbc.Col(
            dbc.Input(
                type="email", id="example-email-row", placeholder="(optional, for internal quality control only)"
            ),
            width=11,
        ),
    ],
    row=True,
)

isoform_subform = dbc.Form([radios_input, selectivity_input, isoform_input, mutant_input], style={'margin-bottom': '0px'})


def produce_kinetics_ui():
    return dbc.Container([
        html.H2('Ion Channels Kinetics Data',
                style={'textAlign': 'center', 'padding': '20px', 'font-size': '36px'}
        ),
        html.H6('This App is still under active construction. We were first focused with Kv and Nav channels, so some \
                channels are missing in the forms/db altogether. We are working on it.',
                style={'textAlign': 'center', 'margin-bottom': '20px', 'font-style': 'italic'}
        ),

        isoform_subform,

        dcc.Tabs(id='mother-tabs', value='select-tab', children=[
            dcc.Tab(label='Insert Data', value='insert-tab'),
            dcc.Tab(label='Consult Data', value='select-tab'),
        ],
        colors={
            "border": "#e6eeff",
            "primary": "#0000c4",
            "background": "#e6eeff"
        },
        style={
            "margin-top": "20px"
        }
        ),
        html.Div(id='tabs-div-container', style={"margin-top": "20px"}),
    ]
    )


def produce_kinetics_subform(type):
    if 'In' in type:
        full_name = 'Inactivation'
    else:
        full_name = 'Activation'
    return dbc.FormGroup(
    [
        dbc.Label(f"V50", html_for="example-email-r33ow", width=1,
                  style={'font-weight': 'bold', 'text-align': 'right', 'float': 'right'}),
        dbc.Col(
            dbc.Input(
                type="number", id=f"{full_name}-V50", placeholder=f"{full_name} V50 (mV)", min=-220, step=0.1
            ),
            width=3,
        ),

        dbc.Label(f"Time", html_for="example-email22-row", width=1,
                    style={'font-weight': 'bold', 'text-align': 'right', 'float': 'right'}),
        dbc.Col(
            dbc.Input(
                type="number", id=f"{full_name}-Time", placeholder=f"{full_name} Time (ms)", min=0.0, step=0.001
            ),
            width=3,
        ),

        dbc.Label('z',
            html_for="example-email22-row", width=1,
            style={'font-weight': 'bold', 'text-align': 'right', 'float': 'right'}),
        dbc.Col(
            dbc.Input(
                type="number", id=f"{full_name}-Z", placeholder=f"{full_name} z", min=0.0, step=0.5
            ),
            width=3,
        ),
    ],
        row=True,
    )


def produce_about_page():
    return dbc.Container([
        html.Div(
            html.A(
                html.H2("Rikard Blunck's Laboratory",
                        style={
                            'textAlign': 'center',
                            'margin-top': '20px',
                            'font-size': '36px',
                            'color': '#514d6b'}
                        ),
                href="http://www.biophys.umontreal.ca/bluncklab/"
            ),
            style={
                "padding": "0px",
                "text-align": "center"
            }
        ),
        dcc.Markdown(
            '''
            [Department of Physics](https://phys.umontreal.ca/accueil/) — [Université de Montréal](https://www.umontreal.ca/)
            ''',
            style={
                "padding": "0px",
                "font-size": "1em",
                "text-align": "center",
                "margin-top": "-3px"
            }),
        html.Div(
            html.A(
                html.Img(
                    src='data:image/png;base64,{}'.format(ENCODED_IMG_TEAM.decode()),
                    style={
                        "width": "80%",
                        "text-align": "center",
                        "margin-top": "-40px"
                        }
                ),
                href="http://www.biophys.umontreal.ca/bluncklab/members.html"
            ),
            style={
                "padding": "30px",
                "text-align": "center"
            }
        ),
        dcc.Markdown(
            '''
           We are a [team](http://www.biophys.umontreal.ca/bluncklab/members.html) of multidisciplinary research scientists studying the molecular mechanisms underlying the function of ion channels as part of [Université de Montréal](https://www.umontreal.ca/)'s Groupe d'Étude des Protéines Membranaires ([GEPROM](http://www.biophys.umontreal.ca/geprom/)).
                    ''',
            style={
                'textAlign': 'center',
                'margin-bottom': '40px',
                'margin-top': '0px',
                "font-size": "1.05rem"
                # 'font-style': 'italic'
            }),

        html.H6("This App serves as an UI to collect and integrate activation and inactivation kinetics data for Ion \
                Channels and their mutants, since the information is so scattered around in the literrature.",

                style={
                    'textAlign': 'center',
                    'margin-bottom': '60px',
                    'font-size': '18px',
                    # 'font-style': 'italic'
                }
            ),

        html.H6("Disclaimer: While we always end up verifying sources and try to maintain high data integrety, there   \
                might be significant delay between then and the time of input. Users are always recommanded to check\
                themselves. We also reserve the right to revoke public access at any time if too much bad information\
                 gets posted.",

                style={
                    'textAlign': 'center',
                    'margin-bottom': '0px',
                    'font-size': '14px',
                    # 'font-style': 'italic'
                }
            ),
    ]
    )


def produce_contact_page():
    return dbc.Container(
    [
        dcc.Markdown('''
            #### For research and collaboration, please address Rikard Blunck at [rikard.blunck@umontreal.ca](mailto:rikard.blunck@umontreal.ca)
            
            ''',
            style={'padding':'40px', 'margin-top':'150px'}),

        dcc.Markdown('''
                ##### To report bugs or for app related questions, please address Michael Morin at [michael.morin.1@umontreal.ca](mailto:michael.morin.1@umontreal.ca)

                ''',
                     style={'padding': '40px'})

    ]

    )