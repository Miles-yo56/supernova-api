from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# ------------------- TOKENS -------------------
valid_tokens = {
    "Matlabinc.67": "Dev",
    "Blinkinc.92": "Estudante",
    "Ckjson90": "Escola",
    "Sparta654.Mp": "Dev Exclusivo"
}

# ------------------- ROTAS -------------------

@app.route("/", methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        token = request.form.get("token")
        if token in valid_tokens:
            return redirect(url_for("dashboard", token=token))
        else:
            error = "Token inválido!"
    return render_template("login.html", error=error)

@app.route("/dashboard")
def dashboard():
    token = request.args.get("token")
    role = valid_tokens.get(token, "Visitante")
    return render_template("dashboard.html", role=role, token=token)

@app.route("/perfil")
def perfil():
    token = request.args.get("token")
    role = valid_tokens.get(token, "Visitante")
    now = datetime.datetime.now()
    return render_template("perfil.html", role=role, now=now)

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
    return render_template("frequencia.html", porcentagem=porcentagem, alerta=alerta, plot_url=plot_url)

@app.route("/pe-de-meia")
def pe_de_meia():
    return render_template("pe_de_meia.html")

@app.route("/olimpico")
def olimpico():
    return render_template("olimpico.html")

@app.route("/cultura")
def cultura():
    return render_template("cultura.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/dev")
def dev():
    token = request.args.get("token")
    role = valid_tokens.get(token,"Visitante")
    if not role.startswith("Dev"):
        return "<h2>Acesso negado</h2>"
    return render_template("dev.html")

# ------------------- EXECUÇÃO -------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port, debug=True)
