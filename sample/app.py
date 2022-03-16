import dash
import warnings
import os
import dash_bootstrap_components as dbc
from dash import Input, Output, html, dcc

from ..adasher.elements import header
from sample import stats

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


warnings.filterwarnings("ignore")
warnings.simplefilter("ignore", UserWarning)

external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


# layout
layout = list()

layout.append(header('Adasher components'))

content_dict = {
    'stats': stats.get_stats_content(),
    'stats with plots': stats.get_stats_with_plots_content(),
    'styles': stats.get_style_content(),
    'advanced': stats.get_advanced_stats_content()
}


tabs = list()
for name, content in content_dict.items():
    tabs.append(dbc.Tab(id=name, children=content, label=name))

layout.append(dbc.Tabs(id='adasher', children=tabs))
app.layout = html.Div(children=layout)

if __name__ == '__main__':
    app.run_server(debug=False, port=8080, use_reloader=False, host='0.0.0.0')
