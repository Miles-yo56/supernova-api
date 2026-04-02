# server.py
from flask import Flask, render_template_string, request, jsonify
import os
import datetime

app = Flask(__name__)

# Tokens válidos
valid_tokens = {
    "Matlabinc.67": "Dev",
    "Blinkinc.92": "Estudante",
    "Ckjson90": "Escola",
    "Sparta654.Mp": "Dev Exclusivo"
}

# Tela de login com imagem
login_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Login Supernova</title>
    <style>
    {% raw %}
        body { 
            background-color: #1E1E2F; 
            color: #fff; 
            font-family: Arial, sans-serif; 
            text-align: center; 
            padding-top: 50px; 
        }
        input[type=text] { padding: 10px; width: 250px; font-size: 16px; }
        input[type=submit] { padding: 10px 20px; font-size: 16px; }
        img { width: 300px; margin-bottom: 20px; border-radius: 10px; }
        a { color: #00BFFF; text-decoration: none; font-weight: bold; }
    {% endraw %}
    </style>
</head>
<body>
    <img src="https://i.pinimg.com/originals/4Q/hi/Xf/4QhIxfhZR.jpg" alt="Login Image"/>
    <h2>Forneça seu token</h2>
    <form method="post">
        <input type="text" name="token" placeholder="Insira seu token" required/><br><br>
        <input type="submit" value="Entrar"/>
    </form>
    {% if error %}
        <p style="color:red;">{{ error }}</p>
    {% endif %}
    <p>Não encontrou o que precisava? Fale com o desenvolvedor: <a href="mailto:gabrielsantosprodrigues85@gmail.com">gabrielsantosprodrigues85@gmail.com</a></p>
</body>
</html>
"""

# Dashboard
dashboard_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Supernova Dashboard</title>
    <style>
    {% raw %}
        body { background-color: #121212; color: #fff; font-family: Arial, sans-serif; margin:0; padding:0; }
        header { background: #1E90FF; padding: 15px; text-align:center; font-size:24px; }
        nav { background: #282828; padding: 10px; }
        nav a { color:#00BFFF; margin: 0 10px; text-decoration:none; font-weight:bold; }
        section { padding:20px; }
        h2 { color:#00FFFF; }
        .dev-only { display: inline-block; background: #FFD700; padding:5px 10px; margin:5px; border-radius:5px; cursor:pointer; }
    {% endraw %}
    </style>
</head>
<body>
    <header>Supernova Space - {{ role }}</header>
    <nav>
        <a href="/perfil?token={{ token }}">Perfil</a>
        <a href="/frequencia?token={{ token }}">Frequência</a>
        <a href="/pe-de-meia?token={{ token }}">Pé de Meia</a>
        <a href="/olimpico?token={{ token }}">Olimpíadas</a>
        <a href="/cultura?token={{ token }}">Cultura</a>
        {% if role.startswith("Dev") %}
            <span class="dev-only"><a href="/liberar?token={{ token }}">Liberar</a></span>
        {% endif %}
    </nav>
    <section>
        <h2>Bem-vindo, {{ role }}!</h2>
        <p>Escolha uma aba acima para navegar pelas funções do sistema.</p>
    </section>
</body>
</html>
"""

# Perfil do usuário
@app.route("/perfil")
def perfil():
    token = request.args.get("token")
    role = valid_tokens.get(token, "Visitante")
    now = datetime.datetime.now()
    return f"""
    <h2>Perfil de {role}</h2>
    <p>Data/Hora: {now.strftime('%d/%m/%Y %H:%M:%S')}</p>
    <p>Foto de Perfil: <img src='https://i.pinimg.com/236x/23/Lz/4A/23Lz4AGye.jpg' width='100'></p>
    <p>Email: gabrielsantosprodrigues85@gmail.com</p>
    """

# Frequência
@app.route("/frequencia")
def frequencia():
    frequencia_val = 85
    alerta = "Atenção! Frequência abaixo de 80%" if frequencia_val < 80 else "Frequência ok"
    return f"<h2>Frequência: {frequencia_val}%</h2><p>{alerta}</p>"

# Pé de meia
@app.route("/pe-de-meia")
def pe_de_meia():
    return """
    <h2>Pé de Meia - Caixa Econômica</h2>
    <ul>
        <li>Depósito 1: 05/04/2026</li>
        <li>Depósito 2: 05/05/2026</li>
        <li>Depósito 3: 05/06/2026</li>
    </ul>
    """

# Olimpíadas
@app.route("/olimpico")
def olimpico():
    return """
    <h2>Olimpíadas</h2>
    <p>Lista de competições</p>
    <ul>
        <li>Olimpíada de Matemática - 2026</li>
        <li>Olimpíada de Física - 2026</li>
    </ul>
    """

# Cultura / Links
@app.route("/cultura")
def cultura():
    return """
    <h2>Cultura e Links</h2>
    <ul>
        <li><a href="https://www.youtube.com/@TecMundo">Canal Tec Mundo</a></li>
        <li><a href="https://www.youtube.com/@CienciaTodoDia">Canal Ciência Todo Dia</a></li>
        <li><a href="https://www.youtube.com/@MatematicaNoPapel">Canal Matemática no Papel</a></li>
        <li><a href="https://www.pinterest.com/">Pinterest</a></li>
    </ul>
    """

# Tela para Dev liberar perfis
@app.route("/liberar")
def liberar():
    token = request.args.get("token")
    if valid_tokens.get(token, "").startswith("Dev"):
        return "<h2>Área de Liberação para Dev</h2><p>Aqui você pode liberar novas funções.</p>"
    return "<h2>Acesso negado</h2>"

# Rota de login principal
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        token = request.form.get("token")
        if token in valid_tokens:
            role = valid_tokens[token]
            return render_template_string(dashboard_html, role=role, token=token)
        else:
            error = "Token inválido!"
    return render_template_string(login_html, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
