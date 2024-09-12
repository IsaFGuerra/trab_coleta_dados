# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

input_file = './wine-raitings-small.csv'

try:
    data_frame = pd.read_csv(input_file, index_col='name')
except FileNotFoundError:
    print("Arquivo CSV não encontrado.")
    data_frame = pd.DataFrame()


def save_data():
    data_frame.to_csv(input_file)


@app.route('/api/data', methods=['GET'])
def get_data():
    if data_frame.empty:
        return jsonify({"error": "Nenhum dado disponível"}), 500

    # Converte o DataFrame para dicionário
    data_as_dict = data_frame.reset_index().to_dict(orient='records')
    return jsonify(data_as_dict)

@app.route('/api/data/<string:name>/<string:notes>', methods=['PATCH'])
def update_data(name, notes):
    # Como os nomes tem espaços, precisa arrumar pra leitura correta
    name = name.replace('%20', ' ')
    notes = notes.replace('%20', ' ') 

    if name in data_frame.index:
        data_frame.loc[name, 'notes'] = notes
        save_data()
        
        data_as_dict = data_frame.reset_index().to_dict(orient='records')
        return jsonify(data_as_dict), 200
    else:
        return jsonify({"error": "Nome do vinho não encontrado"}), 404


@app.route('/api/data/<string:name>', methods=['DELETE'])
def delete_data(name):
    
    if name in data_frame.index:
        name = name.replace('%20', ' ')
        
        data_frame.drop(name, inplace=True)
        save_data()
    
        return jsonify({"message": "Registro deletado com sucesso"}), 200
    else:
        return jsonify({"error": "Nome do vinho não encontrado"}), 404


@app.route('/api/data', methods=['POST'])
def insert_data():
    global data_frame

    #pegar os dados do body
    new_data = request.get_json()

    if data_frame.empty:
        # criar um novo DataFrame caso não tenha ainda
        data_frame = pd.DataFrame(columns=new_data.keys())

    # Cria um DataFrame com os novos dados
    new_data_df = pd.DataFrame([new_data])

    data_frame = pd.concat([data_frame, new_data_df], ignore_index=True)

    # Salvar o DataFrame atualizado de volta ao CSV
    save_data()

    return jsonify({'message': 'Data added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5001)
