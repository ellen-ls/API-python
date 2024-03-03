from flask import Flask, request, jsonify, render_template
import requests
import uuid

app = Flask(__name__)

# Função para obter os dados de um Pokémon da PokéAPI
def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_data = {
            'name': data['name'],
            'weight': data['weight'],
            'height': data['height']
        }
        return pokemon_data
    else:
        return None

# Função para validar o nome de um Pokémon
def is_valid_pokemon_name(pokemon_name):
    return isinstance(get_pokemon_data(pokemon_name), dict)

# Função para obter a lista de Pokémons da PokéAPI
def get_pokemon_list():
    url = "https://pokeapi.co/api/v2/pokemon?limit=1000"  # Limitado a 1000 Pokémons para simplificar
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_list = [pokemon['name'] for pokemon in data['results']]
        return pokemon_list
    else:
        return None

# Lista de Pokémons pré-carregada
pokemon_list = ["bulbasaur", "charmander", "squirtle", "pikachu", "jigglypuff", "meowth"]

# Dicionário para armazenar os times de Pokémon na memória
teams = {}

# Rota para criar ou atualizar um time de Pokémon
@app.route('/api/teams', methods=['POST'])
def create_or_update_team():
    data = request.form
    if 'user' in data and 'team[]' in data:
        user = data['user']
        team = data.getlist('team[]')

        # Verificar se todos os nomes dos Pokémon na equipe são válidos
        if not all(is_valid_pokemon_name(pokemon_name) for pokemon_name in team):
            return jsonify({'error': 'Um ou mais nomes de Pokémon são inválidos.'}), 400

        # Verificar se o usuário já possui um time registrado
        existing_team_id = None
        for team_id, team_data in teams.items():
            if team_data['owner'] == user:
                existing_team_id = team_id
                break

        # Se o time existir, adicionar os novos Pokémon e verificar duplicatas
        if existing_team_id:
            existing_team = teams[existing_team_id]['pokemons']
            for pokemon_name in team:
                if any(pokemon['name'] == pokemon_name for pokemon in existing_team):
                    return jsonify({'error': f'O Pokémon "{pokemon_name}" já está na lista de times.'}), 400
                else:
                    pokemon_data = get_pokemon_data(pokemon_name)
                    existing_team.append(pokemon_data)
            return jsonify({'message': 'Novos Pokémon adicionados ao time existente!'}), 200

        # Se o time não existir, criar um novo time
        else:
            new_team_id = str(uuid.uuid4())
            new_pokemons = [get_pokemon_data(pokemon_name) for pokemon_name in team]
            teams[new_team_id] = {'owner': user, 'pokemons': new_pokemons}
            return jsonify({'message': 'Novo time de Pokémon criado e salvo com sucesso!', 'id': new_team_id}), 201

    else:
        return jsonify({'error': 'Usuário e lista de Pokémon são campos obrigatórios.'}), 400

# Rota para listar todos os times registrados
@app.route('/api/teams', methods=['GET'])
def list_teams():
    return jsonify(teams)

# Rota para buscar um time por usuário
@app.route('/api/teams/<user>', methods=['GET'])
def get_team_by_user(user):
    user_teams = {team_id: team_data for team_id, team_data in teams.items() if team_data['owner'] == user}
    if user_teams:
        return jsonify(user_teams)
    else:
        return jsonify({'error': 'Usuário não possui times registrados.'}), 404

# Rota para renderizar o template HTML
@app.route('/')
def index():
    pokemon_list = get_pokemon_list()

    return render_template('index.html', teams=teams,pokemon_list=pokemon_list)

if __name__ == '__main__':
    app.run(debug=True)
