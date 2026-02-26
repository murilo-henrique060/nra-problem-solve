from pyMetaheuristic.algorithm import genetic_algorithm, particle_swarm_optimization
from collections import defaultdict

def get_fitness(info, nurses_shifts, rooms_shifts):
    # -------------------------------------------------
    # Tratamento dos Dados de entrada
    # -------------------------------------------------
    room_count = info['stats']['total_occupied_room_shifts']
    workload_excess_weight = info['weights']['S4_nurse_excessive_workload']
    skill_deficit_weight = info['weights']['S2_room_nurse_skill']

    nurses = nurses_shifts[['nurse_id', 'global_shift', 'skill_level', 'max_load']].rename(columns={'global_shift': 'nurse_shift'})
    rooms = rooms_shifts[['room_id', 'global_shift', 'max_skill_required', 'total_room_workload']].rename(columns={'global_shift': 'room_shift', 'max_skill_required': 'skill_required','total_room_workload': 'workload'})

    # -------------------------------------------------
    # Otimizações para aumentar a velocidade de execução da função fitness
    # -------------------------------------------------
    nurse_max_loads = {(str(row['nurse_id']).strip(), int(row['nurse_shift'])): row['max_load'] for _, row in nurses.iterrows()}

    nurses_by_shift = {}
    for shift, group in nurses.groupby('nurse_shift'):
        lista_enfermeiros = group[['nurse_id', 'skill_level']].to_dict('records')
        for n in lista_enfermeiros:
            n['nurse_id'] = str(n['nurse_id']).strip()
        nurses_by_shift[int(shift)] = lista_enfermeiros

    # Implementando os dados em listas para otimizar o acesso aos dados durante a execução da função fitness, já que o acesso a elementos de uma lista é mais rápido do que o acesso a elementos de um DataFrame, principalmente quando se tem que acessar muitos elementos em um loop.
    fast_rooms = []
    fast_nurses_options = []

    for _, room in rooms.iterrows():
        r_shift = int(room['room_shift'])
        fast_rooms.append({
            'skill_required': room['skill_required'],
            'workload': room['workload'],
            'shift': r_shift
        })
        fast_nurses_options.append(nurses_by_shift.get(r_shift, []))

    #------------------------------------------------
    # Função de fitness otimizada
    #------------------------------------------------
    def fitness(solution):
        points = 0
        workloads = defaultdict(int)

        for i in range(len(solution)):
            val = int(solution[i])

            nurse_opt = fast_nurses_options[i][val]
            room_data = fast_rooms[i]

            current_shift = room_data['shift']

            # Avaliando o nível de habilidade insuficiente
            points += skill_deficit_weight * max(0, room_data['skill_required'] - nurse_opt['skill_level'])

            # Acumulando a carga de trabalho para cada enfermeiro e turno
            workloads[(nurse_opt['nurse_id'], current_shift)] += room_data['workload']

        for (n_id, shift), current_workload in workloads.items():
            limite_maximo = nurse_max_loads[(n_id, shift)]
            # Avaliando a carga de trabalho excessiva
            points += workload_excess_weight * max(0, current_workload - limite_maximo)

        # A função de fitness é definida como a soma das penalidades por nível de habilidade insuficiente e carga de trabalho excessiva. O objetivo é minimizar essa função, ou seja, encontrar uma solução que minimize as penalidades.
        return points

    #------------------------------------------------
    # Definição dos dados para a execução dos algoritmos de metaheurística
    #------------------------------------------------
    min_values = [0] * room_count # O valor mínimo para cada posição na solução é 0, o que representa a escolha do primeiro enfermeiro disponível para aquele quarto e turno.
    max_values = [len(options) - 0.001 for options in fast_nurses_options] # O valor máximo para cada posição na solução é o número de enfermeiros disponíveis para aquele quarto e turno menos 0.001, o que representa a escolha do último enfermeiro disponível para aquele quarto e turno. O motivo de subtrair 0.001 é para garantir que o valor máximo seja um número inteiro, já que a função de fitness espera que a solução seja uma lista de números inteiros representando as escolhas dos enfermeiros para cada quarto e turno.

    return fitness, min_values, max_values

def solve_genetic_algorithm(info, nurses_shifts, rooms_shifts):
    fitness, min_values, max_values = get_fitness(info, nurses_shifts, rooms_shifts)

    parameters = {
        'min_values': min_values,
        'max_values': max_values,
        'target_function': fitness
    }

    result = genetic_algorithm(**parameters, verbose=False)

    return result[-1]

def solve_genetic_algorithm_adjusted(info, nurses_shifts, rooms_shifts):
    fitness, min_values, max_values = get_fitness(info, nurses_shifts, rooms_shifts)

    parameters = {
        'population_size': 100,
        'min_values': min_values,
        'max_values': max_values,
        'generations': 1000,
        'mutation_rate': 0.5,
        'elite': 14,
        'eta': 123,
        'mu': 18,
        'target_function': fitness
    }

    result = genetic_algorithm(**parameters, verbose=False)

    return result[-1]

def solve_particle_swarm_optimization(info, nurses_shifts, rooms_shifts):
    fitness, min_values, max_values = get_fitness(info, nurses_shifts, rooms_shifts)

    parameters = {
        'min_values': min_values,
        'max_values': max_values,
        'target_function': fitness
    }

    result = particle_swarm_optimization(**parameters, verbose=False)

    return result[-1]

def solve_particle_swarm_optimization_adjusted(info, nurses_shifts, rooms_shifts):
    fitness, min_values, max_values = get_fitness(info, nurses_shifts, rooms_shifts)

    parameters = {
        'swarm_size': 100,
        'min_values': min_values,
        'max_values': max_values,
        'iterations': 1000,
        'w': 0.6758808159809191,
        'c1': 2.153855462060897,
        'c2': 1.2890361910381856,
        'target_function': fitness
    }

    result = particle_swarm_optimization(**parameters, verbose=False)

    return result[-1]