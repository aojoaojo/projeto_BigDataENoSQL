from pywebio.input import input, select, radio, textarea, input_group
from pywebio.output import put_text, popup
from pywebio import start_server
import json

def collect_character_data():
    while True:
        # Solicitar dados do personagem
        data = input_group("Dados do Personagem Fictício", [
            input("Nome", name="nome"),
            select("Vocação", ['Guerreiro', 'Mago', 'Arqueiro', 'Healer'], name="vocacao"),
            radio("Sexo", options=['Masculino', 'Feminino', 'Outro'], name="sexo"),
            textarea("Contexto/História", name="contexto"),
            input("Idade", type="number", name="idade"),
            textarea("Habilidades", name="habilidades"),
            input("Inteligência", type="number", name="inteligencia", min_value=0, max_value=36),
            input("Destreza ", type="number", name="destreza", min_value=0, max_value=36),
            input("Força ", type="number", name="forca", min_value=0, max_value=36),
            input("Carisma ", type="number", name="carisma", min_value=0, max_value=36)
            
        ])

        # Calcular a soma dos atributos
        total_atributos = data['inteligencia'] + data['destreza'] + data['forca'] + data['carisma']
        
        if total_atributos > 36:
            popup("Erro", "A soma total dos atributos não pode exceder 36. Por favor, redistribua os pontos.")
            continue

        break

    # Converter os dados para formato JSON
    json_data = json.dumps(data, indent=4)
    put_text("Dados do personagem em formato JSON:\n" + json_data)

# Iniciar a coleta de dados
if __name__ == '__main__':
    start_server(collect_character_data, port=8080)
