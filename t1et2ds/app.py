from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco
def connect_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criar a tabela no início
with connect_db() as db:
    db.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT
        )
    ''')

@app.route('/')
def index():
    conn = connect_db()
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return render_template('index.html', clientes=clientes)

@app.route('/add', methods=['POST'])
def add_cliente():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']

    if nome and email:
        conn = connect_db()
        conn.execute('INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)',
                     (nome, email, telefone))
        conn.commit()
        conn.close()
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)