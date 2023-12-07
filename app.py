import time
import random
from json import dumps
from pywebio import session, config
from pymongo import MongoClient
from pywebio.input import *
from pywebio.output import *


# Conexão com o MongoDB
client = MongoClient("mongodb://root:mongo@localhost:27017")
db = client["DnD"]
colecao = db["personagem"]
dbSpell = client["DnD"]
colecaoSpell = db["Spells"]
colecaoClasses = db["Classes"]
colecaoSubclasses = db["Subclasses"]

css = """
#pywebio-scope-direita {
    height: calc(100vh - 150px);
    overflow-y: hidden;
}
#pywebio-scope-direita:hover {
    overflow-y: scroll;
    background: gray;
}
#pywebio-scope-esquerda {
    height: calc(100vh - 150px);
    overflow-y: hidden;
}
#pywebio-scope-esquerda:hover {
    overflow-y: scroll;
}
/* Works on Firefox */
* {
  scrollbar-width: thin;
}
/* Works on Chrome, Edge, and Safari */
*::-webkit-scrollbar {
  width: 7px;
}
*::-webkit-scrollbar-track {
  background: gray;
}
*::-webkit-scrollbar-thumb {
  background-color: gray;
  border-radius: 20px;
  border: 2px
}
"""

@config(theme="minty", css_style=css)
def main():
    menu()
    
def get_classes():
    query = {}
    result = colecaoClasses.find(query)
    classes = []
    result = result[0]['results']

    for row in result:
        classes.append(row['name'])

    return classes

def get_subclasses():
    query = {}
    result = colecaoSubclasses.find(query)
    subclasses = []
    result = result[0]['results']

    for row in result:
        subclasses.append(row['name'])
        
    return subclasses

@use_scope('direita', clear=True)
def printar_classes(classes):
    close_popup()
    put_markdown('## Classes disponiveis: ')
    for classe in classes:
        put_markdown('### ' + classe)

@use_scope('direita', clear=True)
def printar_subclasses(subclasses):
    close_popup()
    put_markdown('## Subclasses disponiveis: ')
    for subclasse in subclasses:
        put_markdown('### ' + subclasse)

def gerar_atributos(data):
    # Gerar atributos aleatoriamente
    
    atributos = {'Inteligencia': 0, 'Destreza': 0, 'Forca': 0, 'Carisma': 0, 'Sabedoria': 0, 'Constituicao': 0}

    for atributo in atributos:
        ponto = random.randint(1, 20)
        atributos[atributo] += ponto

    data['atributos'] = atributos
    
    inserir_no_banco(data)


 
@config(theme="minty", css_style=css)
def menu():
    session.set_env(title='DnD', output_max_width='100%')
    
    # Separa em duas colunas
    put_row(
        [put_scope('esquerda'), None, put_scope('direita')],
        size="2fr 40px minmax(60%, 6fr)",
    )

    # Coluna inicial da esquerda (menu)
    with use_scope('esquerda'):
        put_markdown("## Selecione a opção desejada:")
        put_button(['Criar personagem'], onclick = lambda: collect_character_data())
        put_button(['Mostrar todas as Spells'], onclick = lambda: get_spell())
        put_button(['Pesquisar por Spell'], onclick = lambda: get_spell_especifica())
        put_button(['Mostrar todas as classes'], onclick = lambda: printar_classes(get_classes()))
        put_button(['Mostrar todas as Subclasses'], onclick = lambda: printar_subclasses(get_subclasses()))
    
    # Coluna inicial da direita (imagem e mensagem de boas vindas)
     
    with use_scope('direita'):
        img = open('DnD.jpg', 'rb').read()  
        put_image(img, width='1220px')
        put_html('<div style="text-align:center;"><p style="font-size: 30px; font-weight: bold;">Bem-vindo(a) ao Dungeons and Dragons!</p></div>')

# Solicitar dados básicos do personagem, do lado direito
@use_scope('direita', clear=True)
def collect_character_data():
    with use_scope('direita'):
        data = input_group("Dados do Personagem", [
            input("Nome", name="nome"), # nome
            select("Classe", get_classes(), name="classe"), # Classe
            select("Subclasse", get_subclasses(), name="subclasse"), # Subclasse
            radio("Sexo", options=['Masculino', 'Feminino', 'Outro'], name="sexo"), # Sexo
            textarea("Contexto/Historia", name="contexto"), # Historia
            input("Idade", type="number", name="idade"), # Idade
            textarea("Habilidades", name="habilidades") # Habilidades
        ])
    
    # Gerar atributos aleatoriamente
    gerar_atributos(data)    
    
# Inserir dados coletados no Mongo
@use_scope('direita', clear=True)
def inserir_no_banco(data):

    # Printa atributos
    for atrib in data['atributos']:
        put_markdown('## ' + atrib + ': ' + str(data['atributos'][atrib]))
    
    put_markdown("### dados inseridos com sucesso\n")
    
    # Inserir os dados no MongoDB
    colecao.insert_one(data)

# Pega todas as spells no mongo
@use_scope('direita', clear=True)
def get_spell():
    close_popup()
    # Consultar spells no Mongodb    
    query = {}
    result = colecaoSpell.find(query)
    
    # Printa todas as spells
    put_markdown('## Spells disponiveis: ')
    for document in result:
        put_markdown('### ' + document['name'])
        # put_markdown('#### ' + document['description'])

# Procura por spell específica no mongo
@use_scope('direita', clear=True)
def get_spell_especifica():
    # Consultar spells no Mongodb    
    query = {}
    result = colecaoSpell.find(query)
    
    pesquisa = input_group('spell', [input("Spell:", name="pesquisa")])
    put_markdown('## Spell buscada: ')
    
    for document in result:
        if pesquisa['pesquisa'] in document['name'].lower():
            put_markdown('### ' + document['name'])
            put_markdown('#### ' + document['description'])


if __name__ == '__main__':
    main()