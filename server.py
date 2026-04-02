from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import qrcode

app = Flask(__name__)

# ------------------- TOKENS -------------------
valid_tokens = {
    "Matlabinc.67": "Dev",
    "Blinkinc.92": "Estudante",
    "Ckjson90": "Escola",
    "Sparta654.Mp": "Dev Exclusivo"
}

# ------------------- LOGIN -------------------
login_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Login Supernova</title>
    <style>
        body { background-color:#1E1E2F; color:#fff; font-family:Arial; text-align:center; padding-top:50px;}
        input { padding:10px; font-size:16px; }
        img { width:300px; margin-bottom:20px; border-radius:10px;}
        a { color:#00BFFF; font-weight:bold; text-decoration:none; }
    </style>
</head>
<body>
    <img src="https://i.pinimg.com/originals/4Q/hi/Xf/4QhIxfhZR.jpg"/>
    <h2>Forneça seu token</h2>
    <form method="post">
        <input type="text" name="token" placeholder="Insira seu token"/><br><br>
        <input type="submit" value="Entrar"/>
    </form>
    {% if error %}
        <p style="color:red;">{{ error }}</p>
    {% endif %}
    <p>Não encontrou o que precisava? <a href="mailto:gabrielsantosprodrigues85@gmail.com">Contate o Dev</a></p>
</body>
</html>
"""

# ------------------- DASHBOARD -------------------
dashboard_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Supernova Dashboard</title>
    <style>
        body { background-color:#121212;color:#fff;font-family:Arial;margin:0;padding:0;}
        header { background:#1E90FF;padding:15px;text-align:center;font-size:24px; }
        nav { background:#282828;padding:10px; }
        nav a { color:#00BFFF;margin:0 10px;text-decoration:none;font-weight:bold; }
        .dev-only { display:inline-block;background:#FFD700;padding:5px 10px;border-radius:5px;cursor:pointer;}
        section { padding:20px; }
    </style>
</head>
<body>
    <header>Supernova Space - {{ role }}</header>
    <nav>
        <a href="/home?token={{ token }}">Home</a>
        <a href="/perfil?token={{ token }}">Perfil</a>
        <a href="/frequencia?token={{ token }}">Frequência</a>
        <a href="/pe-de-meia?token={{ token }}">Pé de Meia</a>
        <a href="/olimpico?token={{ token }}">Olimpíadas</a>
        <a href="/cultura?token={{ token }}">Cultura</a>
        {% if role.startswith("Dev") %}
            <span class="dev-only"><a href="/dev?token={{ token }}">Dev</a></span>
        {% endif %}
    </nav>
    <section>
        <h2>Bem-vindo, {{ role }}!</h2>
        <p>Escolha uma aba acima para navegar pelas funções do sistema.</p>
    </section>
</body>
</html>
"""

# ------------------- ROTAS -------------------

@app.route("/", methods=["GET","POST"])
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

@app.route("/perfil")
def perfil():
    token = request.args.get("token")
    role = valid_tokens.get(token, "Visitante")
    now = datetime.datetime.now()
    return f"""
    <h2>Perfil de {role}</h2>
    <p>Data/Hora: {now.strftime('%d/%m/%Y %H:%M:%S')}</p>
    <p>Foto de Perfil: <img src='https://i.pinimg.com/236x/23/Lz/4A/23Lz4AGye.jpg' width='150'></p>
    <p>Email: gabrielsantosprodrigues85@gmail.com</p>
    <p>Funcionalidades customizáveis: adicionar fotos PNG/JPEG</p>
    """

@app.route("/frequencia")
def frequencia():
    df = pd.DataFrame({'Dia':['Seg','Ter','Qua','Qui','Sex'],'Presente':['Sim','Sim','Não','Sim','Sim']})
    total = len(df)
    sim_count = df['Presente'].value_counts().get('Sim',0)
    porcentagem = round(sim_count/total*100,2)
    
    fig, ax = plt.subplots()
    ax.pie([sim_count, total-sim_count], labels=['Sim','Não'], autopct='%1.1f%%', colors=['#00FF00','#FF0000'])
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches="tight")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    alerta = "Atenção! Frequência abaixo de 80%" if porcentagem < 80 else "Frequência ok"
    return f"""
    <h2>Frequência: {porcentagem}%</h2>
    <p>{alerta}</p>
    <img src="data:image/png;base64,{plot_url}">
    """

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

@app.route("/olimpico")
def olimpico():
    return """
    <h2>Olimpíadas</h2>
    <ul>
        <li>ONC - Olimpíada Nacional de Ciências</li>
        <li>OBA - Olimpíada Brasileira de Astronomia</li>
        <li>OBMEP - Olimpíada Brasileira de Matemática</li>
        <li>Canguru - Olimpíada Internacional de Matemática</li>
    </ul>
    """

@app.route("/cultura")
def cultura():
    return """
    <h2>Cultura e Integrações</h2>
    <ul>
        <li><a href="https://www.youtube.com">YouTube</a> - Vídeos integrados</li>
        <li><a href="https://www.tiktok.com">TikTok</a></li>
        <li><a href="https://www.google.com/chrome/">Google Chrome</a></li>
    </ul>
    """

@app.route("/home")
def home():
    return """
    <img src="https://i.pin.it/7qnhuklzY" width="500"/>
    <h2 style="font-family:Times;">Qual foi a inspiração do projeto</h2>
    <p style="font-style:italic;">Não foi uma escolha guiada por individualismo, foi pensando nos estudantes que querem ser um <u style='color:green'>diferencial</u> e que gostariam de aperfeiçoar-se constantemente e não ficarem para trás.</p>
    
    <h2 style="font-family:Times;">Por que de tantos sites, o seu seria diferente?</h2>
    <p style="font-style:italic;">Porque o que faz um site <u style='color:purple'>diferente</u> são as pessoas que neles vivem, num site tudo é <u style='color:green'>orgânico</u>, assim como o corpo <u style='color:red'>humano</u>.</p>
    
    <h2 style="font-family:Times;">O que você espera desse projeto?</h2>
    <p style="font-style:italic;">Que ele continue avançando com você, claro que uma hora ou outra vão ter momentos em que eu vou querer desistir desse site, mas se fui persistente até aqui, consigo ir mais longe. (Risos)</p>
    """

@app.route("/dev")
def dev():
    token = request.args.get("token")
    role = valid_tokens.get(token,"Visitante")
    if not role.startswith("Dev"):
        return "<h2>Acesso negado</h2>"
    return """
    <h2>Área do Dev</h2>
    <ul>
        <li>Liberar acesso</li>
        <li>Monitorar tráfego</li>
        <li>Visitantes Online/Offline</li>
        <li>Adicionar nova opção</li>
        <li>Desativar perfil User</li>
        <li>Atualizar dados cadastrais</li>
        <li>Integrar I.A</li>
        <li>PPC - Palavras-chave de pesquisa do usuário</li>
        <li>Redefinir senha</li>
        <li>Aumentar nível do token</li>
    </ul>
    """

# ------------------- EXECUÇÃO -------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port, debug=True)
    # ------------------- CALCULADORA -------------------
calc_html = """
<h2>Calculadora</h2>
<form method="post" action="/calc">
    <input type="text" name="expr" placeholder="Digite a expressão matemática"/>
    <input type="submit" value="Calcular"/>
</form>
{% if resultado is defined %}
<p>Resultado: {{ resultado }}</p>
{% endif %}
"""

@app.route("/calc", methods=["GET","POST"])
def calc():
    resultado = None
    if request.method == "POST":
        expr = request.form.get("expr")
        try:
            resultado = eval(expr)
        except:
            resultado = "Erro na expressão!"
    return render_template_string(calc_html, resultado=resultado)

# ------------------- QR CODE -------------------
qr_html = """
<h2>Gerador de QR Code</h2>
<form method="post" action="/qr">
    <input type="text" name="dados" placeholder="Digite os dados para QR Code"/>
    <input type="submit" value="Gerar QR"/>
</form>
{% if img_qr is defined %}
<img src="data:image/png;base64,{{ img_qr }}" width="200"/>
{% endif %}
"""

@app.route("/qr", methods=["GET","POST"])
def qr():
    img_qr = None
    if request.method == "POST":
        dados = request.form.get("dados")
        qr_img = qrcode.make(dados)
        buf = io.BytesIO()
        qr_img.save(buf)
        buf.seek(0)
        img_qr = base64.b64encode(buf.getvalue()).decode()
    return render_template_string(qr_html, img_qr=img_qr)

# ------------------- CULTURA INTERATIVA -------------------
cultura_html = """
<h2>Cultura Interativa</h2>
<ul>
    <li>YouTube: <iframe width="400" height="225" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe></li>
    <li>TikTok: <iframe src="https://www.tiktok.com/embed/v2/7071234567890123456" width="400" height="500" frameborder="0" allowfullscreen></iframe></li>
    <li>Pinterest: <a href="https://www.pinterest.com" target="_blank">Acesse o Pinterest</a></li>
</ul>
"""

@app.route("/cultura_interativa")
def cultura_interativa():
    return render_template_string(cultura_html)
