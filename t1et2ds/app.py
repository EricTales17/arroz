from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para inicializar o banco de dados
def init_db():
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    # Adicionamos CPF/CNPJ e Redes Sociais aqui
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            cpf_cnpj TEXT NOT NULL,
            redes_sociais TEXT,
            observacoes TEXT 
        )
    ''')
    conn.commit()
    conn.close()

# Rota principal (Lida com exibição e cadastro)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        cpf_cnpj = request.form['cpf_cnpj']
        redes_sociais = request.form['redes_sociais'] # Opcional
        observacoes = request.form['observacoes']     # Opcional

        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        
        # Atualizamos o INSERT para salvar todos os 6 campos
        cursor.execute('''
            INSERT INTO clientes (nome, email, telefone, cpf_cnpj, redes_sociais, observacoes) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, email, telefone, cpf_cnpj, redes_sociais, observacoes))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))

    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()

    return render_template('index.html', clientes=clientes)

# Rota para Excluir Clientes
@app.route('/excluir/<int:id>')
def excluir(id):
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)