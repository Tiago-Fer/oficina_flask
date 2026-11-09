# 🔧 Oficina

Sistema de gestão para oficina mecânica que roda **no navegador, totalmente off-line**.

Este projeto é construído de forma incremental: cada versão adiciona uma camada e
o histórico do Git mostra a evolução. A ideia é que a **camada de armazenamento**
(`repositorio.py`) troque de implementação a cada etapa sem que o resto do sistema mude.

## Rodando

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux / macOS
pip install -r requirements.txt
python app.py
```

Abra <http://127.0.0.1:5000> no navegador.

## Estrutura

```
app.py            # rotas Flask (o que acontece em cada página)
repositorio.py    # onde os dados vivem — ÚNICO arquivo que muda entre versões
templates/        # HTML (Jinja2)
static/           # CSS
```

## Funcionalidades (v0.1)

- **Clientes**: nome e telefone
- **Veículos**: placa, modelo, ano, dono
- **Ordens de serviço**: problema, serviços, peças, valor, status (Aberta → Em andamento → Concluída)
- Painel inicial com totais e últimas ordens

## Roteiro de evolução

| Versão | Armazenamento | O que muda |
|--------|---------------|------------|
| **v0.1** ✅ | Listas de dicionários em memória | Dados somem ao fechar. Proposital. |
| v0.2 | Arquivo JSON | Primeira persistência real, mudança mínima |
| v0.3 | Exportar / importar Excel | Relatórios para o contador |
| v0.4 | SQLite → SQLAlchemy | Relacionamentos de verdade, consultas |
| v0.5 | Testes (`pytest`) + GitHub Actions | Selo verde no repositório |
| v1.0 | Executável (PyInstaller) | Instalar na máquina da oficina |
| futuro | IA | Sugestão de diagnóstico, resumo da OS para o cliente |

## Por que começar com listas em memória?

Porque obriga a separar "o que o sistema faz" de "onde os dados ficam".
Quando a v0.2 chegar, só `repositorio.py` muda e isso fica evidente no diff.
