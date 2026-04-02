from flask import Flask, jsonify, render_template_string, request, redirect, url_for
import os
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Tokens válidos
TOKENS = {
    "Matlabinc.67": "dev",
    "Blinkinc.92": "estudante",
    "Ckjson90": "escola"
}

# Perfil do dev exclusivo
DEV_CREDENTIAL = "Sparta654.Mp"

# Simulação de dados
alunos = {
    "aluno1": {"frequencia": 78, "nome": "João", "email": "joao@email.com"},
    "aluno2": {"frequencia": 92, "nome": "Maria", "email": "maria@email.com"}
}

# Pé de meia (datas reais da Caixa Econômica Federal)
pe_de_meia = [
    {"data": "2026-04-05", "valor": 150.00},
    {"data": "2026-05-05", "valor": 150.00},
    {"data": "2026-06-05", "valor": 150.00}
]

# HTML da tela de login com imagem
LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
body {{
  background-image: url('https://i.pinimg.com/originals/4Q/hI/xf/4QhIxfhZR.jpg');
  background-size: cover;
  font-family: Arial, sans-serif;
  color: white;
  text-align: center;
  padding-top: 200px;
}}
input {{
  padding: 10px;
  font-size: 16px;
}}
button {{
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}}
</style>
</head>
<body>
<h1>Tela de login, forneça seu token</h1>
<form method="post" action="/login">
<input type="text" name="token" placeholder="Digite seu token">
<button type="submit">Entrar</button>
</form>
</body>
</html>
"""

# Rota de login
@app.route("/", methods=["GET"])
def login_page():
    return render_template_string(LOGIN_HTML)

@app.route("/login", methods=["POST"])
def login():
    token = request.form.get("token")
    role = TOKENS.get(token)
    if role:
        return redirect(url_for("dashboard", role=role))
    return "Token inválido. Contate o dev: gabrielsantosprodrigues85@gmail.com"

# Dashboard
@app.route("/dashboard/<role>")
def dashboard(role):
    # Gerar gráfico de frequência
    nomes = [aluno["nome"] for aluno in alunos.values()]
    freq = [aluno["frequencia"] for aluno in alunos.values()]
    plt.figure(figsize=(4,3))
    plt.bar(nomes, freq, color="skyblue")
    plt.ylim(0, 100)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    html = f"""
    <h1>Dashboard - {role.capitalize()}</h1>
    <h2>Frequência</h2>
    <img src="data:image/png;base64,{plot_url}">
    <h3>Pé de meia:</h3>
    <ul>
        {''.join([f"<li>{item['data']}: R${item['valor']}</li>" for item in pe_de_meia])}
    </ul>
    <h3>Horário e data atual:</h3>
    <p>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
    <h3>Links úteis:</h3>
    <ul>
        <li><a href="https://www.youtube.com/@TecMundo" target="_blank">Canal Tec Mundo</a></li>
        <li><a href="https://www.youtube.com/@CienciaTodoDia" target="_blank">Canal Ciência Todo Dia</a></li>
        <li><a href="https://www.youtube.com/@MatematicaNoPapel" target="_blank">Canal Matemática no Papel</a></li>
        <li><a href="https://www.pinterest.com" target="_blank">Pinterest</a></li>
    </ul>
    """
    # Abas especiais do dev
    if role == "dev":
        html += "<h3>Aba Dev:</h3><p>Funções de liberação e atualização de credenciais disponíveis.</p>"
    return html

# Perfil individual do aluno
@app.route("/perfil/<username>")
def perfil(username):
    aluno = alunos.get(username)
    if aluno:
        return jsonify(aluno)
    return "Aluno não encontrado"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
