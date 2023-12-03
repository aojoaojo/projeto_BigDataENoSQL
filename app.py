from pywebio.input import *
from pywebio.output import put_text
import json
import random
from pymongo import MongoClient
from pywebio.output import put_text, popup


# Conexão com o MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["DnD"]
colecao = db["personagem"]

def collect_character_data():
        # Solicitar dados básicos do personagem
    data = input_group("Dados do Personagem", [
        input("Nome", name="nome"),
        select("Classe", ['Guerreiro', 'Mago', 'Arqueiro', 'Healer'], name="vocacao"),
        radio("Sexo", options=['Masculino', 'Feminino', 'Outro'], name="sexo"),
        textarea("Contexto/Historia", name="contexto"),
        input("Idade", type="number", name="idade"),
        textarea("Habilidades", name="habilidades")
    ])

    # Gerar atributos automaticamente
    atributos = {'Inteligência': 0, 'Destreza': 0, 'Força': 0, 'Carisma': 0}
    total_atributos = 36

    while total_atributos > 0:
        for atributo in atributos:
            if total_atributos > 0:
                ponto = random.randint(0, total_atributos)
                atributos[atributo] += ponto
                total_atributos -= ponto

    data['atributos'] = atributos

    # Converter os dados para formato JSON
    json_data = json.dumps(data, indent=4)
    put_text("Dados do personagem em formato JSON:\n" + json_data)

    # Inserir os dados no MongoDB
    colecao.insert_one(data)
    put_text("Dados inseridos no MongoDB com sucesso.")

if __name__ == '__main__':
    collect_character_data()
