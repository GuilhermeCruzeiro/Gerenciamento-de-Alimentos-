import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os 


# Conexão com o banco de dados
def criar_conexao():
    conn = sqlite3.connect('estoque.db')
    return conn

# Criar tabela de produtos
def criar_tabela(conn):
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_fabricacao DATE NOT NULL,
        data_vencimento DATE NOT NULL
    )
    ''')
    conn.commit()

def enviar_email(produto):
    destinatario = 'testepython738@gmail.com'  
    assunto = f'Produto prestes a vencer: {produto[0]}'
    corpo = f'O produto {produto[0]} está prestes a vencer em {produto[1]}.'

    msg = MIMEText(corpo)
    msg['Subject'] = assunto
    msg['From'] = 'testepython738@gmail.com'  
    msg['To'] = destinatario

    # Configurar servidor SMTP
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('testepython738@gmail.com', 'snoibeghwvcbmykc')  
            server.sendmail('testepython738@gmail.com', destinatario, msg.as_string())
            print(f'E-mail enviado para {destinatario} sobre o produto {produto[0]}')
    except Exception as e:
        print(f'Erro ao enviar e-mail: {e}')

# Adicionar Produto
def adicionar_produto(conn, nome, data_fabricacao, data_vencimento):
    c = conn.cursor()
    c.execute('''
    INSERT INTO produtos (nome, data_fabricacao, data_vencimento)
    VALUES (?, ?, ?)
    ''', (nome, data_fabricacao, data_vencimento))
    conn.commit()

# Verificar produtos próximos do vencimento
def verificar_vencimento(conn, dias=7):
    c = conn.cursor()
    data_atual = datetime.now().date()
    data_limite = data_atual + timedelta(days=dias)
    
    c.execute('''
    SELECT nome, data_vencimento FROM produtos WHERE data_vencimento <= ?
    ''', (data_limite,))
    
    return c.fetchall()

#Função Principal
def main():
    conn = criar_conexao()
    criar_tabela(conn)

    while True:
        print("\nMenu:")
        print("1. Adicionar Produto")
        print("2. Verificar Vencimento")
        print("3. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome do produto: ")
            data_fabricacao = input("Data de fabricação (YYYY-MM-DD): ")
            data_vencimento = input("Data de vencimento (YYYY-MM-DD): ")

            # Validação das datas
            try:
                datetime.strptime(data_fabricacao, '%Y-%m-%d')
                datetime.strptime(data_vencimento, '%Y-%m-%d')
            except ValueError:
                print("Data inválida! Certifique-se de usar o formato YYYY-MM-DD.")
                continue
            
            adicionar_produto(conn, nome, data_fabricacao, data_vencimento)
            print("Produto adicionado com sucesso!")

        elif opcao == '2':
            produtos_a_vencer = verificar_vencimento(conn)
            if produtos_a_vencer:
                print("Produtos prestes a vencer:")
                for produto in produtos_a_vencer:
                    enviar_email(produto)  # Enviar e-mail sobre o produto
                    print(f"- {produto[0]} (Vencimento: {produto[1]})")
            else:
                print("Não há produtos prestes a vencer.")

        elif opcao == '3':
            print("Saindo do programa...")
            break

        else:
            print("Opção inválida! Por favor, tente novamente.")

    conn.close()

if __name__ == "__main__":
    main()