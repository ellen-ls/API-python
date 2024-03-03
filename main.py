from flask import Flask, request, jsonify, render_template
import requests
import uuid
import json

app = Flask(__name__)

# Função para obter os dados de um Pokémon da PokéAPI
def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_data = {
            'id': data['id'],
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
pokemon_list = get_pokemon_list()

# Dicionário para armazenar os times de Pokémon na memória
teams = {}

# Rota para criar ou atualizar um time de Pokémon
@app.route('/api/teams', methods=['POST'])
def criar_ou_atualizar_time():
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
        
        # Se o time existir, informar que o time já existe
        if existing_team_id:
            return jsonify({'error': 'Este usuário já possui um time registrado.'}), 400

        # Criar um novo time
        new_team_id = str(uuid.uuid4())
        new_pokemons = []
        for pokemon_name in team:
            pokemon_data = get_pokemon_data(pokemon_name)
            if pokemon_data:
                new_pokemons.append(pokemon_data)
            else:
                return jsonify({'error': f'Pokémon "{pokemon_name}" não encontrado.'}), 404
        teams[new_team_id] = {'owner': user, 'pokemons': new_pokemons}
        return jsonify({'message': 'Time de Pokémon criado e salvo com sucesso!', 'id': new_team_id}), 201

    else:
        return jsonify({'error': 'Usuário e lista de Pokémon são campos obrigatórios.'}), 400

# Rota para listar todos os times registrados
@app.route('/api/teams', methods=['GET'])
def listar_times():
    return jsonify(teams)

# Rota para buscar um time por usuário
@app.route('/api/teams/<user>', methods=['GET'])
def buscar_time_por_usuario(user):
    user_teams = {team_id: team_data for team_id, team_data in teams.items() if team_data['owner'] == user}
    if user_teams:
        return jsonify(user_teams)
    else:
        return jsonify({'error': 'Usuário não possui times registrados.'}), 404

# Rota para renderizar o template HTML
@app.route('/')
def index():
    return render_template('index.html', pokemon_list=pokemon_list)

if __name__ == '__main__':
    app.run(debug=True)








# from flask import Flask, request, jsonify, render_template
# import requests
# import uuid

# app = Flask(__name__)

# # Função para obter a lista de Pokémons da PokéAPI
# def get_pokemon_list():
#     url = "https://pokeapi.co/api/v2/pokemon?limit=1000"  # Limitado a 1000 Pokémons para simplificar
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         pokemon_list = [pokemon['name'] for pokemon in data['results']]
#         return pokemon_list
#     else:
#         return None

# # Dicionário para armazenar os times de Pokémon na memória
# usuarios = {}

# # Função para obter dados de um Pokémon da PokéAPI
# def get_pokemon_data(pokemon_name):
#     url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return None

# # Rota para o usuário criar um novo time de Pokémon
# @app.route('/criar_time', methods=['POST'])
# def criar_time():
#     data = request.json
#     if 'usuario' in data and 'pokemons' in data:
#         usuario = data['usuario']
#         pokemons = data['pokemons']
#         time = []
#         for pokemon in pokemons:
#             pokemon_data = get_pokemon_data(pokemon)
#             if pokemon_data:
#                 time.append({
#                     'nome': pokemon_data['name'],
#                     'tipo': [tipo['type']['name'] for tipo in pokemon_data['types']]
#                 })
#             else:
#                 return jsonify({'error': f'Pokémon "{pokemon}" não encontrado.'}), 404
        
#         # Gerar uma ID única para identificar o time
#         time_id = str(uuid.uuid4())
        
#         # Salvar o time com a ID única
#         usuarios[time_id] = {'usuario': usuario, 'time': time}
        
#         # Retornar a mensagem de validação e a ID única
#         return jsonify({'message': 'Time de Pokémon criado e salvo com sucesso!', 'id': time_id}), 201
#     else:
#         return jsonify({'error': 'Usuário e lista de Pokémon são campos obrigatórios.'}), 400

# # Rota para a página principal
# @app.route('/')
# def index():
#     pokemon_list = get_pokemon_list()
#     if pokemon_list:
#         return render_template('index.html', pokemon_list=pokemon_list, times=usuarios)
#     else:
#         return jsonify({'error': 'Falha ao obter a lista de Pokémons.'}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
