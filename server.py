from flask import Flask, jsonify, render_template
import os

app = Flask(__name__)

# Tela inicial com token
@app.route("/")
def login():
    return "Tela de login - forneça seu token"

# Perfil do aluno
@app.route("/perfil")
def perfil():
    return jsonify({
        "nome": "Gabriel",
        "email": "gabrielsantosprodrigues85@gmail.com",
        "foto": "https://i.pinimg.com/236x/23/Lz/4A/23Lz4AGye.jpg"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
