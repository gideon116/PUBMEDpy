from pymed import PubMed
import json
from dash import no_update
import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import os



def pubtator(output): # output should be "for1", "for2", or "for3"
    pubb = output

    id = '30670346'
    base_url = ["https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/"]

    # pubtator (only accepts PMIDs)
    if pubb == "for1":
        if id[:2] == "PM":
            del base_url[0]
            base_url.append("pubtator does not accept PMCIDs, please provide a PMID")
        else:
            base_url.append("pubtator?pmids=28483577&concepts=gene")

    # BioC-XML
    if pubb == 'for2':
        if id[:2] == "PM":
            base_url.append("biocxml?pmcids=" + id)
        else:
            base_url.append("biocxml?pmids=" + id)

    # BioC-JSON
    if pubb == 'for3':
        if id[:2] == "PM":
            base_url.append("biocjson?pmcids=" + id)
        else:
            base_url.append("biocjson?pmids=" + id)

    if base_url[0] == "pubtator does not accept PMCIDs, please give the PMID":
        return "pubtator does not accept PMCIDs, please give the PMID"
    else:
        response = requests.get("".join(base_url))
        s = response.text
        print(s)


def pymedd(keyword,
           # max_results
           ):

    pubmed = PubMed(tool="MyTool", email="my@email.address")
    query = str(keyword)
    number_of_results = pubmed.getTotalResultsCount(query)
    results = pubmed.query(query,
                           # max_results=max_results
                           )

    abstracts = []
    titles = ''

    PMIDs = ''
    PMIDs_list = []

    for article in results:
        json1 = article.toJSON()
        dict1 = json.loads(json1)

        abstract = dict1.get('abstract')
        title = dict1.get('title')

        PMID = dict1.get('pubmed_id')
        PMIDs_list.append(dict1.get('pubmed_id'))

        abstracts.append(abstract)
        titles = titles + title + '\n'
        PMIDs = PMIDs + PMID + '\n'

    return PMIDs, number_of_results


def main():

    keyword = input("Please enter a keyword  "+'\n')
    print('_______________________________________')
    directr = input("Please give the directory of where you want to save the file "+'\n')
    print('_______________________________________')

    """
    #result_number = input("Please choose how many results you want to see?  ")
    """
    output, totno = pymedd(str(keyword),
                           # int(result_number)
                           )
    print('_______________________________________')
    print('\n'+"total number of results = "+str(totno)+'\n')

    """
    print('_______________________________________')
    print(str(output))
    print('_______________________________________')

    file1 = open("/Users/gideon/Downloads/pmid-biofilmgro-set-2.txt")
    list_from_search = file1.read()

    
    print(set(list(list_from_search)).difference((output)))
    print(np.asarray(list_from_search).tolist())
    """

    with open(str(directr)+"PUBMEDpy-output.txt", "w") as outputs:
        outputs.write(str(output))


main()


def serve_layout():

    # App Layout
    return html.Div(
        id="root",
        children=[
            # Main body
            html.Div([
                html.Div(
                    id="app-container",
                    children=[
                        html.Div(
                            id="banner",
                            children=[html.H2("PubmedPy", id="title", style={'font-weight': 300,
                                                                                  "textAlign": "center",
                                                                          'border': 'thin black dash',
                                                                          'margin-bottom': '5px',
                                                                          'width': '1000px',
                                                                          'backgroundColor': 'rgb(240,240,240)',
                                                                          })]
                            ,
                        ),
                        html.Div(id="do", children=[
                            html.Table(id="nooutput", style={
                                'padding': 50,
                                'margin': 5,
                                'borderRadius': 5,
                                'border': 'thin black solid',
                                'margin-bottom': '5px',
                                'width': '920px',
                                'backgroundColor': 'rgb(230,230,230)',

                                # Remove possibility to select the text for better UX
                                'user-select': 'none',
                                '-moz-user-select': 'none',
                                '-webkit-user-select': 'none',
                                '-ms-user-select': 'none'
                            }),

                            html.Table(id="output", style={
                                'padding': 50,
                                'margin': 5,
                                'borderRadius': 5,
                                'border': 'thin black solid',
                                'margin-bottom': '5px',
                                'width': '920px',
                                'backgroundColor': 'rgb(230,230,230)',

                                # Remove possibility to select the text for better UX
                                'user-select': 'none',
                                '-moz-user-select': 'none',
                                '-webkit-user-select': 'none',
                                '-ms-user-select': 'none'
                            })
                        ]),
                    ],
                ),
            ], className='eight columns', style={'backgroundColor': 'rgb(200,200,200)', 'height': '1000px'}),

            # Sidebar
            html.Div([
                html.Div(
                    id="sidebar",
                    children=[
                        html.Section(
                            children=[
                                html.Div(
                                    dcc.Dropdown(
                                        id="searchtype",
                                        options=[
                                            {"label": "PCMID", "value": "1"},
                                            {"label": "Keyword", "value": "2"}],
                                        searchable=False,
                                        placeholder="Projects",
                                        value='0'
                                    ),
                                    style={'margin-top': '5px', 'margin-bottom': '5px'}
                                ),
                                html.Div(
                                    dcc.Textarea(
                                        id="inputs",
                                        placeholder='Search'

                                    ),
                                    style={'margin-top': '5px', 'margin-bottom': '5px'}
                                ),
                                html.Div(
                                    dcc.Textarea(
                                        id="number of results",
                                        placeholder='Number of Results',
                                        name="wow",
                                        title="wows",
                                        value='0'

                                    ),
                                    style={'margin-top': '5px', 'margin-bottom': '5px'}
                                ),
                                html.Div(
                                    id="button-group",
                                    children=[
                                        html.Button(
                                            "Run Operation", id="button-run-operation",
                                            style={'color': 'rgb(0,0,0)',
                                                   'margin': 5},
                                            n_clicks_timestamp=0
                                        ),
                                        html.Button("Undo", id="button-undo",
                                                    style={'color': 'rgb(0,0,0)'},
                                                    n_clicks_timestamp=0),
                                    ],
                                ),
                            ],
                            style={
                                'padding': 20,
                                'margin': 5,
                                'borderRadius': 5,
                                'border': 'thin black solid',
                                'margin-bottom': '5px',

                                # Remove possibility to select the text for better UX
                                'user-select': 'none',
                                '-moz-user-select': 'none',
                                '-webkit-user-select': 'none',
                                '-ms-user-select': 'none'
                            }),
                    ])
            ], className='four columns', style={
                                                'height': '1000px'}),

        ], className='row'
    )


colors = {
    'background': '#444444',
    'text': '#7FDBFF'
}


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server
app.layout = serve_layout


@app.callback([dash.dependencies.Output('output', 'children'),
               dash.dependencies.Output('nooutput', 'children')],
              [dash.dependencies.Input('searchtype', 'value'),
               dash.dependencies.Input('inputs', 'value'),
               dash.dependencies.Input('number of results', 'value'),
               dash.dependencies.Input('button-run-operation', 'n_clicks_timestamp'),
               dash.dependencies.Input('button-undo', 'n_clicks_timestamp')])
def expp(searchtype, inputs, noresults, run, undo):
    result, nooutput = pymedd(inputs, int(noresults))

    if int(searchtype) == 2:
        if int(run) > 0:

            if int(run) > int(undo):
                return result, nooutput

            elif int(undo) > int(run):
                return no_update, no_update
            else:
                return no_update, no_update
        else:
            return no_update, no_update
    else:
        if int(run) > 0:
            if int(run) > int(undo):
                return no_update, no_update
            else:
                return no_update, no_update
        else:
            return no_update, no_update


#if __name__ == "__main__":
    #app.run_server(host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", "8060")), debug=True, )


