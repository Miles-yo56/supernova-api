from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key_dev_only"

# Tokens permitidos
TOKENS = {
    "Matlabinc.67": "dev",
    "Blinkinc.92": "estudante",
    "Ckjson90": "escola"
}

# Usuário Dev exclusivo
DEV_USER = "Matlabinc.67"

# Dados exemplo
PERFIL = {
    "nome": "Gabriel",
    "email": "gabrielsantosprodrigues85@gmail.com",
    "foto": "https://i.pinimg.com/236x/23/Lz/4A/23Lz4AGye.jpg"
}

PE_DE_MEIA = [
    {"mes": "Março", "valor": 1200, "data_pagamento": "05/03/2026"},
    {"mes": "Abril", "valor": 1200, "data_pagamento": "05/04/2026"},
    {"mes": "Maio", "valor": 1200, "data_pagamento": "05/05/2026"},
]

FREQUENCIA = {
    "Matemática": 85,
    "Português": 90,
    "Ciências": 70,
    "História": 80
}

# HTML Templates
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Login Supernova</title>
<style>
body {{
    background-image: url('https://i.pinimg.com/564x/4Q/hI/xf/4QhIxfhZR.jpg');
    background-size: cover;
    font-family: Arial, sans-serif;
    color: #fff;
    text-align: center;
    padding-top: 100px;
}}
input {{ padding: 10px; font-size:16px; }}
button {{ padding:10px 20px; font-size:16px; cursor:pointer; }}
</style>
</head>
<body>
<h1>Tela de login</h1>
<p>Forneça seu token:</p>
<form method="post">
<input type="text" name="token" placeholder="Digite o token"/>
<br><br>
<button type="submit">Entrar</button>
</form>
{% if error %}
<p style="color:red;">{{ error }}</p>
{% endif %}
</body>
</html>
"""

HOME_HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Supernova API</title>
<style>
body {{ font-family: Arial, sans-serif; background-color:#1a1a2e; color:#fff; }}
nav {{ background-color:#162447; padding:10px; }}
nav a {{ color:#fff; margin:0 10px; text-decoration:none; font-weight:bold; }}
section {{ padding:20px; }}
h2 {{ color:#fca311; }}
table {{ width:50%; border-collapse:collapse; margin-top:10px; }}
table, th, td {{ border:1px solid #fff; padding:8px; }}
</style>
</head>
<body>
<nav>
<a href="{{ url_for('perfil') }}">Perfil</a>
<a href="{{ url_for('frequencia') }}">Frequência</a>
<a href="{{ url_for('pe_de_meia') }}">Pé de Meia</a>
<a href="{{ url_for('olimpico') }}">Olímpico</a>
<a href="{{ url_for('cultura') }}">Cultura</a>
<a href="{{ url_for('atualizar') }}">Atualizar Credenciais</a>
<a href="{{ url_for('faq') }}">FAQ</a>
<a href="{{ url_for('sobre') }}">Sobre Nós</a>
<a href="{{ url_for('links') }}">Links Úteis</a>
{% if session.get('user') == 'dev' %}
<a href="{{ url_for('liberar') }}">Liberar</a>
{% endif %}
</nav>
<section>
<h2>Bem-vindo, {{ perfil['nome'] }}!</h2>
<img src="{{ perfil['foto'] }}" width="120px" style="border-radius:50%;"/>
<p>Email: {{ perfil['email'] }}</p>
<p>Data/Hora Atual: {{ data_hora }}</p>
</section>
</body>
</html>
"""

# Rotas

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        token = request.form.get("token")
        if token in TOKENS:
            session["user"] = TOKENS[token]
            return redirect(url_for("home"))
        else:
            error = "Token inválido!"
    return render_template_string(LOGIN_HTML, error=error)

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template_string(HOME_HTML, perfil=PERFIL, data_hora=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

@app.route("/perfil")
def perfil():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template_string("""
    <h2>Perfil do Usuário</h2>
    <img src="{{ perfil['foto'] }}" width="120px" style="border-radius:50%;"/>
    <p>Nome: {{ perfil['nome'] }}</p>
    <p>Email: {{ perfil['email'] }}</p>
    <p>Data/Hora Atual: {{ data_hora }}</p>
    """, perfil=PERFIL, data_hora=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

@app.route("/frequencia")
def frequencia():
    if "user" not in session:
        return redirect(url_for("login"))
    freq_alertas = {k:v for k,v in FREQUENCIA.items() if v<80}
    return render_template_string("""
    <h2>Frequência</h2>
    <table>
    <tr><th>Matéria</th><th>%</th></tr>
    {% for materia, valor in frequencia.items() %}
        <tr>
        <td>{{ materia }}</td>
        <td style="color:{% if valor<75 %}red{% elif valor<80 %}orange{% else %}green{% endif %}">{{ valor }}%</td>
        </tr>
    {% endfor %}
    </table>
    {% if freq_alertas %}
    <p style="color:red;">Atenção! Algumas matérias estão abaixo de 80%</p>
    {% endif %}
    """, frequencia=FREQUENCIA, freq_alertas=freq_alertas)

@app.route("/pe_de_meia")
def pe_de_meia():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template_string("""
    <h2>Pé de Meia</h2>
    <table>
    <tr><th>Mês</th><th>Valor</th><th>Data de Pagamento</th></tr>
    {% for item in pe_de_meia %}
    <tr>
        <td>{{ item['mes'] }}</td>
        <td>R$ {{ item['valor'] }}</td>
        <td>{{ item['data_pagamento'] }}</td>
    </tr>
    {% endfor %}
    </table>
    """, pe_de_meia=PE_DE_MEIA)

@app.route("/olimpico")
def olimpico():
    if "user" not in session:
        return redirect(url_for("login"))
    return "<h2>Aba Olímpico - Em construção</h2>"

@app.route("/cultura")
def cultura():
    if "user" not in session:
        return redirect(url_for("login"))
    return "<h2>Aba Cultura - Links integrados YouTube, Pinterest, OBMEP</h2>"

@app.route("/atualizar")
def atualizar():
    if "user" not in session:
        return redirect(url_for("login"))
    return "<h2>Aba Atualizar Credenciais</h2>"

@app.route("/faq")
def faq():
    if "user" not in session:
        return redirect(url_for("login"))
    return "<h2>FAQ</h2>"

@app.route("/sobre")
def sobre():
    if "user" not in session:
        return redirect(url_for("login"))
    return "<h2>Sobre Nós</h2>"

@app.route("/links")
def links():
    if "user" not in session:
        return redirect(url_for("login"))
    return """
    <h2>Links Úteis</h2>
    <ul>
    <li><a href='https://www.youtube.com/@tecmundo' target='_blank'>Canal Tec Mundo</a></li>
    <li><a href='https://www.youtube.com/@cienciatododia' target='_blank'>Canal Ciência Todo Dia</a></li>
    <li><a href='https://www.youtube.com/@matematicanopapel' target='_blank'>Canal Matemática no Papel</a></li>
    <li><a href='https://www.pinterest.com/' target='_blank'>Pinterest</a></li>
    </ul>
    """

@app.route("/liberar")
def liberar():
    if session.get("user") != "dev":
        return "<p>Apenas desenvolvedor pode acessar esta função.</p>"
    return "<h2>Função Liberar - Adicionar permissões aos usuários</h2>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
