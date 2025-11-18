from flask import Flask, render_template, request, redirect, url_for
import random
import string
import os
import json

app = Flask(__name__)

participantes = [
    "Fabrício Castanheiro", "daiane meyer castanheiro", "Valdeci deucher", "Gabriela Ribeiro", "Marcelo Onorio",
    "Helena Ribeiro", "Isaac Castanheiro", "Rosenilda Ribeiro", "Fabiano de mattos", "Gabriel de mattos",
    "Ivonete Ribeiro da cunha", "Luciana", "Vanderlei (delei)", "Micael", "Vanessa",
    "Eva", "Jucelino", "daiane castanheiro", "Lucas de Oliveira", "Eloah Castanheiro",
    "Miguel", "Taca", "Yuri", "Fabíola", "cauana da Silva",
    "Lucas schutz", "Eloá schutz", "Marzinho (tuntuna)", "Sandra Mara", "Namir",
    "Duduca"
]

def sortear(participantes):
    sorteio = participantes.copy()
    while True:
        random.shuffle(sorteio)
        if all(p != s for p, s in zip(participantes, sorteio)):
            break
    return dict(zip(participantes, sorteio))

def gerar_codigos(nomes):
    codigos = {}
    usados = set()
    for nome in nomes:
        while True:
            cod = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            if cod not in usados:
                usados.add(cod)
                codigos[nome] = cod
                break
    return codigos

def salvar_sorteio(resultado, codigos):
    with open("sorteio.json", "w", encoding="utf-8") as f:
        json.dump({"resultado": resultado, "codigos": codigos}, f, ensure_ascii=False, indent=2)

def carregar_sorteio():
    if os.path.exists("sorteio.json"):
        with open("sorteio.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            return dados["resultado"], dados["codigos"]
    return None, None

def apagar_sorteio():
    if os.path.exists("sorteio.json"):
        os.remove("sorteio.json")

@app.route('/', methods=['GET', 'POST'])
def lista_links():
    global resultado, codigos
    if request.method == "POST":
        apagar_sorteio()
        resultado = sortear(participantes)
        codigos = gerar_codigos(participantes)
        salvar_sorteio(resultado, codigos)
        return redirect(url_for('lista_links'))
    resultado, codigos = carregar_sorteio()
    if resultado is None or codigos is None:
        resultado = sortear(participantes)
        codigos = gerar_codigos(participantes)
        salvar_sorteio(resultado, codigos)
    return render_template('lista.html',
                           participantes=participantes,
                           codigos=codigos,
                           request=request)

@app.route('/<codigo>')
def revelar(codigo):
    resultado, codigos = carregar_sorteio()
    links = {codigos[nome]: resultado[nome] for nome in participantes} if resultado and codigos else {}
    if codigo in links:
        return render_template('revelar.html', amigo=links[codigo])
    else:
        return "Link inválido! Peça o link correto ao organizador."

if __name__ == '__main__':
    resultado, codigos = carregar_sorteio()
    if resultado is None or codigos is None:
        resultado = sortear(participantes)
        codigos = gerar_codigos(participantes)
        salvar_sorteio(resultado, codigos)
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)