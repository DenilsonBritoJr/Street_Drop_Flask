import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import pymysql

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/sobre.html')
def sobre():
    return render_template('sobre.html')

@app.route('/composicao.html')
def composicao():
    return render_template('composicao.html')

@app.route('/origem.html')
def origem():
    return render_template('origem.html')

# Rota de Cadastro (Fale Conosco -> Banco de Dados)
@app.route('/cadastro', methods=['GET', 'POST'])
@app.route('/contato', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        assunto = request.form.get('assunto')
        mensagem = request.form.get('mensagem')

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO fale_conosco (nome, email, assunto, mensagem)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (nome, email, assunto, mensagem))
            conn.commit()
        finally:
            conn.close()

        return redirect(url_for('listar'))

    return render_template('cadastro.html')

# Rota de Listagem dos registros salvos no MySQL
@app.route('/listar')
def listar():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id, nome, email, assunto, mensagem, data_envio FROM fale_conosco ORDER BY id DESC"
            cursor.execute(sql)
            mensagens = cursor.fetchall()
    finally:
        conn.close()

    return render_template('listar.html', mensagens=mensagens)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
