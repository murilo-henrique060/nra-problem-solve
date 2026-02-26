import json
import pandas as pd

def load_problem(name: str):
    return [
       json.load(open(f'src/problems/ihtc2024-nra/{name}/instance_info.json')), # Instance information
       pd.read_csv(f'src/problems/ihtc2024-nra/{name}/nurse_shifts.csv'), # Nurse shifts information
       pd.read_csv(f'src/problems/ihtc2024-nra/{name}/occupied_room_shifts.csv'), # Occupied room shifts information
    ]