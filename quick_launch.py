import os
import subprocess
from constants import MULTIATTACK_ALGORITHMS, MULTIATTACK_ARGUMENTS, TIME_LOGS_FILE_PATH

def quick():
    time_command = f'time --output {TIME_LOGS_FILE_PATH} -f %E'.split()

    results = {}
    for k, v in MULTIATTACK_ALGORITHMS.items():
        executed_command = time_command + [v + ".out"] + ['8'] + MULTIATTACK_ARGUMENTS
        subprocess.run(executed_command, check=True)

        result = None
        with open(TIME_LOGS_FILE_PATH, "r+") as f:
            result = f.read().split('\n')

        assert result is not None
        results[k] = result[0]

    # Remove the time_logs.txt file
    os.remove(TIME_LOGS_FILE_PATH)

    print()
    print("Results:")
    print(results)

if __name__ == "__main__":
    quick()
