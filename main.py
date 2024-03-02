from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import uuid

app = Flask(__name__)

# Lista para armazenar os usuários registrados
registered_users = []

# Dicionário para armazenar os times de Pokémon, onde a chave é a ID única do time
pokemon_teams = {}

# Função para obter informações de um Pokémon da PokeAPI
def get_pokemon_info(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_info = {
            'name': data['name'],
            'height': data['height'],
            'weight': data['weight'],
            'type': ', '.join([type_info['type']['name'] for type_info in data['types']]),
            'abilities': ', '.join([ability_info['ability']['name'] for ability_info in data['abilities']]),
            'stats': ', '.join([f"{stat['stat']['name']}: {stat['base_stat']}" for stat in data['stats']])
        }
        return pokemon_info
    else:
        return None

# Rota principal, onde os usuários podem adicionar Pokémon aos times
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'register' in request.form:  # Se o formulário for submetido para registro de usuário
            username = request.form['username']
            registered_users.append(username)
            return redirect(url_for('index'))

        if 'add_pokemon' in request.form:  # Se o formulário for submetido para adicionar Pokémon ao time
            username = request.form['username']
            pokemon_names = request.form['pokemon_names'].split(',')
            user_team = []
            for pokemon_name in pokemon_names:
                pokemon_info = get_pokemon_info(pokemon_name.strip())
                if pokemon_info:
                    user_team.append(pokemon_info)
                else:
                    return "Erro: Pokémon não encontrado."
            team_id = str(uuid.uuid4())  # Gerando uma ID única para o time
            
            pokemon_teams[team_id] = {'username': username, 'team': user_team}
            return f"Time salvo com sucesso! ID do time: {team_id}"

    return render_template('index.html', team=pokemon_teams, users=registered_users)

# Rota para registro de usuários
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        registered_users.append(username)
        return redirect(url_for('index'))
    return render_template('register.html')

# Rota para obter todos os times de Pokémon registrados
@app.route('/teams', methods=['GET'])
def get_teams():
    return jsonify(pokemon_teams)

# Rota para obter um time de Pokémon específico pelo ID
@app.route('/team/<team_id>', methods=['GET'])
def get_team(team_id):
    if team_id in pokemon_teams:
        return jsonify(pokemon_teams[team_id])
    else:
        return "Time não encontrado.", 404

if __name__ == '__main__':
    app.run(debug=True)