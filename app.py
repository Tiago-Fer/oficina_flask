"""
Oficina - v0.1
Sistema simples de gestão para oficina mecânica, rodando no navegador (off-line).

Rodar:
    pip install -r requirements.txt
    python app.py
Abrir: http://127.0.0.1:5000
"""

from flask import Flask, flash, redirect, render_template, request, url_for

import repositorio as repo

app = Flask(__name__)
app.secret_key = "troque-isto-depois"  # necessário para as mensagens flash


# ---------------------------------------------------------------------------
# Início
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html", resumo=repo.resumo(), ordens=repo.listar_ordens()[-5:][::-1])


# ---------------------------------------------------------------------------
# Clientes
# ---------------------------------------------------------------------------
@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    if request.method == "POST":
        nome = request.form.get("nome", "")
        if not nome.strip():
            flash("Informe o nome do cliente.", "erro")
        else:
            repo.salvar_cliente(nome, request.form.get("telefone", ""))
            flash("Cliente cadastrado.", "ok")
        return redirect(url_for("clientes"))
    return render_template("clientes.html", clientes=repo.listar_clientes())


@app.route("/clientes/<int:id_>/excluir", methods=["POST"])
def excluir_cliente(id_):
    repo.excluir_cliente(id_)
    flash("Cliente excluído (e seus veículos e ordens).", "ok")
    return redirect(url_for("clientes"))


# ---------------------------------------------------------------------------
# Veículos
# ---------------------------------------------------------------------------
@app.route("/veiculos", methods=["GET", "POST"])
def veiculos():
    if request.method == "POST":
        placa = request.form.get("placa", "")
        cliente_id = request.form.get("cliente_id", type=int)
        if not placa.strip() or cliente_id is None:
            flash("Informe a placa e escolha o dono.", "erro")
        else:
            repo.salvar_veiculo(
                placa,
                request.form.get("modelo", ""),
                request.form.get("ano", ""),
                cliente_id,
            )
            flash("Veículo cadastrado.", "ok")
        return redirect(url_for("veiculos"))
    return render_template(
        "veiculos.html",
        veiculos=repo.listar_veiculos(),
        clientes=repo.listar_clientes(),
    )


@app.route("/veiculos/<int:id_>/excluir", methods=["POST"])
def excluir_veiculo(id_):
    repo.excluir_veiculo(id_)
    flash("Veículo excluído.", "ok")
    return redirect(url_for("veiculos"))


# ---------------------------------------------------------------------------
# Ordens de serviço
# ---------------------------------------------------------------------------
@app.route("/ordens", methods=["GET", "POST"])
def ordens():
    if request.method == "POST":
        veiculo_id = request.form.get("veiculo_id", type=int)
        problema = request.form.get("problema", "")
        if veiculo_id is None or not problema.strip():
            flash("Escolha o veículo e descreva o problema.", "erro")
        else:
            repo.salvar_ordem(
                veiculo_id,
                problema,
                request.form.get("servicos", ""),
                request.form.get("pecas", ""),
                request.form.get("valor", "0"),
            )
            flash("Ordem de serviço aberta.", "ok")
        return redirect(url_for("ordens"))
    return render_template(
        "ordens.html",
        ordens=repo.listar_ordens(),
        veiculos=repo.listar_veiculos(),
        status_opcoes=repo.STATUS_ORDEM,
    )


@app.route("/ordens/<int:id_>/status", methods=["POST"])
def status_ordem(id_):
    repo.atualizar_status_ordem(id_, request.form.get("status", ""))
    return redirect(url_for("ordens"))


@app.route("/ordens/<int:id_>/excluir", methods=["POST"])
def excluir_ordem(id_):
    repo.excluir_ordem(id_)
    flash("Ordem excluída.", "ok")
    return redirect(url_for("ordens"))


# ---------------------------------------------------------------------------
# Filtro para mostrar dinheiro no padrão brasileiro
# ---------------------------------------------------------------------------
@app.template_filter("reais")
def reais(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


if __name__ == "__main__":
    app.run(debug=True)
