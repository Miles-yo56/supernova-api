from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "supernova_secret_key"

# --------------------
# TOKENS E PERFIS
# --------------------
TOKENS = {
    "Matlabinc.67": "Dev",
    "Blinkinc.92": "Estudante",
    "Ckjson90": "Escola"
}
DEV_USERNAME = "Matlabinc.67"
MAX_ATTEMPTS = 3
attempts = {}

# --------------------
# DADOS EXEMPLO
# --------------------
students_data = {
    "Blinkinc.92": {
        "nome": "Gabriel",
        "email": "gabrielsantosprodrigues85@gmail.com",
        "foto": "https://i.pinimg.com/236x/23/Lz/4A/23Lz4AGye.jpg",
        "frequencia": 78,
        "horario_aulas": "08:00-12:00",
        "pe_de_meia": {"proximo_pagamento": "10/04/2026", "valor": 150}
    },
    "Ckjson90": {
        "nome": "Escola Modelo",
        "email": "contato@escolamodelo.com",
        "foto": "https://i.pinimg.com/236x/00/aa/bb/00aabbcc.jpg",
        "frequencia": 100,
        "horario_aulas": "07:00-13:00",
        "pe_de_meia": {"proximo_pagamento": "05/04/2026", "valor": 5000}
    }
}

olimpiadas = ["OBMEP", "OBA", "OBF"]
recomendacoes = [
    {"nome":"Canal Tec Mundo", "link":"https://www.youtube.com/@TecMundo"},
    {"nome":"Canal Ciência Todo Dia", "link":"https://www.youtube.com/@CienciaTodoDia"},
    {"nome":"Canal Matemática no Papel", "link":"https://www.youtube.com/@MatematicaNoPapel"}
]
links_uteis = [
    {"nome":"Pinterest", "link":"https://www.pinterest.com/"},
    {"nome":"ChatGPT", "link":"https://chat.openai.com/"},
    {"nome":"Gemini AI", "link":"https://gemini.ai/"},
    {"nome":"Claude AI", "link":"https://claude.ai/"}
]

# --------------------
# TEMPLATES
# --------------------
LOGIN_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login Supernova</title>
    <style>
        body {{ text-align:center; font-family:sans-serif; background:#1e1e2f; color:white; }}
        img {{ width:200px; margin-top:30px; }}
        input, button {{ font-size:16px; padding:5px; margin:5px; }}
    </style>
</head>
<body>
    <h1>Tela de login</h1>
    <img src="https://i.pinimg.com/564x/4c/32/ab/4c32ab7e6ea5a234f7b2d1c9c42e1a3a.jpg" alt="Supernova">
    <form method="post">
        <input type="text" name="token" placeholder="Forneça seu token" required>
        <button type="submit">Entrar</button>
    </form>
    {% if error %}<p style="color:red">{{ error }}</p>{% endif %}
</body>
</html>
'''

DASHBOARD_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Supernova Dashboard</title>
    <style>
        body {{ font-family:sans-serif; background:#121212; color:white; }}
        .tab {{ padding:10px; margin:5px; display:inline-block; background:#2e2e4e; cursor:pointer; }}
        .active {{ background:#4e4ebf; }}
        .section {{ display:none; padding:20px; }}
        .visible {{ display:block; }}
        .dev-button {{ background:orange; color:black; padding:5px; cursor:pointer; }}
    </style>
    <script>
        function showTab(tabName){{
            let sections = document.querySelectorAll('.section');
            sections.forEach(s => s.classList.remove('visible'));
            document.getElementById(tabName).classList.add('visible');
        }}
    </script>
</head>
<body>
    <h1>Bem-vindo {{ user }}</h1>
    <img src="{{ foto }}" width="100">
    <p>Email: {{ email }}</p>
    <p>Data e hora: {{ now }}</p>
    
    <div>
        <span class="tab active" onclick="showTab('perfil')">Perfil</span>
        <span class="tab" onclick="showTab('frequencia')">Frequência</span>
        <span class="tab" onclick="showTab('pe_meia')">Pé de Meia</span>
        <span class="tab" onclick="showTab('olimpico')">Olimpíadas</span>
        <span class="tab" onclick="showTab('recomendacoes')">Recomendações</span>
        <span class="tab" onclick="showTab('links')">Links Úteis</span>
        <span class="tab" onclick="showTab('cultura')">Cultura</span>
        <span class="tab" onclick="showTab('faq')">FAQ</span>
        {% if user_type == 'Dev' %}
        <span class="tab" onclick="showTab('liberar')">Liberar</span>
        <span class="tab" onclick="showTab('atualizar')">Atualizar Credenciais</span>
        {% endif %}
    </div>
    
    <div id="perfil" class="section visible">
        <h2>Perfil</h2>
        <p>Nome: {{ user }}</p>
        <p>Email: {{ email }}</p>
        <img src="{{ foto }}" width="150">
    </div>
    
    <div id="frequencia" class="section">
        <h2>Frequência</h2>
        <p>{{ frequencia }}%</p>
        {% if frequencia < 80 %}<p style="color:yellow">Alerta: Atingindo limite mínimo!</p>{% endif %}
        <p>Horário aulas: {{ horario_aulas }}</p>
    </div>
    
    <div id="pe_meia" class="section">
        <h2>Pé de Meia</h2>
        <p>Próximo pagamento: {{ pe_meia['proximo_pagamento'] }}</p>
        <p>Valor: R$ {{ pe_meia['valor'] }}</p>
    </div>
    
    <div id="olimpico" class="section">
        <h2>Olimpíadas</h2>
        <ul>{% for o in olimpias %}<li>{{ o }}</li>{% endfor %}</ul>
        {% if user_type == 'Dev' %}
        <button class="dev-button" onclick="alert('Adicionar nova olimpíada')">+</button>
        {% endif %}
    </div>
    
    <div id="recomendacoes" class="section">
        <h2>Recomendações</h2>
        <ul>{% for r in recomendacoes %}<li><a href="{{ r.link }}" target="_blank">{{ r.nome }}</a></li>{% endfor %}</ul>
    </div>
    
    <div id="links" class="section">
        <h2>Links Úteis</h2>
        <ul>{% for l in links_uteis %}<li><a href="{{ l.link }}" target="_blank">{{ l.nome }}</a></li>{% endfor %}</ul>
    </div>
    
    <div id="cultura" class="section">
        <h2>Cultura</h2>
        <p>Integração com YouTube, Pinterest e IA</p>
    </div>
    
    <div id="faq" class="section">
        <h2>FAQ</h2>
        <p>Perguntas frequentes aqui</p>
    </div>
    
    {% if user_type == 'Dev' %}
    <div id="liberar" class="section">
        <h2>Função Liberar</h2>
        <form method="post" action="/liberar">
            <input type="text" name="usuario_liberar" placeholder="Usuário">
            <button type="submit">Liberar</button>
        </form>
    </div>
    <div id="atualizar" class="section">
        <h2>Atualizar Credenciais</h2>
        <p>Função Dev para atualizar credenciais de usuários</p>
    </div>
    {% endif %}
</body>
</html>
'''

# --------------------
# ROTAS
# --------------------
@app.route("/", methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        token = request.form.get("token")
        user_type = TOKENS.get(token)
        
        # Tentativas
        global attempts
        if token not in attempts:
            attempts[token] = 0
        attempts[token] += 1
        if attempts[token] > MAX_ATTEMPTS:
            return f"Você ultrapassou o limite diário. Tente novamente em 24h."
        
        if user_type:
            session['user'] = token
            session['user_type'] = user_type
            return redirect(url_for("dashboard"))
        else:
            error = "Token inválido"
    return render_template_string(LOGIN_PAGE, error=error)

@app.route("/dashboard")
def dashboard():
    user = session.get("user")
    user_type = session.get("user_type")
    if not user:
        return redirect(url_for("login"))
    
    data = students_data.get(user, {
        "nome":user,"email":"-","foto":"https://i.pinimg.com/236x/23/Lz/4A/23Lz4AGye.jpg",
        "frequencia":0, "horario_aulas":"-","pe_de_meia":{"proximo_pagamento":"-","valor":0}})
    
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    return render_template_string(DASHBOARD_PAGE,
                                  user=user,
                                  user_type=user_type,
                                  foto=data['foto'],
                                  email=data['email'],
                                  frequencia=data['frequencia'],
                                  horario_aulas=data['horario_aulas'],
                                  pe_meia=data['pe_de_meia'],
                               olimpias=olimpiadas,
                                  recomendacoes=recomendacoes,
                                  links_uteis=links_uteis,
                                  now=now)

@app.route("/liberar", methods=["POST"])
def liberar():
    if session.get("user_type") != "Dev":
        return "Acesso negado"
    usuario = request.form.get("usuario_liberar")
    if usuario in students_data:
        return f"Acesso liberado para {usuario}"
    else:
        return f"Usuário {usuario} não encontrado"

# --------------------
# EXECUÇÃO
# --------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
