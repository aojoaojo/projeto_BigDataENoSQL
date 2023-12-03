from pywebio.input import *

    
nome = input("Digite o nome do seu personagem: ", type=TEXT)
classe = select("Escolha a classe do seu personagem: ", ['Guerreiro', 'Mago', 'Arqueiro'])
genero = checkbox("Escolha o seu gênero:", options=["Masculino",'Feminino','Corno','Doido'])
# radio("Select any one", options=['1', '2', '3'])
# textarea('Text Area', rows=3, placeholder='Multiple line text input')



with open('personagem.txt', 'w') as f:
    code = f.write(f'Nome: {nome}\nClasse: {classe}\nGenero: {genero}\n')

f.close()