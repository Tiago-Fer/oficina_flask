"""
Camada de armazenamento da v0.1.

Nesta versão tudo fica em listas de dicionários em memória.
Ao fechar o servidor, os dados são perdidos (de propósito).

Nas próximas versões, só este arquivo muda:
  v0.2 -> salvar/ler em JSON
  v0.3 -> exportar/importar Excel
  v0.4 -> SQLite / SQLAlchemy

O resto do sistema (app.py e templates) não precisa saber onde os dados vivem.
"""

from datetime import datetime
from itertools import count

# ---------------------------------------------------------------------------
# "Banco de dados": três listas de dicionários
# ---------------------------------------------------------------------------
clientes: list[dict] = []
veiculos: list[dict] = []
ordens: list[dict] = []

# Geradores de id (1, 2, 3, ...) para cada lista
_id_cliente = count(1)
_id_veiculo = count(1)
_id_ordem = count(1)

STATUS_ORDEM = ["Aberta", "Em andamento", "Concluída"]


# ---------------------------------------------------------------------------
# Funções genéricas
# ---------------------------------------------------------------------------
def _buscar(lista: list[dict], id_: int) -> dict | None:
    """Retorna o dicionário com o id informado, ou None."""
    for item in lista:
        if item["id"] == id_:
            return item
    return None


def _excluir(lista: list[dict], id_: int) -> bool:
    """Remove o item da lista. Retorna True se removeu."""
    item = _buscar(lista, id_)
    if item is None:
        return False
    lista.remove(item)
    return True


# ---------------------------------------------------------------------------
# Clientes
# ---------------------------------------------------------------------------
def listar_clientes() -> list[dict]:
    return clientes


def buscar_cliente(id_: int) -> dict | None:
    return _buscar(clientes, id_)


def salvar_cliente(nome: str, telefone: str) -> dict:
    cliente = {
        "id": next(_id_cliente),
        "nome": nome.strip(),
        "telefone": telefone.strip(),
    }
    clientes.append(cliente)
    return cliente


def excluir_cliente(id_: int) -> bool:
    # Remove também os veículos e ordens ligados a este cliente
    for v in [v for v in veiculos if v["cliente_id"] == id_]:
        excluir_veiculo(v["id"])
    return _excluir(clientes, id_)


# ---------------------------------------------------------------------------
# Veículos
# ---------------------------------------------------------------------------
def listar_veiculos() -> list[dict]:
    """Retorna os veículos já com o nome do dono anexado (para exibir)."""
    resultado = []
    for v in veiculos:
        dono = buscar_cliente(v["cliente_id"])
        resultado.append({**v, "cliente_nome": dono["nome"] if dono else "—"})
    return resultado


def buscar_veiculo(id_: int) -> dict | None:
    return _buscar(veiculos, id_)


def salvar_veiculo(placa: str, modelo: str, ano: str, cliente_id: int) -> dict:
    veiculo = {
        "id": next(_id_veiculo),
        "placa": placa.strip().upper(),
        "modelo": modelo.strip(),
        "ano": ano.strip(),
        "cliente_id": cliente_id,
    }
    veiculos.append(veiculo)
    return veiculo


def excluir_veiculo(id_: int) -> bool:
    for o in [o for o in ordens if o["veiculo_id"] == id_]:
        excluir_ordem(o["id"])
    return _excluir(veiculos, id_)


# ---------------------------------------------------------------------------
# Ordens de serviço
# ---------------------------------------------------------------------------
def listar_ordens() -> list[dict]:
    """Retorna as ordens com dados do veículo e do cliente anexados."""
    resultado = []
    for o in ordens:
        veiculo = buscar_veiculo(o["veiculo_id"])
        dono = buscar_cliente(veiculo["cliente_id"]) if veiculo else None
        resultado.append({
            **o,
            "veiculo_desc": f"{veiculo['placa']} - {veiculo['modelo']}" if veiculo else "—",
            "cliente_nome": dono["nome"] if dono else "—",
        })
    return resultado


def buscar_ordem(id_: int) -> dict | None:
    return _buscar(ordens, id_)


def salvar_ordem(veiculo_id: int, problema: str, servicos: str, pecas: str, valor: str) -> dict:
    ordem = {
        "id": next(_id_ordem),
        "veiculo_id": veiculo_id,
        "problema": problema.strip(),
        "servicos": servicos.strip(),
        "pecas": pecas.strip(),
        "valor": _para_float(valor),
        "status": STATUS_ORDEM[0],
        "aberta_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "concluida_em": None,
    }
    ordens.append(ordem)
    return ordem


def atualizar_status_ordem(id_: int, status: str) -> bool:
    ordem = buscar_ordem(id_)
    if ordem is None or status not in STATUS_ORDEM:
        return False
    ordem["status"] = status
    if status == "Concluída":
        ordem["concluida_em"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    else:
        ordem["concluida_em"] = None
    return True


def excluir_ordem(id_: int) -> bool:
    return _excluir(ordens, id_)


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def _para_float(texto: str) -> float:
    """Aceita '150', '150.50' ou '150,50'. Vazio ou inválido vira 0.0."""
    try:
        return float(texto.replace(",", ".").strip() or 0)
    except ValueError:
        return 0.0


def resumo() -> dict:
    """Números para o painel inicial."""
    return {
        "clientes": len(clientes),
        "veiculos": len(veiculos),
        "ordens_abertas": sum(1 for o in ordens if o["status"] != "Concluída"),
        "faturado": sum(o["valor"] for o in ordens if o["status"] == "Concluída"),
    }
