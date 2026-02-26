import pulp
import pandas as pd

def model_pli(info, nurse_shifts, rooms_shifts):
    #-------------------------------------------------
    # Tratamento dos Dados de entrada
    #-------------------------------------------------

    # Carregando os pesos de penalidade para carga de trabalho excessiva e nível de habilidade insuficiente
    workload_excess_weight = info['weights']['S4_nurse_excessive_workload']
    skill_deficit_weight = info['weights']['S2_room_nurse_skill']

    # Criando DataFrames para enfermeiros e quartos, renomeando colunas para facilitar a manipulação
    # OBS: Resolvemos utilizar a coluna 'global_shift' para facilitar a identificação dos turnos, já que tem o mesmo eveito de utilizar os dias e turnos combinados
    nurses = nurse_shifts[['nurse_id', 'global_shift', 'skill_level', 'max_load']].rename(columns={'global_shift': 'nurse_shift'})
    rooms = rooms_shifts[['room_id', 'global_shift', 'max_skill_required', 'total_room_workload']].rename(columns={'global_shift': 'room_shift', 'max_skill_required': 'skill_required', 'total_room_workload': 'workload'})

    # Cruzamento dos DataFrames de enfermeiros e quartos para criar um DataFrame que representa todas as possíveis alocações de enfermeiros para quartos, considerando os turnos
    nurses_rooms = pd.merge(nurses, rooms, how='cross')
    # filtra apenas os enfermeiros que podem ser alocados nos respectivos quartos, reduzindo o espaço de busca e dinimuindo o tempo de execução
    nurses_rooms = nurses_rooms[nurses_rooms['nurse_shift'] == nurses_rooms['room_shift']]

    # Criando uma coluna 'shift' para facilitar a identificação dos turnos, já que tem o mesmo eveito de utilizar os dias e turnos combinados
    nurses_rooms['shift'] = nurses_rooms['nurse_shift']

    #-------------------------------------------------
    # Modelagem do problema de otimização
    #-------------------------------------------------

    prob = pulp.LpProblem("NRA", pulp.LpMinimize)

    # Criando variáveis de decisão binárias para cada possível alocação de enfermeiro para quarto
    nurses_rooms['x'] = [pulp.LpVariable(f'x_{row['nurse_id']}_{row['room_id']}_{row['shift']}', cat=pulp.LpBinary) for _, row in nurses_rooms.iterrows()]

    # Inicializando variaveis de penalidade para carga de trabalho excessiva
    nurses['y'] = [pulp.LpVariable(f"y_excess_{row['nurse_id']}_{row['nurse_shift']}", lowBound=0, cat=pulp.LpInteger) for _, row in nurses.iterrows()]
    # Inicializando variaveis de penalidade para nível de trabalho insuficiente
    rooms['z'] = [pulp.LpVariable(f"z_deficit_{row['room_id']}_{row['room_shift']}", lowBound=0, cat=pulp.LpInteger) for _, row in rooms.iterrows()]
    # OBS: O uso de variáveis auxiliares para representar as penalidades é por ser necessário garantir que as penalidades sejam sempre positivas, já que o modelo de otimização pode tentar minimizar a função objetivo para atribuir valores negativos às penalidades, o que não faria sentido no contexto do problema.

    for _, room in rooms.iterrows():
        r = room['room_id']
        gs = room['room_shift']

        # Filtrando as alocações de enfermeiros para o quarto e turno específicos
        room_nurses = nurses_rooms[(nurses_rooms['room_id'] == r) & (nurses_rooms['shift'] == gs)]

        # Adicionando limitação de um enfermeiro por quarto
        prob += pulp.lpSum(room_nurses['x']) == 1, f'one_nurse_room_{r}_shift_{gs}'

        # Adicionando restrição para nível de habilidade insuficiente
        prob += room['z'] >= room['skill_required'] - pulp.lpSum(pulp.lpDot(room_nurses['x'], room_nurses['skill_level'])), f'ability_restriction_{r}_{gs}'

    for _, nurse in nurses.iterrows():
        n = nurse['nurse_id']
        gs = nurse['nurse_shift']

        # Filtrando as alocações de quartos para o enfermeiro e turno específicos
        nurse_rooms = nurses_rooms[(nurses_rooms['nurse_id'] == n) & (nurses_rooms['nurse_shift'] == gs)]

        # Adicionando restrição para carga de trabalho excessivo
        prob += nurse['y'] >= pulp.lpSum(pulp.lpDot(nurse_rooms['x'], nurse_rooms['workload'])) - nurse['max_load'], f'workload_restriction_{n}_{gs}'

    prob += (skill_deficit_weight * pulp.lpSum(rooms['z']) + workload_excess_weight * pulp.lpSum(nurses['y'])), "minimize_penalities"

    return prob

def solve_cbc(info, nurse_shifts, rooms_shifts):
    prob = model_pli(info, nurse_shifts, rooms_shifts)
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    if pulp.LpStatus[prob.status] != 'Optimal':
        return False

    return pulp.value(prob.objective)

def solve_glpk(info, nurse_shifts, rooms_shifts):
    prob = model_pli(info, nurse_shifts, rooms_shifts)
    prob.solve(pulp.GLPK_CMD(msg=False))

    if pulp.LpStatus[prob.status] != 'Optimal':
        return False

    return pulp.value(prob.objective)