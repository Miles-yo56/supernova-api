from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
import os
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = "supernova_secret_key_123"

# Tokens válidos
TOKENS = {
    "Matlabinc.67": "dev",
    "Blinkinc.92": "student",
    "Ckjson90": "school"
}

# Usuário Dev exclusivo
DEV_CREDENTIAL = "Sparta654.Mp"

# Dados de exemplo do perfil
PROFILES = {
    "dev": {"nome": "Gabriel", "email": "gabrielsantosprodrigues85@gmail.com", "foto": "https://i.pinimg.com/236x/23/Lz/4A/23Lz4AGye.jpg"},
    "student": {"nome": "Aluno Teste", "email": "aluno@escola.com", "foto": "https://i.pinimg.com/236x/23/Lz/4A/23Lz4AGye.jpg"},
    "school": {"nome": "Escola XYZ", "email": "contato@escola.com", "foto": "https://i.pinimg.com/236x/23/Lz/4A/23Lz4AGye.jpg"}
}

# Frequência de exemplo
FREQUENCIA = {
    "Matemática": 78,
    "Português": 82,
    "Ciências": 74,
    "História": 85
}

# Pé de meia exemplo (datas reais da Caixa Econômica)
PE_DE_MEIA = [
    {"mês": "Abril 2026", "data_pagamento": "10/04/2026", "valor": 120.00},
    {"mês": "Maio 2026", "data_pagamento": "10/05/2026", "valor": 120.00},
    {"mês": "Junho 2026", "data_pagamento": "10/06/2026", "valor": 120.00},
]

# Template principal
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Supernova API Login</title>
<style>
body {{ font-family: Arial; text-align: center; background-color: #f0f8ff; }}
.container {{ margin-top: 50px; }}
img {{ max-width: 300px; border-radius: 15px; }}
input {{ padding: 10px; margin: 10px; font-size: 16px; }}
button {{ padding: 10px 20px; font-size: 16px; cursor: pointer; background-color: #007BFF; color: white; border: none; border-radius: 5px; }}
.alert {{ color: red; font-weight: bold; }}
</style>
</head>
<body>
<div class="container">
<h1>Tela de Login</h1>
<img src="https://pin.it/2VxPkKbED" alt="Token Image">
<form method="post">
<br>
<input type="text" name="token" placeholder="Forneça seu token">
<br>
<button type="submit">Entrar</button>
</form>
{% if error %}
<p class="alert">{{ error }}</p>
{% endif %}
</div>
</body>
</html>
"""

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Supernova API - {{ user_role }}</title>
<style>
body {{ font-family: Arial; background-color: #e6f7ff; }}
header {{ background-color: #007BFF; color: white; padding: 15px; text-align: center; font-size: 24px; }}
nav {{ margin: 10px; }}
nav a {{ margin: 0 10px; color: #007BFF; text-decoration: none; font-weight: bold; }}
section {{ padding: 20px; }}
img {{ width: 100px; border-radius: 50%; }}
.alert {{ color: red; font-weight: bold; }}
</style>
</head>
<body>
<header>Supernova API - {{ user_role }}</header>
<nav>
<a href="{{ url_for('home_page') }}">Perfil</a>
<a href="{{ url_for('frequencia') }}">Frequência</a>
<a href="{{ url_for('pe_de_meia') }}">Pé de Meia</a>
<a href="{{ url_for('calculadora') }}">Calculadora</a>
<a href="{{ url_for('olimpico') }}">Olímpico</a>
<a href="{{ url_for('cultura') }}">Cultura</a>
<a href="{{ url_for('atualizar_credenciais') }}">Atualizar Credenciais</a>
<a href="{{ url_for('links_uteis') }}">Links Úteis</a>
<a href="{{ url_for('sobre') }}">Sobre Nós</a>
<a href="{{ url_for('faq') }}">FAQ</a>
<a href="{{ url_for('reclamacoes') }}">Reclamações/Sugestões</a>
{% if user_role == 'dev' %}
<a href="{{ url_for('liberar') }}">Liberar</a>
{% endif %}
</nav>
<section>
<h2>Perfil do Usuário</h2>
<img src="{{ profile.foto }}" alt="Foto">
<p><strong>Nome:</strong> {{ profile.nome }}</p>
<p><strong>Email:</strong> {{ profile.email }}</p>
<p><strong>Data e Hora:</strong> {{ datetime_now }}</p>
</section>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        token = request.form.get("token")
        role = TOKENS.get(token)
        if role:
            session["user_role"] = role
            session["token"] = token
            return redirect(url_for("home_page"))
        else:
            error = "Token inválido ou limite de tentativas excedido."
    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route("/home")
def home_page():
    if "user_role" not in session:
        return redirect(url_for("login"))
    user_role = session["user_role"]
    profile = PROFILES[user_role]
    datetime_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return render_template_string(HOME_TEMPLATE, user_role=user_role, profile=profile, datetime_now=datetime_now)

# Frequência
@app.route("/frequencia")
def frequencia():
    alerta = any(v < 80 for v in FREQUENCIA.values())
    return jsonify({"frequencia": FREQUENCIA, "alerta": alerta})

# Pé de meia
@app.route("/pe_de_meia")
def pe_de_meia():
    return jsonify({"pe_de_meia": PE_DE_MEIA})

# Calculadora simples
@app.route("/calculadora/<float:a>/<float:b>/<oper>")
def calculadora(a, b, oper):
    if oper == "soma":
        return jsonify({"resultado": a+b})
    elif oper == "sub":
        return jsonify({"resultado": a-b})
    elif oper == "mult":
        return jsonify({"resultado": a*b})
    elif oper == "div":
        if b == 0:
            return jsonify({"erro": "Divisão por zero"})
        return jsonify({"resultado": a/b})
    return jsonify({"erro": "Operação inválida"})

# Olímpico
@app.route("/olimpico")
def olimpico():
    return jsonify({"mensagem": "Aba Olímpico em construção"})

# Cultura
@app.route("/cultura")
def cultura():
    return jsonify({
        "youtube": ["https://youtube.com"],
        "pinterest": ["https://pinterest.com"],
        "chatgpt": ["https://chat.openai.com/"]
    })

# Atualizar credenciais
@app.route("/atualizar_credenciais")
def atualizar_credenciais():
    return jsonify({"mensagem": "Atualizar Credenciais disponível apenas para Dev"})

# Links úteis
@app.route("/links_uteis")
def links_uteis():
    return jsonify({
        "tec_mundo": "https://www.tecmundo.com.br/",
        "ciencia_todo_dia": "https://www.youtube.com/@CienciaTodoDia",
        "matematica_no_papel": "https://www.youtube.com/@MatematicaNoPapel"
    })

# Sobre nós
@app.route("/sobre")
def sobre():
    return jsonify({"mensagem": "Sobre a Supernova API, equipe de desenvolvimento, missão e visão"})

# FAQ
@app.route("/faq")
def faq():
    return jsonify({"mensagem": "Perguntas Frequentes"})

# Reclamações/Sugestões
@app.route("/reclamacoes")
def reclamacoes():
    return jsonify({"mensagem": "Envie suas sugestões ou reclamações para o Dev"})

# Liberar funções (Dev apenas)
@app.route("/liberar")
def liberar():
    if session.get("user_role") == "dev":
        return jsonify({"mensagem": "Funções desbloqueadas"})
    return jsonify({"erro": "Acesso negado"}), 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)                font-size: 16px; 
            }
            button { 
                cursor: pointer; 
                background-color: #ff5722; 
                color: white; 
                border: none; 
                border-radius: 5px; 
            }
            img { 
                width: 200px; 
                margin-bottom: 20px; 
                border-radius: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Tela de Login - Forneça seu token</h1>
        <img src="https://pin.it/2VxPkKbED" alt="Supernova Logo">
        <form method="POST">
            <input type="text" name="token" placeholder="Digite seu token" required>
            <br>
            <button type="submit">Entrar</button>
        </form>
        <p>Não encontrou o que precisava? Contate: gabrielsantosprodrigues85@gmail.com</p>
    </body>
    </html>
    """)

# Página principal após login
@app.route("/home")
def home():
    perfil = request.args.get("perfil", "Visitante")
    return f"<h2>Bem-vindo(a), {perfil}! Supernova API Online 🚀</h2>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
