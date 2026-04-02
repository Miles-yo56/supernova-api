from flask import Flask, request, render_template_string, redirect, url_for
import os

app = Flask(__name__)

# Lista de tokens válidos
TOKENS = {
    "Matlabinc.67": "Dev",
    "Blinkinc.92": "Estudante",
    "Ckjson90": "Escola"
}

# Rota de login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        token = request.form.get("token")
        if token in TOKENS:
            return redirect(url_for("home", perfil=TOKENS[token]))
        else:
            return "<h3>Token inválido! Tente novamente.</h3>"
    
    return render_template_string("""
    <html>
    <head>
        <title>Supernova Space - Login</title>
        <style>
            body { 
                background-color: #0f0f2e; 
                color: white; 
                text-align: center; 
                font-family: Arial; 
            }
            input, button { 
                padding: 10px; 
                margin: 10px; 
                font-size: 16px; 
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
