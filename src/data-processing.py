import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

RESULTS_FILES = ['output/results_test.csv', 'output/results_recommended.csv', 'output/results_challenging.csv']

def process_recommended_challenging():
    for file in RESULTS_FILES[1:]:
        df = pd.read_csv(file).rename(columns={
            'time_ns': 'Time (s)',
            'result': 'Cost (Fitness)',
            'solver': 'Solver',
            'instance': 'Test Instance'
        })
        print(f"Processing {file}")

        df['Time (s)'] = df['Time (s)'] / 1e9  # Converte de nanosegundos para segundos para melhor legibilidade
        df['Solver'] = df['Solver'].map({
            'CBC': 'CBC',
            'Genetic Algorithm': 'GA',
            'Genetic Algorithm Adjusted': 'GA Adj',
            'Particle Swarm Optimization': 'PSO',
            'Particle Swarm Optimization Adjusted': 'PSO Adj'
        })
        tests = df['Test Instance'].unique()

        for test in tests:
            test_df = df[df['Test Instance'] == test]

            # Configura o estilo "limpo" e acadêmico do Seaborn
            sns.set_theme(style="whitegrid", font_scale=1.1)

            # Cria a figura com dois quadros (1 linha, 2 colunas)
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

            sns.scatterplot(
                data=test_df, 
                x='Time (s)',
                y='Cost (Fitness)',
                hue='Solver',
                s=250, # Tamanho dos pontos
                alpha=0.8,
                ax=ax1
            )

            ax1.set_title('Trade-off: Tempo Computacional vs. Qualidade da Solução', pad=15, fontweight='bold')
            ax1.set_xlabel('Tempo de Execução (Segundos)')
            ax1.set_ylabel('Custo Total (Fitness)')


            # ---------------------------------------------------------
            # GRÁFICO 2: Boxplot (Estabilidade Estatística) com Seaborn
            # ---------------------------------------------------------
            sns.boxplot(
                data=test_df, 
                x='Solver',
                y='Cost (Fitness)', 
                width=0.3, 
                color='dodgerblue',
                boxprops=dict(alpha=0.7), # Deixa a caixa levemente transparente
                ax=ax2
            )

            ax2.set_title('Estabilidade Estatística dos Solvers', pad=15, fontweight='bold')
            ax2.set_xlabel('Solução')
            ax2.set_ylabel('Custo Total (Fitness)')

            # Ajusta os espaçamentos para ficar perfeito no PDF
            plt.tight_layout()
            plt.savefig(f"output/{test}_{file.replace('.csv', '.png')}")
            plt.clf()  # Clear the figure for the next plot

            print('-' * 50)
            print(f"Média com ic por Solver para {test}:")
            data = test_df.groupby('Solver')['Cost (Fitness)'].agg(['mean', 'std', 'count']).rename(columns={
                'mean': 'Média',
                'std': 'Desvio Padrão',
                'count': 'Contagem'
            })
            data ['IC'] = 1.96 * (data['Desvio Padrão'] / data['Contagem']**0.5)
            print(data[['Média', 'IC']])
            
            print('-' * 50)
            print("\n\n")

if __name__ == '__main__':
    process_recommended_challenging()
