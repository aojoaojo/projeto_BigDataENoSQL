from pywebio.input import *
from pywebio.output import put_text
import json
import random
from pymongo import MongoClient
from pywebio.output import put_text, popup, put_markdown, clear
import time

# Conexão com o MongoDB
client = MongoClient("mongodb://root:mongo@localhost:27017")
db = client["DnD"]
colecao = db["personagem"]
dbSpell = client["DnD"]
colecaoSpell = db["Spells"]


def main():
    data = collect_character_data()
    converter_para_json(data)
    consultar_spell(data)




def collect_character_data():
        # Solicitar dados básicos do personagem
    data = input_group("Dados do Personagem", [
        input("Nome", name="nome"),
        select("Classe", ['Artificer', 'Sorcerer', 'Wizard', 'Bard', 'Warlock', 'Druid', 'Cleric', 'Ranger', 'Paladin'], name="classe"),
        radio("Sexo", options=['Masculino', 'Feminino', 'Outro'], name="sexo"),
        textarea("Contexto/Historia", name="contexto"),
        input("Idade", type="number", name="idade"),
        textarea("Habilidades", name="habilidades")
    ])

    # Gerar atributos automaticamente
    atributos = {'Inteligencia': 0, 'Destreza': 0, 'Forca': 0, 'Carisma': 0}
    total_atributos = 36

    while total_atributos > 0:
        for atributo in atributos:
            if total_atributos > 0:
                ponto = random.randint(0, total_atributos)
                atributos[atributo] += ponto
                total_atributos -= ponto

    data['atributos'] = atributos
    
    return data




def converter_para_json(data):
    # Converter os dados para formato JSON
    # json_data = json.dumps(data, indent=4)
    put_markdown("# Os seus atributos foram:\n")
    for atrib in data['atributos']:
        put_markdown('### ' + atrib + ': ' + str(data['atributos'][atrib]))
    
    # Inserir os dados no MongoDB
    colecao.insert_one(data)
    time.sleep(1)
    clear()
    # put_text("Dados inseridos no MongoDB com sucesso.")





def consultar_spell(data):
    # Consultar spells no Mongodb
    
    query = {}
    result = colecaoSpell.find(query)
    
    put_markdown('## Spells disponiveis para a sua classe: ')
    for document in result:
        if data['classe'] in document['classes']:
            put_markdown('### ' + document['name'])
            put_markdown('#### ' + document['description'])



if __name__ == '__main__':
    main()