<h1 align="center"> NRA Problem Solve  </h1> 

<p align="center"><i> Projeto com scripts para executar testes e gerar gráficos de resultados na resolução dos problemas NRA usando técnica PLI (Programação Linear Inteira) e metaheurísticas. </i></p>

**Principais scripts**
- `src/test-runnner.py` — executa os solvers e gera CSVs de resultados em `output/`.
- `src/data-processing.py` — gera gráficos (PNG) a partir dos CSVs em `output/`.

## Instalação (Linux / macOS)

1. Clone o repositório:

```sh
git clone https://github.com/murilo-henrique060/nra-problem-solve.git
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

<h2> Ferramentas </h2> 
<p display="inline-block">
  <img width="48" src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" alt="python-logo"/>
</p>

<h2> Ambientes de desenvolvimento </h2>
<img width="35" src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Visual_Studio_Code_1.35_icon.svg/2048px-Visual_Studio_Code_1.35_icon.svg.png" alt="vscode-image"/>


## Autores 
- [@murilo-henrique060](https://github.com/murilo-henrique060)
- [@nathil](https://github.com/nathil)
- [@PedroMends30](https://github.com/PedroMends30)
