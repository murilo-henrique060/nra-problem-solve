from problems.problems import load_problem
from solutions.pli import solve_cbc, solve_glpk
from solutions.metaheuristics import solve_genetic_algorithm, solve_genetic_algorithm_adjusted, solve_particle_swarm_optimization, solve_particle_swarm_optimization_adjusted
from time import perf_counter_ns, sleep
import pandas as pd
from tqdm.contrib.concurrent import process_map
import multiprocessing
import os

solvers = {
    'CBC': solve_cbc,
    'Genetic Algorithm': solve_genetic_algorithm,
    'Genetic Algorithm Adjusted': solve_genetic_algorithm_adjusted,
    'Particle Swarm Optimization': solve_particle_swarm_optimization,
    'Particle Swarm Optimization Adjusted': solve_particle_swarm_optimization_adjusted
}

SOLVERS_TESTS = ['CBC']
INSTANCES_TESTS = ['i01', 'i02', 'i03'] # Just PLI

SOLVERS_RECOMMENDED = ['CBC', 'Genetic Algorithm', 'Genetic Algorithm Adjusted', 'Particle Swarm Optimization', 'Particle Swarm Optimization Adjusted']
INSTANCES_RECOMMENDED = ['i04', 'i06'] # PlI x Metaheuristics

SOLVERS_CHALLENGING = ['Genetic Algorithm', 'Genetic Algorithm Adjusted', 'Particle Swarm Optimization', 'Particle Swarm Optimization Adjusted']
INSTANCES_CHALLENGING = ['i05', 'i18'] # Just Metaheuristics

def run_test(data):
    solver, instance = data
    solver_alg = solvers[solver]
    problem = load_problem(instance)

    start_time = perf_counter_ns()
    result = solver_alg(*problem)
    end_time = perf_counter_ns()

    return instance, solver, result, (end_time - start_time)

def run_tests(solvers, instances, r=10, results_file='results.csv'):
    results = []

    total_tests = len(solvers) * len(instances) * r

    workers = min(multiprocessing.cpu_count(), total_tests) # Limit workers to the number of tests to avoid overhead
    inputs = [(solver, instance) for solver in solvers for instance in instances for _ in range(r)]

    print(f'Running {total_tests} tests with {workers} workers...')
    results = process_map(run_test, inputs, max_workers=workers)

    df = pd.DataFrame(results, columns=['instance', 'solver', 'result', 'time_ns'])
    os.makedirs('output', exist_ok=True)
    df.to_csv(results_file, index=False)
    print('All tests completed. Results saved to', results_file)

def main():
    run_tests(SOLVERS_TESTS, INSTANCES_TESTS, r=10, results_file='output/results_test.csv')
    run_tests(SOLVERS_RECOMMENDED, INSTANCES_RECOMMENDED, r=10, results_file='output/results_recommended.csv')
    run_tests(SOLVERS_CHALLENGING, INSTANCES_CHALLENGING, r=10, results_file='output/results_challenging.csv')

if __name__ == '__main__':
    main()
