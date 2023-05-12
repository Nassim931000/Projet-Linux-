import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import random
 
# Charger le dataset (questions et réponses)
dataset = pd.read_csv('/home/ec2-user/questions_reponses.csv', names=['question', 'answer'])
 
# Initialiser l'application Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
 
# Définir le layout de l'application
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Quiz Python Linux Git'), className="text-center")
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Store(id='question-storage', storage_type='session'),
            html.Div(id='question-area', className="text-center", style={'font-weight': 'bold', 'font-size': '20px'}),
            dcc.Input(id='user-answer', type='text', placeholder='Entrez votre réponse ici', className="form-control mt-3"),
            html.Br(),
            dbc.Button('Vérifier la réponse', id='verify-button', color='primary', className="mt-3 w-100"),
            html.Div(id='result-area', className="text-center mt-3"),
            html.Br(),
            dbc.Button('Nouvelle question', id='new-question-button', color='success', className="mt-3 w-100"),
            html.Div(id='hidden-div', style={'display': 'none'})
        ])
    ]),
], fluid=True)
 
# Sélectionner une question aléatoire
def pick_random_question():
    return dataset.sample(1).iloc[0]
 
# Callback pour afficher une question initiale au chargement de la page et une nouvelle question
@app.callback(
    Output('question-storage', 'data'),
    Output('question-area', 'children'),
    Output('user-answer', 'value'),
    Input('hidden-div', 'n_clicks'),
    Input('new-question-button', 'n_clicks')
)
def update_question(hidden_n_clicks, new_question_n_clicks):
    ctx = dash.callback_context
    if not ctx.triggered or ctx.triggered[0]['prop_id'].split('.')[0] == 'hidden-div':
        question = pick_random_question()
        return question.to_dict(), question['question'], ''
    elif ctx.triggered[0]['prop_id'].split('.')[0] == 'new-question-button':
        question = pick_random_question()
        return question.to_dict(), question['question'], ''
 
# Callback pour vérifier la réponse
@app.callback(
    Output('result-area', 'children'),
    Input('verify-button', 'n_clicks'),
    State('question-storage', 'data'),
    State('user-answer', 'value')
)
def check_answer(n_clicks, question_data, answer):
    if not question_data:
        return "Veuillez d'abord choisir une question."
    correct_answer = str(question_data['answer']).lower().strip()
    if answer.lower().strip() == correct_answer:
        return dbc.Alert('Bonne réponse !', color='success')
    else:
        return dbc.Alert(f'Mauvaise réponse. La bonne réponse était: {correct_answer}.', color='danger')
 
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050, debug=True)
