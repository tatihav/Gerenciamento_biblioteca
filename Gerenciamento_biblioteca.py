import json
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Livro:
    def __init__(self, id, titulo, autor, ano, isbn, disponivel=True):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.isbn = isbn
        self.disponivel = disponivel

    def exibir_informacoes(self):
        status = "Disponível" if self.disponivel else "Emprestado"
        print(f"ID: {self.id}, Título: {self.titulo}, Autor: {self.autor}, Ano: {self.ano}, ISBN: {self.isbn}, Status: {status}")
class Usuario:
    def __init__(self, id, nome, email, telefone):
        self.id = id
        self.nome = nome
        self.email  = email
        self.telefone = telefone
    def exibir_informacoes(self):
        print(f"ID: {self.id}, Nome: {self.nome}, Email: {self.email}, Telefone: {self.telefone}")
class Emprestimo:
    def __init__(self, id, usuario_id, livro_id, data_emprestimo, data_devolucao=None):
        self.id = id
        self.usuario_id = usuario_id
        self.livro_id = livro_id
        self.data_emprestimo = data_emprestimo
        self.data_devolucao = data_devolucao
    def exibir_informacoes(self):
        status = "Devolvido" if self.data_devolucao else "Pendende"
        print(f"ID: {self.id}, Usuário ID: {self.usuario_id}, Livro ID: {self.livro_id}, Data Emprestimo: {self.data_emprestimo}, Data Devolução: {self.data_devolucao}, Status: {status}")
    
def carregar_dados(nome_arquivo):
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, 'r') as arquivo:
                return json.load(arquivo)
        else:
            return []
def salvar_dados(nome_arquivo, dados):
        with open(nome_arquivo, 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)
    
def cadastrar_livro(livros):
    id = len(livros) + 1
    titulo  = input("Título do Livro: ")
    autor = input("Autor: ")
    ano = input("Ano de Publicação: ")
    isbn = input("ISBN: ")
    livro = Livro(id, titulo, autor, ano, isbn)
    livros.append(livro.__dict__)
    salvar_dados('livros.json', livros)
    logging.info(f"Livro '{titulo}' cadastrado com sucesso!")
def listar_livros(livros):
    print("\n=== Lista de Livros ===")
    for livro_dict in livros:
            livro = Livro(**livro_dict)
            livro.exibir_informacoes()
def cadastrar_usuario(usuarios):
        id = len(usuarios) + 1
        nome = input("Nome do Usuário: ")
        email = input("Email: ")
        telefone = input("Telefone: ")
        usuario = Usuario(id, nome, email, telefone)
        usuarios.append(usuario.__dict__)
        salvar_dados('usuarios.json', usuarios)
        logging.info(f"Usuário '{nome}' cadastrado com sucesso!")
def listar_usuarios(usuarios):
        print("\n=== Lista de Usuários ===")
        for usuario_dict in usuarios:
            usuario = Usuario(**usuario_dict)
            usuario.exibir_informacoes()
def emprestar_livro(emprestimos, livros, usuarios):
        id = len(emprestimos) + 1
        usuario_id = int(input("ID do usuário: "))
        livro_id = int(input("ID do Livro: "))
        usuario_existente = any(u['id'] == usuario_id for u in usuarios)
        if not usuario_existente:
            print("Usuário não encontrado!")
            return
        livro = next((l for l in livros if l['id'] == livro_id), None)
        if not livro:
            print("Livro não encontrado!")
            return
        if not livro['disponivel']:
            print("Livro não está disponível para empréstimo!")
            return
        data_emprestimo = datetime.now().strftime('%d/%m/%Y')
        emprestimo = Emprestimo(id, usuario_id, livro_id, data_emprestimo)
        emprestimos.append(emprestimo.__dict__)
        livro['disponivel'] = False
        salvar_dados('emprestimos.json', emprestimos)
        salvar_dados('livros.json', livros)
        logging.info(f"Livro ID {livro_id} emprestimo para Usuário ID {usuario_id}.")
def devolver_livro(emprestimos, livros):
        id_emprestimo = int(input("ID do emprestimo: "))
        emprestimo = next((e for e in emprestimos if e['id'] == id_emprestimo), None)
        if not emprestimo:
            print("Emprestimo não encontrado.")
            return
        if emprestimo['data_devolucao']:
            print("Livro já devolvido.")
            return
        data_devolucao = datetime.now().strftime('%d/%m/%Y')
        emprestimo['data_devolucao'] = data_devolucao
        livro_id = emprestimo['livro_id']
        livro = next ((l for l in livros if l['id'] == livro_id), None)
        if livro:
            livro['disponivel'] = True
        salvar_dados('emprestimos.json', emprestimos)
        salvar_dados('livros.json', livros)
        logging.info(f"Livro ID {livro_id} devolvido pelo usuário ID {emprestimo['usuario_id']}.")
def listar_emprestimos(emprestimos):
        print("\n=== Lista de Empréstimos")
        for emprestimo_dict in emprestimos:
            emprestimo = Emprestimo(**emprestimo_dict)
            emprestimo.exibir_informacoes()
def pesquisar_livros(livros):
     termo = input("Digite o termo de pesquisa para livros: ").lower()                                      
     resultados = [l for l in livros if termo in l['titulo'].lower()or termo in l['autor'].lower()]
     if resultados:
          print(f"\n=== Resultados da pesquisa por Livros: '{termo}' ===")
          for livro_dict in resultados:
               livro = Livro(**livro_dict)
               livro.exibir_informacoes()
     else:
        print("Nenhum livro encontrado com o termo especificado.")
def pesquisar_usuarios(usuarios):
     termo = input("Digite o termo de pesquisa para usuários: ").lower() 
     resultados = [u for u in usuarios if termo in u['nome'].lower() or termo in u['email'].lower()]
     if resultados:
          print(f"\n=== Resultados da pesquisa por usuários: '{termo}'=== ")
          for usuario_dict in resultados:
               usuario = Usuario(**usuario_dict)
               usuario.exibir_informacoes()
     else:
          print("Nenhum usuário encontrado com o termo especificado.")
def gerar_relatorio_emprestimos(emprestimos, usuarios, livros):
     print("\n=== Relatório de Empréstimo ===")
     for emprestimo_dict in emprestimos:
          emprestimo = Emprestimo(**emprestimo_dict)
          usuario = next((u for u in usuarios if u['id']==emprestimo.usuario_id), None)
          livro = next((l for l in livros if l['id'] == emprestimo.livro_id), None)
          if usuario and livro:
               status = "Devolvido" if emprestimo.data_devolucao else "Pendente"
               print(f"Emprestimo ID: {emprestimo.id}, Usuário: {usuario['nome']}, Livro: {livro['titulo']}, Data Empréstimo: {emprestimo.data_emprestimo}, Data Devolução: {emprestimo.data_devolucao}, Status:{status}")
def menu():
     print("\n=== Sistema de Gerenciamento de Biblioteca ===")
     print("1. Cadastrar Livro")
     print("2. Listar Livro")
     print("3. Cadastrar Usuários")
     print("4. Listar Usuários")
     print("5. Emprestar Livro")
     print("6. Devolver Livro")
     print("7. Listar Empréstimo")
     print("8. Pesquisar Livros")
     print("9. Pesquisar Usuários")
     print("10. Gerar Relatório de Empréstimos")
     print("11. Sair")
     opcao = input("Escolha uma opção: ")
     return opcao
def main():
     livros = carregar_dados('livros.json')
     usuarios = carregar_dados('usuarios.json')
     emprestimos = carregar_dados('empréstimos.json')
     while True:
          opcao = menu()
          if opcao =='1':
               cadastrar_livro(livros)
          elif opcao == '2':
               listar_livros(livros)
          elif opcao == '3':
               cadastrar_usuario(usuarios)
          elif opcao == '4':
               listar_usuarios(usuarios)
          elif opcao == '5':
               emprestar_livro(emprestimos, livros, usuarios)
          elif opcao == '6':
               devolver_livro(emprestimos, livros)
          elif opcao == '7':
               listar_emprestimos(emprestimos)
          elif opcao == '8':
               pesquisar_livros(livros)
          elif opcao == '9':
               pesquisar_usuarios(usuarios)
          elif opcao == '10':
               gerar_relatorio_emprestimos(emprestimos, usuarios, livros)
          elif opcao == '11':
               print("Encerrando o sistema de biblioteca. Até mais!")
               break
          else:
               print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__== '__main__':
     main()



        

     




                                                  
