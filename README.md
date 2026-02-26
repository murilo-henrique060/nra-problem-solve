# NRA Problem Solve

Projeto com scripts para executar testes e gerar gráficos de resultados na resolução dos problemas NRA usando técnica PLI (Programação Linear Inteira) e metaheurísticas.

**Principais scripts**
- `src/test-runnner.py` — executa os solvers e gera CSVs de resultados em `output/`.
- `src/data-processing.py` — gera gráficos (PNG) a partir dos CSVs em `output/`.

## Instalação (Linux / macOS)

1. Clone o repositório:

```sh
git clone <repo-url>
cd nra-problem-solve
```

2. Crie e ative um ambiente virtual:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:

```sh
pip install -r requirements.txt
```

## Execução

- Para rodar os testes (gera CSVs em `output/`):

```sh
cd src
python test-runnner.py
```

- Para gerar os gráficos a partir dos CSVs gerados:

```sh
cd src
python data-processing.py
```

## Saída

- Resultados dos testes: `output/results_test.csv`, `output/results_recommended.csv`, `output/results_challenging.csv`.
- Gráficos: imagens PNG salvas em `output/` (um arquivo por instância/arquivo de resultados).

## Observações

- Os solvers estão em `src/solutions/` (PLI e metaheurísticas).
- Execute os scripts a partir da pasta `src/` para que os imports relativos funcionem conforme o código atual.

---

Se quiser, posso também commitar a alteração e/ou rodar os scripts aqui para validar.

