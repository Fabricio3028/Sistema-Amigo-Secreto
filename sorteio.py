# Dicionário de restrições: quem não pode tirar quem
restricoes = {
    # Exemplo:
    "Fabrício Castanheiro": ["Namir", "Duduca","Cauana da Silva","Marzinho (Tuntuna)","Eloá Schutz","Lucas Schutz","Sandra Mara"],
    "Daiane Meyer Castanheiro": ["Namir", "Duduca","Cauana da Silva","Marzinho (Tuntuna)","Eloá Schutz","Lucas Schutz","Sandra Mara"],
    "Patricia": ["Namir", "Duduca","Cauana da Silva","Marzinho (Tuntuna)","Eloá Schutz","Lucas Schutz","Sandra Mara"],
    "Iasmim": ["Namir", "Duduca","Cauana da Silva","Marzinho (Tuntuna)","Eloá Schutz","Lucas Schutz","Sandra Mara"],
}
from flask import Flask, render_template, request, redirect, url_for
import random
import string
import os
import json

app = Flask(__name__)

participantes = [
    "Fabrício Castanheiro",
    "Daiane Meyer Castanheiro",
    "Valdeci Deucher",
    "Gabriela Ribeiro",
    "Marcelo Onório",
    "Helena Ribeiro",
    "Isaac Castanheiro",
    "Rosenilda Ribeiro",
    "Fabiano de Mattos",
    "Gabriel de Mattos",
    "Ivonete Ribeiro da Cunha",
    "Luciana",
    "Vanderlei (delei)",
    "Micael",
    "Vanessa",
    "Eva",
    "Jucelino",
    "Daiane Castanheiro",
    "Lucas de Oliveira",
    "Eloah Castanheiro",
    "Miguel",
    "Taca",
    "Yuri",
    "Fabíola",
    "Cauana da Silva",
    "Lucas Schutz",
    "Eloá Schutz",
    "Marzinho (Tuntuna)",
    "Sandra Mara",
    "Namir",
    "Duduca",
    "Patricia",
    "Rodsom(Robinho)",
    "Iasmim",
    "Adão (Tio Dão)",
    "Saléte (Tia Saléte)",
    "Adriano",
    "Dayane",
    "Viviane",
    "Vitinho",
    "Vitória"
]

def sortear(participantes):
    sorteio = participantes.copy()
    tentativas = 0
    while True:
        random.shuffle(sorteio)
        valido = True
        for p, s in zip(participantes, sorteio):
            if p == s:
                valido = False
                break
            if p in restricoes and s in restricoes[p]:
                valido = False
                break
        if valido:
            break
        tentativas += 1
        if tentativas > 10000:
            raise Exception("Não foi possível sortear respeitando todas as restrições. Reveja as regras!")
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


# Salva participantes em arquivo
def salvar_participantes():
    with open("participantes.json", "w", encoding="utf-8") as f:
        json.dump(participantes, f, ensure_ascii=False, indent=2)

# Carrega participantes do arquivo, se existir
def carregar_participantes():
    global participantes
    if os.path.exists("participantes.json"):
        with open("participantes.json", "r", encoding="utf-8") as f:
            participantes.clear()
            participantes.extend(json.load(f))


@app.route('/', methods=['GET', 'POST'])
def lista_links():
    global resultado, codigos, participantes
    carregar_participantes()
    if request.method == "POST":
        if 'novo_nome' in request.form and request.form['novo_nome'].strip():
            novo_nome = request.form['novo_nome'].strip()
            if novo_nome not in participantes:
                participantes.append(novo_nome)
                salvar_participantes()
            apagar_sorteio()
            resultado = sortear(participantes)
            codigos = gerar_codigos(participantes)
            salvar_sorteio(resultado, codigos)
            return redirect(url_for('lista_links'))
        if 'remover_nome' in request.form and request.form['remover_nome'].strip():
            nome_remover = request.form['remover_nome'].strip()
            if nome_remover in participantes:
                participantes.remove(nome_remover)
                salvar_participantes()
            apagar_sorteio()
            resultado = sortear(participantes)
            codigos = gerar_codigos(participantes)
            salvar_sorteio(resultado, codigos)
            return redirect(url_for('lista_links'))
        if 'refazer' in request.form:
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
    # Monta links com nome no final
    links = {}
    for nome in participantes:
        if nome.strip():
            nome_url = nome.replace(' ', '-').replace('(', '').replace(')', '').replace('ç', 'c').replace('ã', 'a').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('â', 'a').replace('ê', 'e').replace('ô', 'o').replace('õ', 'o').replace('ü', 'u').replace('í', 'i').replace('ú', 'u').replace('É', 'E').replace('Á', 'A').replace('Ó', 'O').replace('Í', 'I').replace('Ú', 'U').replace('Ç', 'C').replace('Ã', 'A').replace('Õ', 'O').replace('Ê', 'E').replace('Ô', 'O').replace('Â', 'A').replace('Ü', 'U')
            links[nome] = f"{codigos[nome]}-{nome_url}"
        else:
            links[nome] = ""
    return render_template('lista.html',
                           participantes=participantes,
                           codigos=codigos,
                           links=links,
                           request=request)

@app.route('/<codigo_nome>')
def revelar(codigo_nome):
    resultado, codigos = carregar_sorteio()
    # Monta dicionário de links válidos: {"codigo-nome-url": (nome, sorteado)}
    links = {}
    for nome in participantes:
        if nome.strip():
            nome_url = nome.replace(' ', '-').replace('(', '').replace(')', '').replace('ç', 'c').replace('ã', 'a').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('â', 'a').replace('ê', 'e').replace('ô', 'o').replace('õ', 'o').replace('ü', 'u').replace('í', 'i').replace('ú', 'u').replace('É', 'E').replace('Á', 'A').replace('Ó', 'O').replace('Í', 'I').replace('Ú', 'U').replace('Ç', 'C').replace('Ã', 'A').replace('Õ', 'O').replace('Ê', 'E').replace('Ô', 'O').replace('Â', 'A').replace('Ü', 'U')
            links[f"{codigos[nome]}-{nome_url}"] = (nome, resultado[nome])
    if codigo_nome in links:
        nome, amigo = links[codigo_nome]
        return render_template('revelar.html', amigo=amigo, nome=nome)
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